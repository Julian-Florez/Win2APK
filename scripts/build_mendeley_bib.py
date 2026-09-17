#!/usr/bin/env python3
"""Construye un archivo BibTeX importable en Mendeley desde bibliografia/.

La deduplicación se realiza primero por hash del PDF y después por DOI o título
normalizado. Los metadatos existentes se enriquecen con Crossref cuando es
posible, sin descartar los registros que no tienen DOI.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from pypdf import PdfReader


ROOT = Path("/home/julian/Tesis/Win2APK")
BIB_DIR = ROOT / "bibliografia"
OUT = BIB_DIR / "bibliografia_mendeley.bib"
MASTER = ROOT / "review_output/master_inventory.csv"
LISTA = BIB_DIR / "LISTA_FINAL.csv"
SCOPUS_EXPORT = BIB_DIR / "estado_del_arte/export_24f23048-3942-463f-9f1d-46dcf6a7f367_2026-08-30T004723.331226035.csv"

MANUAL_OVERRIDES = {
    "A-Comparative-Study-of-Operating-Systems.pdf": {
        "title": "A Comparative Study of Operating Systems: Case of Windows, UNIX, Linux, Mac, Android and iOS",
        "authors": ["Adekotujo, Akinlolu", "Odumabo, Adedoyin"],
        "year": "2020",
        "doi": "10.5120/ijca2020920494",
        "venue": "International Journal of Computer Applications",
    },
    "A-Cross-Platform-Graphics-API-Solution-for-Modern-and-Legacy-Development-Styles.pdf": {
        "title": "A Cross-Platform Graphics API Solution for Modern and Legacy Development Styles",
        "doi": "10.1007/978-3-031-44751-8_4",
        "year": "2023",
        "venue": "Lecture Notes in Computer Science",
    },
    "A2P2–An-Android-Application-Patching-Pipeline-Based-on-Generic-Changesets.pdf": {
        "title": "A2P2: An Android Application Patching Pipeline Based on Generic Changesets",
        "authors": ["Draschbacher, Florian"],
        "year": "2023",
        "doi": "10.1145/3600160.3600172",
        "venue": "Proceedings of the 18th ACM International Conference on Software Engineering and Formal Methods",
    },
    "Arming_x86_games.pdf": {
        "title": "ARMing x86 Games: Accelerating Binary Translation Using Software-Only Validated Flag Speculation",
        "authors": ["Yen, James", "Wang, Jiarui", "Huang, Zhibai", "Wei, Zhixiang", "Zhang, Ziyang", "Chen, Chen", "Yu, Senhao", "Wang, Yun", "Wang, Hao", "Qi, Zhengwei"],
        "year": "2025",
        "doi": "10.1145/3711875.3729163",
        "venue": "Proceedings of the 23rd Annual International Conference on Mobile Systems, Applications and Services",
    },
    "BTBench_ISPASS_2024.pdf": {
        "title": "BTBench: A Benchmark for Comprehensive Binary Translation Performance Evaluation",
        "authors": ["Li, Xinyu", "Lan, Yanzhi", "Niu, Gen", "Xue, Feng", "Zhang, Fuxin"],
        "year": "2024",
        "doi": "10.1109/ISPASS61541.2024.00014",
        "venue": "2024 IEEE International Symposium on Performance Analysis of Systems and Software",
    },
    "Characterizing-Installation-and-Run-time-CompatibilityIssues-in-Android-Benign-Apps-and-Malware.pdf": {
        "title": "Characterizing Installation- and Run-time Compatibility Issues in Android Benign Apps and Malware",
        "authors": ["Guo, Jiawei", "Fu, Xiaoqin", "Li, Li", "Zhang, Tao", "Fazzini, Mattia", "Cai, Haipeng"],
        "year": "2025",
        "doi": "10.1145/3725810",
        "venue": "ACM Transactions on Software Engineering and Methodology",
    },
    "Contemporary-Software-Modernization-Strategies-Driving.pdf": {
        "title": "Contemporary Software Modernization: Strategies, Driving Forces, and Research Opportunities",
        "authors": ["Assunção, Wesley K. G.", "Marchezan, Luciano", "Arkoh, Lawrence", "Egyed, Alexander", "Ramler, Rudolf"],
        "year": "2025",
        "doi": "10.1145/3708527",
        "venue": "ACM Transactions on Software Engineering and Methodology",
    },
    "Dynamic_binary_translators.pdf": {
        "title": "An Instruction Inflation Analyzing Framework for Dynamic Binary Translators",
        "authors": ["Xie, Benyi", "Yan, Yue", "Yan, Chenghao", "Tao, Sicheng", "Zhang, Zhuangzhuang", "Li, Xinyu", "Lan, Yanzhi", "Wu, Xiang", "Liu, Tianyi", "Zhang, Tingting", "Zhang, Fuxin"],
        "year": "2024",
    },
    "EXPLORING-OPERATING-SYSTEM-DIVERSITY-A.pdf": {
        "title": "Exploring Operating System Diversity: A Comparative Analysis of Windows, Mac OS, Android and iOS",
        "authors": ["Ukpabi, Kosisochukwu Henry", "Ibrahim, Abdullahi Mohammed"],
        "year": "2024",
        "venue": "Journal of Systematic and Modern Science Research",
        "url": "https://berkeleypublications.com/bjsmsr/article/view/264",
        "note": "No se localizó un DOI en el artículo ni en el registro editorial consultado; se conserva la URL de publicación.",
    },
    "Loupe-Driving-the-Development-of-OS-Compatibility-Layers.pdf": {
        "title": "Loupe: Driving the Development of OS Compatibility Layers",
        "authors": ["Lefeuvre, Hugo", "Gain, Gaulthier", "Bădoiu, Vlad-Andrei", "Dinca, Daniel", "Schiller, Vlad-Radu", "Raiciu, Costin", "Huici, Felipe", "Olivier, Pierre"],
        "year": "2024",
        "doi": "10.1145/3617232.3624861",
        "venue": "Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",
    },
    "OS_COMPATIBILITY_loupe_driving_the_development_of_os_compatibility_layers-Lefeuvre_H.pdf": {
        "title": "Loupe: Driving the Development of OS Compatibility Layers",
        "authors": ["Lefeuvre, Hugo", "Gain, Gaulthier", "Bădoiu, Vlad-Andrei", "Dinca, Daniel", "Schiller, Vlad-Radu", "Raiciu, Costin", "Huici, Felipe", "Olivier, Pierre"],
        "year": "2024",
        "doi": "10.1145/3617232.3624861",
        "venue": "Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",
    },
    "practical_&_efficient_x86-64_Emulation_on_RISC-V.pdf": {
        "title": "Practical and Efficient x86-64 Emulation on RISC-V",
        "authors": ["Tan, Xiongchuan", "Liu, Yang", "Chevalier, Sebastien", "Chen, Yangyu", "Liu, Xiaoyi", "Fu, Haohuan"],
        "year": "2026",
        "doi": "10.1145/3767295.3803574",
        "venue": "Proceedings of the 21st European Conference on Computer Systems",
    },
    "LINUX_GAMING_a_survey_of_the_ability_of_the_linux_operating_system_to_support_online_game_execution-Peoples_C.pdf": {
        "title": "A Survey of the Ability of the Linux Operating System to Support Online Game Execution",
        "authors": ["Peoples, Cathryn"],
        "year": "2019",
        "venue": "Open Journal of Web Technologies",
        "volume": "6",
        "issue": "1",
        "pages": "1-15",
        "url": "https://www.ronpub.com/OJWT_2019v6i1n01_Peoples.pdf",
        "note": "No se localizó un DOI en el registro editorial; el artículo conserva la URL y el identificador URN de RonPub.",
    },
    "WINE_interactive_launch_of_16000_microsoft_windows_instances_on_a_supercomputer-Jones_M.pdf": {
        "title": "Interactive Launch of 16,000 Microsoft Windows Instances on a Supercomputer",
        "authors": ["Jones, Matthew", "Dorr, David", "Keller, Michael", "Hendrickson, Joshua", "McLay, Robert", "Towns, John"],
        "year": "2018",
        "doi": "10.1109/HPEC.2018.8547782",
        "venue": "2018 IEEE High Performance Extreme Computing Conference",
    },
    "VULKAN_multithreaded_rendering_for_cross_platform_3d_visualization_based_on_vulkan_api-Ioannidis_C.pdf": {
        "title": "Multithreaded Rendering for Cross-Platform 3D Visualization Based on Vulkan API",
        "authors": ["Ioannidis, Charalabos", "Verykokou, Styliani", "Tsakiri, Maria"],
        "year": "2020",
        "doi": "10.5194/isprs-archives-xliv-4-w1-2020-57-2020",
        "venue": "The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences",
    },
    "DIRECT3D_programming_interfaces_for_cross_platform_image_rendering_and_deep_learning_gpgpu-Georgiev_G_G.pdf": {
        "title": "Programming Interfaces for Cross-platform Image Rendering and Deep Learning GPGPU",
        "authors": ["Georgiev, Georgi G.", "Kovachev, Venelin", "Kovachev, Venelin"],
        "year": "2023",
        "doi": "10.1109/COMSCI59259.2023.10315835",
        "venue": "2023 International Conference on Computer Systems and Technologies",
    },
    "CLOUD_GAMING_towards_an_efficient_containerized_cloud_gaming_platform-Gegout_A.pdf": {
        "title": "Towards an Efficient Containerized Cloud Gaming Platform",
        "authors": ["Gégout, Arthur", "Gougeon, Jean-Baptiste", "Pérès, Yann", "Dalmasso, Nicolas", "Mouchère, Harold"],
        "year": "2025",
        "doi": "10.1109/IPDPSW66978.2025.00018",
        "venue": "2025 IEEE International Parallel and Distributed Processing Symposium Workshops",
    },
    "WINE_virtual_operating_system_for_windows_to_linux_migration-Giri_N_H.pdf": {
        "title": "Virtual Operating System for Windows to Linux Migration",
        "authors": ["Giri, N. H.", "Mishra, S. K.", "Rath, S. K."],
        "year": "2017",
        "doi": "10.1109/ICECDS.2017.8389825",
        "venue": "2017 International Conference on Electrical, Computer and Communication Technologies",
    },
    "CROSSMAPPING_crossmapping_harmonizing_memory_consistency_in_cross_isa_binary_translation-Gao_Chen.pdf": {
        "title": "CrossMapping: Harmonizing Memory Consistency in Cross-ISA Binary Translation",
        "authors": ["Gao, Chen", "Li, Yifan", "Liu, Yizhou", "Liu, Xu", "Zhang, Yifan", "Ruan, Xue"],
        "year": "2024",
        "venue": "2024 USENIX Annual Technical Conference (USENIX ATC 24)",
        "url": "https://www.usenix.org/conference/atc24/presentation/gao-chen",
        "note": "El registro oficial de USENIX y DBLP no asignan DOI a este artículo; se conserva la URL editorial.",
    },
    "X86_dynamically_translating_x86_to_llvm_using_qemu-Chipounov_V.pdf": {
        "title": "Dynamically Translating x86 to LLVM using QEMU",
        "authors": ["Chipounov, Vitaly", "Candea, George"],
        "year": "2010",
        "venue": "EPFL Technical Report EPFL-TR-149975",
        "url": "https://infoscience.epfl.ch/entities/publication/c105c6c4-5d0a-4a93-a8ea-68a229d701e0",
        "note": "Informe técnico de EPFL; no se localizó un DOI en el registro institucional ni en Crossref.",
    },
    "LEGACY_CODE_leveraging_legacy_code_to_deploy_desktop_applications_on_the_web-Douceur_John_R.pdf": {
        "title": "Leveraging Legacy Code to Deploy Desktop Applications on the Web",
        "authors": ["Douceur, John R.", "Elson, Jeremy", "Howell, Jon", "Lorch, Jacob R."],
        "year": "2008",
        "venue": "8th USENIX Symposium on Operating Systems Design and Implementation (OSDI 08)",
        "url": "https://www.usenix.org/conference/osdi-08/leveraging-legacy-code-deploy-desktop-applications-web",
        "note": "El registro oficial de USENIX no asigna DOI a este artículo; se conserva la URL editorial.",
    },
    "QEMU_qemu_a_fast_and_portable_dynamic_translator-Bellard_Fabrice.pdf": {
        "title": "QEMU, a Fast and Portable Dynamic Translator",
        "authors": ["Bellard, Fabrice"],
        "year": "2005",
        "venue": "2005 USENIX Annual Technical Conference, FREENIX Track",
        "pages": "41-46",
        "url": "https://www.usenix.org/publications/library/proceedings/usenix05/tech/freenix/full_papers/bellard/bellard.pdf",
        "note": "El registro DBLP indica que este artículo no tiene DOI; se conserva la URL del texto publicado por USENIX.",
    },
    "PROTON_is_proton_good_enough_a_performance_comparison_between_gaming_on_windows_and_linux-Kopel_M.pdf": {
        "title": "Is Proton Good Enough? - A Performance Comparison Between Gaming on Windows and Linux",
        "authors": ["Kopel, Marek", "Bożek, Michał"],
        "year": "2023",
        "doi": "10.1007/978-3-031-41456-5_48",
        "venue": "Computational Collective Intelligence",
        "volume": "14162",
        "pages": "634-646",
        "publisher": "Springer",
    },
    "BTBENCH_btbench_a_benchmark_for_comprehensive_binary_translation_performance_evaluation-Li_X.pdf": {
        "title": "BTBench: A Benchmark for Comprehensive Binary Translation Performance Evaluation",
        "authors": ["Li, Xinyu", "Lan, Yanzhi", "Niu, Gen", "Xue, Feng", "Zhang, Fuxin"],
        "year": "2024",
        "doi": "10.1109/ISPASS61541.2024.00014",
        "venue": "2024 IEEE International Symposium on Performance Analysis of Systems and Software",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    if "|" in value:
        value = value.split("|")[0].strip()
    value = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", value)
    value = value.strip().rstrip(".;")
    return value if valid_metadata(value) else ""


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").replace("\ufeff", "")).strip(" ;,")


def valid_metadata(value: str) -> bool:
    value = clean_text(value)
    if not value:
        return False
    invalid = {
        "no verificado en el pdf",
        "no verificado",
        "untitled",
        "anonymous",
        "n/r",
        "07_aleksandar",
        "hdwcm_6611867 1..12",
        "itmo_3_2020.indd",
    }
    return normalize(value) not in {normalize(item) for item in invalid}


def split_authors(value: str) -> list[str]:
    value = clean_text(value)
    if not value or value.upper().startswith("NO VERIFICADO"):
        return []
    value = re.sub(r"\s*[Ⱐ整⁡氮].*$", "", value)
    value = re.sub(r"\s+\d+(?=\s|$)", "", value)
    if ";" in value:
        parts = [x.strip() for x in value.split(";")]
    elif " and " in value:
        parts = [x.strip() for x in re.split(r"\s+and\s+", value)]
    else:
        parts = [value]
    return [p for p in parts if p and not p.upper().startswith("NO VERIFICADO")]


def author_to_bib(name: str) -> str:
    name = clean_text(name)
    name = re.sub(r"\s*\d+$", "", name)
    if "," in name:
        family, given = [x.strip() for x in name.split(",", 1)]
        return f"{family}, {given}" if given else family
    words = name.split()
    if len(words) == 1:
        return words[0]
    return f"{words[-1]}, {' '.join(words[:-1])}"


def crossref_authors(items: list[dict]) -> list[str]:
    result = []
    for item in items or []:
        family = clean_text(item.get("family", ""))
        given = clean_text(item.get("given", ""))
        if family:
            result.append(f"{family}, {given}" if given else family)
    return result


def fallback_title(path: Path) -> str:
    name = path.stem.replace("–", "-").replace("_", " ")
    name = re.sub(r"^[A-Z0-9]+\s+", "", name)
    name = re.sub(r"-[A-Za-z]+(?:_[A-Za-z]+)*$", "", name)
    return re.sub(r"\s+", " ", name).strip(" -")


def pdf_metadata(path: Path) -> dict[str, str]:
    result = {"title": "", "authors": [], "year": ""}
    try:
        reader = PdfReader(str(path))
        metadata = reader.metadata or {}
        result["title"] = clean_text(str(metadata.get("/Title", "")))
        result["authors"] = split_authors(str(metadata.get("/Author", "")))
        date = str(metadata.get("/CreationDate", ""))
        match = re.search(r"(20\d{2})", date)
        if match:
            result["year"] = match.group(1)
        if not result["title"] or not result["authors"]:
            text = "\n".join((page.extract_text() or "") for page in reader.pages[:2])
            compact = " ".join(text.split())
            if not result["title"]:
                result["title"] = compact[:240]
    except Exception:
        pass
    result["title"] = result["title"] or fallback_title(path)
    return result


def fetch_crossref(doi: str = "", title: str = "") -> dict:
    if not doi and not title:
        return {}
    if doi:
        url = "https://api.crossref.org/works/" + quote(doi, safe="")
    else:
        url = "https://api.crossref.org/works?query.title=" + quote(title) + "&rows=1"
    try:
        request = Request(url, headers={"User-Agent": "Win2APK bibliography builder/1.0 (mailto:research@example.invalid)"})
        with urlopen(request, timeout=12) as response:
            payload = json.load(response)
        if doi:
            return payload.get("message", {})
        items = payload.get("message", {}).get("items", [])
        if not items:
            return {}
        candidate = items[0]
        score = SequenceMatcher(None, normalize(title), normalize(" ".join(candidate.get("title", [])))).ratio()
        return candidate if score >= 0.82 else {}
    except Exception:
        return {}


def merge_metadata(base: dict, item: dict) -> dict:
    if not item:
        return base
    title = clean_text(" ".join(item.get("title", [])))
    authors = crossref_authors(item.get("author", []))
    issued = item.get("published-print") or item.get("published-online") or item.get("issued") or {}
    date_parts = issued.get("date-parts", [[]])
    year = str(date_parts[0][0]) if date_parts and date_parts[0] else ""
    for key, value in [("title", title), ("year", year)]:
        if value:
            base[key] = value
    if authors:
        base["authors"] = authors
    if item.get("DOI"):
        base["doi"] = normalize_doi(item["DOI"])
    base["venue"] = clean_text(item.get("container-title", [""])[0] if item.get("container-title") else base.get("venue", ""))
    base["volume"] = clean_text(str(item.get("volume", base.get("volume", ""))))
    base["issue"] = clean_text(str(item.get("issue", base.get("issue", ""))))
    base["pages"] = clean_text(str(item.get("page", base.get("pages", ""))))
    base["publisher"] = clean_text(item.get("publisher", base.get("publisher", "")))
    base["crossref_type"] = item.get("type", base.get("crossref_type", ""))
    return base


def bib_escape(value: str) -> str:
    value = clean_text(value)
    return value.replace("\\", "").replace("{", "\\{").replace("}", "\\}").replace("&", r"\&").replace("%", r"\%")


def key_for(record: dict, used: set[str]) -> str:
    author = normalize((record.get("authors") or ["unknown"])[0]).split()
    family = author[0] if author else "unknown"
    year = record.get("year") or "nd"
    words = normalize(record.get("title", "reference")).split()
    stem = f"{family}{year}{words[0] if words else 'reference'}"
    stem = re.sub(r"[^a-z0-9]", "", stem) or "reference"
    candidate = stem
    counter = 2
    while candidate in used:
        candidate = f"{stem}{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def entry_type(record: dict) -> str:
    cross_type = record.get("crossref_type", "")
    if cross_type == "book-chapter":
        return "incollection"
    if cross_type == "journal-article":
        return "article"
    if record.get("venue") == "IEEE Xplore" and not record.get("doi"):
        return "misc"
    venue = normalize(record.get("venue", ""))
    if any(token in venue for token in ["journal", "transactions", "electronics", "mobile information systems", "wireless"]):
        return "article"
    if venue:
        return "inproceedings"
    return "misc"


def make_entry(record: dict, used: set[str]) -> str:
    key = key_for(record, used)
    entry = [f"@{entry_type(record)}{{{key},"]
    fields: list[tuple[str, str]] = [("title", record["title"])]
    if record.get("authors"):
        fields.append(("author", " and ".join(author_to_bib(a) for a in record["authors"])))
    if record.get("year"):
        fields.append(("year", record["year"]))
    if record.get("venue") and not entry[0].startswith("@misc"):
        fields.append(("journal" if entry[0].startswith("@article") else "booktitle", record["venue"]))
    elif record.get("venue"):
        fields.append(("howpublished", record["venue"]))
    for field in ["volume", "issue", "pages", "publisher"]:
        if record.get(field):
            fields.append((field, record[field]))
    if record.get("doi"):
        fields.append(("doi", record["doi"]))
        fields.append(("url", "https://doi.org/" + record["doi"]))
    elif record.get("url"):
        fields.append(("url", record["url"]))
    if record.get("file"):
        fields.append(("file", record["file"]))
    if record.get("keywords"):
        fields.append(("keywords", record["keywords"]))
    if record.get("note"):
        fields.append(("note", record["note"]))
    for i, (field, value) in enumerate(fields):
        escaped = value if field in {"url", "file"} else bib_escape(value)
        entry.append(f"  {field} = {{{escaped}}}" + ("," if i < len(fields) - 1 else ""))
    entry.append("}")
    return "\n".join(entry)


def main() -> None:
    master_rows = read_csv(MASTER)
    lista_rows = read_csv(LISTA)
    export_rows = read_csv(SCOPUS_EXPORT)
    master_by_filename = {row.get("filename", ""): row for row in master_rows}
    lista_by_filename = {row.get("archivo", ""): row for row in lista_rows}
    export_by_doi = {normalize_doi(row.get("DOI", "")): row for row in export_rows if normalize_doi(row.get("DOI", ""))}

    files = sorted(BIB_DIR.rglob("*.pdf"))
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        by_hash[hashlib.sha256(path.read_bytes()).hexdigest()].append(path)

    def path_priority(path: Path) -> tuple[int, str]:
        text = str(path)
        if "/bibliografia/articulos/" in text:
            return (0, text)
        if "/bibliografia/Artículosmt/" in text:
            return (1, text)
        return (2, text)

    canonical_files = [sorted(paths, key=path_priority)[0] for paths in by_hash.values()]
    records = []
    for path in sorted(canonical_files, key=str):
        filename = path.name
        master = master_by_filename.get(filename, {})
        lista = lista_by_filename.get(filename, {})
        pdf = pdf_metadata(path)
        override = MANUAL_OVERRIDES.get(filename, {})
        title_candidates = [
            override.get("title", ""),
            lista.get("titulo", ""),
            master.get("external_metadata_title", ""),
            master.get("metadata_title", ""),
            master.get("title_pdf", ""),
            pdf.get("title", ""),
        ]
        title = next((clean_text(value) for value in title_candidates if valid_metadata(value)), "")
        author_candidates = [
            "; ".join(override.get("authors", [])),
            master.get("authors_pdf", ""),
            master.get("external_metadata_authors", ""),
            lista.get("primer_autor", ""),
        ]
        authors = next((split_authors(value) for value in author_candidates if valid_metadata(value) and split_authors(value)), pdf.get("authors", []))
        year_candidates = [override.get("year", ""), master.get("year_pdf", ""), master.get("external_metadata_year", ""), pdf.get("year", "")]
        year = next((clean_text(value) for value in year_candidates if re.fullmatch(r"(?:19|20)\d{2}", clean_text(value))), "")
        if not year:
            year = re.search(r"(?:19|20)\d{2}", path.name).group(0) if re.search(r"(?:19|20)\d{2}", path.name) else ""
        doi = normalize_doi(override.get("doi", "") or lista.get("doi") or master.get("external_metadata_doi", ""))
        if not doi and " | " not in (master.get("doi_pdf", "") or ""):
            doi = normalize_doi(master.get("doi_pdf", ""))
        venue = clean_text(override.get("venue", "") or master.get("external_metadata_venue", ""))
        record = {
            "title": title or fallback_title(path),
            "authors": authors,
            "year": year,
            "doi": doi,
            "venue": venue,
            "file": str(path),
            "keywords": path.parent.name,
            "note": "Registro local; metadatos normalizados para importación en Mendeley.",
        }
        if override.get("url"):
            record["url"] = override["url"]
        if override.get("note"):
            record["note"] = override["note"]
        doi_key = normalize_doi(record["doi"])
        external = export_by_doi.get(doi_key, {})
        if external:
            record["venue"] = clean_text(external.get("Source title", "")) or record["venue"]
            record["volume"] = external.get("Volume", "")
            record["issue"] = external.get("Issue", "")
            record["pages"] = "-".join(x for x in [external.get("Page start", ""), external.get("Page end", "")] if x)
            record = merge_metadata(record, {"DOI": doi_key, "title": [external.get("Title", "")], "author": []})
        enriched = fetch_crossref(record["doi"]) if record["doi"] else {}
        if enriched:
            record = merge_metadata(record, enriched)
        # Keep explicitly curated local metadata when a publisher API returns a
        # different date or only an abbreviated author list.
        for field in ["title", "authors", "year", "doi", "venue", "volume", "issue", "pages", "publisher"]:
            if override.get(field):
                record[field] = override[field]
        records.append(record)
        time.sleep(0.03)

    # Include the three URLs supplied by the researcher.
    records.extend([
        {
            "title": "IEEE Xplore record 11576690",
            "authors": [],
            "year": "",
            "doi": "",
            "venue": "IEEE Xplore",
            "url": "https://ieeexplore.ieee.org/document/11576690",
            "file": "",
            "keywords": "external source",
            "note": "Registro agregado desde el enlace proporcionado; los metadatos no se pudieron resolver automáticamente desde IEEE Xplore.",
        },
        {
            "title": "Dissecting APKs from Google Play: Trends, Insights and Security Implications",
            "authors": ["Ruiz Jiménez, Pedro Jesús", "Samhi, Jordan", "Bissyandé, Tegawendé F.", "Klein, Jacques"],
            "year": "2025",
            "doi": "10.1109/SANER64311.2025.00074",
            "venue": "2025 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER)",
            "url": "https://www.researchgate.net/publication/391952136_Dissecting_APKs_from_Google_Play_Trends_Insights_and_Security_Implications",
            "file": "",
            "keywords": "external source",
            "note": "Registro agregado desde ResearchGate.",
        },
        {
            "title": "Is Proton Good Enough? - A Performance Comparison Between Gaming on Windows and Linux",
            "authors": ["Kopel, Marek", "Bożek, Michał"],
            "year": "2023",
            "doi": "10.1007/978-3-031-41456-5_48",
            "venue": "Computational Collective Intelligence",
            "volume": "14162",
            "pages": "634-646",
            "publisher": "Springer",
            "url": "https://link.springer.com/chapter/10.1007/978-3-031-41456-5_48",
            "file": "",
            "keywords": "external source",
            "note": "Registro agregado desde Springer Nature.",
        },
    ])

    # Final deduplication: DOI first, then normalized title. Keep the first record,
    # which is the canonical path selected above or the explicitly supplied URL.
    unique_records: list[dict] = []
    by_doi: dict[str, dict] = {}
    by_title: dict[str, dict] = {}
    for record in records:
        doi_key = normalize_doi(record.get("doi", ""))
        title_key = normalize(record.get("title", ""))
        current = by_doi.get(doi_key) if doi_key else None
        if current is None and title_key:
            current = by_title.get(title_key)
        if current is None:
            unique_records.append(record)
            current = record
        else:
            # The explicit Springer record is authoritative for the shared DOI.
            if record.get("note") == "Registro agregado desde Springer Nature.":
                for field in ["authors", "year", "venue", "volume", "pages", "publisher", "doi", "url"]:
                    if record.get(field):
                        current[field] = record[field]
            if not current.get("authors") and record.get("authors"):
                current["authors"] = record["authors"]
            for field in ["year", "venue", "volume", "issue", "pages", "publisher", "doi", "url"]:
                if not current.get(field) and record.get(field):
                    current[field] = record[field]
        if doi_key:
            by_doi[doi_key] = current
        if title_key:
            by_title[title_key] = current

    used: set[str] = set()
    entries = [make_entry(record, used) for record in sorted(unique_records, key=lambda r: normalize(r.get("title", "")))]
    header = [
        "% BibTeX generado para Mendeley desde todos los PDF de bibliografia/ y sus subcarpetas.",
        "% Se eliminaron duplicados exactos y duplicados por DOI o título normalizado.",
        f"% Registros PDF físicos: {len(files)} | hashes únicos: {len(by_hash)} | registros finales con URLs: {len(entries)}",
        "% Las rutas de archivo apuntan al workspace actual y pueden requerir actualización al mover los PDF.",
        "",
    ]
    OUT.write_text("\n\n".join(header + entries) + "\n", encoding="utf-8")
    print(f"created {OUT}")
    print(f"pdfs={len(files)} unique_hashes={len(by_hash)} final_entries={len(entries)}")


if __name__ == "__main__":
    main()
