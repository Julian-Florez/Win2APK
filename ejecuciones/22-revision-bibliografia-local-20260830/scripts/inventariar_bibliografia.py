#!/usr/bin/env python3
"""Inventario reproducible de la bibliografia local y su conciliacion con Scopus."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
import warnings
from collections import defaultdict
from contextlib import redirect_stderr
from difflib import SequenceMatcher
from io import StringIO
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
BIB_DIR = ROOT / "bibliografia"
ART_DIR = BIB_DIR / "articulos"
LISTA = BIB_DIR / "LISTA_FINAL.csv"
SCOPUS = ROOT / "estado_del_arte" / "export_24f23048-3942-463f-9f1d-46dcf6a7f367_2026-08-30T004723.331226035.csv"
OUT_DIR = ROOT / "ejecuciones" / "22-revision-bibliografia-local-20260830" / "evidencias"


CORE = {
    "WINE", "OS_COMPATIBILITY", "ANDROID", "BOX64", "DBT", "LLVM", "SIMD",
    "ARM", "DUAL_ISA", "X86", "CROSS_ISA", "CROSS_ARCHITECTURE",
    "MEMORY_VIRTUALIZATION", "CROSSDBT", "CROSSMAPPING", "BTBENCH",
    "BINARY_TRANSLATION", "SYSTEM_CALLS", "PROTON", "LEGACY_CODE",
    "SOFTWARE_MODERNIZATION", "QEMU", "DYNAMIC_BINARY_TRANSLATION",
}
COMPLEMENTARY = {
    "ANDROID_SECURITY", "ANDROID_LIBRARIES", "CONTAINERIZATION", "CLOUD_GAMING",
    "LINUX_GAMING", "VULKAN", "DIRECT3D", "SHADERS", "SHADER_COMPILER",
    "SHADER_TRANSLATION",
}


def norm(value: str | None) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "", value)


def norm_doi(value: str | None) -> str:
    value = (value or "").strip()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.I)
    value = value.rstrip(" .;,)]}")
    return norm(value)


def hash_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_pdf(path: Path) -> dict[str, object]:
    result: dict[str, object] = {
        "paginas": "N/R", "texto_extraible": "No", "titulo_pdf": "N/R",
        "autores_pdf": "N/R", "ano_detectado": "N/R", "extracto": "N/R",
        "error_pdf": "N/R",
    }
    try:
        with redirect_stderr(StringIO()):
            reader = PdfReader(str(path), strict=False)
            result["paginas"] = len(reader.pages)
            text_parts = []
            for page in reader.pages[:3]:
                text_parts.append(page.extract_text() or "")
            text = re.sub(r"\s+", " ", " ".join(text_parts)).strip()
            result["extracto"] = text[:1200] if text else "N/R"
            result["texto_extraible"] = "Sí" if len(text) >= 300 else "No"
            metadata = reader.metadata or {}
            if metadata.get("/Title"):
                result["titulo_pdf"] = str(metadata["/Title"]).strip()
            if metadata.get("/Author"):
                result["autores_pdf"] = str(metadata["/Author"]).strip()
            if text:
                years = [int(y) for y in re.findall(r"(?<!\d)(20\d{2}|19\d{2})(?!\d)", text)]
                if years:
                    # El año de publicación suele aparecer antes que los años de referencias.
                    result["ano_detectado"] = min(years[:4])
    except Exception as exc:  # pragma: no cover - se conserva el error en la evidencia
        result["error_pdf"] = f"{type(exc).__name__}: {exc}"
    return result


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    warnings.filterwarnings("ignore")
    lista = load_csv(LISTA)
    scopus = load_csv(SCOPUS)

    by_doi: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_title: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in scopus:
        doi = norm_doi(row.get("DOI"))
        title = norm(row.get("Title"))
        if doi:
            by_doi[doi].append(row)
        if title:
            by_title[title].append(row)

    scopus_titles = [norm(row.get("Title")) for row in scopus]
    inventory: list[dict[str, object]] = []
    for source in lista:
        path = ART_DIR / source["archivo"]
        exists = path.exists()
        pdf_data = extract_pdf(path) if exists else {
            "paginas": "N/R", "texto_extraible": "No", "titulo_pdf": "N/R",
            "autores_pdf": "N/R", "ano_detectado": "N/R", "extracto": "N/R",
            "error_pdf": "Archivo no encontrado",
        }
        doi = norm_doi(source.get("doi"))
        title = norm(source.get("titulo"))
        matches = by_doi.get(doi, []) if doi else []
        match_method = "DOI" if matches else ""
        if not matches and title:
            matches = by_title.get(title, [])
            match_method = "Título exacto" if matches else ""

        # La clasificación es una preselección por metadatos. La lectura completa
        # y la decisión final de inclusión se mantienen pendientes.
        if not exists:
            classification = "Registro sin archivo local"
            level = "N/R"
        elif matches:
            classification = "Duplicado de registro Scopus"
            level = "Directa" if source["keyword"] in CORE else "Complementaria"
        elif source["keyword"] in CORE:
            classification = "Candidato adicional directo"
            level = "Directa"
        elif source["keyword"] in COMPLEMENTARY:
            classification = "Candidato adicional complementario"
            level = "Complementaria"
        else:
            classification = "No prioritario por metadatos"
            level = "N/R"

        year = pdf_data.get("ano_detectado", "N/R")
        if matches and matches[0].get("Year"):
            year = matches[0]["Year"]
        if isinstance(year, int):
            temporal = "Sí" if 2020 <= year <= 2026 else "No"
        else:
            temporal = "N/R"

        match_row = matches[0] if matches else {}
        near_id = "N/R"
        near_score = "N/R"
        if title and scopus_titles:
            score, index = max((SequenceMatcher(None, title, candidate).ratio(), i)
                               for i, candidate in enumerate(scopus_titles))
            if score >= 0.90 and not matches:
                near_id = scopus[index].get("EID", "N/R")
                near_score = f"{score:.3f}"

        if exists:
            content = "Texto extraíble" if pdf_data.get("texto_extraible") == "Sí" else "PDF sin texto suficiente / marcador"
            sha256 = hash_sha256(path)
            relative_path = path.relative_to(ROOT).as_posix()
        else:
            content = "N/A"
            sha256 = "N/R"
            relative_path = "N/R"

        inventory.append({
            "BIB_ID": f"BIB-{int(source['n']):04d}",
            "n_lista": source["n"],
            "archivo": source["archivo"],
            "ruta_relativa": relative_path,
            "archivo_existe": "Sí" if exists else "No",
            "estado_manifest": source.get("estado", "N/R"),
            "contenido_local": content,
            "paginas": pdf_data.get("paginas", "N/R"),
            "titulo": source.get("titulo", "N/R"),
            "titulo_pdf": pdf_data.get("titulo_pdf", "N/R"),
            "autores": source.get("primer_autor", "N/R"),
            "autores_pdf": pdf_data.get("autores_pdf", "N/R"),
            "ano": year,
            "ventana_2020_2026": temporal,
            "doi": source.get("doi") or "N/R",
            "keyword": source.get("keyword", "N/R"),
            "nivel_relevancia": level,
            "clasificacion": classification,
            "metodo_coincidencia": match_method or "N/R",
            "eid_scopus_coincidente": match_row.get("EID", "N/R") or "N/R",
            "ano_scopus_coincidente": match_row.get("Year", "N/R") or "N/R",
            "candidato_similar_eid": near_id,
            "similitud_titulo": near_score,
            "sha256": sha256,
            "fuente_pdf": source.get("fuente_pdf", "N/R") or "N/R",
            "nota_manifest": source.get("nota", "N/R") or "N/R",
            "extracto_inicial": pdf_data.get("extracto", "N/R"),
            "error_pdf": pdf_data.get("error_pdf", "N/R"),
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = list(inventory[0].keys())
    write_csv(OUT_DIR / "inventario_bibliografia.csv", inventory, fields)

    additional = [row for row in inventory if row["clasificacion"].startswith("Candidato adicional")]
    duplicates = [row for row in inventory if row["clasificacion"] == "Duplicado de registro Scopus"]
    write_csv(OUT_DIR / "candidatos_adicionales.csv", additional, fields)
    write_csv(OUT_DIR / "duplicados_scopus.csv", duplicates, fields)

    summary = {
        "registros_lista_final": len(lista),
        "archivos_pdf_presentes": sum(row["archivo_existe"] == "Sí" for row in inventory),
        "registros_sin_archivo": sum(row["archivo_existe"] == "No" for row in inventory),
        "pdfs_con_texto_extraible": sum(row["contenido_local"] == "Texto extraíble" for row in inventory),
        "pdfs_sin_texto_suficiente": sum(row["contenido_local"] == "PDF sin texto suficiente / marcador" for row in inventory),
        "duplicados_scopus": len(duplicates),
        "candidatos_adicionales": len(additional),
        "candidatos_directos": sum(row["nivel_relevancia"] == "Directa" for row in additional),
        "candidatos_complementarios": sum(row["nivel_relevancia"] == "Complementaria" for row in additional),
        "candidatos_en_ventana_2020_2026": sum(row["ventana_2020_2026"] == "Sí" for row in additional),
        "candidatos_fuera_ventana": sum(row["ventana_2020_2026"] == "No" for row in additional),
        "candidatos_ventana_no_registrada": sum(row["ventana_2020_2026"] == "N/R" for row in additional),
        "criterio": {
            "directa": "Palabras clave centradas en Wine, compatibilidad de SO, traducción binaria, emulación, ISA, QEMU/LLVM, migración de software o capas de compatibilidad.",
            "complementaria": "Palabras clave sobre contenedores, virtualización de aplicaciones, seguridad nativa Android, gráficos/API o reproducibilidad que pueden apoyar el diseño, pero no sustituyen evidencia directa.",
            "duplicado": "Coincidencia exacta por DOI o título con los 533 registros Scopus.",
            "limitacion": "La clasificación es por metadatos y texto inicial disponible; no equivale a inclusión final en la síntesis PRISMA.",
        },
    }
    (OUT_DIR / "resumen_revision.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\nCANDIDATOS ADICIONALES")
    for row in additional:
        print(f"{row['BIB_ID']}\t{row['nivel_relevancia']}\t{row['ventana_2020_2026']}\t{row['contenido_local']}\t{row['titulo']}")
    print("\nDUPLICADOS")
    for row in duplicates:
        print(f"{row['BIB_ID']}\t{row['eid_scopus_coincidente']}\t{row['titulo']}")


if __name__ == "__main__":
    main()
