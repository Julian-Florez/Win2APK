#!/usr/bin/env python3
"""Recupera versiones públicas y legales de los 45 estudios priorizados."""

from __future__ import annotations

import csv
import hashlib
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SELECTION = ROOT / "outputs/prisma_screening_union_20260830/priorizacion_45.csv"
OUT = ROOT / "estado_del_arte/textos_completos_45"
PDF_DIR = OUT / "pdfs"
PDF_DIR.mkdir(parents=True, exist_ok=True)

# Solo se incluyen URLs públicas de editor, repositorios institucionales,
# servidores de autores o preprints. No se incluyen enlaces que evadan acceso.
PUBLIC_PDFS = {
    "PRISMA-0005": ("https://crad.ict.ac.cn/cn/article/pdf/preview/10.7544/issn1000-1239.202550135.pdf", "editor", "PDF de vista previa del editor"),
    "PRISMA-0008": ("https://www.usenix.org/system/files/atc24-gao-chen.pdf", "editor", "PDF oficial USENIX"),
    "PRISMA-0010": ("https://finkmartin.com/papers/pldi22-lasagne.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0011": ("https://www.st.ewi.tudelft.nl/sschakraborty/papers/ASPLOS2026-Arancini.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0012": ("https://tr0py.github.io/files/QEMU-ABA-CGO2021.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0015": ("https://research-repository.st-andrews.ac.uk/bitstream/10023/30039/1/Accelerating_Shared_Library_Execution_in_a_DBT_LCTES_v6.pdf", "repositorio", "Manuscrito aceptado en repositorio institucional"),
    "PRISMA-0016": ("https://mdpi-res.com/d_attachment/electronics/electronics-12-03014/article_deploy/electronics-12-03014.pdf", "editor", "PDF oficial MDPI"),
    "PRISMA-0018": ("https://cobweb.cs.uga.edu/~wenwen/papers/icse2022.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0023": ("https://binary-translation.github.io/pubs/asplos23-risotto.pdf", "autor", "PDF del sitio del proyecto"),
    "PRISMA-0024": ("https://hal.science/hal-03417343v1/document", "repositorio", "Manuscrito en repositorio HAL"),
    "PRISMA-0027": ("https://arxiv.org/pdf/2501.03427", "preprint", "Preprint arXiv"),
    "PRISMA-0034": ("https://thucloud.com/zhenhua/papers/TOCS%2724%20Trinity%20Emulator.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0036": ("https://cs.brown.edu/people/vpk/papers/egalito.asplos20.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0078": ("https://dice.cs.depaul.edu/pdfs/pubs/C31.pdf", "autor", "PDF del sitio del grupo de investigación"),
    "PRISMA-0082": ("https://www.csie.ntu.edu.tw/~hchsiao/pub/2024_ACM_CODASPY.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0102": ("https://hal.science/hal-04480308v2/document", "repositorio", "Manuscrito en repositorio HAL"),
    "PRISMA-0106": ("https://papers.ssrn.com/sol3/Delivery.cfm/38c3f20f-2651-4f02-b0d9-198095444e02-MECA.pdf?abstractid=5131936&mirid=1", "preprint", "Preprint SSRN, no es la versión final de Future Generation Computer Systems"),
    "PRISMA-0110": ("https://www.cloud-conf.net/ispa2021/proc/pdfs/ISPA-BDCloud-SocialCom-SustainCom2021-3mkuIWCJVSdKJpBYM7KEKW/264600a618/264600a618.pdf", "editor", "PDF de las actas de la conferencia"),
    "PRISMA-0113": ("https://www.scitepress.org/PublishedPapers/2020/94149/94149.pdf", "editor", "PDF oficial SciTePress"),
    "PRISMA-0139": ("https://europepmc.org/articles/PMC8237318?pdf=render", "repositorio", "PDF del artículo en Europe PMC"),
    "PRISMA-0142": ("https://www.cs.ucr.edu/~heng/pubs/sacmat2020.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0321": ("https://arxiv.org/pdf/2104.14614", "preprint", "Preprint arXiv"),
    "PRISMA-0393": ("https://pdfs.semanticscholar.org/5115/1972ab2aa58dba95458366bf7bbebc186018.pdf", "repositorio", "Copia pública indexada por Semantic Scholar, artículo de acceso abierto"),
    "PRISMA-0404": ("https://www.scitepress.org/Papers/2022/110837/110837.pdf", "editor", "PDF oficial SciTePress"),
    "PRISMA-0424": ("https://userweb.cs.txstate.edu/~aq10/papers/ford_nas21.pdf", "autor", "PDF del sitio del autor"),
    "PRISMA-0458": ("https://rapidoworkshop.github.io/RapidoProceedings.pdf", "actas-extraido", "Artículo extraído de las páginas 26-33 de las actas públicas RAPIDO 2020"),
    "PRISMA-0474": ("https://ntv.ifmo.ru/file/article/19640.pdf", "editor", "PDF oficial de la revista"),
    # Ya existía en el repositorio del proyecto, se incorpora a esta entrega.
    "PRISMA-0468": ("local:estado_del_arte/Runtime-Application-Migration-using-CheckpointRestore-In-Userspace_2024_River-Publishers.pdf", "local", "Archivo local existente en el proyecto"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def valid_pdf(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(4) == b"%PDF"
    except OSError:
        return False


def download(url: str, target: Path) -> tuple[str, str]:
    command = [
        "curl",
        "--ipv4",
        "--fail",
        "--location",
        "--retry",
        "0",
        "--max-time",
        "25",
        "--user-agent",
        "Mozilla/5.0 (compatible; Win2APK-research-retrieval/1.0)",
        "--header",
        "Accept: application/pdf",
        "--output",
        str(target),
        url,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        try:
            target.unlink()
        except FileNotFoundError:
            pass
        detail = (result.stderr or result.stdout).strip().replace("\n", " ")
        return "No recuperado", detail[-400:]
    if not valid_pdf(target):
        target.unlink(missing_ok=True)
        return "No recuperado", "La respuesta no era un PDF válido"
    return "Descargado", "PDF válido"


def process_row(row: dict[str, str]) -> tuple[dict[str, str], str]:
    study_id = row["ID"]
    source = PUBLIC_PDFS.get(study_id)
    doi = row["DOI"]
    official = "N/R" if doi in {"", "N/R"} else f"https://doi.org/{doi}"
    if source is None:
        manifest_row = {
            "ID": study_id,
            "Prioridad": row["Prioridad"],
            "Título": row["Título"],
            "DOI": doi,
            "EID": row["EID"],
            "Estado": "No intentado",
            "Versión": "N/R",
            "Archivo local": "N/R",
            "Fuente": official,
            "Observación": "No se identificó una copia pública directa en las fuentes consultadas; el DOI queda como ruta oficial.",
            "SHA256": "N/R",
        }
        return manifest_row, f"{study_id}\tNo intentado\t{official}\tN/R"

    url, version, note = source
    target = PDF_DIR / f"{study_id}.pdf"
    if url.startswith("local:"):
        original = ROOT / url.removeprefix("local:")
        if original.exists() and valid_pdf(original):
            shutil.copy2(original, target)
            status, detail = "Descargado", "Copia local verificada como PDF"
        else:
            status, detail = "No recuperado", "El archivo local indicado no existe o no es PDF"
    elif target.exists() and valid_pdf(target):
        status, detail = "Descargado", "PDF válido ya recuperado en un intento anterior"
    else:
        status, detail = download(url, target)

    manifest_row = {
        "ID": study_id,
        "Prioridad": row["Prioridad"],
        "Título": row["Título"],
        "DOI": doi,
        "EID": row["EID"],
        "Estado": status,
        "Versión": version,
        "Archivo local": str(target.relative_to(ROOT)) if status == "Descargado" else "N/R",
        "Fuente": url,
        "Observación": f"{note}. {detail}.",
        "SHA256": sha256(target) if status == "Descargado" else "N/R",
    }
    return manifest_row, f"{study_id}\t{status}\t{url}\t{detail}"


def main() -> None:
    with SELECTION.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(process_row, rows))
    manifest_rows = [result[0] for result in results]
    log_rows = [result[1] for result in results]

    manifest_path = OUT / "manifest_recuperacion_45.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(manifest_rows[0])
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    (OUT / "recuperacion.log").write_text("\n".join(log_rows) + "\n", encoding="utf-8")
    downloaded = sum(row["Estado"] == "Descargado" for row in manifest_rows)
    attempted = sum(row["Estado"] in {"Descargado", "No recuperado"} for row in manifest_rows)
    print(f"Descargados: {downloaded}/{len(manifest_rows)}")
    print(f"Intentados: {attempted}/{len(manifest_rows)}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
