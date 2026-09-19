#!/usr/bin/env python3
"""Remove an Android package and time a full bundletool reinstall."""

from __future__ import annotations

import argparse
import subprocess
import time
from pathlib import Path

from common import (
    EVENT_HEADER,
    INSTALL_HEADER,
    adb,
    adb_shell,
    append_csv,
    find_repo,
    read_run,
    relative_to_repo,
    sha256_file,
    utc_now,
)


def data_free_kib(serial: str) -> str:
    try:
        output = adb_shell(serial, "df -k /data | tail -n 1")
        columns = output.split()
        return columns[3] if len(columns) >= 4 and columns[3].isdigit() else ""
    except RuntimeError:
        return ""


def package_path(serial: str, package: str) -> str:
    result = adb(serial, ["shell", "pm", "path", package], timeout=30)
    return result.stdout.strip()


def record_step(
    run_dir: Path,
    device_id: str,
    step: str,
    started_at: str,
    ended_at: str,
    duration: float,
    result: str,
    exit_code: int,
    artifact_hash: str,
    artifact_bytes: int,
    free_before: str,
    free_after: str,
    log_path: Path,
    message: str,
) -> None:
    repo = find_repo(run_dir)
    run = read_run(run_dir)
    append_csv(run_dir / "instalaciones.csv", INSTALL_HEADER, {
        "run_id": run["run_id"],
        "device_id": device_id,
        "step": step,
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "duration_seconds": f"{duration:.3f}",
        "result": result,
        "exit_code": exit_code,
        "artifact_sha256": artifact_hash,
        "artifact_bytes": artifact_bytes,
        "free_data_before_kib": free_before,
        "free_data_after_kib": free_after,
        "log_relpath": relative_to_repo(log_path, repo),
        "message": message,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--device-id", required=True)
    parser.add_argument("--serial", required=True)
    parser.add_argument("--apks", type=Path, required=True)
    parser.add_argument("--bundletool", type=Path, required=True)
    parser.add_argument("--package")
    parser.add_argument("--java", default="java")
    parser.add_argument("--confirm-delete", required=True)
    args = parser.parse_args()

    if args.confirm_delete != "ELIMINAR-COMPLETO":
        parser.error("La eliminación fría requiere --confirm-delete ELIMINAR-COMPLETO")
    run_dir = args.run_dir.resolve()
    run = read_run(run_dir)
    package = args.package or run["package_name"]
    apks = args.apks.resolve()
    bundletool = args.bundletool.resolve()
    if not apks.is_file() or not bundletool.is_file():
        parser.error("No existe APKS o bundletool")
    expected_hash = run["artifact_sha256"]
    actual_hash = sha256_file(apks)
    if expected_hash and expected_hash != actual_hash:
        raise RuntimeError("El hash del APKS no coincide con run.csv")

    device_id = args.device_id
    logs = run_dir / "logs" / device_id
    logs.mkdir(parents=True, exist_ok=True)
    free_before = data_free_kib(args.serial)

    uninstall_log = logs / "uninstall.log"
    started_at = utc_now()
    started = time.monotonic()
    uninstall = adb(args.serial, ["uninstall", package], timeout=300)
    duration = time.monotonic() - started
    ended_at = utc_now()
    uninstall_text = (uninstall.stdout + uninstall.stderr).strip()
    installed_path = package_path(args.serial, package)
    removed = not installed_path
    uninstall_result = "success" if removed else "failed"
    if "Unknown package" in uninstall_text and removed:
        uninstall_result = "not_installed"
    uninstall_log.write_text(uninstall.stdout + uninstall.stderr, encoding="utf-8")
    record_step(
        run_dir, device_id, "uninstall", started_at, ended_at, duration,
        uninstall_result, uninstall.returncode, actual_hash, apks.stat().st_size,
        free_before, data_free_kib(args.serial), uninstall_log, uninstall_text,
    )
    if not removed:
        raise RuntimeError(f"{device_id}: el paquete continúa instalado")

    install_log = logs / "install-apks.log"
    free_install_before = data_free_kib(args.serial)
    started_at = utc_now()
    started = time.monotonic()
    command = [
        args.java,
        "-jar", str(bundletool),
        "install-apks",
        f"--apks={apks}",
        f"--device-id={args.serial}",
    ]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    duration = time.monotonic() - started
    ended_at = utc_now()
    install_log.write_text(process.stdout, encoding="utf-8")
    installed_path = package_path(args.serial, package)
    result = "success" if process.returncode == 0 and installed_path else "failed"
    message = process.stdout.strip().splitlines()[-1] if process.stdout.strip() else ""
    record_step(
        run_dir, device_id, "install_apks", started_at, ended_at, duration,
        result, process.returncode, actual_hash, apks.stat().st_size,
        free_install_before, data_free_kib(args.serial), install_log, message,
    )
    if result != "success":
        append_csv(run_dir / "eventos.csv", EVENT_HEADER, {
            "run_id": run["run_id"], "device_id": device_id,
            "timestamp_utc": utc_now(), "elapsed_ms": "",
            "event_type": "install_failed", "severity": "error",
            "message": message, "evidence_relpath": relative_to_repo(install_log, find_repo(run_dir)),
        })
        raise RuntimeError(f"{device_id}: bundletool no instaló el paquete")
    print(f"{device_id}: instalación completa en {duration:.3f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
