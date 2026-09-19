#!/usr/bin/env python3
"""Create an immutable run folder and its paired execution record."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

from common import (
    CAPTURE_HEADER,
    CATALOG_DEVICE_HEADER,
    CATALOG_RESULT_HEADER,
    CATALOG_RUN_HEADER,
    DEVICE_HEADER,
    EVENT_HEADER,
    INSTALL_HEADER,
    RUN_HEADER,
    SAMPLE_HEADER,
    SUMMARY_HEADER,
    append_csv,
    ensure_csv,
    find_repo,
    relative_to_repo,
    rewrite_csv,
    safe_name,
    sha256_file,
    utc_now,
)


def next_run_id(repo: Path) -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    pattern = re.compile(rf"RUN-{today}-(\d{{3}})$")
    numbers = []
    for path in (repo / "metricas/runs").glob(f"RUN-{today}-*"):
        match = pattern.fullmatch(path.name)
        if match:
            numbers.append(int(match.group(1)))
    return f"RUN-{today}-{max(numbers, default=0) + 1:03d}"


def next_exec_number(repo: Path) -> int:
    numbers = []
    for path in (repo / "ejecuciones").iterdir():
        if path.is_dir() and (match := re.match(r"^(\d+)-", path.name)):
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def initial_matrix(exec_id: str, run_id: str, row: dict[str, object], run_relpath: str) -> str:
    return f"""# {exec_id}: {row['scenario_description']}

- **Run de métricas:** `{run_id}`
- **Fecha:** {str(row['created_at_utc'])[:10]}
- **Tipo:** automatizada, instalación fría y medición temporal
- **Resultado general:** N/R; ejecución en curso
- **Método:** reinstalación secuencial y observación ADB sin root

## Condiciones de prueba

| Campo | Valor | Fuente o condición |
|---|---|---|
| Aplicación | `{row['package_name']}` | Parámetro de ejecución |
| Publicación/hash | `{row['artifact_sha256'] or 'N/R'}` | SHA-256 del artefacto |
| Método | `{row['install_mode']}` | Automatización de la skill |
| Escenario | `{row['scenario_id']}` | {row['scenario_description']} |
| Estado esperado | {row['expected_state'] or 'N/R'} | Hipótesis previa; no sustituye la observación |
| Duración | {row['duration_seconds']} s por dispositivo | Reloj monótono del host |
| Intervalo | {row['sample_interval_seconds']} s | Muestreo ADB |
| Captura canónica | T+{row['screenshot_second']} s | Pantalla real sin navegación automática |

## Observación

Pendiente hasta finalizar la captura de datos.

## Interpretación

N/R.

## Decisión

N/R.

## Evidencia

- [Datos estructurados]({run_relpath})
- Capturas: pendientes en `screenshots/<device_id>/`.
- Logs: pendientes en `logs/<device_id>/`.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--expected-state", default="N/R")
    parser.add_argument("--duration", type=int, default=300)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--screenshot-second", type=int, default=60)
    parser.add_argument("--package", default="com.cuphead")
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--install-mode", default="bundletool-install-apks-cold")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    if args.duration <= 0 or args.interval <= 0:
        parser.error("duration e interval deben ser positivos")
    if not 0 <= args.screenshot_second <= args.duration:
        parser.error("screenshot-second debe estar dentro de la duración")
    artifact = args.artifact.resolve()
    if not artifact.is_file():
        parser.error(f"No existe el artefacto: {artifact}")

    repo = (args.repo or find_repo()).resolve()
    run_id = next_run_id(repo)
    exec_number = next_exec_number(repo)
    exec_id = f"EXEC-{exec_number:03d}"
    run_dir = repo / "metricas/runs" / run_id
    if run_dir.exists():
        raise RuntimeError(f"La ejecución ya existe: {run_dir}")
    (run_dir / "screenshots").mkdir(parents=True)
    (run_dir / "logs").mkdir()

    artifact_hash = sha256_file(artifact)
    row: dict[str, object] = {
        "run_id": run_id,
        "exec_id": exec_id,
        "created_at_utc": utc_now(),
        "scenario_id": safe_name(args.scenario),
        "scenario_description": args.description,
        "expected_state": args.expected_state,
        "duration_seconds": args.duration,
        "sample_interval_seconds": args.interval,
        "screenshot_second": args.screenshot_second,
        "package_name": args.package,
        "artifact_path": relative_to_repo(artifact, repo),
        "artifact_sha256": artifact_hash,
        "artifact_bytes": artifact.stat().st_size,
        "install_mode": args.install_mode,
        "status": "initialized",
        "notes": args.notes,
    }
    rewrite_csv(run_dir / "run.csv", RUN_HEADER, [row])
    for name, header in [
        ("dispositivos.csv", DEVICE_HEADER),
        ("instalaciones.csv", INSTALL_HEADER),
        ("muestras.csv", SAMPLE_HEADER),
        ("eventos.csv", EVENT_HEADER),
        ("capturas.csv", CAPTURE_HEADER),
        ("resumen.csv", SUMMARY_HEADER),
    ]:
        ensure_csv(run_dir / name, header)

    catalog = repo / "metricas/catalogo"
    ensure_csv(catalog / "runs.csv", CATALOG_RUN_HEADER)
    ensure_csv(catalog / "devices.csv", CATALOG_DEVICE_HEADER)
    ensure_csv(catalog / "resultados.csv", CATALOG_RESULT_HEADER)
    append_csv(catalog / "runs.csv", CATALOG_RUN_HEADER, row)

    exec_slug = f"{exec_number:02d}-metricas-{safe_name(args.scenario)}-{datetime.now(timezone.utc):%Y%m%d}"
    exec_dir = repo / "ejecuciones" / exec_slug
    (exec_dir / "evidencias").mkdir(parents=True)
    (exec_dir / "logs").mkdir()
    run_relpath = Path("../../metricas/runs") / run_id
    (exec_dir / "matriz.md").write_text(
        initial_matrix(exec_id, run_id, row, str(run_relpath)), encoding="utf-8"
    )
    (run_dir / "execution-link.txt").write_text(
        relative_to_repo(exec_dir, repo) + "\n", encoding="utf-8"
    )

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

