#!/usr/bin/env python3
"""Aggregate a run, update the global catalog, and render its Markdown matrix."""

from __future__ import annotations

import argparse
import math
import statistics
from datetime import datetime
from pathlib import Path

from common import (
    CATALOG_RESULT_HEADER,
    RUN_HEADER,
    SUMMARY_HEADER,
    find_repo,
    read_csv,
    read_run,
    rewrite_csv,
    set_run_status,
    upsert_csv,
)


def numeric(rows: list[dict[str, str]], column: str) -> list[float]:
    values = []
    for row in rows:
        try:
            value = float(row.get(column, ""))
            if not math.isnan(value) and not math.isinf(value):
                values.append(value)
        except ValueError:
            continue
    return values


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def fmt(value: float | None, digits: int = 3) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def mean(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def maximum(values: list[float]) -> float | None:
    return max(values) if values else None


def minimum(values: list[float]) -> float | None:
    return min(values) if values else None


def first_event_ms(events: list[dict[str, str]], event_type: str) -> str:
    matches = [row for row in events if row["event_type"] == event_type and row["elapsed_ms"]]
    return min((row["elapsed_ms"] for row in matches), key=lambda value: int(value), default="")


def parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def delivery_to_first_frame(installs: list[dict[str, str]], events: list[dict[str, str]]) -> float | None:
    install = next((row for row in reversed(installs) if row["step"] == "install_apks"), None)
    frame_events = [row for row in events if row["event_type"] == "first_game_frame_observed"]
    if not install or not frame_events:
        return None
    started = parse_timestamp(install.get("started_at_utc", ""))
    observed = min(
        (timestamp for row in frame_events if (timestamp := parse_timestamp(row.get("timestamp_utc", "")))),
        default=None,
    )
    if started is None or observed is None or observed < started:
        return None
    return (observed - started).total_seconds()


def ratio(rows: list[dict[str, str]], column: str) -> float | None:
    values = [row[column].lower() == "true" for row in rows if row.get(column, "").lower() in {"true", "false"}]
    return sum(values) / len(values) if values else None


def summarize_device(
    run: dict[str, str],
    device_id: str,
    samples: list[dict[str, str]],
    installs: list[dict[str, str]],
    events: list[dict[str, str]],
    captures: list[dict[str, str]],
) -> dict[str, str]:
    install = next((row for row in reversed(installs) if row["step"] == "install_apks"), {})
    capture = captures[-1] if captures else {}
    app_alive = ratio(samples, "app_alive")
    game_alive = ratio(samples, "game_alive")
    final_app_alive = samples[-1].get("app_alive", "false") == "true" if samples else False
    primary = capture.get("primary_class", "")
    expected = run.get("expected_state", "")
    install_result = install.get("result", "")
    if install_result != "success":
        result = "failed_install"
        notes = "La instalación completa no quedó verificada."
    elif not samples:
        result = "inconclusive"
        notes = "No se registraron muestras temporales."
    elif not final_app_alive:
        result = "failed_process_exit"
        notes = "El proceso principal no estaba presente en la última muestra."
    elif primary in {"error_screen", "black_screen"}:
        result = "failed_visual_state"
        notes = f"La captura canónica se clasificó como {primary}."
    elif primary == "pending":
        result = "pending_classification"
        notes = "La medición terminó y la clasificación visual está pendiente."
    elif expected and expected != "N/R" and primary == expected:
        result = "approved_experimental"
        notes = "El estado observado coincide con el estado esperado en esta ejecución."
    elif primary in {"unknown", "other", "loading", "compatibility_ui", "android_dialog", "android_home", ""}:
        result = "partial"
        notes = "El proceso permaneció observable, pero la captura no confirma el estado esperado."
    else:
        result = "partial_state_mismatch"
        notes = f"Estado observado {primary}; estado esperado {expected or 'N/R'}."

    elapsed = numeric(samples, "elapsed_ms")
    metric = lambda column: numeric(samples, column)
    return {
        "run_id": run["run_id"], "exec_id": run["exec_id"], "device_id": device_id,
        "samples": str(len(samples)),
        "observed_seconds": fmt(max(elapsed) / 1000 if elapsed else None),
        "install_seconds": install.get("duration_seconds", ""),
        "delivery_to_first_frame_seconds": fmt(delivery_to_first_frame(installs, events)),
        "install_result": install_result,
        "app_first_seen_ms": first_event_ms(events, "app_process_first_seen"),
        "game_first_seen_ms": first_event_ms(events, "game_process_first_seen"),
        "first_frame_seen_ms": first_event_ms(events, "first_game_frame_observed"),
        "app_alive_ratio": fmt(app_alive), "game_alive_ratio": fmt(game_alive),
        "cpu_system_mean_pct": fmt(mean(metric("cpu_system_busy_pct"))),
        "cpu_app_mean_pct": fmt(mean(metric("cpu_app_total_capacity_pct"))),
        "cpu_app_p95_pct": fmt(percentile(metric("cpu_app_total_capacity_pct"), 0.95)),
        "cpu_game_mean_pct": fmt(mean(metric("cpu_game_total_capacity_pct"))),
        "app_rss_mean_kib": fmt(mean(metric("app_rss_kib"))),
        "app_rss_max_kib": fmt(maximum(metric("app_rss_kib"))),
        "game_rss_mean_kib": fmt(mean(metric("game_rss_kib"))),
        "game_rss_max_kib": fmt(maximum(metric("game_rss_kib"))),
        "app_pss_mean_kib": fmt(mean(metric("app_pss_kib"))),
        "app_pss_max_kib": fmt(maximum(metric("app_pss_kib"))),
        "game_pss_mean_kib": fmt(mean(metric("game_pss_kib"))),
        "game_pss_max_kib": fmt(maximum(metric("game_pss_kib"))),
        "mem_available_min_kib": fmt(minimum(metric("mem_available_kib"))),
        "gpu_busy_mean_pct": fmt(mean(metric("gpu_busy_pct"))),
        "gpu_busy_p95_pct": fmt(percentile(metric("gpu_busy_pct"), 0.95)),
        "fps_mean": fmt(mean(metric("fps_presented"))),
        "fps_p05": fmt(percentile(metric("fps_presented"), 0.05)),
        "fps_p95": fmt(percentile(metric("fps_presented"), 0.95)),
        "battery_temp_max_c": fmt(maximum(metric("battery_temp_c"))),
        "thermal_max_c": fmt(maximum(metric("thermal_max_c"))),
        "data_free_min_kib": fmt(minimum(metric("data_free_kib"))),
        "screen_primary_class": primary,
        "screen_description": capture.get("description", ""),
        "result": result, "notes": notes,
    }


def nr(value: str) -> str:
    return value if value not in {"", None} else "N/R"


def render_matrix(run: dict[str, str], summaries: list[dict[str, str]], run_relpath: str) -> str:
    results = {row["result"] for row in summaries}
    if summaries and results == {"approved_experimental"}:
        overall = "aprobado experimentalmente en los dispositivos medidos"
    elif any(result.startswith("failed") for result in results):
        overall = "parcial o fallido; consultar resultados por dispositivo"
    elif "pending_classification" in results:
        overall = "pendiente de clasificación visual"
    else:
        overall = "parcial o no concluyente"
    rows = []
    evidence = []
    for item in summaries:
        rows.append(
            f"| {item['device_id']} | {nr(item['install_result'])} | {nr(item['install_seconds'])} s | "
            f"{nr(item['delivery_to_first_frame_seconds'])} s | "
            f"{nr(item['app_first_seen_ms'])} ms | {nr(item['game_first_seen_ms'])} ms | "
            f"{nr(item['fps_mean'])} | {nr(item['app_pss_max_kib'])} | "
            f"{nr(item['screen_primary_class'])} | {item['result']} |"
        )
        evidence.append(
            f"- `{item['device_id']}`: [captura y CSV]({run_relpath}); "
            f"descripción: {nr(item['screen_description'])}."
        )
    return f"""# {run['exec_id']}: {run['scenario_description']}

- **Run de métricas:** `{run['run_id']}`
- **Fecha:** {run['created_at_utc'][:10]}
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** {overall}
- **Método:** `{run['install_mode']}`, secuencial, sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `{run['package_name']}` | `run.csv` |
| Artefacto | `{run['artifact_path']}` | Archivo medido |
| SHA-256 | `{run['artifact_sha256']}` | Calculado antes de instalar |
| Escenario | `{run['scenario_id']}` | {run['scenario_description']} |
| Estado esperado | `{run['expected_state']}` | Hipótesis previa |
| Duración | {run['duration_seconds']} s por dispositivo | Reloj monótono del host |
| Intervalo nominal | {run['sample_interval_seconds']} s | ADB sin root |
| Captura canónica | T+{run['screenshot_second']} s | Clasificación visual posterior |

## Métricas por dispositivo

| Dispositivo | Instalación | Tiempo instalación | Envío a primer frame | App visible | Juego visible | FPS medio | PSS app máx. KiB | Captura T+60 | Resultado |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
{chr(10).join(rows) if rows else '| N/R | N/R | N/R | N/R | N/R | N/R | N/R | N/R | N/R | N/R |'}

## Observación

Los valores anteriores provienen de los CSV y de la captura canónica; las celdas
`N/R` no se infieren a partir de otras métricas.

## Interpretación

Cada resultado solo representa el dispositivo, artefacto y condiciones de este
run. Una captura negra se interpreta junto con la presencia de procesos y no
demuestra por sí sola un cierre.

## Decisión

Revisar `resumen.csv`, los logs y la clasificación visual antes de aceptar o
descartar una configuración para otra familia de dispositivos.

## Evidencias

{chr(10).join(evidence) if evidence else '- N/R.'}

- [Carpeta estructurada del run]({run_relpath})
"""


def update_index(repo: Path, run: dict[str, str], summaries: list[dict[str, str]], exec_dir: Path) -> None:
    index = repo / "ejecuciones/index.md"
    content = index.read_text(encoding="utf-8")
    if f"| {run['exec_id']} |" in content:
        return
    devices = ", ".join(row["device_id"] for row in summaries) or "N/R"
    results = ", ".join(sorted({row["result"] for row in summaries})) or "N/R"
    rel = exec_dir.relative_to(repo / "ejecuciones")
    row = (
        f"| {run['exec_id']} | {run['scenario_description']} | Métricas automatizadas | "
        f"{devices} | {results} | [matriz.md](./{rel}/matriz.md) | "
        f"[datos](../metricas/runs/{run['run_id']}/) |\n"
    )
    marker = "\n## Plantilla"
    if marker in content:
        content = content.replace(marker, "\n" + row + marker, 1)
    else:
        content += "\n" + row
    index.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    run = read_run(run_dir)
    repo = find_repo(run_dir)
    samples = read_csv(run_dir / "muestras.csv")
    installs = read_csv(run_dir / "instalaciones.csv")
    events = read_csv(run_dir / "eventos.csv")
    captures = read_csv(run_dir / "capturas.csv")
    devices = read_csv(run_dir / "dispositivos.csv")
    device_ids = sorted({row["device_id"] for row in devices} | {row["device_id"] for row in samples})
    summaries = []
    for device_id in device_ids:
        select = lambda rows: [row for row in rows if row.get("device_id") == device_id]
        summary = summarize_device(run, device_id, select(samples), select(installs), select(events), select(captures))
        summaries.append(summary)
        upsert_csv(
            repo / "metricas/catalogo/resultados.csv",
            CATALOG_RESULT_HEADER,
            summary,
            ["run_id", "device_id"],
        )
    rewrite_csv(run_dir / "resumen.csv", SUMMARY_HEADER, summaries)
    pending = any(row["result"] == "pending_classification" for row in summaries)
    set_run_status(run_dir, "awaiting_classification" if pending else "summarized")
    run = read_run(run_dir)

    exec_relpath = (run_dir / "execution-link.txt").read_text(encoding="utf-8").strip()
    exec_dir = repo / exec_relpath
    run_relpath = str(Path("../../metricas/runs") / run["run_id"])
    (exec_dir / "matriz.md").write_text(render_matrix(run, summaries, run_relpath), encoding="utf-8")
    update_index(repo, run, summaries, exec_dir)
    print(f"{run['run_id']}: {len(summaries)} dispositivos resumidos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
