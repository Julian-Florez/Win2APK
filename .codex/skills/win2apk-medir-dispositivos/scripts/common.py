#!/usr/bin/env python3
"""Shared schemas and process helpers for Win2APK device measurements."""

from __future__ import annotations

import csv
import hashlib
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence


RUN_HEADER = [
    "run_id", "exec_id", "created_at_utc", "scenario_id",
    "scenario_description", "expected_state", "duration_seconds",
    "sample_interval_seconds", "screenshot_second", "package_name",
    "artifact_path", "artifact_sha256", "artifact_bytes", "install_mode",
    "status", "notes",
]

DEVICE_HEADER = [
    "run_id", "device_id", "observed_at_utc", "manufacturer", "model",
    "product", "android_device", "android_version", "api_level", "abi_list",
    "hardware", "soc_model", "cpu_cores", "cpu_max_freq_khz", "ram_total_kib",
    "gpu_vendor", "gpu_renderer", "gpu_version", "vulkan_version",
    "screen_resolution", "screen_density_dpi", "serial_hash",
]

INSTALL_HEADER = [
    "run_id", "device_id", "step", "started_at_utc", "ended_at_utc",
    "duration_seconds", "result", "exit_code", "artifact_sha256",
    "artifact_bytes", "free_data_before_kib", "free_data_after_kib",
    "log_relpath", "message",
]

SAMPLE_HEADER = [
    "run_id", "device_id", "sample_index", "timestamp_utc", "elapsed_ms",
    "phase", "app_alive", "game_alive", "app_pid_count", "game_pid_count",
    "cpu_system_busy_pct", "cpu_app_total_capacity_pct", "cpu_game_total_capacity_pct",
    "load_1m", "app_rss_kib", "game_rss_kib", "app_pss_kib", "game_pss_kib",
    "graphics_pss_kib", "swap_pss_kib", "mem_total_kib", "mem_available_kib",
    "ion_heap_kib", "gpu_memory_kib", "gpu_busy_pct", "gpu_freq_hz",
    "fps_presented", "frame_count_delta", "fps_source", "battery_pct",
    "battery_temp_c", "thermal_max_c", "thermal_status", "data_free_kib",
    "screen_on", "metric_status",
]

EVENT_HEADER = [
    "run_id", "device_id", "timestamp_utc", "elapsed_ms", "event_type",
    "severity", "message", "evidence_relpath",
]

CAPTURE_HEADER = [
    "run_id", "device_id", "captured_at_utc", "elapsed_ms", "scheduled_second",
    "image_relpath", "primary_class", "secondary_class", "description",
    "visible_text", "confidence", "classification_method", "classifier_model",
    "classified_at_utc", "human_review_status",
]

SUMMARY_HEADER = [
    "run_id", "exec_id", "device_id", "samples", "observed_seconds",
    "install_seconds", "delivery_to_first_frame_seconds", "install_result",
    "app_first_seen_ms", "game_first_seen_ms", "first_frame_seen_ms",
    "app_alive_ratio", "game_alive_ratio", "cpu_system_mean_pct",
    "cpu_app_mean_pct", "cpu_app_p95_pct", "cpu_game_mean_pct",
    "app_rss_mean_kib", "app_rss_max_kib", "game_rss_mean_kib",
    "game_rss_max_kib", "app_pss_mean_kib", "app_pss_max_kib",
    "game_pss_mean_kib", "game_pss_max_kib", "mem_available_min_kib",
    "gpu_busy_mean_pct", "gpu_busy_p95_pct", "fps_mean", "fps_p05",
    "fps_p95", "battery_temp_max_c", "thermal_max_c", "data_free_min_kib",
    "screen_primary_class", "screen_description", "result", "notes",
]

CATALOG_RUN_HEADER = RUN_HEADER
CATALOG_DEVICE_HEADER = [column for column in DEVICE_HEADER if column != "run_id"] + ["last_run_id"]
CATALOG_RESULT_HEADER = SUMMARY_HEADER

SCREEN_CLASSES = {
    "pending", "gameplay", "title_screen", "loading", "menu", "cutscene",
    "settings", "compatibility_ui", "android_dialog", "error_screen",
    "black_screen", "android_home", "other", "unknown",
}
CONFIDENCE_VALUES = {"pending", "high", "medium", "low"}
REVIEW_VALUES = {"unreviewed", "confirmed", "corrected"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def find_repo(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "AGENTS.md").is_file() and (candidate / "ejecuciones").is_dir():
            return candidate
    script_repo = Path(__file__).resolve().parents[4]
    if (script_repo / "AGENTS.md").is_file():
        return script_repo
    raise RuntimeError("No se encontró la raíz del repositorio Win2APK")


def sha256_file(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def short_serial_hash(serial: str) -> str:
    return hashlib.sha256(serial.encode("utf-8")).hexdigest()[:12]


def safe_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not normalized:
        raise ValueError(f"Identificador vacío después de normalizar: {value!r}")
    return normalized


def ensure_csv(path: Path, header: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size:
        with path.open(newline="", encoding="utf-8") as source:
            existing = next(csv.reader(source), [])
        if list(existing) != list(header):
            raise RuntimeError(f"Esquema inesperado en {path}: {existing}")
        return
    with path.open("w", newline="", encoding="utf-8") as target:
        csv.writer(target).writerow(header)


def append_csv(path: Path, header: Sequence[str], row: Mapping[str, object]) -> None:
    ensure_csv(path, header)
    with path.open("a", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=header, extrasaction="ignore")
        writer.writerow({key: row.get(key, "") for key in header})


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def rewrite_csv(path: Path, header: Sequence[str], rows: Iterable[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in header})
    os.replace(temporary, path)


def upsert_csv(
    path: Path,
    header: Sequence[str],
    row: Mapping[str, object],
    key_columns: Sequence[str],
) -> None:
    rows = read_csv(path)
    wanted = tuple(str(row.get(column, "")) for column in key_columns)
    output: list[Mapping[str, object]] = []
    replaced = False
    for existing in rows:
        current = tuple(existing.get(column, "") for column in key_columns)
        if current == wanted:
            output.append(row)
            replaced = True
        else:
            output.append(existing)
    if not replaced:
        output.append(row)
    rewrite_csv(path, header, output)


def run_command(
    command: Sequence[str],
    *,
    timeout: float | None = None,
    check: bool = False,
    text: bool = True,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        timeout=timeout,
        check=check,
    )


def adb(
    serial: str,
    arguments: Sequence[str],
    *,
    timeout: float | None = 30,
    check: bool = False,
    text: bool = True,
) -> subprocess.CompletedProcess:
    return run_command(["adb", "-s", serial, *arguments], timeout=timeout, check=check, text=text)


def adb_shell(serial: str, command: str, *, timeout: float | None = 30) -> str:
    result = adb(serial, ["shell", command], timeout=timeout)
    if result.returncode != 0:
        error = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"ADB falló ({result.returncode}): {error}")
    return result.stdout.replace("\r\n", "\n")


def relative_to_repo(path: Path, repo: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo.resolve()))
    except ValueError:
        return str(path.resolve())


def read_run(run_dir: Path) -> dict[str, str]:
    rows = read_csv(run_dir / "run.csv")
    if len(rows) != 1:
        raise RuntimeError(f"Se esperaba una fila en {run_dir / 'run.csv'}")
    return rows[0]


def set_run_status(run_dir: Path, status: str) -> None:
    row = read_run(run_dir)
    row["status"] = status
    rewrite_csv(run_dir / "run.csv", RUN_HEADER, [row])
    repo = find_repo(run_dir)
    upsert_csv(repo / "metricas/catalogo/runs.csv", CATALOG_RUN_HEADER, row, ["run_id"])
