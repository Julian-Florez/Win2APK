#!/usr/bin/env python3
"""Record a paired second opening without reinstalling the Android package."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

from common import (
    CAPTURE_HEADER,
    EVENT_HEADER,
    INSTALL_HEADER,
    RUN_HEADER,
    SAMPLE_HEADER,
    SUMMARY_HEADER,
    adb,
    adb_shell,
    append_csv,
    ensure_csv,
    find_repo,
    read_csv,
    read_run,
    rewrite_csv,
    safe_name,
    utc_now,
)


SCRIPT_DIR = Path(__file__).resolve().parent


def shell_output(serial: str, *arguments: str) -> tuple[int, str]:
    result = adb(serial, ["shell", *arguments], timeout=45)
    return result.returncode, (result.stdout or result.stderr).strip()


def display_is_on(serial: str) -> bool:
    raw = adb_shell(serial, "dumpsys power | grep -E 'mWakefulness=|Display Power'")
    lowered = raw.lower()
    return "awake" in lowered or "state=on" in lowered


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Force-stop and measure the second opening for an existing cold-install run."
    )
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--device-id", required=True)
    parser.add_argument("--serial", required=True, help="ADB serial; never written to the run files")
    parser.add_argument("--game-process", required=True)
    parser.add_argument("--surface-pattern", default="")
    args = parser.parse_args()

    parent = args.run_dir.resolve()
    phase = parent / "second-open"
    if phase.exists():
        parser.error(f"La fase second-open ya existe; no se sobrescribirá: {phase}")
    run = read_run(parent)
    repo = find_repo(parent)
    package = run["package_name"]
    devices = read_csv(parent / "dispositivos.csv")
    device = next((row for row in devices if row["device_id"] == args.device_id), None)
    if device is None:
        parser.error(f"El run no tiene inventario para {args.device_id}")
    cold_captures = [
        row for row in read_csv(parent / "capturas.csv")
        if row["device_id"] == args.device_id
    ]
    if not cold_captures or cold_captures[-1].get("primary_class") in {"", "pending"}:
        parser.error("Clasifica primero la captura T+60 de la fase fría")
    if run.get("status") != "summarized":
        parser.error(f"La fase fría debe estar resumida antes de la reapertura (estado: {run.get('status')})")

    state = adb(args.serial, ["get-state"], timeout=20)
    if state.returncode != 0 or state.stdout.strip() != "device":
        parser.error("El dispositivo ADB no está en estado device")
    model = adb_shell(args.serial, "getprop ro.product.model").strip()
    if safe_name(model) != safe_name(device["model"]):
        parser.error(f"El serial no corresponde al modelo inventariado: {model!r}")
    package_path = adb_shell(args.serial, f"pm path {package}").strip()
    if not package_path.startswith("package:"):
        parser.error("El paquete no está instalado; second-open requiere conservar la instalación fría")

    screen_before = display_is_on(args.serial)
    wake_action = "no requerido"
    if not screen_before:
        adb(args.serial, ["shell", "input", "keyevent", "224"], timeout=15)
        time.sleep(0.5)
        adb(args.serial, ["shell", "input", "keyevent", "82"], timeout=15)
        time.sleep(0.5)
        wake_action = "keyevent 224 y 82"
    screen_after = display_is_on(args.serial)

    force = adb(args.serial, ["shell", "am", "force-stop", package], timeout=30)
    process_state = ""
    app_pids = game_pids = ""
    for _ in range(10):
        _, app_pids = shell_output(args.serial, "pidof", package)
        _, game_pids = shell_output(args.serial, "pidof", args.game_process)
        process_state = f"app={app_pids or 'absente'}; game={game_pids or 'ausente'}"
        if not app_pids and not game_pids:
            break
        time.sleep(1)

    preflight_path = parent / "logs" / args.device_id / "second-open-preflight.txt"
    preflight_path.parent.mkdir(parents=True, exist_ok=True)
    preflight = (
        f"Preflight {run['run_id']} / {run['exec_id']}, segunda apertura sin reinstalación.\n"
        f"Dispositivo: {model} (alias {args.device_id}; serial no persistido).\n"
        f"Pantalla antes/después de comprobar: {screen_before}/{screen_after}; acción wake: {wake_action}.\n"
        f"pm path confirmó instalación: sí.\n"
        f"am force-stop: exit={force.returncode}; salida={(force.stdout or force.stderr).strip() or 'sin salida'}.\n"
        f"PID tras force-stop: {process_state}.\n"
    )
    preflight_path.write_text(preflight, encoding="utf-8")
    if not screen_after or force.returncode != 0 or app_pids or game_pids:
        print(preflight, file=sys.stderr)
        print("Preflight second-open inválido; no se inició el monitor.", file=sys.stderr)
        return 2

    phase.mkdir(parents=True)
    phase_run = dict(run)
    phase_run.update({
        "scenario_id": run["scenario_id"] + "-second-open",
        "scenario_description": f"Reapertura {run['scenario_description']} sin reinstalación; {run['duration_seconds']} s",
        "install_mode": "second_open_no_reinstall",
        "status": "running",
        "notes": run["notes"] + " Fase second-open: instalación conservada, force-stop verificado y nuevo lanzamiento.",
    })
    rewrite_csv(phase / "run.csv", RUN_HEADER, [phase_run])
    shutil.copy2(parent / "dispositivos.csv", phase / "dispositivos.csv")
    shutil.copy2(parent / "execution-link.txt", phase / "execution-link.txt")
    for name, header in [
        ("instalaciones.csv", INSTALL_HEADER),
        ("muestras.csv", SAMPLE_HEADER),
        ("eventos.csv", EVENT_HEADER),
        ("capturas.csv", CAPTURE_HEADER),
        ("resumen.csv", SUMMARY_HEADER),
    ]:
        ensure_csv(phase / name, header)
    for folder in (phase / "screenshots" / args.device_id, phase / "logs" / args.device_id):
        folder.mkdir(parents=True, exist_ok=True)
    append_csv(phase / "eventos.csv", EVENT_HEADER, {
        "run_id": run["run_id"], "device_id": args.device_id,
        "timestamp_utc": utc_now(), "elapsed_ms": 0,
        "event_type": "second_open_preflight_passed", "severity": "info",
        "message": "Paquete instalado, proceso previo detenido y pantalla encendida; no se reinstala.",
        "evidence_relpath": str(preflight_path.resolve().relative_to(repo)),
    })

    command = [
        sys.executable, str(SCRIPT_DIR / "monitor_device.py"),
        "--run-dir", str(phase), "--device-id", args.device_id,
        "--serial", args.serial, "--package", package,
        "--game-process", args.game_process,
        "--duration", run["duration_seconds"],
        "--interval", run["sample_interval_seconds"],
        "--screenshot-second", run["screenshot_second"],
    ]
    if args.surface_pattern:
        command.extend(["--surface-pattern", args.surface_pattern])
    result = subprocess.run(command, check=False)
    phase_run["status"] = "awaiting_classification" if result.returncode == 0 else "completed_with_errors"
    rewrite_csv(phase / "run.csv", RUN_HEADER, [phase_run])
    print(f"SECOND_OPEN_DIR={phase}", flush=True)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
