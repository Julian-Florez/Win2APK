#!/usr/bin/env python3
"""Safely publish the Win2APK repository and the Winlator app submodule."""

from __future__ import annotations

import argparse
import fnmatch
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


FORBIDDEN_PATTERNS = (
    "*.apk",
    "*.aab",
    "*.apks",
    "*.keystore",
    "*.jks",
    "cuphead/",
    "cuphead_data",
    "cuphead_files_",
    "app/build/",
    "outputs/",
)

ROOT_DEFAULT_PATHS = (
    "AGENTS.md",
    ".gitignore",
    ".codex/skills/win2apk-publicar-repos",
    ".codex/skills/win2apk-medir-dispositivos",
    "bitacora",
    "config",
    "documentacion",
    "ejecuciones",
    "limitaciones",
    "metricas",
    "third_party",
)

APP_DEFAULT_PATHS = (
    "app/build.gradle",
    "app/src/main/assets/win2apk.json",
    "app/src/main/assets/dxwrapper/dxvk-*.tzst",
    "app/src/main/assets/graphics_driver/bcn-layer-*.tzst",
    "app/src/main/jniLibs/arm64-v8a/libVkLayer_BCN_BCnLayer.so",
    "app/src/main/jniLibs/arm64-v8a/libbcn_layer.so",
    "app/src/main/cpp/vortekrenderer",
    "app/src/main/java/com/winlator",
    "settings.gradle",
)


@dataclass(frozen=True)
class Repo:
    name: str
    path: Path
    remote: str


class PublishError(RuntimeError):
    pass


def run(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and proc.returncode != 0:
        command = shlex.join(["git", *args])
        raise PublishError(f"{repo}: falló `{command}`\n{proc.stdout.strip()}")
    return proc.stdout.rstrip()


def git_status(repo: Path) -> list[str]:
    output = run(repo, "status", "--short", "--untracked-files=all")
    return output.splitlines() if output else []


def branch(repo: Path) -> str:
    value = run(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    if not value:
        raise PublishError(f"{repo}: detached HEAD; no se publica automáticamente")
    return value


def remote_url(repo: Path, remote: str) -> str:
    value = run(repo, "remote", "get-url", remote, check=False)
    if not value:
        raise PublishError(f"{repo}: no existe el remoto de publicación `{remote}`")
    return value


def changed_paths(status_lines: list[str]) -> list[str]:
    paths = []
    for line in status_lines:
        if len(line) < 4:
            continue
        value = line[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value)
    return paths


def is_forbidden(path: str) -> bool:
    normalized = path.replace(os.sep, "/")
    basename = Path(normalized).name
    if any(fnmatch.fnmatch(basename, pattern) for pattern in ("*.apk", "*.aab", "*.apks", "*.keystore", "*.jks")):
        return True
    if normalized.startswith(("cuphead/", "cuphead_data", "cuphead_files_", "app/build/", "outputs/")):
        return True
    return False


def is_generated(path: str) -> bool:
    normalized = path.replace(os.sep, "/")
    return "/__pycache__/" in f"/{normalized}/" or normalized.endswith(".pyc")


def matches_path(path: str, pathspec: str) -> bool:
    normalized = path.replace(os.sep, "/")
    spec = pathspec.rstrip("/").replace(os.sep, "/")
    if "*" in spec or "?" in spec or "[" in spec:
        return fnmatch.fnmatch(normalized, spec) or fnmatch.fnmatch(normalized, f"*/{spec}")
    return normalized == spec or normalized.startswith(f"{spec}/")


def select_paths(repo: Repo, extra_paths: list[str], defaults: tuple[str, ...]) -> tuple[list[str], list[str]]:
    status = git_status(repo.path)
    paths = changed_paths(status)
    pathspecs = list(defaults) + extra_paths
    selected = [path for path in paths if any(matches_path(path, spec) for spec in pathspecs)]
    generated = [path for path in selected if is_generated(path)]
    selected = [path for path in selected if not is_generated(path)]
    excluded = [path for path in paths if path not in selected]
    if generated:
        print(f"[{repo.name}] se omiten artefactos generados: {', '.join(generated)}")
    forbidden = [path for path in selected if is_forbidden(path)]
    if forbidden:
        raise PublishError(f"{repo.name}: rutas prohibidas seleccionadas: {', '.join(forbidden)}")
    return selected, excluded


def show_repo(repo: Repo, paths: list[str], excluded: list[str]) -> None:
    print(f"\n[{repo.name}] {repo.path}")
    print(f"  rama:   {branch(repo.path)}")
    print(f"  remoto: {repo.remote} -> {remote_url(repo.path, repo.remote)}")
    print(f"  incluir ({len(paths)}):")
    for path in paths:
        print(f"    + {path}")
    if excluded:
        print(f"  fuera de alcance ({len(excluded)}):")
        for path in excluded[:40]:
            print(f"    ! {path}")
        if len(excluded) > 40:
            print(f"    ! ... y {len(excluded) - 40} más")


def stage(repo: Repo, paths: list[str]) -> None:
    if not paths:
        return
    run(repo.path, "add", "--", *paths)
    staged = run(repo.path, "diff", "--cached", "--name-only").splitlines()
    forbidden = [path for path in staged if is_forbidden(path)]
    if forbidden:
        raise PublishError(f"{repo.name}: el índice contiene rutas prohibidas: {', '.join(forbidden)}")


def staged_paths(repo: Repo) -> list[str]:
    output = run(repo.path, "diff", "--cached", "--name-only")
    return output.splitlines() if output else []


def commit(repo: Repo, message: str) -> str | None:
    paths = staged_paths(repo)
    if not paths:
        print(f"[{repo.name}] sin cambios preparados; no se crea commit")
        return None
    run(repo.path, "commit", "-m", message)
    return run(repo.path, "rev-parse", "HEAD")


def push(repo: Repo, sha: str) -> None:
    current_branch = branch(repo.path)
    run(repo.path, "push", repo.remote, f"HEAD:refs/heads/{current_branch}")
    print(f"[{repo.name}] publicado {sha[:12]} en {repo.remote}/{current_branch}")


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[4]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=root)
    parser.add_argument("--app", type=Path, default=root / "winlator" / "app")
    parser.add_argument("--superproject", type=Path, default=root / "winlator")
    parser.add_argument("--root-remote", default="origin")
    parser.add_argument("--app-remote", default="julian")
    parser.add_argument("--superproject-remote", default="julian")
    parser.add_argument("--message", help="mensaje base de los commits")
    parser.add_argument("--root-path", action="append", default=[], help="ruta adicional del repositorio raíz")
    parser.add_argument("--only-root-paths", action="store_true", help="usar solo las rutas indicadas con --root-path")
    parser.add_argument("--app-path", action="append", default=[], help="ruta adicional de winlator/app")
    parser.add_argument("--execute", action="store_true", help="preparar y crear commits; sin esto solo inspecciona")
    parser.add_argument("--push", action="store_true", help="hacer push después de los commits")
    parser.add_argument("--skip-superproject", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.push and not args.execute:
        raise PublishError("--push requiere --execute")
    if args.execute and not args.message:
        raise PublishError("--execute requiere --message")

    root_repo = Repo("Win2APK", args.root.resolve(), args.root_remote)
    app_repo = Repo("Winlator app", args.app.resolve(), args.app_remote)
    manifest_repo = Repo("Winlator manifest", args.superproject.resolve(), args.superproject_remote)

    for repo in (root_repo, app_repo):
        if not (repo.path / ".git").exists() and not (repo.path / "HEAD").exists():
            raise PublishError(f"{repo.name}: no parece un repositorio Git: {repo.path}")

    root_defaults = () if args.only_root_paths else ROOT_DEFAULT_PATHS
    root_paths, root_excluded = select_paths(root_repo, args.root_path, root_defaults)
    app_paths, app_excluded = select_paths(app_repo, args.app_path, APP_DEFAULT_PATHS)
    show_repo(root_repo, root_paths, root_excluded)
    show_repo(app_repo, app_paths, app_excluded)

    if args.skip_superproject:
        manifest_paths, manifest_excluded = [], []
    else:
        manifest_status = git_status(manifest_repo.path)
        manifest_status_paths = changed_paths(manifest_status)
        manifest_pointer_paths = set(run(manifest_repo.path, "diff", "--name-only", "--", "app").splitlines())
        manifest_pointer_paths.update(run(manifest_repo.path, "diff", "--cached", "--name-only", "--", "app").splitlines())
        manifest_paths = ["app"] if "app" in manifest_pointer_paths else []
        manifest_excluded = [path for path in manifest_status_paths if path != "app"]
        show_repo(manifest_repo, manifest_paths, manifest_excluded)
        if manifest_excluded:
            raise PublishError("Winlator manifest: hay cambios fuera del puntero app; revisar antes de publicar")

    if not args.execute:
        print("\nInspección completada. No se modificó el índice, no se creó ningún commit y no se hizo push.")
        return 0

    if not root_paths and not app_paths and (args.skip_superproject or not manifest_paths):
        print("No hay cambios seleccionados para publicar.")
        return 0

    stage(app_repo, app_paths)
    app_sha = commit(app_repo, f"{args.message} (winlator app)")

    if not args.skip_superproject:
        if app_sha:
            run(manifest_repo.path, "add", "--", "app")
        manifest_sha = commit(manifest_repo, f"Update app submodule: {app_sha[:12] if app_sha else 'existing'}")
    else:
        manifest_sha = None

    stage(root_repo, root_paths)
    root_sha = commit(root_repo, f"{args.message} (Win2APK)")

    if args.push:
        if app_sha:
            push(app_repo, app_sha)
        if manifest_sha:
            push(manifest_repo, manifest_sha)
        if root_sha:
            push(root_repo, root_sha)

    print("\nPublicación finalizada.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PublishError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(2)
