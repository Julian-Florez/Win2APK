#!/usr/bin/env python3
"""Build a local-testing APKS archive without persisting keystore passwords."""

from __future__ import annotations

import argparse
import os
import tempfile
import time
from pathlib import Path

from common import sha256_file, utc_now


def secret_file(value: str) -> tuple[tempfile.NamedTemporaryFile, str]:
    handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=True)
    os.chmod(handle.name, 0o600)
    handle.write(value)
    handle.flush()
    return handle, f"file:{handle.name}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aab", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bundletool", type=Path, required=True)
    parser.add_argument("--ks", type=Path, required=True)
    parser.add_argument("--ks-key-alias", default="androiddebugkey")
    parser.add_argument("--ks-pass-env", default="WIN2APK_KS_PASS")
    parser.add_argument("--key-pass-env", default="WIN2APK_KEY_PASS")
    parser.add_argument("--java", default="java")
    args = parser.parse_args()

    for path in (args.aab, args.bundletool, args.ks):
        if not path.expanduser().is_file():
            parser.error(f"No existe: {path}")
    ks_password = os.environ.get(args.ks_pass_env)
    key_password = os.environ.get(args.key_pass_env, ks_password or "")
    if not ks_password or not key_password:
        parser.error("Las contraseñas deben llegar por las variables de entorno indicadas")

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    log = output.with_suffix(output.suffix + ".build.log")
    ks_handle, ks_reference = secret_file(ks_password)
    key_handle, key_reference = secret_file(key_password)
    command = [
        args.java,
        "-jar", str(args.bundletool.resolve()),
        "build-apks",
        f"--bundle={args.aab.resolve()}",
        f"--output={output}",
        "--local-testing",
        "--overwrite",
        f"--ks={args.ks.expanduser().resolve()}",
        f"--ks-key-alias={args.ks_key_alias}",
        f"--ks-pass={ks_reference}",
        f"--key-pass={key_reference}",
    ]
    started = time.monotonic()
    try:
        import subprocess

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    finally:
        ks_handle.close()
        key_handle.close()
    duration = time.monotonic() - started
    log.write_text(
        f"started_at_utc={utc_now()}\nduration_seconds={duration:.3f}\nexit_code={result.returncode}\n"
        + result.stdout,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(f"bundletool falló; consulte {log}")
    print(f"{output}\t{output.stat().st_size}\t{sha256_file(output)}\t{duration:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

