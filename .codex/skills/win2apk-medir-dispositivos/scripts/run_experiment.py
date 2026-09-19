#!/usr/bin/env python3
"""Orchestrate sequential cold installs and measurements across Android devices."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from common import EVENT_HEADER, append_csv, read_run, set_run_status, utc_now


SCRIPT_DIR = Path(__file__).resolve().parent


def run_script(name: str, arguments: list[str], check: bool = True) -> subprocess.CompletedProcess:
    command = [sys.executable, str(SCRIPT_DIR / name), *arguments]
    print(f"+ {name}", flush=True)
    return subprocess.run(command, check=check)


def parse_device(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("use alias=serial")
    alias, serial = value.split("=", 1)
    if not alias.strip() or not serial.strip():
        raise argparse.ArgumentTypeError("alias y serial no pueden estar vacíos")
    return alias.strip(), serial.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--apks", type=Path, required=True)
    parser.add_argument("--bundletool", type=Path, required=True)
    parser.add_argument("--device", action="append", type=parse_device, required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--expected-state", default="N/R")
    parser.add_argument("--duration", type=int, default=300)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--screenshot-second", type=int, default=60)
    parser.add_argument("--package", default="com.cuphead")
    parser.add_argument("--game-process", default="Cuphead.exe")
    parser.add_argument("--surface-pattern", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--confirm-delete-all", required=True)
    args = parser.parse_args()
    if args.confirm_delete_all != "ELIMINAR-COMPLETO":
        parser.error("La prueba fría requiere --confirm-delete-all ELIMINAR-COMPLETO")
    aliases = [alias for alias, _ in args.device]
    if len(aliases) != len(set(aliases)):
        parser.error("Los alias de dispositivo deben ser únicos")

    create = subprocess.run(
        [
            sys.executable, str(SCRIPT_DIR / "create_run.py"),
            "--repo", str(args.repo.resolve()), "--scenario", args.scenario,
            "--description", args.description, "--expected-state", args.expected_state,
            "--duration", str(args.duration), "--interval", str(args.interval),
            "--screenshot-second", str(args.screenshot_second), "--package", args.package,
            "--artifact", str(args.apks.resolve()), "--notes", args.notes,
        ],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    run_dir = Path(create.stdout.strip().splitlines()[-1]).resolve()
    run = read_run(run_dir)
    print(f"Creado {run['run_id']} en {run_dir}", flush=True)
    set_run_status(run_dir, "running")

    for alias, serial in args.device:
        run_script("inventory_devices.py", ["--run-dir", str(run_dir), "--device-id", alias, "--serial", serial])

    failures = 0
    for alias, serial in args.device:
        print(f"\n[{alias}] instalación fría y medición", flush=True)
        install = run_script(
            "cold_install.py",
            [
                "--run-dir", str(run_dir), "--device-id", alias, "--serial", serial,
                "--apks", str(args.apks.resolve()), "--bundletool", str(args.bundletool.resolve()),
                "--package", args.package, "--confirm-delete", "ELIMINAR-COMPLETO",
            ],
            check=False,
        )
        if install.returncode != 0:
            failures += 1
            append_csv(run_dir / "eventos.csv", EVENT_HEADER, {
                "run_id": run["run_id"], "device_id": alias,
                "timestamp_utc": utc_now(), "elapsed_ms": "",
                "event_type": "device_skipped_after_install_failure", "severity": "error",
                "message": f"cold_install.py terminó con código {install.returncode}",
                "evidence_relpath": "",
            })
            continue
        monitor_arguments = [
            "--run-dir", str(run_dir), "--device-id", alias, "--serial", serial,
            "--package", args.package, "--game-process", args.game_process,
            "--duration", str(args.duration), "--interval", str(args.interval),
            "--screenshot-second", str(args.screenshot_second),
        ]
        if args.surface_pattern:
            monitor_arguments.extend(["--surface-pattern", args.surface_pattern])
        monitor = run_script("monitor_device.py", monitor_arguments, check=False)
        if monitor.returncode != 0:
            failures += 1
            append_csv(run_dir / "eventos.csv", EVENT_HEADER, {
                "run_id": run["run_id"], "device_id": alias,
                "timestamp_utc": utc_now(), "elapsed_ms": "",
                "event_type": "monitor_failed", "severity": "error",
                "message": f"monitor_device.py terminó con código {monitor.returncode}",
                "evidence_relpath": "",
            })

    run_script("summarize_run.py", ["--run-dir", str(run_dir)], check=False)
    validation = run_script(
        "validate_dataset.py",
        ["--run-dir", str(run_dir), "--allow-pending-classification"],
        check=False,
    )
    if validation.returncode != 0:
        failures += 1
    set_run_status(run_dir, "awaiting_classification" if failures == 0 else "completed_with_errors")
    print(f"RUN_DIR={run_dir}", flush=True)
    print("Las capturas T+60 deben clasificarse con classify_screenshot.py y luego resumirse de nuevo.", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
