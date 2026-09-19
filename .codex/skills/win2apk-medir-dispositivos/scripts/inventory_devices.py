#!/usr/bin/env python3
"""Capture a reproducible, privacy-preserving Android device inventory."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import (
    CATALOG_DEVICE_HEADER,
    DEVICE_HEADER,
    adb,
    adb_shell,
    append_csv,
    find_repo,
    read_run,
    safe_name,
    short_serial_hash,
    upsert_csv,
    utc_now,
)


def parse_getprop(raw: str) -> dict[str, str]:
    properties: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.match(r"^\[([^]]+)\]: \[(.*)\]$", line)
        if match:
            properties[match.group(1)] = match.group(2)
    return properties


def extract_value(raw: str, pattern: str) -> str:
    match = re.search(pattern, raw, re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else ""


def shell_or_empty(serial: str, command: str, timeout: float = 30) -> str:
    try:
        return adb_shell(serial, command, timeout=timeout)
    except (RuntimeError, TimeoutError):
        return ""


def inventory(serial: str, device_id: str, run_id: str) -> dict[str, object]:
    state = adb(serial, ["get-state"], timeout=10)
    if state.returncode != 0 or state.stdout.strip() != "device":
        raise RuntimeError(f"{device_id}: ADB no está en estado device")

    props = parse_getprop(shell_or_empty(serial, "getprop"))
    meminfo = shell_or_empty(serial, "cat /proc/meminfo")
    cpu_present = shell_or_empty(serial, "cat /sys/devices/system/cpu/present").strip()
    cpuinfo = shell_or_empty(serial, "cat /proc/cpuinfo")
    wm_size = shell_or_empty(serial, "wm size")
    wm_density = shell_or_empty(serial, "wm density")
    surface = shell_or_empty(serial, "dumpsys SurfaceFlinger", timeout=45)
    frequencies = shell_or_empty(
        serial,
        "for f in /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_max_freq; do cat $f 2>/dev/null; done",
    )

    if match := re.match(r"0-(\d+)", cpu_present):
        cpu_cores = int(match.group(1)) + 1
    else:
        cpu_cores = len(re.findall(r"^processor\s*:", cpuinfo, re.MULTILINE))

    max_freqs = [int(value) for value in frequencies.split() if value.isdigit()]
    gles_line = next((line.strip() for line in surface.splitlines() if "GLES:" in line), "")
    gpu_vendor = gpu_renderer = gpu_version = ""
    if gles_line:
        gles_data = gles_line.split("GLES:", 1)[1].strip()
        parts = [part.strip() for part in gles_data.split(",", 2)]
        if parts:
            gpu_vendor = parts[0]
        if len(parts) > 1:
            gpu_renderer = parts[1]
        if len(parts) > 2:
            gpu_version = parts[2]

    row: dict[str, object] = {
        "run_id": run_id,
        "device_id": safe_name(device_id),
        "observed_at_utc": utc_now(),
        "manufacturer": props.get("ro.product.manufacturer", ""),
        "model": props.get("ro.product.model", ""),
        "product": props.get("ro.product.name", ""),
        "android_device": props.get("ro.product.device", ""),
        "android_version": props.get("ro.build.version.release", ""),
        "api_level": props.get("ro.build.version.sdk", ""),
        "abi_list": props.get("ro.product.cpu.abilist", ""),
        "hardware": props.get("ro.hardware", ""),
        "soc_model": props.get("ro.soc.model", props.get("ro.board.platform", "")),
        "cpu_cores": cpu_cores or "",
        "cpu_max_freq_khz": max(max_freqs) if max_freqs else "",
        "ram_total_kib": extract_value(meminfo, r"^MemTotal:\s+(\d+)\s+kB"),
        "gpu_vendor": gpu_vendor,
        "gpu_renderer": gpu_renderer,
        "gpu_version": gpu_version,
        "vulkan_version": props.get("ro.hardware.vulkan.version", ""),
        "screen_resolution": extract_value(wm_size, r"Physical size:\s*([^\r\n]+)"),
        "screen_density_dpi": extract_value(wm_density, r"Physical density:\s*(\d+)"),
        "serial_hash": short_serial_hash(serial),
    }
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--device-id", required=True)
    parser.add_argument("--serial", required=True)
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    run = read_run(run_dir)
    repo = find_repo(run_dir)
    row = inventory(args.serial, args.device_id, run["run_id"])
    upsert_csv(run_dir / "dispositivos.csv", DEVICE_HEADER, row, ["run_id", "device_id"])

    catalog_row = {key: value for key, value in row.items() if key != "run_id"}
    catalog_row["last_run_id"] = run["run_id"]
    upsert_csv(
        repo / "metricas/catalogo/devices.csv",
        CATALOG_DEVICE_HEADER,
        catalog_row,
        ["device_id"],
    )
    print(f"{row['device_id']}: {row['manufacturer']} {row['model']} / Android {row['android_version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

