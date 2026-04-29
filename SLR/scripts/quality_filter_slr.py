"""
quality_filter_slr.py — SLR Quality Filter + Acquisition Pipeline
==================================================================
Implements the 3-stage pipeline described in:
  concept/conceptual/research_concept_slr.md — Section 5

  Stage 1 │ Inclusion/Exclusion filter (IC-01–IC-06, EC-01–EC-06)
  Stage 2 │ Weighted quality scoring (0–10 composite, 5 dimensions)
  Stage 3 │ Cascading OA acquisition (no API key required for first 5):
             OpenAlex → Unpaywall → MDPI-Direct → CrossRef → arXiv
             → Semantic Scholar → CORE (optional key) → DirectURL

Usage
-----
    python quality_filter_slr.py                          # default: scripts/papers_raw.csv
    python quality_filter_slr.py path/to/papers_raw.csv  # custom input

Input CSV columns (see Section 5.3 of research_concept_slr.md):
    doi, title, year, journal, sjr_quartile, core_rank,
    citations, source_db, oa_url, abstract, is_duplicate, language

Output files (written to scripts/output/):
    slr_included_corpus.csv   — final included set with quality scores
    slr_borderline.csv        — 4.0–5.9 range; human adjudication required
    slr_excluded_log.csv      — excluded papers with reason code
    manual_download_log.txt   — included/borderline; no OA version found
    PDFs saved to:  papers/ (sibling of scripts/)

Requirements
------------
    pip install requests pandas tqdm
"""

from __future__ import annotations

import re
import os
import sys
import time
import json
import logging
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv

# Load .env from repo root (two levels up from this script: SLR/scripts/ → root)
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
ROOT_DIR     = SCRIPT_DIR.parent           # SLR/
OUTPUT_DIR   = SCRIPT_DIR / "output"
PDF_DIR      = ROOT_DIR / "papers"
DEFAULT_INPUT = SCRIPT_DIR / "papers_raw.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
YEAR_MIN         = 2010
YEAR_MAX         = 2026
SCORE_INCLUDE    = 5.5    # ≥ this → included corpus
SCORE_BORDER     = 4.0    # ≥ this → borderline review; < this → excluded
MIN_PDF_BYTES    = 8_000
REQUEST_TIMEOUT  = 30     # seconds
DELAY_SEC        = 1.5    # polite delay between API calls

# Unpaywall requires an email for ToS compliance
UNPAYWALL_EMAIL  = "researcher@binus.ac.id"

# Optional API keys — loaded from .env (see .env.example at repo root)
# CORE API key: free signup at https://core.ac.uk/services/api
CORE_API_KEY     = os.getenv("CORE_API_KEY", "")
# Semantic Scholar API key: free at https://www.semanticscholar.org/product/api
S2_API_KEY       = os.getenv("S2_API_KEY", "")

# Predatory journal indicators (lightweight keyword list; extend as needed)
PREDATORY_KEYWORDS = [
    "omics international", "omicsonline", "sciforschenonline",
    "scirp.org", "ijset", "wseas", "waset", "academicjournals",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,*/*;q=0.9",
}

# Rotate log file so each run appends a fresh session separator
_LOG_FILE = OUTPUT_DIR / "pipeline.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(_LOG_FILE, mode="a", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)
# Keep console at INFO; file gets full DEBUG detail
logging.getLogger().handlers[0].setLevel(logging.INFO)
logging.getLogger().handlers[1].setLevel(logging.DEBUG)


# ─────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────────────────────

def safe_str(val) -> str:
    """Convert any value to stripped lowercase string; treat NaN as empty."""
    if pd.isna(val):
        return ""
    return str(val).strip().lower()


def safe_int(val, default: int = 0) -> int:
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Make a string safe for use as a filename."""
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:max_len].rstrip("_")


def normalise_arxiv_url(url: str) -> str:
    """Convert arXiv /abs/ links to direct /pdf/ links."""
    if "arxiv.org/abs/" in url:
        url = url.replace("arxiv.org/abs/", "arxiv.org/pdf/")
        if not url.endswith(".pdf"):
            url += ".pdf"
    return url


def is_valid_pdf(path: Path) -> bool:
    """Check PDF magic bytes."""
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"%PDF"
    except Exception:
        return False


def is_doi(val: str) -> bool:
    """Loose DOI format check."""
    return bool(re.match(r"10\.\d{4,}/", val.strip()))


# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 — Inclusion / Exclusion filters
# ─────────────────────────────────────────────────────────────────────────────

INDEXED_SOURCES = {
    "scopus", "ieee", "wos", "openalex", "semantic scholar",
    "acm", "springer", "elsevier", "wiley", "emerald",
}

PRIVATE_SECTOR_KEYWORDS = [
    "credit card", "bank fraud", "insurance fraud", "healthcare fraud",
    "corporate fraud", "stock market", "equity market",
]

COMPUTATIONAL_KEYWORDS = [
    "machine learning", "deep learning", "neural network", "random forest",
    "isolation forest", "anomaly detection", "fraud detection", "clustering",
    "classification", "regression", "rule-based", "decision tree", "svm",
    "logistic regression", "ensemble", "autoencoder", "lof", "dbscan",
    "statistical", "algorithm", "model", "detection", "prediction",
]


def ic01_indexed_outlet(row: pd.Series) -> tuple[bool, str]:
    """IC-01: Peer-reviewed, Scopus/ISI/IEEE-indexed outlet."""
    source = safe_str(row.get("source_db", ""))
    journal = safe_str(row.get("journal", ""))
    # Accept if the source_db matches known indexed databases
    for db in INDEXED_SOURCES:
        if db in source or db in journal:
            return True, ""
    # Accept if sjr_quartile or core_rank is present (implies indexed venue)
    if safe_str(row.get("sjr_quartile", "")) or safe_str(row.get("core_rank", "")):
        return True, ""
    return False, "IC-01: Source not identifiably Scopus/ISI/IEEE indexed"


def ic02_year_range(row: pd.Series) -> tuple[bool, str]:
    """IC-02: Publication year 2010–2026."""
    year = safe_int(row.get("year", 0))
    if YEAR_MIN <= year <= YEAR_MAX:
        return True, ""
    if year < YEAR_MIN:
        return False, f"IC-02: Year {year} < {YEAR_MIN} (use as anchor only)"
    return False, f"IC-02: Year {year} > {YEAR_MAX}"


def ic03_topic_relevance(row: pd.Series) -> tuple[bool, str]:
    """IC-03: Addresses financial anomaly/fraud/corruption detection."""
    text = safe_str(row.get("title", "")) + " " + safe_str(row.get("abstract", ""))
    keywords = [
        "anomaly", "fraud", "corruption", "irregularity", "misconduct",
        "embezzlement", "misappropriation", "fictitious", "mark-up",
        "procurement", "audit", "financial crime", "public expenditure",
        "village fund", "dana desa", "government spending",
    ]
    for kw in keywords:
        if kw in text:
            return True, ""
    return False, "IC-03: No relevant topic keyword in title/abstract"


def ic04_computational_method(row: pd.Series) -> tuple[bool, str]:
    """IC-04: Applies a computational method to financial data."""
    text = safe_str(row.get("title", "")) + " " + safe_str(row.get("abstract", ""))
    for kw in COMPUTATIONAL_KEYWORDS:
        if kw in text:
            return True, ""
    return False, "IC-04: No computational method keyword found"


def ic05_text_available(row: pd.Series) -> tuple[bool, str]:
    """IC-05: Full text or abstract available."""
    abstract = safe_str(row.get("abstract", ""))
    oa_url = safe_str(row.get("oa_url", ""))
    doi = safe_str(row.get("doi", ""))
    if len(abstract) > 50 or oa_url or doi:
        return True, ""
    return False, "IC-05: No abstract, OA URL, or DOI available"


def ic06_language(row: pd.Series) -> tuple[bool, str]:
    """IC-06: English, OR Bahasa Indonesia with English abstract present."""
    lang = safe_str(row.get("language", "en"))
    abstract = safe_str(row.get("abstract", ""))
    if not lang or lang in ("en", "english", "eng"):
        return True, ""
    if lang in ("id", "indonesian", "bahasa", "bahasa indonesia"):
        # Accept if abstract is in English (heuristic: mostly ASCII)
        ascii_ratio = sum(c.isascii() for c in abstract) / max(len(abstract), 1)
        if len(abstract) > 50 and ascii_ratio > 0.90:
            return True, ""
        return False, "IC-06: Bahasa Indonesia paper without sufficient English abstract"
    return False, f"IC-06: Unsupported language '{lang}'"


def ec01_private_sector_only(row: pd.Series) -> tuple[bool, str]:
    """EC-01: Focuses exclusively on private-sector fraud (no public sector)."""
    text = safe_str(row.get("title", "")) + " " + safe_str(row.get("abstract", ""))
    has_private = any(kw in text for kw in PRIVATE_SECTOR_KEYWORDS)
    if not has_private:
        return False, ""
    # Exclude only if NO public sector signal present
    public_signals = [
        "government", "public sector", "village", "municipal", "procurement",
        "dana desa", "state", "ministry", "regional", "audit board",
    ]
    if any(s in text for s in public_signals):
        return False, ""
    return True, "EC-01: Private-sector only; no public sector element"


def ec02_legal_no_computation(row: pd.Series) -> tuple[bool, str]:
    """EC-02: Legal/forensic analysis without computational method."""
    text = safe_str(row.get("title", "")) + " " + safe_str(row.get("abstract", ""))
    legal_signals = ["legal analysis", "juridical", "court decision", "sentencing"]
    if not any(s in text for s in legal_signals):
        return False, ""
    if any(kw in text for kw in COMPUTATIONAL_KEYWORDS):
        return False, ""
    return True, "EC-02: Legal/forensic analysis; no computational method"


def ec03_non_indexed_conference(row: pd.Series) -> tuple[bool, str]:
    """EC-03: Conference proceedings from non-indexed venues."""
    source = safe_str(row.get("source_db", ""))
    journal = safe_str(row.get("journal", ""))
    sjr = safe_str(row.get("sjr_quartile", ""))
    core = safe_str(row.get("core_rank", ""))
    # If it has a quartile or CORE rank, it's indexed
    if sjr or core:
        return False, ""
    # If source_db is a known indexed database, it passes
    for db in INDEXED_SOURCES:
        if db in source:
            return False, ""
    # Flag as potentially non-indexed conference only if clearly a conference
    if "conference" in journal or "proceedings" in journal or "workshop" in journal:
        return True, "EC-03: Conference proceedings from apparently non-indexed venue"
    return False, ""


def ec04_duplicate(row: pd.Series) -> tuple[bool, str]:
    """EC-04: Duplicate records."""
    if str(row.get("is_duplicate", "")).strip().lower() in ("true", "1", "yes"):
        return True, "EC-04: Duplicate record"
    return False, ""


def ec05_purely_theoretical(row: pd.Series) -> tuple[bool, str]:
    """EC-05: Purely theoretical; no empirical validation or case application."""
    text = safe_str(row.get("title", "")) + " " + safe_str(row.get("abstract", ""))
    empirical_signals = [
        "experiment", "case study", "dataset", "evaluation", "result",
        "accuracy", "precision", "recall", "f1", "auc", "performance",
        "implementation", "prototype", "proposed", "validation", "deployed",
        "applied", "empirical",
    ]
    if any(s in text for s in empirical_signals):
        return False, ""
    theoretical_signals = [
        "propose a framework", "theoretical framework", "conceptual model",
        "literature review", "position paper",
    ]
    if any(s in text for s in theoretical_signals):
        return True, "EC-05: Purely theoretical; no empirical outcome reported"
    return False, ""


def ec06_predatory(row: pd.Series) -> tuple[bool, str]:
    """EC-06: Predatory journal (Beall's List / Cabells indicators)."""
    journal = safe_str(row.get("journal", ""))
    oa_url = safe_str(row.get("oa_url", ""))
    combined = journal + " " + oa_url
    for kw in PREDATORY_KEYWORDS:
        if kw in combined:
            return True, f"EC-06: Predatory journal indicator found ('{kw}')"
    return False, ""


# Ordered filter chains
INCLUSION_FILTERS = [ic01_indexed_outlet, ic02_year_range, ic03_topic_relevance,
                     ic04_computational_method, ic05_text_available, ic06_language]
EXCLUSION_FILTERS = [ec01_private_sector_only, ec02_legal_no_computation,
                     ec03_non_indexed_conference, ec04_duplicate,
                     ec05_purely_theoretical, ec06_predatory]


def apply_stage1_filters(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Apply IC and EC filters to every row.

    Returns
    -------
    candidates  : rows that passed all checks
    excluded    : rows that failed, with 'exclusion_reason' column appended
    """
    passed, failed = [], []
    for _, row in df.iterrows():
        # Check exclusion first (faster rejection)
        excluded = False
        for fn in EXCLUSION_FILTERS:
            triggered, reason = fn(row)
            if triggered:
                row = row.copy()
                row["exclusion_reason"] = reason
                failed.append(row)
                excluded = True
                break
        if excluded:
            continue
        # Check inclusion criteria
        failed_ic = None
        for fn in INCLUSION_FILTERS:
            passes, reason = fn(row)
            if not passes:
                failed_ic = reason
                break
        if failed_ic:
            row = row.copy()
            row["exclusion_reason"] = failed_ic
            failed.append(row)
        else:
            passed.append(row)

    return (
        pd.DataFrame(passed).reset_index(drop=True) if passed else pd.DataFrame(),
        pd.DataFrame(failed).reset_index(drop=True) if failed else pd.DataFrame(),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 — Quality Scoring
# ─────────────────────────────────────────────────────────────────────────────

SJR_SCORE = {"q1": 10, "q2": 7, "q3": 5, "q4": 3}
CORE_SCORE = {"a*": 10, "a": 7, "b": 5, "c": 2}

WEIGHTS = {
    "journal_quality":      0.25,
    "methodological_rigor": 0.25,
    "relevance_to_rq":      0.20,
    "recency":              0.15,
    "citation_impact":      0.15,
}


def score_journal_quality(row: pd.Series) -> float:
    sjr = safe_str(row.get("sjr_quartile", ""))
    core = safe_str(row.get("core_rank", ""))
    if sjr:
        return float(SJR_SCORE.get(sjr.lower(), 3))
    if core:
        for key, val in CORE_SCORE.items():
            if core.lower().startswith(key):
                return float(val)
    return 2.0  # unranked


def score_methodological_rigor(row: pd.Series) -> float:
    text = safe_str(row.get("abstract", ""))
    has_validation = any(
        kw in text for kw in [
            "validation", "validated", "cross-validation", "ground truth",
            "expert validation", "precision", "recall", "f1", "auc",
        ]
    )
    is_reproducible = any(
        kw in text for kw in [
            "open source", "github", "replicat", "code available",
            "dataset available", "reproducib",
        ]
    )
    if has_validation and is_reproducible:
        return 10.0
    if has_validation:
        return 7.0
    return 3.0


def score_relevance_to_rq(row: pd.Series) -> float:
    """
    RQ coverage:
      RQ1 = detection method + IS theory
      RQ2 = corruption typology operationalization / feature engineering
      RQ3 = gaps / applicability / developing country / village level
    """
    text = safe_str(row.get("title", "")) + " " + safe_str(row.get("abstract", ""))
    rq1 = any(kw in text for kw in [
        "machine learning", "anomaly detection", "fraud detection",
        "information system", "design science",
    ])
    rq2 = any(kw in text for kw in [
        "feature engineering", "typolog", "modus operandi", "corruption pattern",
        "mark-up", "fictitious", "procurement irregularit",
    ])
    rq3 = any(kw in text for kw in [
        "developing countr", "village", "sub-national", "decentralized",
        "dana desa", "scalab", "real-time", "label scarci",
    ])
    coverage = sum([rq1, rq2, rq3])
    if coverage == 3:
        return 10.0
    if coverage == 2:
        return 7.0
    if coverage == 1:
        return 4.0
    return 1.0


def score_recency(row: pd.Series) -> float:
    year = safe_int(row.get("year", 0))
    if 2022 <= year <= 2026:
        return 10.0
    if 2018 <= year <= 2021:
        return 7.0
    if 2014 <= year <= 2017:
        return 5.0
    return 3.0


def score_citation_impact(row: pd.Series, citation_quartile_thresholds: dict) -> float:
    """
    Year-normalized citation scoring using pre-computed quartile thresholds.
    citation_quartile_thresholds: {year: (q3_val, q2_val, q1_val)}
    If thresholds not available for year, fall back to raw tertile within corpus.
    """
    year = safe_int(row.get("year", 0))
    cites = safe_int(row.get("citations", 0))
    thresholds = citation_quartile_thresholds.get(year)
    if thresholds:
        q3, q2, q1 = thresholds
        if cites >= q1:
            return 10.0
        if cites >= q2:
            return 7.0
        return 4.0
    # Fallback: raw count heuristics
    if cites >= 100:
        return 10.0
    if cites >= 30:
        return 7.0
    return 4.0


def compute_citation_quartiles(df: pd.DataFrame) -> dict:
    """
    Compute year-stratified citation quartile thresholds from candidate corpus.
    Returns {year: (q1_threshold, q2_threshold, q3_threshold)}.
    """
    thresholds = {}
    for year, group in df.groupby("year"):
        cites = group["citations"].apply(lambda x: safe_int(x)).values
        if len(cites) >= 4:
            import numpy as np
            thresholds[int(year)] = (
                float(np.percentile(cites, 25)),   # q3 boundary (lower)
                float(np.percentile(cites, 50)),   # q2 boundary
                float(np.percentile(cites, 75)),   # q1 boundary (upper)
            )
    return thresholds


def compute_quality_scores(candidates: pd.DataFrame) -> pd.DataFrame:
    """Apply composite quality scoring to candidate corpus."""
    if candidates.empty:
        return candidates

    citation_quartiles = compute_citation_quartiles(candidates)
    rows = []
    for _, row in candidates.iterrows():
        sub = {
            "journal_quality":      score_journal_quality(row),
            "methodological_rigor": score_methodological_rigor(row),
            "relevance_to_rq":      score_relevance_to_rq(row),
            "recency":              score_recency(row),
            "citation_impact":      score_citation_impact(row, citation_quartiles),
        }
        composite = sum(sub[k] * WEIGHTS[k] for k in sub)
        row = row.copy()
        for k, v in sub.items():
            row[f"score_{k}"] = round(v, 2)
        row["quality_score"] = round(composite, 3)
        rows.append(row)

    return pd.DataFrame(rows).reset_index(drop=True)


def split_by_threshold(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split into included / borderline / excluded based on quality score."""
    included   = scored[scored["quality_score"] >= SCORE_INCLUDE].copy()
    borderline = scored[(scored["quality_score"] >= SCORE_BORDER) & (scored["quality_score"] < SCORE_INCLUDE)].copy()
    excluded   = scored[scored["quality_score"] < SCORE_BORDER].copy()
    excluded["exclusion_reason"] = "Stage 2: Quality score below threshold (" + excluded["quality_score"].astype(str) + " < " + str(SCORE_BORDER) + ")"
    return included, borderline, excluded


# ─────────────────────────────────────────────────────────────────────────────
# Stage 3 — OA Acquisition
# ─────────────────────────────────────────────────────────────────────────────

def _download_pdf(url: str, dest: Path) -> tuple[bool, str]:
    """
    Download and validate a PDF from a URL.
    Returns (success, message).
    """
    url = normalise_arxiv_url(url)
    try:
        head = requests.head(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        ct = head.headers.get("Content-Type", "")
        if head.status_code in (403, 405):
            pass  # Server blocks HEAD (e.g. MDPI); proceed to GET
        elif head.status_code >= 400:
            return False, f"HEAD {head.status_code}"
        elif "html" in ct.lower() and not (url.lower().endswith(".pdf") or url.lower().endswith("/pdf")):
            return False, "Content-Type HTML — likely landing page"
    except Exception:
        pass  # Proceed to GET if HEAD unsupported

    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, stream=True)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.HTTPError as e:
        dest.unlink(missing_ok=True)
        return False, f"HTTP {e.response.status_code}"
    except requests.ConnectionError:
        dest.unlink(missing_ok=True)
        return False, "Connection error"
    except requests.Timeout:
        dest.unlink(missing_ok=True)
        return False, f"Timeout after {REQUEST_TIMEOUT}s"
    except Exception as e:
        dest.unlink(missing_ok=True)
        return False, f"Error: {e}"

    if not is_valid_pdf(dest):
        size = dest.stat().st_size
        dest.unlink(missing_ok=True)
        return False, f"Not a valid PDF ({size} bytes)"
    if dest.stat().st_size < MIN_PDF_BYTES:
        size = dest.stat().st_size
        dest.unlink(missing_ok=True)
        return False, f"Too small ({size} bytes)"

    size_kb = dest.stat().st_size / 1024
    return True, f"OK ({size_kb:.1f} KB)"


def acquire_openalex(doi: str) -> Optional[str]:
    """Query OpenAlex for OA PDF URL by DOI."""
    if not doi or not is_doi(doi):
        return None
    url = f"https://api.openalex.org/works/doi:{doi}"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT,
                            params={"select": "open_access"})
        log.debug(f"    [OpenAlex] HTTP {resp.status_code} for doi:{doi}")
        if resp.status_code == 200:
            data = resp.json()
            oa = data.get("open_access", {})
            pdf = oa.get("oa_url") or oa.get("landing_page_url")
            if pdf and pdf.startswith("http"):
                log.debug(f"    [OpenAlex] Found URL: {pdf[:80]}")
                return pdf
            log.debug("    [OpenAlex] No OA URL in response")
        else:
            log.debug(f"    [OpenAlex] Non-200 response: {resp.status_code}")
    except Exception as exc:
        log.debug(f"    [OpenAlex] Exception: {exc}")
    return None


def acquire_unpaywall(doi: str) -> Optional[str]:
    """Query Unpaywall API for best OA PDF URL."""
    if not doi or not is_doi(doi):
        return None
    url = f"https://api.unpaywall.org/v2/{doi}"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT,
                            params={"email": UNPAYWALL_EMAIL})
        log.debug(f"    [Unpaywall] HTTP {resp.status_code} for doi:{doi}")
        if resp.status_code == 200:
            data = resp.json()
            best = data.get("best_oa_location") or {}
            pdf = best.get("url_for_pdf") or best.get("url")
            if pdf and pdf.startswith("http"):
                log.debug(f"    [Unpaywall] Found URL: {pdf[:80]}")
                return pdf
            log.debug("    [Unpaywall] No OA location in response")
        else:
            log.debug(f"    [Unpaywall] Non-200 response: {resp.status_code}")
    except Exception as exc:
        log.debug(f"    [Unpaywall] Exception: {exc}")
    return None


def acquire_semantic_scholar(doi: str) -> Optional[str]:
    """Query Semantic Scholar Graph API for openAccessPdf."""
    if not doi or not is_doi(doi):
        return None
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    headers = {"x-api-key": S2_API_KEY} if S2_API_KEY else {}
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT,
                            params={"fields": "openAccessPdf"},
                            headers=headers)
        log.debug(f"    [S2] HTTP {resp.status_code} for doi:{doi}")
        if resp.status_code == 200:
            data = resp.json()
            pdf_info = data.get("openAccessPdf") or {}
            pdf = pdf_info.get("url")
            if pdf and pdf.startswith("http"):
                log.debug(f"    [S2] Found URL: {pdf[:80]}")
                return pdf
            log.debug("    [S2] No openAccessPdf in response")
        elif resp.status_code == 429:
            log.debug("    [S2] 429 rate-limited (no API key set)")
        else:
            log.debug(f"    [S2] Non-200 response: {resp.status_code}")
    except Exception as exc:
        log.debug(f"    [S2] Exception: {exc}")
    return None


def acquire_mdpi(doi: str) -> Optional[str]:
    """Construct direct PDF URL for MDPI journals (DOI prefix 10.3390/).

    MDPI is a fully open-access publisher; all articles are freely available
    at https://www.mdpi.com/{doi}/pdf  — no API key required.
    """
    if not doi or not doi.strip().startswith("10.3390/"):
        return None
    pdf_url = f"https://www.mdpi.com/{doi.strip()}/pdf"
    log.debug(f"    [MDPI] Constructed URL: {pdf_url}")
    return pdf_url


def acquire_crossref(doi: str) -> Optional[str]:
    """Query CrossRef Works API for an open-access PDF link.

    CrossRef stores publisher-supplied PDF links in the 'link' array.
    No API key required — uses the polite pool with a mailto User-Agent.
    """
    if not doi or not is_doi(doi):
        return None
    url = f"https://api.crossref.org/works/{doi}"
    headers = {
        "User-Agent": f"SLR-pipeline/1.0 (mailto:{UNPAYWALL_EMAIL})"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        log.debug(f"    [CrossRef] HTTP {resp.status_code} for doi:{doi}")
        if resp.status_code == 200:
            links = resp.json().get("message", {}).get("link", [])
            # Prefer explicit PDF content-type first
            for link in links:
                if link.get("content-type") == "application/pdf":
                    pdf = link.get("URL", "")
                    if pdf.startswith("http"):
                        log.debug(f"    [CrossRef] Found PDF link: {pdf[:80]}")
                        return pdf
            # Fallback: any link whose URL looks like a PDF
            for link in links:
                pdf = link.get("URL", "")
                if pdf.startswith("http") and pdf.lower().endswith(".pdf"):
                    log.debug(f"    [CrossRef] Found .pdf link: {pdf[:80]}")
                    return pdf
            log.debug(f"    [CrossRef] {len(links)} links but no PDF found")
        else:
            log.debug(f"    [CrossRef] Non-200 response: {resp.status_code}")
    except Exception as exc:
        log.debug(f"    [CrossRef] Exception: {exc}")
    return None


def acquire_arxiv(doi: str, title: str = "") -> Optional[str]:
    """Search arXiv for a preprint version of the paper.

    Tries DOI-based arXiv search first, then falls back to title search.
    No API key required. Returns direct PDF URL (abs → pdf redirect).
    """
    def _pdf_from_entry(entry: ET.Element, ns: dict) -> Optional[str]:
        for link in entry.findall("atom:link", ns):
            if link.get("type") == "application/pdf":
                href = link.get("href", "")
                if href.startswith("http"):
                    return href
        # Fallback: construct from <id>
        id_el = entry.find("atom:id", ns)
        if id_el is not None and id_el.text:
            arxiv_id = id_el.text.strip()
            # Convert abs URL to PDF URL
            pdf = arxiv_id.replace("/abs/", "/pdf/")
            if not pdf.endswith(".pdf"):
                pdf += ".pdf"
            return pdf
        return None

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    api_url = "https://export.arxiv.org/api/query"

    # Tier A: search by DOI field
    if doi and is_doi(doi):
        try:
            resp = requests.get(
                api_url,
                params={"search_query": f"all:{doi}", "start": 0, "max_results": 3},
                timeout=REQUEST_TIMEOUT,
            )
            log.debug(f"    [arXiv-DOI] HTTP {resp.status_code} query={doi}")
            if resp.status_code == 200:
                root = ET.fromstring(resp.text)
                for entry in root.findall("atom:entry", ns):
                    pdf = _pdf_from_entry(entry, ns)
                    if pdf:
                        log.debug(f"    [arXiv-DOI] Found: {pdf[:80]}")
                        return pdf
                log.debug("    [arXiv-DOI] No matching entries")
        except Exception as exc:
            log.debug(f"    [arXiv-DOI] Exception: {exc}")

    # Tier B: title search
    if title and title.strip():
        query = title.strip()[:100]
        try:
            resp = requests.get(
                api_url,
                params={"search_query": f'ti:"{query}"', "start": 0, "max_results": 3},
                timeout=REQUEST_TIMEOUT,
            )
            log.debug(f"    [arXiv-Title] HTTP {resp.status_code} query='{query[:50]}'")
            if resp.status_code == 200:
                root = ET.fromstring(resp.text)
                for entry in root.findall("atom:entry", ns):
                    pdf = _pdf_from_entry(entry, ns)
                    if pdf:
                        log.debug(f"    [arXiv-Title] Found: {pdf[:80]}")
                        return pdf
                log.debug("    [arXiv-Title] No matching entries")
        except Exception as exc:
            log.debug(f"    [arXiv-Title] Exception: {exc}")

    return None


def acquire_ieee(doi: str) -> Optional[str]:
    """Attempt direct PDF download for IEEE Open Access papers.

    Resolves the DOI redirect to obtain the correct IEEE Xplore article number
    (the DOI suffix is NOT the article number), then tries stamp.jsp.
    Only attempted for 10.1109/* DOIs.
    """
    if not doi or not is_doi(doi):
        return None
    if not doi.lower().startswith("10.1109/"):
        return None
    # Step 1: Resolve DOI to get actual IEEE Xplore article number
    try:
        r = requests.get(
            f"https://doi.org/{doi}",
            headers={"User-Agent": HEADERS["User-Agent"]},
            allow_redirects=True,
            timeout=REQUEST_TIMEOUT,
        )
        import re as _re
        m = _re.search(r'/document/(\d+)', r.url)
        if not m:
            log.debug(f"    [IEEE] Could not extract article # from: {r.url}")
            return None
        arnumber = m.group(1)
    except Exception as exc:
        log.debug(f"    [IEEE] DOI resolution failed: {exc}")
        return None
    # Step 2: Try stamp.jsp (requires browser session — will fail without cookie)
    stamp_url = f"https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber={arnumber}"
    log.debug(f"    [IEEE] stamp URL: {stamp_url}")
    return stamp_url


def acquire_core(doi: str, title: str = "") -> Optional[str]:
    """Query CORE API v3 for direct PDF download URL.

    Falls back to title search when DOI lookup yields no PDF.
    Requires CORE_API_KEY (free at core.ac.uk/services/api).
    Without a key the function is skipped to avoid 401 errors.
    """
    if not CORE_API_KEY:
        return None
    auth_headers = {"Authorization": f"Bearer {CORE_API_KEY}"}

    # --- Tier A: exact DOI lookup ---
    if doi and is_doi(doi):
        try:
            resp = requests.get(
                f"https://api.core.ac.uk/v3/works/doi/{doi}",
                headers=auth_headers,
                timeout=REQUEST_TIMEOUT,
            )
            log.debug(f"    [CORE-DOI] HTTP {resp.status_code} for doi:{doi}")
            if resp.status_code == 200:
                pdf = resp.json().get("downloadUrl")
                if pdf and pdf.startswith("http"):
                    log.debug(f"    [CORE-DOI] Found URL: {pdf[:80]}")
                    return pdf
                log.debug("    [CORE-DOI] No downloadUrl in response")
            else:
                log.debug(f"    [CORE-DOI] Non-200 response: {resp.status_code}")
        except Exception as exc:
            log.debug(f"    [CORE-DOI] Exception: {exc}")

    # --- Tier B: title-based search (when DOI fails or is missing) ---
    if title and title.strip():
        query = title.strip()[:120]  # keep query concise
        try:
            resp = requests.get(
                "https://api.core.ac.uk/v3/search/works",
                headers=auth_headers,
                params={"q": f'title:"{query}"', "limit": 3},
                timeout=REQUEST_TIMEOUT,
            )
            log.debug(f"    [CORE-Title] HTTP {resp.status_code} query='{query[:50]}'")
            if resp.status_code == 200:
                hits = resp.json().get("results", [])
                for hit in hits:
                    pdf = hit.get("downloadUrl")
                    if pdf and pdf.startswith("http"):
                        log.debug(f"    [CORE-Title] Found URL: {pdf[:80]}")
                        return pdf
                log.debug(f"    [CORE-Title] {len(hits)} hits but none with downloadUrl")
            else:
                log.debug(f"    [CORE-Title] Non-200 response: {resp.status_code}")
        except Exception as exc:
            log.debug(f"    [CORE-Title] Exception: {exc}")

    return None


def acquire_paper(row: pd.Series, pdf_dir: Path) -> tuple[bool, str, str]:
    """
    Attempt OA acquisition via cascading sources.

    Returns (success, pdf_filename_or_empty, reason_if_failed).
    """
    doi   = safe_str(row.get("doi", "")).strip()
    title = str(row.get("title", "unknown"))[:60]
    slug  = sanitize_filename(title)
    dest  = pdf_dir / f"{slug}.pdf"

    # Skip if already downloaded and valid
    if dest.exists() and is_valid_pdf(dest) and dest.stat().st_size >= MIN_PDF_BYTES:
        return True, dest.name, "Already exists"

    sources = [
        ("OpenAlex",       lambda: acquire_openalex(doi)),
        ("Unpaywall",      lambda: acquire_unpaywall(doi)),
        ("MDPI",           lambda: acquire_mdpi(doi)),
        ("CrossRef",       lambda: acquire_crossref(doi)),
        ("arXiv",          lambda: acquire_arxiv(doi, title)),
        ("IEEE",           lambda: acquire_ieee(doi)),
        ("SemanticScholar",lambda: acquire_semantic_scholar(doi)),
        ("CORE",           lambda: acquire_core(doi, title)),
        ("DirectURL",      lambda: safe_str(row.get("oa_url", "")) or None),
    ]

    log.debug(f"  Trying acquisition for: {title[:60]}")
    for source_name, url_fn in sources:
        time.sleep(DELAY_SEC)
        try:
            pdf_url = url_fn()
        except Exception as exc:
            log.debug(f"    [{source_name}] url_fn raised: {exc}")
            pdf_url = None
        if not pdf_url:
            log.debug(f"    [{source_name}] No URL returned — skipping")
            continue
        pdf_url = normalise_arxiv_url(pdf_url)
        log.debug(f"    [{source_name}] Attempting download: {pdf_url[:80]}")
        success, msg = _download_pdf(pdf_url, dest)
        if success:
            log.info(f"  ✓ [{source_name}] {title[:50]} — {msg}")
            return True, dest.name, f"Downloaded via {source_name}"
        log.debug(f"    [{source_name}] Download failed: {msg}")

    always_tried = "OpenAlex, Unpaywall, MDPI, CrossRef, arXiv, IEEE, SemanticScholar"
    opt_tried = (", CORE" if CORE_API_KEY else "") + ", DirectURL"
    return False, "", f"No open-access version found (tried {always_tried}{opt_tried})"


# ─────────────────────────────────────────────────────────────────────────────
# Main pipeline orchestration
# ─────────────────────────────────────────────────────────────────────────────

# Per-source success counter (module-level so acquire_paper can update it)
_SOURCE_COUNTS: dict[str, int] = {}


def run_pipeline(input_path: Path) -> None:
    global _SOURCE_COUNTS
    _SOURCE_COUNTS = {}
    log.info("\n" + "=" * 70)
    log.info(f"{'SLR Quality Filter + Acquisition Pipeline':^70}")
    log.info("=" * 70)
    log.info(f"Input  : {input_path}")
    log.info(f"Output : {OUTPUT_DIR}")
    log.info(f"PDFs   : {PDF_DIR}")
    log.info(f"Log    : {_LOG_FILE}")
    log.info("Free sources  : OpenAlex, Unpaywall, MDPI-Direct, CrossRef, arXiv, IEEE (always active)")
    log.info(f"CORE API  : {'✓ configured' if CORE_API_KEY else '✗ not set (skip CORE tier)'}")
    log.info(f"S2 API    : {'✓ configured' if S2_API_KEY else '✗ not set (may hit 429)'}")
    log.info("=" * 70)

    # ── Load input ──────────────────────────────────────────────────────────
    if not input_path.exists():
        log.error(f"Input file not found: {input_path}")
        log.error("Please create papers_raw.csv first (Phase C — Retrieval).")
        sys.exit(1)

    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    log.info(f"Loaded {len(df)} records from {input_path.name}")

    # Normalize column names to lowercase
    df.columns = [c.strip().lower() for c in df.columns]

    # ── Stage 1: Filter ─────────────────────────────────────────────────────
    log.info("\n── Stage 1: Inclusion / Exclusion Filtering ──")
    candidates, s1_excluded = apply_stage1_filters(df)
    log.info(f"  Passed : {len(candidates)}")
    log.info(f"  Excluded (Stage 1) : {len(s1_excluded)}")

    # ── Stage 2: Quality scoring ────────────────────────────────────────────
    log.info("\n── Stage 2: Quality Scoring ──")
    if candidates.empty:
        log.warning("No candidates remain after Stage 1. Exiting.")
        s1_excluded.to_csv(OUTPUT_DIR / "slr_excluded_log.csv", index=False, encoding="utf-8")
        return

    scored = compute_quality_scores(candidates)
    included, borderline, s2_excluded = split_by_threshold(scored)
    log.info(f"  Included (≥{SCORE_INCLUDE})  : {len(included)}")
    log.info(f"  Borderline ({SCORE_BORDER}–{SCORE_INCLUDE - 0.1:.1f}) : {len(borderline)}")
    log.info(f"  Excluded (<{SCORE_BORDER})   : {len(s2_excluded)}")

    # Merge all excluded records
    all_excluded = pd.concat([s1_excluded, s2_excluded], ignore_index=True)

    # ── Stage 3: Acquire PDFs ───────────────────────────────────────────────
    log.info("\n── Stage 3: OA Acquisition ──")
    acquire_targets = pd.concat([included, borderline], ignore_index=True)
    manual_list: list[dict] = []
    pdf_results: dict[int, str] = {}

    for idx, row in tqdm(acquire_targets.iterrows(), total=len(acquire_targets), desc="Acquiring"):
        success, fname, reason = acquire_paper(row, PDF_DIR)
        acquire_targets.at[idx, "pdf_filename"] = fname
        acquire_targets.at[idx, "acquisition_status"] = reason
        pdf_results[idx] = fname
        # Track per-source success
        if success and reason != "Already exists":
            src = reason.replace("Downloaded via ", "")
            _SOURCE_COUNTS[src] = _SOURCE_COUNTS.get(src, 0) + 1
        elif reason == "Already exists":
            _SOURCE_COUNTS["Already exists"] = _SOURCE_COUNTS.get("Already exists", 0) + 1
        if not success:
            manual_list.append({
                "title":  str(row.get("title", "")),
                "doi":    str(row.get("doi", "")),
                "reason": reason,
                "score":  str(row.get("quality_score", "")),
            })

    # Split acquire_targets back into included / borderline with acquisition info
    included_final  = acquire_targets[acquire_targets["quality_score"].astype(float) >= SCORE_INCLUDE].copy()
    borderline_final = acquire_targets[acquire_targets["quality_score"].astype(float) < SCORE_INCLUDE].copy()

    # ── Write outputs ───────────────────────────────────────────────────────
    log.info("\n── Writing Outputs ──")

    included_final.to_csv(OUTPUT_DIR / "slr_included_corpus.csv", index=False, encoding="utf-8")
    log.info(f"  ✓ slr_included_corpus.csv  ({len(included_final)} papers)")

    borderline_final.to_csv(OUTPUT_DIR / "slr_borderline.csv", index=False, encoding="utf-8")
    log.info(f"  ✓ slr_borderline.csv       ({len(borderline_final)} papers)")

    all_excluded.to_csv(OUTPUT_DIR / "slr_excluded_log.csv", index=False, encoding="utf-8")
    log.info(f"  ✓ slr_excluded_log.csv     ({len(all_excluded)} papers)")

    manual_path = OUTPUT_DIR / "manual_download_log.txt"
    with open(manual_path, "w", encoding="utf-8") as f:
        f.write("# Manual Download Required\n")
        f.write("# These papers passed quality filtering but have no open-access version.\n")
        f.write("# Download manually and place in: papers/\n\n")
        for i, entry in enumerate(manual_list, 1):
            score_label = f" [score={entry['score']}]" if entry['score'] else ""
            f.write(f"[{i}]{score_label} {entry['title']}\n")
            if entry['doi']:
                f.write(f"    DOI       : {entry['doi']}\n")
                f.write(f"    Publisher : https://doi.org/{entry['doi']}\n")
            f.write(f"    Reason    : {entry['reason']}\n\n")
    log.info(f"  ✓ manual_download_log.txt  ({len(manual_list)} papers need manual download)")

    # ── Summary ─────────────────────────────────────────────────────────────
    downloaded = sum(1 for e in manual_list if "Already" in e.get("reason", ""))
    total_acquire = len(acquire_targets)
    auto_success = total_acquire - len(manual_list)

    log.info("\n" + "=" * 70)
    log.info("PIPELINE COMPLETE")
    log.info(f"  Total input records     : {len(df)}")
    log.info(f"  Passed Stage 1 filter   : {len(candidates)}")
    log.info(f"  Included corpus (≥{SCORE_INCLUDE})  : {len(included_final)}")
    log.info(f"  Borderline pool         : {len(borderline_final)}")
    log.info(f"  Excluded (all stages)   : {len(all_excluded)}")
    log.info(f"  Auto-downloaded PDFs    : {auto_success}")
    log.info(f"  Require manual download : {len(manual_list)}")
    log.info("─" * 70)
    log.info("  Acquisition breakdown by source:")
    for src, cnt in sorted(_SOURCE_COUNTS.items(), key=lambda x: -x[1]):
        log.info(f"    {src:<20} : {cnt}")
    log.info("=" * 70)

    if len(included_final) < 40:
        log.warning(f"Corpus size {len(included_final)} < 40 target minimum.")
        log.warning("Consider: broadening search strings or lowering threshold to 5.5 (sensitivity lower bound).")
    elif len(included_final) > 80:
        log.warning(f"Corpus size {len(included_final)} > 80 target maximum.")
        log.warning("Consider: narrowing EC criteria or raising threshold to 6.5 (sensitivity upper bound).")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SLR Quality Filter + OA Acquisition Pipeline"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=str(DEFAULT_INPUT),
        help="Path to papers_raw.csv (default: scripts/papers_raw.csv)",
    )
    args = parser.parse_args()
    run_pipeline(Path(args.input))
