#!/usr/bin/env python3
"""Persist an AI visual classification for a run screenshot."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    CAPTURE_HEADER,
    CONFIDENCE_VALUES,
    REVIEW_VALUES,
    SCREEN_CLASSES,
    find_repo,
    read_csv,
    read_run,
    rewrite_csv,
    utc_now,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--device-id", required=True)
    parser.add_argument("--primary", choices=sorted(SCREEN_CLASSES - {"pending"}), required=True)
    parser.add_argument("--secondary", choices=[""] + sorted(SCREEN_CLASSES - {"pending"}), default="")
    parser.add_argument("--description", required=True)
    parser.add_argument("--visible-text", default="")
    parser.add_argument("--confidence", choices=sorted(CONFIDENCE_VALUES - {"pending"}), required=True)
    parser.add_argument("--model", default="N/R")
    parser.add_argument("--review-status", choices=sorted(REVIEW_VALUES), default="unreviewed")
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    read_run(run_dir)
    repo = find_repo(run_dir)
    capture_path = run_dir / "capturas.csv"
    rows = read_csv(capture_path)
    matches = [row for row in rows if row["device_id"] == args.device_id]
    if len(matches) != 1:
        raise RuntimeError(f"Se esperaba una captura para {args.device_id}; se encontraron {len(matches)}")
    target = matches[0]
    image_path = repo / target["image_relpath"]
    if not image_path.is_file():
        raise RuntimeError(f"No existe la evidencia visual: {image_path}")

    for row in rows:
        if row["device_id"] != args.device_id:
            continue
        row.update({
            "primary_class": args.primary,
            "secondary_class": args.secondary,
            "description": args.description,
            "visible_text": args.visible_text,
            "confidence": args.confidence,
            "classification_method": "ai_vision",
            "classifier_model": args.model,
            "classified_at_utc": utc_now(),
            "human_review_status": args.review_status,
        })
    rewrite_csv(capture_path, CAPTURE_HEADER, rows)
    print(f"{args.device_id}: {args.primary} ({args.confidence})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

