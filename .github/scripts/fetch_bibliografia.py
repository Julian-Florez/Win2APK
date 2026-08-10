#!/usr/bin/env python3
import csv, json, os, re, sys, time, unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

UA = "Win2APK-bibliografia/1.0 (academic bibliography retrieval)"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept": "*/*"})

# These direct links were manually verified as open-licensed sources.
MANUAL = {
    1: [
        {"pdf_url": "https://link.springer.com/content/pdf/10.1007%2Fs11416-018-0319-9.pdf",
         "license": "cc-by-4.0", "landing_page_url": "https://link.springer.com/article/10.1007/s11416-018-0319-9"}
    ],
    4: [
        {"pdf_url": "https://iopscience.iop.org/article/10.1088/1757-899X/1007/1/012120/pdf",
         "license": "cc-by-3.0", "landing_page_url": "https://iopscience.iop.org/article/10.1088/1757-899X/1007/1/012120"}
    ],
}

ALLOWED_LICENSE_PREFIXES = (
    "cc-", "creative-commons", "public-domain", "cc0"
)

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def title_match(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def license_allows_redistribution(lic):
    if not lic:
        return False
    x = str(lic).strip().lower().replace("_", "-")
    return x.startswith(ALLOWED_LICENSE_PREFIXES)

def openalex_work(rec):
    doi = (rec.get("doi") or "").strip()
    try:
        if doi:
            u = "https://api.openalex.org/works/https://doi.org/" + quote(doi, safe="")
            r = S.get(u, timeout=25)
            if r.status_code == 200:
                w = r.json()
                if title_match(rec["title"], w.get("display_name")) >= 0.72:
                    return w
        r = S.get("https://api.openalex.org/works",
                  params={"search": rec["title"], "per-page": 5}, timeout=25)
        if r.status_code == 200:
            candidates = r.json().get("results", [])
            candidates.sort(key=lambda w: title_match(rec["title"], w.get("display_name")), reverse=True)
            if candidates and title_match(rec["title"], candidates[0].get("display_name")) >= 0.80:
                return candidates[0]
    except Exception:
        pass
    return None

def candidate_locations(rec, work):
    out = []
    out.extend(MANUAL.get(rec["index"], []))
    if work:
        locs = []
        if work.get("best_oa_location"):
            locs.append(work["best_oa_location"])
        locs.extend(work.get("locations") or [])
        seen = set()
        for loc in locs:
            if not isinstance(loc, dict):
                continue
            pdf = loc.get("pdf_url")
            if not pdf or pdf in seen:
                continue
            seen.add(pdf)
            source = loc.get("source") or {}
            out.append({
                "pdf_url": pdf,
                "license": loc.get("license"),
                "landing_page_url": loc.get("landing_page_url") or "",
                "source_name": source.get("display_name") or source.get("host_organization_name") or "",
                "is_oa": loc.get("is_oa"),
            })
    out.sort(key=lambda x: (not license_allows_redistribution(x.get("license")),
                            "researchgate.net" in (x.get("pdf_url") or ""),
                            "arxiv.org" in (x.get("pdf_url") or "")))
    return out

def download_pdf(url, dest):
    headers = {
        "User-Agent": UA,
        "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.5",
        "Referer": url,
    }
    try:
        with S.get(url, headers=headers, timeout=45, allow_redirects=True, stream=True) as r:
            if r.status_code != 200:
                return False, f"HTTP {r.status_code}"
            data = bytearray()
            for chunk in r.iter_content(1024 * 256):
                if chunk:
                    data.extend(chunk)
                    if len(data) > 80 * 1024 * 1024:
                        return False, "PDF >80 MB"
            head = bytes(data[:2048]).lstrip()
            if not head.startswith(b"%PDF"):
                return False, "respuesta no es PDF"
            if len(data) < 1500:
                return False, "PDF demasiado pequeno"
            Path(dest).write_bytes(bytes(data))
            return True, ""
    except Exception as e:
        return False, type(e).__name__

def make_blank_pdf(dest):
    c = canvas.Canvas(str(dest), pagesize=A4, pageCompression=1)
    c.showPage()
    c.save()

def main():
    manifest = Path(sys.argv[1] if len(sys.argv) > 1 else "bibliografia_manifest.json")
    outdir = Path(sys.argv[2] if len(sys.argv) > 2 else "output/bibliografia")
    outdir.mkdir(parents=True, exist_ok=True)
    records = json.loads(manifest.read_text(encoding="utf-8"))
    rows = []

    for pos, rec in enumerate(records, 1):
        work = openalex_work(rec)
        oa_title = work.get("display_name", "") if work else ""
        oa_doi = work.get("doi", "") if work else ""
        candidates = candidate_locations(rec, work)
        status = "PDF_EN_BLANCO"
        reason = "No se encontro una version PDF con licencia explicita de redistribucion"
        used = ""
        used_license = ""
        attempts = []

        for loc in candidates:
            lic = (loc.get("license") or "").lower()
            url = loc.get("pdf_url") or ""
            if not license_allows_redistribution(lic):
                attempts.append(f"sin licencia redistribuible: {url}")
                continue
            if rec["index"] == 49 and "arxiv.org" in url:
                attempts.append(f"version de autor no redistribuible: {url}")
                continue
            ok, why = download_pdf(url, outdir / rec["filename"])
            if ok:
                status = "DESCARGADO"
                reason = "PDF de acceso abierto con licencia de redistribucion"
                used = url
                used_license = lic
                break
            attempts.append(f"{why}: {url}")

        if status != "DESCARGADO":
            make_blank_pdf(outdir / rec["filename"])
            if candidates and attempts:
                reason += "; " + " | ".join(attempts[:3])

        rows.append({
            "n": rec["index"],
            "keyword": rec["keyword"],
            "titulo": rec["title"],
            "primer_autor": rec["first_author"],
            "doi": rec.get("doi", ""),
            "archivo": rec["filename"],
            "estado": status,
            "licencia": used_license,
            "fuente_pdf": used,
            "openalex_titulo": oa_title,
            "openalex_doi": oa_doi,
            "nota": reason,
        })
        print(f"[{pos:02d}/{len(records)}] {status}: {rec['filename']}", flush=True)
        time.sleep(0.08)

    csv_path = outdir / "LISTA_FINAL.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    found = sum(r["estado"] == "DESCARGADO" for r in rows)
    blank = len(rows) - found
    md = [
        "# Bibliografia Win2APK",
        "",
        f"- Referencias procesadas: **{len(rows)}**",
        f"- PDFs descargados con licencia explicita de redistribucion: **{found}**",
        f"- PDFs en blanco usados como reemplazo: **{blank}**",
        "",
        "Los PDF en blanco se usan cuando no se encontro una version que pudiera copiarse legitimamente al repositorio,",
        "o cuando la descarga publica fallo. La fuente y el motivo detallado quedan en `LISTA_FINAL.csv`.",
        "",
        "| # | Estado | Keyword | Titulo | Archivo |",
        "|---:|---|---|---|---|",
    ]
    for r in rows:
        title = r["titulo"].replace("|", "\\|")
        md.append(f"| {r['n']} | {r['estado']} | {r['keyword']} | {title} | `{r['archivo']}` |")
    (outdir / "README.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    summary = {"total": len(rows), "descargados": found, "pdf_en_blanco": blank}
    (outdir / "RESUMEN.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("SUMMARY", json.dumps(summary), flush=True)

if __name__ == "__main__":
    main()
