#!/usr/bin/env python3
"""Completa y depura export.bib sin inventar identificadores.

La fuente principal es el BibTeX entregado por Scopus. Los registros incompletos
se completan con la información de los PDF locales y los DOI se contrastan con
Crossref cuando el registro está disponible. Los trabajos para los que no se
localizó DOI conservan su URL editorial o institucional.
"""

from __future__ import annotations

import json
import re
import time
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


SOURCE = Path("/home/julian/Downloads/export.bib")
OUTPUT = Path("/home/julian/Downloads/export_completado.bib")


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def parse_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    offset = 0
    while True:
        match = re.search(r"(?m)^@(\w+)\{", text[offset:])
        if not match:
            break
        start = offset + match.start()
        position = offset + match.end()
        depth = 1
        while position < len(text) and depth:
            if text[position] == "{":
                depth += 1
            elif text[position] == "}":
                depth -= 1
            position += 1
        raw = text[start:position]
        header = re.match(r"@(?P<type>\w+)\{(?P<key>[^,]*),", raw)
        if not header:
            offset = position
            continue
        body_start = header.end()
        fields: dict[str, str] = {}
        cursor = body_start
        field_start = re.compile(r"(?m)^\s*([A-Za-z][\w-]*)\s*=\s*")
        while True:
            field_match = field_start.search(raw, cursor)
            if not field_match:
                break
            name = field_match.group(1).lower()
            value_start = field_match.end()
            if value_start >= len(raw):
                break
            if raw[value_start] == "{":
                value_end = value_start + 1
                nested = 1
                while value_end < len(raw) and nested:
                    if raw[value_end] == "{":
                        nested += 1
                    elif raw[value_end] == "}":
                        nested -= 1
                    value_end += 1
                value = raw[value_start + 1 : value_end - 1]
                cursor = value_end
            elif raw[value_start] == '"':
                value_end = value_start + 1
                while value_end < len(raw):
                    if raw[value_end] == '"' and raw[value_end - 1] != "\\":
                        break
                    value_end += 1
                value = raw[value_start + 1 : value_end]
                cursor = value_end + 1
            else:
                value_end = raw.find("\n", value_start)
                if value_end < 0:
                    value_end = len(raw)
                value = raw[value_start:value_end].rstrip(" ,")
                cursor = value_end
            fields[name] = value.strip()
        entries.append({"type": header.group("type"), "key": header.group("key").strip(), **fields})
        offset = position
    return entries


def doi_clean(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value)
    value = value.rstrip(".;, }")
    if not value or "xxxx" in value or "doi" == value:
        return ""
    return value


def author_list(value: str) -> list[str]:
    value = (value or "").replace("*", "")
    return [part.strip() for part in re.split(r"\s+and\s+", value) if part.strip()]


def author_to_bib(name: str) -> str:
    name = re.sub(r"\s+", " ", name.strip())
    if "," in name:
        family, given = [part.strip() for part in name.split(",", 1)]
        return f"{family}, {given}" if given else family
    parts = name.split()
    return f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) > 1 else name


def crossref_authors(items: list[dict]) -> list[str]:
    result = []
    for item in items or []:
        family = (item.get("family") or "").strip()
        given = (item.get("given") or "").strip()
        if family:
            result.append(f"{family}, {given}" if given else family)
    return result


def crossref(doi: str) -> dict:
    try:
        request = Request(
            "https://api.crossref.org/works/" + quote(doi, safe=""),
            headers={"User-Agent": "Win2APK bibliography verifier/1.0"},
        )
        with urlopen(request, timeout=15) as response:
            return json.load(response).get("message", {})
    except Exception:
        return {}


def text_from_crossref(item: dict) -> str:
    return " ".join(item.get("title", []))


# Keyed by distinctive fragments from incomplete titles or records whose DOI
# was demonstrably wrong in the supplied export.
MANUAL: list[tuple[str, dict[str, object]]] = [
    (
        "xploring operating system diversity",
        {
            "title": "Exploring Operating System Diversity: A Comparative Analysis of Windows, Mac OS, Android and iOS",
            "author": ["Ukpabi, Kosisochukwu Henry", "Ibrahim, Abdullahi Mohammed"],
            "year": "2024",
            "journal": "Journal of Systematic and Modern Science Research",
            "volume": "5",
            "number": "9",
            "url": "https://berkeleypublications.com/bjsmsr/article/view/264",
            "note": "No se localizó DOI en el registro editorial consultado.",
        },
    ),
    (
        "x86 riscing it all",
        {
            "title": "RISCing it All: Accelerating Binary Translation Using Software-Only Validated Flag Speculation",
            "author": [
                "Yen, James", "Wang, Jiarui", "Wei, Zhixiang", "Huang, Zhibai",
                "Zhang, Ziyang", "Gu, Yicheng", "Yu, Senhao", "Chen, Chen",
                "Wang, Yun", "Yu, Xingzi", "Wang, Hao", "Qi, Zhengwei",
            ],
            "year": "2026",
            "doi": "10.1109/tmc.2026.3718184",
            "journal": "IEEE Transactions on Mobile Computing",
        },
    ),
    (
        "too quiet in the library",
        {
            "title": "Too Quiet in the Library: An Empirical Study of Security Updates in Android Apps' Native Code",
            "author": ["Almanee, Sumaya", "Unal, Arda", "Payer, Mathias", "Garcia, Joshua"],
            "year": "2021",
            "doi": "10.1109/icse43902.2021.00122",
            "booktitle": "2021 IEEE/ACM 43rd International Conference on Software Engineering (ICSE)",
        },
    ),
    (
        "to pin or not to pin",
        {
            "title": "To Pin or Not to Pin: Asserting the Scalability of QEMU Parallel Implementation",
            "author": ["Badaroux, Marie", "Miroddi, Saverio", "Pétrot, Frédéric"],
            "year": "2021",
            "doi": "10.1109/dsd53832.2021.00045",
            "booktitle": "2021 24th Euromicro Conference on Digital System Design (DSD)",
        },
    ),
    (
        "system call interposition",
        {
            "title": "System Call Interposition Without Compromise",
            "author": ["Jacobs, Adriaan", "Gülmez, Merve", "Andries, Alicia", "Volckaert, Stijn", "Voulimeneas, Alexios"],
            "year": "2024",
            "doi": "10.1109/dsn58291.2024.00030",
            "booktitle": "2024 IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)",
        },
    ),
    (
        "software modernization contemporary",
        {
            "title": "Contemporary Software Modernization: Strategies, Driving Forces, and Research Opportunities",
            "author": ["Assunção, Wesley K. G.", "Marchezan, Luciano", "Arkoh, Lawrence", "Egyed, Alexander", "Ramler, Rudolf"],
            "year": "2025",
            "doi": "10.1145/3708527",
            "journal": "ACM Transactions on Software Engineering and Methodology",
        },
    ),
    (
        "qemu a fast",
        {
            "title": "QEMU, a Fast and Portable Dynamic Translator",
            "author": ["Bellard, Fabrice"],
            "year": "2005",
            "booktitle": "2005 USENIX Annual Technical Conference, FREENIX Track",
            "pages": "41-46",
            "url": "https://www.usenix.org/publications/library/proceedings/usenix05/tech/freenix/full_papers/bellard/bellard.pdf",
            "note": "El registro DBLP indica que este artículo no tiene DOI.",
        },
    ),
    (
        "proton is proton good",
        {
            "title": "Is Proton Good Enough? - A Performance Comparison Between Gaming on Windows and Linux",
            "author": ["Kopel, Marek", "Bożek, Michał"],
            "year": "2023",
            "doi": "10.1007/978-3-031-41456-5_48",
            "booktitle": "Computational Collective Intelligence",
            "volume": "14162",
            "pages": "634-646",
            "publisher": "Springer",
        },
    ),
    (
        "automated diagnosis and testing",
        {
            "title": "Automated Diagnosis and Testing of Game Compatibility Layers",
            "author": ["Dai, Hu"],
            "year": "2026",
            "doi": "10.1145/3803437.3804876",
            "booktitle": "Proceedings of the 34th ACM International Conference on the Foundations of Software Engineering",
        },
    ),
    (
        "hqemu a multi threaded",
        {
            "title": "HQEMU: A Multi-Threaded and Retargetable Dynamic Binary Translator on Multicores",
            "author": ["Hong, Ding-Yong", "Hsu, Chun-Chen", "Yew, Pen-Chung", "Wu, Jan-Jan", "Hsu, Wei-Chung", "Liu, Pangfeng", "Wang, Chien-Min", "Chung, Yeh-Ching"],
            "year": "2012",
            "doi": "10.1145/2259016.2259030",
            "booktitle": "2012 International Symposium on Code Generation and Optimization (CGO)",
            "pages": "104-113",
        },
    ),
    (
        "linux gaming a survey",
        {
            "title": "A Survey of the Ability of the Linux Operating System to Support Online Game Execution",
            "author": ["Peoples, Cathryn"],
            "year": "2019",
            "journal": "Open Journal of Web Technologies",
            "volume": "6",
            "number": "1",
            "pages": "1-15",
            "url": "https://www.ronpub.com/OJWT_2019v6i1n01_Peoples.pdf",
            "note": "El registro editorial de RonPub no asigna DOI; se conserva la URL y el URN del artículo.",
        },
    ),
    (
        "legacy code leveraging",
        {
            "title": "Leveraging Legacy Code to Deploy Desktop Applications on the Web",
            "author": ["Douceur, John R.", "Elson, Jeremy", "Howell, Jon", "Lorch, Jacob R."],
            "year": "2008",
            "booktitle": "8th USENIX Symposium on Operating Systems Design and Implementation (OSDI 08)",
            "url": "https://www.usenix.org/conference/osdi-08/leveraging-legacy-code-deploy-desktop-applications-web",
            "note": "El registro oficial de USENIX no asigna DOI a este artículo.",
        },
    ),
    (
        "dynamically translating x86",
        {
            "title": "Dynamically Translating x86 to LLVM using QEMU",
            "author": ["Chipounov, Vitaly", "Candea, George"],
            "year": "2010",
            "note": "Informe técnico de EPFL; no se localizó DOI en el registro institucional ni en Crossref.",
            "url": "https://infoscience.epfl.ch/entities/publication/c105c6c4-5d0a-4a93-a8ea-68a229d701e0",
        },
    ),
    (
        "efficient condition code emulation",
        {
            "title": "Efficient Condition Code Emulation for Dynamic Binary Translation Systems",
            "author": ["Zeng, H."],
            "year": "2023",
            "doi": "10.1117/12.2660798",
            "booktitle": "Third International Symposium on Computer Engineering and Intelligent Communications (ISCEIC 2022)",
        },
    ),
    (
        "efact",
        {
            "title": "EFACT: An External Function Auto-Completion Tool to Strengthen Static Binary Lifting",
            "author": ["Zhang, Yilei", "Liao, Haoyu", "Wang, Zekun", "Huang, Bo", "Guo, Jianmei"],
            "year": "2024",
            "doi": "10.1016/j.jss.2024.112092",
            "journal": "Journal of Systems and Software",
        },
    ),
    (
        "programming interfaces for cross platform",
        {
            "title": "Programming Interfaces for Cross-platform Image Rendering and Deep Learning GPGPU",
            "author": ["Georgiev, Georgi Georgiev", "Lazarova, Milena Kirilova"],
            "year": "2023",
            "doi": "10.1109/comsci59259.2023.10315835",
            "booktitle": "2023 International Scientific Conference on Computer Science (COMSCI)",
        },
    ),
    (
        "towards efficient dynamic binary translation",
        {
            "title": "Towards Efficient Dynamic Binary Translation Optimizations Based on RISC Architectural Features",
            "author": ["Xie, WenBing", "Tang, DaGuo", "Qi, FengBin", "Chai, ZhiLei", "Luo, QiaoLing", "Lin, Yuan"],
            "year": "2023",
            "doi": "10.1142/s0218126624501044",
            "journal": "Journal of Circuits, Systems and Computers",
        },
    ),
    (
        "instruction inflation analyzing",
        {
            "title": "An Instruction Inflation Analyzing Framework for Dynamic Binary Translators",
            "year": "2024",
            "doi": "10.1145/3640813",
            "journal": "ACM Transactions on Architecture and Code Optimization",
        },
    ),
    (
        "accelerating shared library",
        {
            "title": "Accelerating Shared Library Execution in a DBT",
            "author": ["Spink, Tom", "Franke, Björn"],
            "year": "2024",
            "doi": "10.1145/3652032.3657565",
            "booktitle": "Proceedings of the 25th ACM SIGPLAN/SIGBED International Conference on Languages, Compilers, and Tools for Embedded Systems",
        },
    ),
    (
        "dynamic security analysis on android",
        {
            "title": "Dynamic Security Analysis on Android: A Systematic Literature Review",
            "author": ["Sutter, Thomas", "Kehrer, Timo", "Rennhard, Marc", "Tellenbach, Bernhard", "Klein, Jacques"],
            "year": "2024",
            "doi": "10.1109/access.2024.3390612",
            "journal": "IEEE Access",
        },
    ),
    (
        "crossmapping harmonizing",
        {
            "title": "CrossMapping: Harmonizing Memory Consistency in Cross-ISA Binary Translation",
            "author": ["Gao, Chen", "Meng, Xiangwei", "Lai, Jinhui", "Li, Wei", "Zhang, Yiran", "Ren, Fengyuan"],
            "year": "2024",
            "booktitle": "2024 USENIX Annual Technical Conference (USENIX ATC 24)",
            "url": "https://www.usenix.org/conference/atc24/presentation/gao-chen",
            "note": "El registro oficial de USENIX y DBLP no asignan DOI a este artículo.",
        },
    ),
    (
        "btbench",
        {
            "title": "BTBench: A Benchmark for Comprehensive Binary Translation Performance Evaluation",
            "author": ["Li, Xinyu", "Lan, Yanzhi", "Niu, Gen", "Xue, Feng", "Zhang, Fuxin"],
            "year": "2024",
            "doi": "10.1109/ispass61541.2024.00014",
            "booktitle": "2024 IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS)",
        },
    ),
    (
        "box64 practical",
        {
            "title": "Practical and Efficient x86-64 Emulation on RISC-V",
            "year": "2026",
            "doi": "10.1145/3767295.3803574",
            "booktitle": "EUROSYS 2026 - Proceedings of the 2026 European Conference on Computer Systems",
        },
    ),
    (
        "box64 analysis",
        {
            "title": "Analysis and Research on BOX64's Core Technologies for Cross-Architecture Software Migration",
            "author": ["Zhang, Jin", "Shan, Zehu", "Liu, Xiaodong", "Wang, Wenzhu", "Li, Zhuoheng", "Peng, Long", "Yu, Jie"],
            "year": "2023",
            "doi": "10.1109/frse58934.2023.00064",
            "booktitle": "2023 International Conference on Frontiers of Robotics and Software Engineering (FRSE)",
        },
    ),
    (
        "arming x86 games",
        {
            "title": "ARMing x86 Games: Accelerating Binary Translation Using Software-Only Validated Flag Speculation",
            "author": ["Yen, James", "Wang, Jiarui", "Huang, Zhibai", "Wei, Zhixiang", "Zhang, Ziyang", "Chen, Chen", "Yu, Senhao", "Wang, Yun", "Wang, Hao", "Qi, Zhengwei"],
            "year": "2025",
            "doi": "10.1145/3711875.3729163",
            "booktitle": "MobiSys 2025 - Proceedings of the 23rd ACM International Conference on Mobile Systems, Applications, and Services",
        },
    ),
    (
        "mambo a low overhead",
        {
            "title": "MAMBO: A Low-Overhead Dynamic Binary Modification Tool for ARM",
            "author": ["Gorgovan, Cosmin", "d'Antras, Amanieu", "Luján, Mikel"],
            "year": "2016",
            "doi": "10.1145/2896451",
            "journal": "ACM Transactions on Architecture and Code Optimization",
        },
    ),
    (
        "nativeguard protecting",
        {
            "title": "NativeGuard: Protecting Android Applications from Third-Party Native Libraries",
            "author": ["Sun, Mengtao", "Tan, Gang"],
            "year": "2014",
            "doi": "10.1145/2627393.2627396",
            "booktitle": "Proceedings of the 2014 ACM Conference on Security and Privacy in Wireless & Mobile Networks",
        },
    ),
    (
        "interactive launch of 16000",
        {
            "title": "Interactive Launch of 16,000 Microsoft Windows Instances on a Supercomputer",
            "year": "2018",
            "doi": "10.1109/hpec.2018.8547782",
            "booktitle": "2018 IEEE High Performance Extreme Computing Conference (HPEC)",
        },
    ),
    (
        "reproducible notebook containers",
        {
            "title": "Reproducible Notebook Containers using Application Virtualization",
            "year": "2022",
            "doi": "10.1109/escience55777.2022.00015",
            "booktitle": "2022 IEEE 18th International Conference on e-Science (e-Science)",
        },
    ),
    (
        "boosting cross architectural emulation",
        {
            "title": "Boosting Cross-Architectural Emulation Performance by Foregoing the Intermediate Representation Model",
            "author": ["Parker, Amy Iris"],
            "year": "2025",
            "doi": "10.48550/arXiv.2501.03427",
            "url": "https://arxiv.org/abs/2501.03427",
        },
    ),
    (
        "a comparative study of operating systems",
        {
            "title": "A Comparative Study of Operating Systems: Case of Windows, UNIX, Linux, Mac, Android and iOS",
            "author": ["Adekotujo, Akinlolu", "Odumabo, Adedoyin", "Adedokun, Ademola", "Aiyeniko, Olukayode"],
            "year": "2020",
            "doi": "10.5120/ijca2020920494",
            "journal": "International Journal of Computer Applications",
        },
    ),
    (
        "application virtualization an agent encapsulation",
        {
            "title": "Application Virtualization: An Agent Encapsulation of Software in Virtual Machines to Archive the Execution Performance in Hosts",
            "author": ["Liang, Yifan", "Dai, Hongjun"],
            "year": "2021",
            "doi": "10.1109/ISPA-BDCloud-SocialCom-SustainCom52081.2021.00090",
            "booktitle": "2021 IEEE International Conferences on Parallel and Distributed Processing with Applications, Big Data and Cloud Computing, Sustainable Computing and Communications, Social Computing and Networking (ISPA/BDCloud/SocialCom/SustainCom)",
        },
    ),
    (
        "a system level dynamic binary translator",
        {
            "title": "A System-Level Dynamic Binary Translator Using Automatically-Learned Translation Rules",
            "author": ["Jiang, Jinhu", "Liang, Chaoyi", "Dong, Rongchao", "Yang, Zhaohui", "Zhou, Zhongjun", "Wang, Wenwen", "Yew, Pen-Chung", "Zhang, Weihua"],
            "year": "2024",
            "doi": "10.1109/cgo57630.2024.10444850",
            "booktitle": "2024 IEEE/ACM International Symposium on Code Generation and Optimization (CGO)",
        },
    ),
    (
        "a study on windows based ransomware",
        {
            "title": "A Study on Windows-Based Ransomware Implications on Linux Operating System Using Compatibility Layer Wine Based on Dynamic Analysis",
            "author": ["Septiasari, Rycka", "Pramadi, Yogha Restu"],
            "year": "2020",
            "doi": "10.1088/1757-899X/1007/1/012120",
            "booktitle": "IOP Conference Series: Materials Science and Engineering",
        },
    ),
]


def manual_for(title: str) -> dict[str, object]:
    key = normalize(title)
    for needle, data in MANUAL:
        if needle in key:
            return dict(data)
    return {}


def apply_crossref(record: dict[str, str]) -> None:
    doi = doi_clean(record.get("doi", ""))
    if not doi:
        record.pop("doi", None)
        return
    record["doi"] = doi
    item = crossref(doi)
    if not item:
        return
    api_title = text_from_crossref(item)
    title = record.get("title", "")
    similarity = SequenceMatcher(None, normalize(title), normalize(api_title)).ratio()
    # Some publishers register abbreviated titles (e.g., "Cider" or
    # "NativeGuard"). Keep the supplied full title in that case, but use the
    # authoritative author list, date, venue, pages and publisher.
    if api_title and (similarity >= 0.72 or not title):
        record["title"] = api_title
    authors = crossref_authors(item.get("author", []))
    if authors:
        record["author"] = " and ".join(authors)
    issued = item.get("published-print") or item.get("published-online") or item.get("issued") or {}
    parts = issued.get("date-parts", [[]])
    if parts and parts[0]:
        record["year"] = str(parts[0][0])
    if item.get("container-title"):
        container = item["container-title"][0]
        if item.get("type") == "journal-article":
            record["journal"] = container
            record.pop("booktitle", None)
        elif container:
            record["booktitle"] = container
            record.pop("journal", None)
    for source, target in [("volume", "volume"), ("issue", "number"), ("page", "pages"), ("publisher", "publisher")]:
        if item.get(source):
            record[target] = str(item[source])
    time.sleep(0.03)


def merge(base: dict[str, str], extra: dict[str, object]) -> dict[str, str]:
    result = dict(base)
    for key, value in extra.items():
        if isinstance(value, list):
            result[key] = " and ".join(str(x) for x in value)
        elif value:
            result[key] = str(value)
    return result


def quality(record: dict[str, str]) -> tuple[int, int, int]:
    useful = sum(bool(record.get(field)) for field in ["author", "year", "doi", "journal", "booktitle", "url", "pages"])
    return (useful, len(record.get("author", "")), len(record.get("abstract", "")))


def key_for(record: dict[str, str], used: set[str]) -> str:
    first = author_list(record.get("author", ""))
    family = normalize(first[0]).split()[0] if first else "reference"
    year = record.get("year", "nd")
    word = normalize(record.get("title", "reference")).split()
    base = re.sub(r"[^a-z0-9]", "", family + year + (word[0] if word else "reference")) or "reference"
    key = base
    counter = 2
    while key in used:
        key = f"{base}{counter}"
        counter += 1
    used.add(key)
    return key


def bib_value(value: str) -> str:
    # Existing Scopus abstracts may contain LaTeX commands and nested braces;
    # those are preserved because they are valid BibTeX content.
    return value.replace("\n", " ").strip()


def write_entry(record: dict[str, str], key: str) -> str:
    entry_type = record.pop("_type", "misc").lower()
    if entry_type == "techreport":
        entry_type = "techreport"
    preferred = [
        "author", "editor", "title", "year", "journal", "booktitle", "volume", "number",
        "issue", "pages", "publisher", "isbn", "issn", "doi", "url", "keywords", "abstract", "note",
    ]
    fields = [(field, record[field]) for field in preferred if record.get(field)]
    fields.extend((field, value) for field, value in record.items() if field not in preferred and not field.startswith("_"))
    lines = [f"@{entry_type}{{{key},"]
    for index, (field, value) in enumerate(fields):
        comma = "," if index < len(fields) - 1 else ""
        lines.append(f"  {field} = {{{bib_value(value)}}}{comma}")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    entries = parse_entries(SOURCE.read_text(encoding="utf-8"))
    records: list[dict[str, str]] = []
    for original in entries:
        record = {key: value for key, value in original.items() if key not in {"type", "key"}}
        record["_type"] = original.get("type", "misc")
        manual = manual_for(record.get("title", ""))
        record = merge(record, manual)
        record["doi"] = doi_clean(record.get("doi", ""))
        # Explicit corrections take precedence over the source export.
        if normalize(record.get("title", "")) == normalize("Dynamic Security Analysis on Android: A Systematic Literature Review"):
            record["doi"] = "10.1109/access.2024.3390612"
        apply_crossref(record)
        # Reapply curated fields after Crossref so full titles and official
        # publisher links are not replaced by abbreviated registrations.
        record = merge(record, manual)
        record["doi"] = doi_clean(record.get("doi", ""))
        records.append(record)

    # Merge duplicate/placeholder records after manual titles have been fixed.
    merged: dict[str, dict[str, str]] = {}
    order: list[str] = []
    for record in records:
        title_key = normalize(record.get("title", ""))
        doi_key = record.get("doi", "")
        identity = "doi:" + doi_key if doi_key else "title:" + title_key
        current = merged.get(identity)
        if current is None:
            merged[identity] = record
            order.append(identity)
            continue
        if quality(record) > quality(current):
            record.update({key: value for key, value in current.items() if key not in record or not record[key]})
            merged[identity] = record
        else:
            for key, value in record.items():
                if key not in current or not current[key]:
                    current[key] = value

    used: set[str] = set()
    output_entries = []
    for identity in order:
        record = dict(merged[identity])
        key = key_for(record, used)
        record.pop("key", None)
        output_entries.append(write_entry(record, key))

    header = [
        "% export_completado.bib: metadatos revisados y normalizados para Mendeley.",
        "% Los DOI se conservaron solo cuando pudieron asociarse al título del registro.",
        "% Los trabajos sin DOI conservan la URL editorial o institucional disponible.",
        f"% Registros de entrada: {len(entries)} | registros finales: {len(output_entries)}",
        "",
    ]
    OUTPUT.write_text("\n\n".join(header + output_entries) + "\n", encoding="utf-8")
    missing = sum("doi = {" not in entry for entry in output_entries)
    print(f"created {OUTPUT}")
    print(f"input={len(entries)} output={len(output_entries)} without_doi={missing}")


if __name__ == "__main__":
    main()
