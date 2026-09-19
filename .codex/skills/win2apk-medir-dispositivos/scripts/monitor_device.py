#!/usr/bin/env python3
"""Launch an Android package and record a time series plus a T+60 screenshot."""

from __future__ import annotations

import argparse
import csv
import math
import re
import shlex
import subprocess
import threading
import time
from pathlib import Path

from common import (
    CAPTURE_HEADER,
    EVENT_HEADER,
    SAMPLE_HEADER,
    adb,
    adb_shell,
    append_csv,
    find_repo,
    read_run,
    relative_to_repo,
    utc_now,
)


def shell_or_empty(serial: str, command: str, timeout: float = 15) -> str:
    try:
        return adb_shell(serial, command, timeout=timeout)
    except (RuntimeError, subprocess.TimeoutExpired):
        return ""


def integer(raw: str) -> int | None:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def number(raw: str) -> float | None:
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def format_value(value: object, digits: int = 3) -> object:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.{digits}f}"
    return value


def pids_for(serial: str, name: str) -> list[int]:
    output = shell_or_empty(serial, f"pidof {shlex.quote(name)}").strip()
    return [int(value) for value in output.split() if value.isdigit()]


def parse_meminfo(raw: str) -> dict[str, int]:
    values: dict[str, int] = {}
    for line in raw.splitlines():
        match = re.match(r"^([^:]+):\s+(\d+)\s+kB", line)
        if match:
            values[match.group(1).strip()] = int(match.group(2))
    return values


def parse_system_stat(raw: str) -> tuple[int | None, int | None, float | None]:
    lines = raw.splitlines()
    cpu_line = next((line for line in lines if line.startswith("cpu ")), "")
    values = [integer(value) for value in cpu_line.split()[1:]]
    cpu_values = [value for value in values if value is not None]
    total = sum(cpu_values) if cpu_values else None
    idle = None
    if len(cpu_values) >= 5:
        idle = cpu_values[3] + cpu_values[4]
    load_line = next((line for line in lines if re.match(r"^\d+(?:\.\d+)?\s", line)), "")
    load_1m = number(load_line.split()[0]) if load_line else None
    return total, idle, load_1m


def read_processes(serial: str, pids: list[int]) -> dict[int, dict[str, int]]:
    if not pids:
        return {}
    commands = []
    for pid in pids:
        commands.append(
            f"echo __PID__{pid}; cat /proc/{pid}/stat 2>/dev/null; "
            f"grep -E '^(VmRSS|VmSwap):' /proc/{pid}/status 2>/dev/null"
        )
    raw = shell_or_empty(serial, "; ".join(commands))
    result: dict[int, dict[str, int]] = {}
    current: int | None = None
    for line in raw.splitlines():
        if line.startswith("__PID__"):
            current = integer(line.removeprefix("__PID__"))
            if current is not None:
                result[current] = {}
            continue
        if current is None:
            continue
        if re.match(rf"^{current}\s+\(.*\)\s+", line):
            tail = re.sub(rf"^{current}\s+\(.*\)\s+", "", line, count=1).split()
            if len(tail) > 12:
                utime = integer(tail[11])
                stime = integer(tail[12])
                if utime is not None and stime is not None:
                    result[current]["jiffies"] = utime + stime
        elif match := re.match(r"^(VmRSS|VmSwap):\s+(\d+)\s+kB", line):
            result[current][match.group(1)] = int(match.group(2))
    return result


def parse_dumpsys_meminfo(raw: str) -> dict[str, int]:
    output: dict[str, int] = {}
    for key, pattern in {
        "pss": r"TOTAL PSS:\s+(\d+)",
        "rss": r"TOTAL RSS:\s+(\d+)",
        "swap_pss": r"TOTAL SWAP PSS:\s+(\d+)",
        "graphics": r"^\s*Graphics:\s+(\d+)",
    }.items():
        if match := re.search(pattern, raw, re.MULTILINE):
            output[key] = int(match.group(1))
    if "pss" not in output:
        for line in raw.splitlines():
            if re.match(r"^\s*TOTAL\s+\d+", line):
                columns = line.split()
                if len(columns) > 1 and columns[1].isdigit():
                    output["pss"] = int(columns[1])
                    break
    return output


def detailed_process_memory(serial: str, pids: list[int]) -> dict[str, int]:
    totals = {"pss": 0, "rss": 0, "graphics": 0, "swap_pss": 0}
    seen = {key: False for key in totals}
    for pid in pids:
        parsed = parse_dumpsys_meminfo(shell_or_empty(serial, f"dumpsys meminfo {pid}", timeout=25))
        for key in totals:
            if key in parsed:
                totals[key] += parsed[key]
                seen[key] = True
    return {key: value for key, value in totals.items() if seen[key]}


def process_cpu(
    previous: dict[int, int],
    current: dict[int, dict[str, int]],
    total_delta: int | None,
) -> tuple[float | None, dict[int, int]]:
    current_jiffies = {
        pid: values["jiffies"] for pid, values in current.items() if "jiffies" in values
    }
    if not previous or not total_delta or total_delta <= 0:
        return None, current_jiffies
    delta = sum(max(0, value - previous.get(pid, value)) for pid, value in current_jiffies.items())
    return 100.0 * delta / total_delta, current_jiffies


def data_free_kib(serial: str) -> int | None:
    raw = shell_or_empty(serial, "df -k /data | tail -n 1")
    columns = raw.split()
    return integer(columns[3]) if len(columns) >= 4 else None


def battery_thermal(serial: str) -> tuple[float | None, float | None, float | None, str]:
    battery = shell_or_empty(serial, "dumpsys battery")
    battery_pct = number(next((line.split(":", 1)[1].strip() for line in battery.splitlines() if line.strip().startswith("level:")), ""))
    battery_temp_raw = number(next((line.split(":", 1)[1].strip() for line in battery.splitlines() if line.strip().startswith("temperature:")), ""))
    battery_temp = battery_temp_raw / 10 if battery_temp_raw is not None else None
    thermal_raw = shell_or_empty(
        serial,
        "for f in /sys/class/thermal/thermal_zone*/temp; do cat $f 2>/dev/null; done",
    )
    temperatures = []
    for token in thermal_raw.split():
        value = number(token)
        if value is None or value <= 0:
            continue
        temperatures.append(value / 1000 if value > 1000 else value)
    thermal_service = shell_or_empty(serial, "dumpsys thermalservice | head -n 30")
    status = ""
    if match := re.search(r"Thermal Status[^:]*:\s*([^\r\n]+)", thermal_service, re.IGNORECASE):
        status = match.group(1).strip()
    return battery_pct, battery_temp, max(temperatures, default=None), status


def gpu_sample(serial: str) -> tuple[float | None, int | None, str]:
    raw = shell_or_empty(
        serial,
        "if [ -r /sys/class/kgsl/kgsl-3d0/gpubusy ]; then "
        "echo BUSY $(cat /sys/class/kgsl/kgsl-3d0/gpubusy); fi; "
        "if [ -r /sys/class/kgsl/kgsl-3d0/gpuclk ]; then "
        "echo FREQ $(cat /sys/class/kgsl/kgsl-3d0/gpuclk); fi; "
        "for f in /sys/class/devfreq/*/cur_freq; do case $f in *gpu*|*mali*) "
        "[ -r $f ] && echo DEVFREQ $(cat $f) && break;; esac; done",
    )
    busy = None
    frequency = None
    source = ""
    if match := re.search(r"^BUSY\s+(\d+)\s+(\d+)", raw, re.MULTILINE):
        numerator, denominator = int(match.group(1)), int(match.group(2))
        if denominator > 0:
            busy = 100.0 * numerator / denominator
            source = "kgsl-gpubusy"
    if match := re.search(r"^FREQ\s+(\d+)", raw, re.MULTILINE):
        frequency = int(match.group(1))
    elif match := re.search(r"^DEVFREQ\s+(\d+)", raw, re.MULTILINE):
        frequency = int(match.group(1))
    return busy, frequency, source


def find_surface(serial: str, package: str, pattern: str) -> str:
    raw = shell_or_empty(serial, "dumpsys SurfaceFlinger --list", timeout=25)
    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    def layer_name(line: str) -> str:
        if line.startswith("RequestedLayerState{") and line.endswith("}"):
            line = line[len("RequestedLayerState{"):-1]
            line = re.split(r"\s+(?:parentId|relativeParentId|z)=|\s+!handle", line, maxsplit=1)[0]
        return line

    needles = [pattern, package, "XServerDisplayActivity", "Cuphead"]
    for needle in needles:
        if not needle:
            continue
        candidates = [line for line in lines if needle.lower() in line.lower() and "SurfaceView" in line]
        if candidates:
            blast = [line for line in candidates if "(BLAST)" in line]
            return layer_name((blast or candidates)[-1])
    return ""


def surface_frames(serial: str, surface: str, previous_timestamp: int | None) -> tuple[int | None, int | None]:
    if not surface:
        return None, previous_timestamp
    raw = shell_or_empty(serial, f"dumpsys SurfaceFlinger --latency {shlex.quote(surface)}", timeout=20)
    timestamps = []
    for line in raw.splitlines()[1:]:
        columns = line.split()
        if len(columns) != 3 or not all(value.isdigit() for value in columns):
            continue
        presented = int(columns[1])
        if 0 < presented < 2**63 - 1:
            timestamps.append(presented)
    if not timestamps:
        return None, previous_timestamp
    latest = max(timestamps)
    if previous_timestamp is None:
        return None, latest
    return sum(timestamp > previous_timestamp for timestamp in timestamps), latest


def screen_is_on(serial: str) -> str:
    raw = shell_or_empty(serial, "dumpsys power | grep -E 'mWakefulness=|Display Power'")
    lowered = raw.lower()
    if "awake" in lowered or "state=on" in lowered:
        return "true"
    if "asleep" in lowered or "state=off" in lowered:
        return "false"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--device-id", required=True)
    parser.add_argument("--serial", required=True)
    parser.add_argument("--package")
    parser.add_argument("--game-process", default="Cuphead.exe")
    parser.add_argument("--duration", type=int)
    parser.add_argument("--interval", type=float)
    parser.add_argument("--screenshot-second", type=int)
    parser.add_argument("--surface-pattern", default="")
    parser.add_argument("--no-launch", action="store_true")
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    run = read_run(run_dir)
    repo = find_repo(run_dir)
    package = args.package or run["package_name"]
    duration = args.duration if args.duration is not None else int(run["duration_seconds"])
    interval = args.interval if args.interval is not None else float(run["sample_interval_seconds"])
    screenshot_second = args.screenshot_second if args.screenshot_second is not None else int(run["screenshot_second"])
    device_id = args.device_id
    log_dir = run_dir / "logs" / device_id
    screenshot_dir = run_dir / "screenshots" / device_id
    log_dir.mkdir(parents=True, exist_ok=True)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    event_lock = threading.Lock()
    start_wall = utc_now()
    start = time.monotonic()

    def event(event_type: str, severity: str, message: str, evidence: Path | None = None) -> None:
        with event_lock:
            append_csv(run_dir / "eventos.csv", EVENT_HEADER, {
                "run_id": run["run_id"], "device_id": device_id,
                "timestamp_utc": utc_now(), "elapsed_ms": int((time.monotonic() - start) * 1000),
                "event_type": event_type, "severity": severity, "message": message,
                "evidence_relpath": relative_to_repo(evidence, repo) if evidence else "",
            })

    screenshot_path = screenshot_dir / f"t{screenshot_second:03d}.png"

    def capture_at_deadline() -> None:
        delay = start + screenshot_second - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        captured_at = utc_now()
        elapsed_ms = int((time.monotonic() - start) * 1000)
        result = adb(args.serial, ["exec-out", "screencap", "-p"], timeout=45, text=False)
        if result.returncode == 0 and result.stdout.startswith(b"\x89PNG"):
            screenshot_path.write_bytes(result.stdout)
            append_csv(run_dir / "capturas.csv", CAPTURE_HEADER, {
                "run_id": run["run_id"], "device_id": device_id,
                "captured_at_utc": captured_at, "elapsed_ms": elapsed_ms,
                "scheduled_second": screenshot_second,
                "image_relpath": relative_to_repo(screenshot_path, repo),
                "primary_class": "pending", "secondary_class": "",
                "description": "", "visible_text": "", "confidence": "pending",
                "classification_method": "pending", "classifier_model": "",
                "classified_at_utc": "", "human_review_status": "unreviewed",
            })
            event("screenshot_captured", "info", f"Captura canónica T+{screenshot_second}s", screenshot_path)
        else:
            message = result.stderr.decode("utf-8", errors="replace").strip() if result.stderr else "screencap no produjo PNG"
            event("screenshot_failed", "error", message)

    adb(args.serial, ["logcat", "-c"], timeout=30)
    logcat_path = log_dir / "logcat.txt"
    logcat_handle = logcat_path.open("w", encoding="utf-8")
    logcat = subprocess.Popen(
        ["adb", "-s", args.serial, "logcat", "-v", "threadtime"],
        stdout=logcat_handle,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if not args.no_launch:
        launch = adb(
            args.serial,
            ["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"],
            timeout=45,
        )
        (log_dir / "launch.log").write_text(launch.stdout + launch.stderr, encoding="utf-8")
        event("launch_requested", "info" if launch.returncode == 0 else "error", (launch.stdout + launch.stderr).strip(), log_dir / "launch.log")
    else:
        event("monitor_started", "info", f"Monitoreo sin lanzamiento; inicio UTC {start_wall}")

    screenshot_thread = threading.Thread(target=capture_at_deadline, name=f"capture-{device_id}", daemon=True)
    screenshot_thread.start()
    samples_path = run_dir / "muestras.csv"
    previous_total = previous_idle = None
    previous_app: dict[int, int] = {}
    previous_game: dict[int, int] = {}
    previous_frame_timestamp = None
    previous_frame_time = None
    app_first_seen = game_first_seen = first_frame_seen = False
    app_was_alive = game_was_alive = False
    surface = ""
    detailed_app: dict[str, int] = {}
    detailed_game: dict[str, int] = {}
    battery_pct = battery_temp = thermal_max = None
    thermal_status = ""
    free_data = None
    screen_on = ""
    sample_index = 0
    next_sample = start

    try:
        while True:
            now = time.monotonic()
            if now < next_sample:
                time.sleep(next_sample - now)
            sample_started = time.monotonic()
            elapsed = sample_started - start
            if elapsed > duration + interval / 2:
                break

            metric_errors = []
            app_pids = pids_for(args.serial, package)
            game_pids = pids_for(args.serial, args.game_process)
            app_alive = bool(app_pids)
            game_alive = bool(game_pids)
            if app_alive and not app_first_seen:
                event("app_process_first_seen", "info", f"Proceso principal observado: {len(app_pids)}")
                app_first_seen = True
            if game_alive and not game_first_seen:
                event("game_process_first_seen", "info", f"{args.game_process} observado: {len(game_pids)}")
                game_first_seen = True
            if app_was_alive and not app_alive:
                event("app_process_disappeared", "error", "El proceso principal dejó de observarse")
            if game_was_alive and not game_alive:
                event("game_process_disappeared", "error", f"{args.game_process} dejó de observarse")
            app_was_alive, game_was_alive = app_alive, game_alive

            system_raw = shell_or_empty(args.serial, "cat /proc/stat; cat /proc/loadavg")
            total, idle, load_1m = parse_system_stat(system_raw)
            total_delta = total - previous_total if total is not None and previous_total is not None else None
            idle_delta = idle - previous_idle if idle is not None and previous_idle is not None else None
            system_busy = None
            if total_delta and idle_delta is not None and total_delta > 0:
                system_busy = 100.0 * (total_delta - idle_delta) / total_delta

            proc_values = read_processes(args.serial, sorted(set(app_pids + game_pids)))
            app_values = {pid: proc_values[pid] for pid in app_pids if pid in proc_values}
            game_values = {pid: proc_values[pid] for pid in game_pids if pid in proc_values}
            app_cpu, previous_app = process_cpu(previous_app, app_values, total_delta)
            game_cpu, previous_game = process_cpu(previous_game, game_values, total_delta)
            app_rss = sum(value.get("VmRSS", 0) for value in app_values.values()) if app_values else None
            game_rss = sum(value.get("VmRSS", 0) for value in game_values.values()) if game_values else None

            mem = parse_meminfo(shell_or_empty(args.serial, "cat /proc/meminfo"))
            if sample_index % max(1, round(5 / interval)) == 0:
                detailed_app = detailed_process_memory(args.serial, app_pids)
                detailed_game = detailed_process_memory(args.serial, game_pids)
            if sample_index % max(1, round(10 / interval)) == 0:
                battery_pct, battery_temp, thermal_max, thermal_status = battery_thermal(args.serial)
                free_data = data_free_kib(args.serial)
                screen_on = screen_is_on(args.serial)

            gpu_busy, gpu_freq, gpu_source = gpu_sample(args.serial)
            if not surface or sample_index % max(1, round(10 / interval)) == 0:
                surface = find_surface(args.serial, package, args.surface_pattern)
            frame_count, previous_frame_timestamp = surface_frames(args.serial, surface, previous_frame_timestamp)
            if game_alive and frame_count is not None and frame_count > 0 and not first_frame_seen:
                event(
                    "first_game_frame_observed",
                    "info",
                    "Primer timestamp de presentación observado en la superficie del juego",
                )
                first_frame_seen = True
            fps = None
            fps_source = ""
            if frame_count is not None and previous_frame_time is not None:
                frame_elapsed = sample_started - previous_frame_time
                if frame_elapsed > 0:
                    fps = frame_count / frame_elapsed
                    fps_source = "surfaceflinger_latency"
            if frame_count is not None:
                previous_frame_time = sample_started

            if not system_raw:
                metric_errors.append("proc_stat")
            if not mem:
                metric_errors.append("meminfo")
            if gpu_busy is None:
                metric_errors.append("gpu_util_N/R")
            if fps is None:
                metric_errors.append("fps_N/R")
            metric_status = "ok" if not metric_errors else "partial:" + "|".join(metric_errors)
            append_csv(samples_path, SAMPLE_HEADER, {
                "run_id": run["run_id"], "device_id": device_id,
                "sample_index": sample_index, "timestamp_utc": utc_now(),
                "elapsed_ms": int(elapsed * 1000),
                "phase": "runtime" if game_first_seen else "startup",
                "app_alive": str(app_alive).lower(), "game_alive": str(game_alive).lower(),
                "app_pid_count": len(app_pids), "game_pid_count": len(game_pids),
                "cpu_system_busy_pct": format_value(system_busy),
                "cpu_app_total_capacity_pct": format_value(app_cpu),
                "cpu_game_total_capacity_pct": format_value(game_cpu),
                "load_1m": format_value(load_1m),
                "app_rss_kib": format_value(app_rss, 0), "game_rss_kib": format_value(game_rss, 0),
                "app_pss_kib": detailed_app.get("pss", ""), "game_pss_kib": detailed_game.get("pss", ""),
                "graphics_pss_kib": detailed_app.get("graphics", 0) + detailed_game.get("graphics", 0) if detailed_app or detailed_game else "",
                "swap_pss_kib": detailed_app.get("swap_pss", 0) + detailed_game.get("swap_pss", 0) if detailed_app or detailed_game else "",
                "mem_total_kib": mem.get("MemTotal", ""), "mem_available_kib": mem.get("MemAvailable", ""),
                "ion_heap_kib": mem.get("ION_heap", ""), "gpu_memory_kib": mem.get("Gpu", ""),
                "gpu_busy_pct": format_value(gpu_busy), "gpu_freq_hz": format_value(gpu_freq, 0),
                "fps_presented": format_value(fps), "frame_count_delta": format_value(frame_count, 0),
                "fps_source": fps_source, "battery_pct": format_value(battery_pct),
                "battery_temp_c": format_value(battery_temp), "thermal_max_c": format_value(thermal_max),
                "thermal_status": thermal_status, "data_free_kib": format_value(free_data, 0),
                "screen_on": screen_on, "metric_status": metric_status + (f"|gpu:{gpu_source}" if gpu_source else ""),
            })
            previous_total, previous_idle = total, idle
            sample_index += 1
            if sample_index == 1 or sample_index % max(1, round(30 / interval)) == 0:
                print(f"{device_id}: {elapsed:.1f}/{duration}s, app={app_alive}, game={game_alive}", flush=True)
            next_sample += interval
    finally:
        screenshot_thread.join(timeout=max(5, screenshot_second + 5 - (time.monotonic() - start)))
        logcat.terminate()
        try:
            logcat.wait(timeout=10)
        except subprocess.TimeoutExpired:
            logcat.kill()
            logcat.wait(timeout=5)
        logcat_handle.close()
        exit_info = shell_or_empty(args.serial, f"dumpsys activity exit-info {shlex.quote(package)}", timeout=45)
        (log_dir / "exit-info.txt").write_text(exit_info, encoding="utf-8")
        event("monitor_finished", "info", f"{sample_index} muestras registradas", log_dir / "exit-info.txt")

    print(f"{device_id}: monitoreo finalizado con {sample_index} muestras")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
