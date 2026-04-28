"""
retrieve_apis.py — Phase C: Automated Retrieval from OpenAlex + Semantic Scholar
==================================================================================
Executes targeted search queries against OpenAlex and Semantic Scholar APIs,
normalizes results to papers_raw.csv format, and outputs:

  scripts/papers_raw.csv             — merged, deduplicated API results
  scripts/papers_manual_template.csv — blank template for Scopus/IEEE/WoS exports
  scripts/retrieval_report.txt       — per-query counts + deduplication summary

Strategy (informed by Phase B scoping):
  - S3 (Dana Desa, N=57)     → retrieve ALL
  - S4 (Typology, N=249)     → retrieve ALL
  - S5 (Decentralized, N=642)→ top 300 by relevance
  - S1 (Broad ML, N=4370)    → top 200 by citation count (too noisy otherwise)
  - S6 (Procurement, N=3310) → top 150 by citation count
  S2/S7 excluded from retrieval (too noisy; S2 returns unrelated content)

Run:
    python scripts/retrieve_apis.py

No API key required. Polite delay between requests.
"""

from __future__ import annotations

import csv
import time
import sys
import re
import json
import unicodedata
from pathlib import Path
from datetime import date
from typing import Optional

import requests

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
ROOT_DIR     = SCRIPT_DIR.parent
OUTPUT_CSV   = SCRIPT_DIR / "papers_raw.csv"
TEMPLATE_CSV = SCRIPT_DIR / "papers_manual_template.csv"
REPORT_TXT   = SCRIPT_DIR / "retrieval_report.txt"

MAILTO  = "researcher@binus.ac.id"
DELAY   = 0.8   # seconds between API calls
TIMEOUT = 30

# ─────────────────────────────────────────────────────────────────────────────
# Canonical columns for papers_raw.csv
# ─────────────────────────────────────────────────────────────────────────────
COLUMNS = [
    "doi", "title", "year", "journal", "sjr_quartile", "core_rank",
    "citations", "source_db", "oa_url", "abstract", "is_duplicate", "language",
    "authors", "paper_type",
]


# ─────────────────────────────────────────────────────────────────────────────
# Query definitions
# ─────────────────────────────────────────────────────────────────────────────
OPENALEX_QUERIES = [
    {
        "id":      "S3-OA",
        "label":   "Village Fund / Dana Desa",
        "search":  "village fund dana desa corruption irregularity detection",
        "filter":  "publication_year:2010-2026",
        "max":     None,   # retrieve ALL (57 expected)
        "sort":    None,
    },
    {
        "id":      "S4-OA",
        "label":   "Feature Engineering + Corruption Typology",
        "search":  "feature engineering corruption typology fraud pattern government financial data",
        "filter":  "publication_year:2010-2026",
        "max":     300,
        "sort":    "cited_by_count:desc",
    },
    {
        "id":      "S5-OA",
        "label":   "Decentralized Fund Audit Analytics",
        "search":  "decentralized fund audit analytics anomaly unsupervised machine learning public",
        "filter":  "publication_year:2010-2026",
        "max":     300,
        "sort":    "cited_by_count:desc",
    },
    {
        "id":      "S1-OA",
        "label":   "Core ML + Public Finance Fraud (capped)",
        "search":  "anomaly detection fraud detection public sector government financial machine learning",
        "filter":  "publication_year:2015-2026,type:article",
        "max":     200,
        "sort":    "cited_by_count:desc",
    },
    {
        "id":      "S6-OA",
        "label":   "Procurement Fraud ML (capped)",
        "search":  "procurement fraud detection machine learning public sector audit",
        "filter":  "publication_year:2015-2026,type:article",
        "max":     150,
        "sort":    "cited_by_count:desc",
    },
]

SEMANTIC_SCHOLAR_QUERIES = [
    {
        "id":    "S3-S2",
        "label": "Village Fund Corruption Detection",
        "query": "village fund dana desa corruption anomaly detection",
        "max":   100,
    },
    {
        "id":    "S4-S2",
        "label": "Feature Engineering Corruption Typology",
        "query": "feature engineering corruption typology fraud pattern public finance",
        "max":   150,
    },
    {
        "id":    "S5-S2",
        "label": "Decentralized Public Fund Anomaly ML",
        "query": "anomaly detection machine learning government public expenditure audit decentralized",
        "max":   150,
    },
    {
        "id":    "S1-S2",
        "label": "Fraud Detection Public Sector IS (capped)",
        "query": "fraud detection information system government financial machine learning anomaly",
        "max":   100,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# OpenAlex retrieval (paginated)
# ─────────────────────────────────────────────────────────────────────────────

def openalex_fetch_all(query_def: dict) -> list[dict]:
    """Paginate through OpenAlex results for a single query definition."""
    search  = query_def["search"]
    filter_ = query_def.get("filter", "")
    sort    = query_def.get("sort", "")
    max_n   = query_def.get("max")      # None = fetch all
    per_page = 200

    all_results: list[dict] = []
    page = 1
    total_available = None

    print(f"    [OpenAlex] '{query_def['label']}' ...", end="", flush=True)

    while True:
        params = {
            "search":   search,
            "per-page": per_page,
            "page":     page,
            "mailto":   MAILTO,
            "select":   (
                "id,doi,title,publication_year,type,cited_by_count,"
                "open_access,primary_location,authorships,abstract_inverted_index,"
                "language"
            ),
        }
        if filter_:
            params["filter"] = filter_
        if sort:
            params["sort"] = sort

        try:
            resp = requests.get(
                "https://api.openalex.org/works",
                params=params, timeout=TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f" [ERROR: {e}]")
            break

        if total_available is None:
            total_available = data.get("meta", {}).get("count", 0)

        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)
        print(f".", end="", flush=True)

        # Stop if we've hit our cap
        if max_n and len(all_results) >= max_n:
            all_results = all_results[:max_n]
            break

        # Stop if we've fetched everything
        fetched_so_far = (page - 1) * per_page + len(results)
        if fetched_so_far >= (total_available or 0):
            break

        page += 1
        time.sleep(DELAY)

    print(f" → {len(all_results)} records (of {total_available} available)")
    return all_results


def reconstruct_abstract(inverted_index: Optional[dict]) -> str:
    """Reconstruct abstract from OpenAlex inverted index format."""
    if not inverted_index:
        return ""
    try:
        word_pos: list[tuple[int, str]] = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_pos.append((pos, word))
        word_pos.sort()
        return " ".join(w for _, w in word_pos)
    except Exception:
        return ""


def normalize_openalex(record: dict, source_id: str) -> dict:
    """Convert an OpenAlex work record to papers_raw.csv row."""
    doi = (record.get("doi") or "").replace("https://doi.org/", "").strip()
    title = (record.get("title") or "").strip()
    year  = record.get("publication_year") or ""
    cites = record.get("cited_by_count") or 0

    # Journal
    try:
        journal = record["primary_location"]["source"]["display_name"] or ""
    except (KeyError, TypeError):
        journal = ""

    # OA URL
    try:
        oa_info = record.get("open_access") or {}
        oa_url  = oa_info.get("oa_url") or oa_info.get("landing_page_url") or ""
    except Exception:
        oa_url = ""

    # Abstract
    abstract = reconstruct_abstract(record.get("abstract_inverted_index"))

    # Language
    language = record.get("language") or "en"

    # Authors (first 3)
    try:
        auth_list = record.get("authorships") or []
        authors = "; ".join(
            a["author"]["display_name"]
            for a in auth_list[:3]
            if a.get("author", {}).get("display_name")
        )
    except Exception:
        authors = ""

    paper_type = record.get("type") or ""

    return {
        "doi":          doi,
        "title":        title,
        "year":         str(year),
        "journal":      journal,
        "sjr_quartile": "",
        "core_rank":    "",
        "citations":    str(cites),
        "source_db":    f"openalex-{source_id}",
        "oa_url":       oa_url,
        "abstract":     abstract[:1000],  # cap for CSV manageability
        "is_duplicate": "False",
        "language":     language,
        "authors":      authors,
        "paper_type":   paper_type,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Semantic Scholar retrieval (paginated)
# ─────────────────────────────────────────────────────────────────────────────

S2_FIELDS = "paperId,externalIds,title,year,citationCount,openAccessPdf,journal,abstract,authors,publicationTypes"

def semantic_scholar_fetch(query_def: dict) -> list[dict]:
    """Fetch results from Semantic Scholar Paper Search API."""
    query = query_def["query"]
    max_n = query_def.get("max", 100)
    limit = min(100, max_n)  # S2 max per page = 100

    all_results: list[dict] = []
    offset = 0

    print(f"    [S2] '{query_def['label']}' ...", end="", flush=True)

    while len(all_results) < max_n:
        params = {
            "query":  query,
            "fields": S2_FIELDS,
            "limit":  limit,
            "offset": offset,
        }
        try:
            resp = requests.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params=params, timeout=TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f" [ERROR: {e}]")
            break

        results = data.get("data", [])
        if not results:
            break

        all_results.extend(results)
        print(f".", end="", flush=True)

        total = data.get("total", 0)
        offset += len(results)
        if offset >= total or offset >= max_n:
            break
        time.sleep(DELAY)

    all_results = all_results[:max_n]
    print(f" → {len(all_results)} records")
    return all_results


def normalize_semantic_scholar(record: dict, source_id: str) -> dict:
    """Convert a Semantic Scholar record to papers_raw.csv row."""
    ext_ids = record.get("externalIds") or {}
    doi     = (ext_ids.get("DOI") or "").strip()
    title   = (record.get("title") or "").strip()
    year    = record.get("year") or ""
    cites   = record.get("citationCount") or 0

    try:
        journal = record.get("journal", {}).get("name") or ""
    except (AttributeError, TypeError):
        journal = ""

    try:
        pdf_info = record.get("openAccessPdf") or {}
        oa_url   = pdf_info.get("url") or ""
    except Exception:
        oa_url = ""

    abstract = (record.get("abstract") or "")[:1000]

    try:
        authors = "; ".join(
            a.get("name", "") for a in (record.get("authors") or [])[:3]
        )
    except Exception:
        authors = ""

    try:
        pub_types = record.get("publicationTypes") or []
        paper_type = pub_types[0] if pub_types else ""
    except Exception:
        paper_type = ""

    return {
        "doi":          doi,
        "title":        title,
        "year":         str(year),
        "journal":      journal,
        "sjr_quartile": "",
        "core_rank":    "",
        "citations":    str(cites),
        "source_db":    f"semantic_scholar-{source_id}",
        "oa_url":       oa_url,
        "abstract":     abstract,
        "is_duplicate": "False",
        "language":     "en",   # S2 doesn't return language; assume English
        "authors":      authors,
        "paper_type":   paper_type,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Deduplication
# ─────────────────────────────────────────────────────────────────────────────

def normalize_doi(doi: str) -> str:
    return doi.strip().lower().rstrip(".")


def normalize_title(title: str) -> str:
    t = title.lower().strip()
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t


def deduplicate(rows: list[dict]) -> list[dict]:
    """
    Mark duplicates by DOI (exact) then by title similarity (fuzzy).
    Priority order: openalex > semantic_scholar (keeps more metadata).
    """
    # Sort so openalex-* comes first (preferred source)
    rows.sort(key=lambda r: (0 if r["source_db"].startswith("openalex") else 1, r["source_db"]))

    seen_dois:   dict[str, int] = {}   # norm_doi → index of first occurrence
    seen_titles: dict[str, int] = {}   # norm_title[:60] → index

    for i, row in enumerate(rows):
        doi   = normalize_doi(row.get("doi", ""))
        title = normalize_title(row.get("title", ""))
        title_key = title[:60]

        is_dup = False

        if doi and doi in seen_dois:
            is_dup = True
        elif doi:
            seen_dois[doi] = i

        if not is_dup:
            if title_key and title_key in seen_titles:
                is_dup = True
            elif title_key:
                seen_titles[title_key] = i

        rows[i]["is_duplicate"] = "True" if is_dup else "False"

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Manual template
# ─────────────────────────────────────────────────────────────────────────────

def write_manual_template(path: Path) -> None:
    """Write a blank CSV template for Scopus / IEEE / WoS manual exports."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        # Three example placeholder rows
        for db in ["scopus", "ieee", "wos"]:
            writer.writerow({
                "doi":          "10.XXXX/example",
                "title":        f"[Replace with title from {db.upper()} export]",
                "year":         "2024",
                "journal":      "[Journal / Conference name]",
                "sjr_quartile": "[Q1/Q2/Q3/Q4 — look up at scimago.com]",
                "core_rank":    "[A*/A/B/C — look up at core.edu.au if conference]",
                "citations":    "0",
                "source_db":    db,
                "oa_url":       "",
                "abstract":     "[Paste abstract here]",
                "is_duplicate": "False",
                "language":     "en",
                "authors":      "[Author1; Author2]",
                "paper_type":   "article",
            })


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def run_retrieval():
    today = date.today().isoformat()
    print("=" * 70)
    print("Phase C — Automated API Retrieval")
    print(f"Date: {today}")
    print("=" * 70)

    all_rows: list[dict] = []
    report_lines: list[str] = []

    report_lines.append(f"Phase C — Retrieval Report\nDate: {today}\n{'='*60}\n")

    # ── OpenAlex ──────────────────────────────────────────────────────────────
    print("\n[1/2] OpenAlex retrieval")
    oa_total = 0
    for q in OPENALEX_QUERIES:
        time.sleep(DELAY)
        records = openalex_fetch_all(q)
        rows = [normalize_openalex(r, q["id"]) for r in records]
        # Filter: year 2010–2026, must have a title
        rows = [r for r in rows if r["title"] and 2010 <= int(r["year"] or 0) <= 2026]
        all_rows.extend(rows)
        oa_total += len(rows)
        report_lines.append(f"  {q['id']} ({q['label']}): {len(rows)} records retrieved")

    report_lines.append(f"  OpenAlex subtotal: {oa_total}\n")

    # ── Semantic Scholar ───────────────────────────────────────────────────────
    print("\n[2/2] Semantic Scholar retrieval")
    s2_total = 0
    for q in SEMANTIC_SCHOLAR_QUERIES:
        time.sleep(DELAY)
        records = semantic_scholar_fetch(q)
        rows = [normalize_semantic_scholar(r, q["id"]) for r in records]
        rows = [r for r in rows if r["title"] and 2010 <= int(r["year"] or 0) <= 2026]
        all_rows.extend(rows)
        s2_total += len(rows)
        report_lines.append(f"  {q['id']} ({q['label']}): {len(rows)} records retrieved")

    report_lines.append(f"  Semantic Scholar subtotal: {s2_total}\n")

    # ── Deduplicate ────────────────────────────────────────────────────────────
    print(f"\nTotal before dedup: {len(all_rows)}")
    all_rows = deduplicate(all_rows)
    n_dup    = sum(1 for r in all_rows if r["is_duplicate"] == "True")
    n_unique = len(all_rows) - n_dup
    print(f"Duplicates flagged: {n_dup}")
    print(f"Unique records    : {n_unique}")
    report_lines.append(f"Total raw records   : {len(all_rows)}")
    report_lines.append(f"Duplicates flagged  : {n_dup}")
    report_lines.append(f"Unique records      : {n_unique}")
    report_lines.append("")
    report_lines.append("NOTE: Scopus, IEEE Xplore, WoS records NOT included.")
    report_lines.append("      Add manually using papers_manual_template.csv, then re-run dedup.")
    report_lines.append("")

    # Coverage check
    report_lines.append("── Coverage check ──")
    for db in ["openalex", "semantic_scholar"]:
        n = sum(1 for r in all_rows if r["source_db"].startswith(db) and r["is_duplicate"] == "False")
        report_lines.append(f"  {db:25s}: {n} unique")
    report_lines.append("")

    # Corpus size advisory
    if n_unique < 40:
        report_lines.append("ADVISORY: Unique count < 40 target. After adding Scopus/IEEE/WoS,")
        report_lines.append("  expect significant growth. Proceed with full pipeline once manual")
        report_lines.append("  exports are merged.")
    elif n_unique > 300:
        report_lines.append("ADVISORY: Large raw pool. IC/EC filtering in quality_filter_slr.py")
        report_lines.append("  will reduce this significantly — expected ~15–25% pass rate.")
    else:
        report_lines.append(f"ADVISORY: Pool size {n_unique} is in expected range.")
        report_lines.append("  After adding Scopus/IEEE/WoS, quality_filter_slr.py should yield")
        report_lines.append("  40–80 included papers. Proceed to Phase D.")

    # ── Write papers_raw.csv ───────────────────────────────────────────────────
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for row in all_rows:
            writer.writerow({k: row.get(k, "") for k in COLUMNS})

    print(f"\n✓ Written: {OUTPUT_CSV}  ({len(all_rows)} rows, {n_unique} unique)")

    # ── Write manual template ──────────────────────────────────────────────────
    write_manual_template(TEMPLATE_CSV)
    print(f"✓ Written: {TEMPLATE_CSV}  (blank template for Scopus/IEEE/WoS)")

    # ── Write report ───────────────────────────────────────────────────────────
    with open(REPORT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"✓ Written: {REPORT_TXT}")

    # ── Console summary ────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("PHASE C (API RETRIEVAL) COMPLETE")
    print(f"  Raw records total   : {len(all_rows)}")
    print(f"  Unique (de-duped)   : {n_unique}")
    print(f"  Duplicates flagged  : {n_dup}")
    print(f"\nNext steps:")
    print(f"  1. Run Scopus Boolean S-PRI + S-SUP → export CSV → copy into")
    print(f"     {TEMPLATE_CSV.name}")
    print(f"     (see SLR/docs/draft/search_strings.md for exact queries)")
    print(f"  2. Repeat for IEEE Xplore + WoS")
    print(f"  3. Append manual rows to {OUTPUT_CSV.name}")
    print(f"  4. Proceed to Phase D: python scripts/quality_filter_slr.py")
    print("=" * 70)


if __name__ == "__main__":
    run_retrieval()
