#!/usr/bin/env python3
"""Generate adaptive and legacy Android launcher resources from one image.

The input can be a raster image or an SVG understood by ImageMagick/Inkscape.
Generated resources are written to a build-only directory; the source image is
never modified.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


DENSITIES = {
    "mdpi": 1,
    "hdpi": 1.5,
    "xhdpi": 2,
    "xxhdpi": 3,
    "xxxhdpi": 4,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Android adaptive, monochrome and legacy launcher icons."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input image or SVG")
    parser.add_argument("--res-dir", required=True, type=Path, help="Generated Android res directory")
    parser.add_argument(
        "--resource-prefix",
        default="win2apk_launcher",
        help="Resource prefix used in generated XML and PNG names",
    )
    parser.add_argument(
        "--background-color",
        default="#000000",
        help="Opaque adaptive-icon background color, e.g. #FFCC16",
    )
    parser.add_argument(
        "--safe-zone-dp",
        type=float,
        default=66.0,
        help="Maximum logo box in the 108 dp adaptive-icon canvas",
    )
    return parser.parse_args()


def run_image(tool: str, args: list[str]) -> None:
    subprocess.run([tool, *args], check=True)


def require_image_tool() -> str:
    magick = shutil.which("magick")
    if magick:
        return magick
    convert = shutil.which("convert")
    if convert:
        return convert
    raise SystemExit(
        "Win2APK icon generation requires ImageMagick (magick/convert) on the build host."
    )


def validate_color(value: str) -> str:
    if not re.fullmatch(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?", value):
        raise SystemExit("--background-color must be #RRGGBB or #RRGGBBAA")
    return value


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def adaptive_xml(prefix: str, round_icon: bool = False) -> str:
    del round_icon  # The round wrapper intentionally reuses the same layers.
    return f'''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/{prefix}_background" />
    <foreground android:drawable="@mipmap/{prefix}_foreground" />
    <monochrome android:drawable="@mipmap/{prefix}_monochrome" />
</adaptive-icon>
'''


def main() -> None:
    args = parse_args()
    source = args.input.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Icon input does not exist or is not a file: {source}")
    if args.safe_zone_dp < 48 or args.safe_zone_dp > 66:
        raise SystemExit("--safe-zone-dp must be between 48 and 66 dp")
    background = validate_color(args.background_color)
    tool = require_image_tool()
    out_dir = args.res_dir.expanduser().resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    with tempfile.TemporaryDirectory(prefix="win2apk-icon-") as temp_name:
        temp = Path(temp_name)
        normalized = temp / "normalized.png"
        if source.suffix.lower() == ".svg" and shutil.which("inkscape"):
            subprocess.run(
                [
                    shutil.which("inkscape"),
                    str(source),
                    "--export-filename=" + str(normalized),
                    "--export-width=2048",
                    "--export-height=2048",
                ],
                check=True,
            )
        else:
            run_image(
                tool,
                [
                    str(source),
                    "-background",
                    "none",
                    "-alpha",
                    "on",
                    "-trim",
                    "+repage",
                    str(normalized),
                ],
            )

        values_dir = out_dir / "values"
        write_text(
            values_dir / f"{args.resource_prefix}_background.xml",
            f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="{args.resource_prefix}_background">{background}</color>
</resources>
''',
        )

        for density, multiplier in DENSITIES.items():
            adaptive_size = round(108 * multiplier)
            safe_size = round(args.safe_zone_dp * multiplier)
            legacy_size = round(48 * multiplier)
            mipmap_dir = out_dir / f"mipmap-{density}"
            mipmap_dir.mkdir(parents=True, exist_ok=True)

            foreground = mipmap_dir / f"{args.resource_prefix}_foreground.png"
            run_image(
                tool,
                [
                    str(normalized),
                    "-filter",
                    "Lanczos",
                    "-resize",
                    f"{safe_size}x{safe_size}",
                    "-gravity",
                    "center",
                    "-background",
                    "none",
                    "-extent",
                    f"{adaptive_size}x{adaptive_size}",
                    "-define",
                    "png:color-type=6",
                    str(foreground),
                ],
            )

            monochrome = mipmap_dir / f"{args.resource_prefix}_monochrome.png"
            alpha_mask = temp / f"alpha-{density}.png"
            run_image(
                tool,
                [
                    str(foreground),
                    "-alpha",
                    "extract",
                    str(alpha_mask),
                ],
            )
            run_image(
                tool,
                [
                    "-size",
                    f"{adaptive_size}x{adaptive_size}",
                    "xc:white",
                    str(alpha_mask),
                    "-compose",
                    "CopyOpacity",
                    "-composite",
                    "-define",
                    "png:color-type=6",
                    str(monochrome),
                ],
            )

            legacy_foreground = temp / f"legacy-foreground-{density}.png"
            legacy_content_size = round(legacy_size * 0.90)
            run_image(
                tool,
                [
                    str(normalized),
                    "-filter",
                    "Lanczos",
                    "-resize",
                    f"{legacy_content_size}x{legacy_content_size}",
                    "-gravity",
                    "center",
                    "-background",
                    "none",
                    "-extent",
                    f"{legacy_size}x{legacy_size}",
                    "-define",
                    "png:color-type=6",
                    str(legacy_foreground),
                ],
            )
            legacy = mipmap_dir / f"{args.resource_prefix}.png"
            run_image(
                tool,
                [
                    "-size",
                    f"{legacy_size}x{legacy_size}",
                    f"xc:{background}",
                    str(legacy_foreground),
                    "-gravity",
                    "center",
                    "-composite",
                    str(legacy),
                ],
            )
            shutil.copyfile(legacy, mipmap_dir / f"{args.resource_prefix}_round.png")

        anydpi_dir = out_dir / "mipmap-anydpi-v26"
        write_text(anydpi_dir / f"{args.resource_prefix}.xml", adaptive_xml(args.resource_prefix))
        write_text(
            anydpi_dir / f"{args.resource_prefix}_round.xml",
            adaptive_xml(args.resource_prefix, round_icon=True),
        )

    print(
        f"Win2APK icon: generated {args.resource_prefix} resources from {source} "
        f"(safe zone {args.safe_zone_dp:g}dp, background {background})"
    )


if __name__ == "__main__":
    main()
