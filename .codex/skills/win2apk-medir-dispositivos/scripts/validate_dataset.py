#!/usr/bin/env python3
"""Validate run schemas, time coverage, screenshots, and classifications."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from common import (
    CAPTURE_HEADER,
    CONFIDENCE_VALUES,
    DEVICE_HEADER,
    EVENT_HEADER,
    INSTALL_HEADER,
    REVIEW_VALUES,
    RUN_HEADER,
    SAMPLE_HEADER,
    SCREEN_CLASSES,
    SUMMARY_HEADER,
    find_repo,
    read_csv,
    read_run,
)


SCHEMAS = {
    "run.csv": RUN_HEADER,
    "dispositivos.csv": DEVICE_HEADER,
    "instalaciones.csv": INSTALL_HEADER,
    "muestras.csv": SAMPLE_HEADER,
    "eventos.csv": EVENT_HEADER,
    "capturas.csv": CAPTURE_HEADER,
    "resumen.csv": SUMMARY_HEADER,
}


NUMERIC_SAMPLE_COLUMNS = {
    "sample_index", "elapsed_ms", "app_pid_count", "game_pid_count",
    "cpu_system_busy_pct", "cpu_app_total_capacity_pct", "cpu_game_total_capacity_pct",
    "load_1m", "app_rss_kib", "game_rss_kib", "app_pss_kib", "game_pss_kib",
    "graphics_pss_kib", "swap_pss_kib", "mem_total_kib", "mem_available_kib",
    "ion_heap_kib", "gpu_memory_kib", "gpu_busy_pct", "gpu_freq_hz",
    "fps_presented", "frame_count_delta", "battery_pct", "battery_temp_c",
    "thermal_max_c", "data_free_kib",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-classification", action="store_true")
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    repo = find_repo(run_dir)
    errors: list[str] = []
    warnings: list[str] = []

    for filename, expected in SCHEMAS.items():
        path = run_dir / filename
        if not path.is_file():
            errors.append(f"falta {filename}")
            continue
        with path.open(newline="", encoding="utf-8") as source:
            actual = next(csv.reader(source), [])
        if actual != expected:
            errors.append(f"esquema incorrecto en {filename}")
    if errors:
        for message in errors:
            print(f"ERROR: {message}")
        return 1

    run = read_run(run_dir)
    duration = float(run["duration_seconds"])
    interval = float(run["sample_interval_seconds"])
    screenshot_second = float(run["screenshot_second"])
    samples = read_csv(run_dir / "muestras.csv")
    devices = read_csv(run_dir / "dispositivos.csv")
    captures = read_csv(run_dir / "capturas.csv")
    summaries = read_csv(run_dir / "resumen.csv")
    device_ids = [row["device_id"] for row in devices]
    if len(device_ids) != len(set(device_ids)):
        errors.append("hay dispositivos duplicados en dispositivos.csv")

    sample_keys = set()
    for row in samples:
        key = (row["run_id"], row["device_id"], row["sample_index"])
        if key in sample_keys:
            errors.append(f"muestra duplicada: {key}")
        sample_keys.add(key)
        for column in NUMERIC_SAMPLE_COLUMNS:
            value = row[column]
            if not value:
                continue
            try:
                float(value)
            except ValueError:
                errors.append(f"valor no numérico en {column}: {value!r}")

    for device_id in device_ids:
        device_samples = [row for row in samples if row["device_id"] == device_id]
        if not device_samples:
            errors.append(f"{device_id}: sin muestras")
            continue
        elapsed = [float(row["elapsed_ms"]) / 1000 for row in device_samples]
        if elapsed != sorted(elapsed):
            errors.append(f"{device_id}: elapsed_ms no es monótono")
        if max(elapsed) < duration * 0.95:
            errors.append(f"{device_id}: cobertura {max(elapsed):.1f}s menor al 95% de {duration}s")
        nominal_count = duration / interval
        if len(device_samples) < nominal_count * 0.5:
            warnings.append(f"{device_id}: solo {len(device_samples)} de ~{nominal_count:.0f} muestras nominales")
        device_captures = [row for row in captures if row["device_id"] == device_id]
        if len(device_captures) != 1:
            errors.append(f"{device_id}: se esperaba una captura y hay {len(device_captures)}")
            continue
        capture = device_captures[0]
        capture_elapsed = float(capture["elapsed_ms"]) / 1000
        if abs(capture_elapsed - screenshot_second) > 5:
            errors.append(f"{device_id}: captura en T+{capture_elapsed:.1f}s, fuera de tolerancia")
        image = repo / capture["image_relpath"]
        if not image.is_file() or image.stat().st_size == 0:
            errors.append(f"{device_id}: no existe PNG de captura")
        if capture["primary_class"] not in SCREEN_CLASSES:
            errors.append(f"{device_id}: clase visual inválida")
        if capture["confidence"] not in CONFIDENCE_VALUES:
            errors.append(f"{device_id}: confianza inválida")
        if capture["human_review_status"] not in REVIEW_VALUES:
            errors.append(f"{device_id}: estado de revisión inválido")
        if capture["primary_class"] == "pending" and not args.allow_pending_classification:
            errors.append(f"{device_id}: clasificación visual pendiente")
    if summaries and {row["device_id"] for row in summaries} != set(device_ids):
        errors.append("resumen.csv no contiene exactamente los dispositivos inventariados")

    for warning in warnings:
        print(f"AVISO: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"OK: {run['run_id']} válido; {len(device_ids)} dispositivos, {len(samples)} muestras")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

