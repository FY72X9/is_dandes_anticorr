"""
enrich_journal_metadata.py
──────────────────────────
Enriches `sjr_quartile` and `core_rank` fields in papers_raw.csv.

Problem: All 1001 records retrieved from OpenAlex have empty sjr_quartile
and core_rank, causing score_journal_quality() to default to 2.0/10.0 for
every paper. This depresses composite quality scores below the 6.0 include
threshold even for high-quality journals like IEEE Access (Q1).

Strategy (3-tier, ordered by reliability):
  1. Hardcoded mapping  — curated ISSN→quartile for known IS/CS journals
  2. OpenAlex source API — 2yr mean citedness heuristic for unknowns
  3. Fallback             — leave as blank (conservative; do not assign Q4)

Safe to run multiple times (idempotent — skips rows that already have values).

Usage:
    python SLR/scripts/enrich_journal_metadata.py
    python SLR/scripts/enrich_journal_metadata.py --dry-run    (preview only)
    python SLR/scripts/enrich_journal_metadata.py --doi-lookup  (slower; does DOI→ISSN lookup)

Output:
    papers_raw.csv updated in-place (backup saved as papers_raw.csv.bak)
"""

import argparse
import logging
import shutil
import sys
import time
from pathlib import Path

import pandas as pd
import requests

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
INPUT_CSV  = SCRIPT_DIR / "papers_raw.csv"
BACKUP_CSV = SCRIPT_DIR / "papers_raw.csv.bak"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s │ %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

REQUEST_TIMEOUT = 20
DELAY_SEC       = 1.0   # polite delay between API calls

# ─────────────────────────────────────────────────────────────────────────────
# Tier-1: Hardcoded ISSN → SJR Quartile mapping
# Source: Scimago Journal Rank (2022/2023 data) + Scopus journal list
# Covers IS, CS, finance, governance, public admin, ML/AI journals
# ─────────────────────────────────────────────────────────────────────────────
ISSN_TO_SJR: dict[str, str] = {
    # ── IEEE journals ────────────────────────────────────────────────────────
    "2169-3536": "Q1",   # IEEE Access
    "0018-9448": "Q1",   # IEEE Transactions on Information Theory
    "1549-8328": "Q1",   # IEEE Transactions on Circuits and Systems
    "1545-5955": "Q1",   # IEEE Transactions on Automation Science
    "1063-6536": "Q1",   # IEEE Transactions on Control Systems Technology
    "2325-5870": "Q1",   # IEEE Transactions on Control of Network Systems
    "1083-4435": "Q1",   # IEEE/ASME Transactions on Mechatronics
    "1941-0476": "Q1",   # IEEE Transactions on Signal and Information Processing
    "2471-285X": "Q1",   # IEEE Transactions on Neural Networks and Learning Systems
    "1556-4967": "Q1",   # IEEE Transactions on Information Forensics and Security
    "1556-6021": "Q1",   # IEEE Transactions on Information Forensics and Security alt
    "0018-9340": "Q1",   # IEEE Transactions on Computers
    "1045-9219": "Q1",   # IEEE Transactions on Parallel and Distributed Systems
    "1089-7801": "Q1",   # IEEE Internet Computing
    "2168-2267": "Q1",   # IEEE Transactions on Cybernetics
    # ── MDPI journals ────────────────────────────────────────────────────────
    "2076-3417": "Q2",   # Applied Sciences
    "2079-9292": "Q2",   # Electronics (MDPI)
    "2504-2289": "Q2",   # Big Data and Cognitive Computing
    "2073-431X": "Q2",   # Computers (MDPI)
    "2227-7390": "Q2",   # Mathematics (MDPI)
    "2079-8954": "Q2",   # Systems (MDPI)
    "2073-8994": "Q2",   # Symmetry (MDPI)
    "2413-4155": "Q2",   # Blockchain: Research and Applications
    "2071-1050": "Q2",   # Sustainability (MDPI)
    "2079-3197": "Q2",   # Computation (MDPI)
    "1999-5903": "Q2",   # Future Internet (MDPI)
    "2305-6290": "Q2",   # Journal of Risk and Financial Management
    "2313-4461": "Q2",   # Economies (MDPI)
    # ── Elsevier journals ────────────────────────────────────────────────────
    "0950-7051": "Q1",   # Knowledge-Based Systems
    "0957-4174": "Q1",   # Expert Systems with Applications
    "0167-4048": "Q1",   # Computers & Security
    "0306-4573": "Q1",   # Information Processing & Management
    "0268-4012": "Q1",   # International Journal of Information Management
    "0378-7206": "Q1",   # Information & Management
    "0306-4379": "Q1",   # Information Systems (Elsevier)
    "0167-9236": "Q1",   # Decision Support Systems
    "0740-817X": "Q1",   # IIE Transactions
    "0925-5273": "Q1",   # International Journal of Production Economics
    "1572-9419": "Q1",   # Electronic Commerce Research and Applications
    "1567-4223": "Q1",   # Electronic Commerce Research and Applications (alt)
    "0747-5632": "Q1",   # Computers in Human Behavior
    "0167-739X": "Q1",   # Future Generation Computer Systems
    "0020-0255": "Q1",   # Information Sciences
    "0957-1787": "Q1",   # Computer Law & Security Review
    "1568-4946": "Q1",   # Applied Soft Computing
    "0952-1976": "Q1",   # Engineering Applications of Artificial Intelligence
    "0925-2312": "Q1",   # Neurocomputing
    "0893-6080": "Q1",   # Neural Networks
    # ── Springer journals ────────────────────────────────────────────────────
    "0269-2821": "Q1",   # Artificial Intelligence Review
    "1382-6905": "Q1",   # Journal of Combinatorial Optimization
    "1573-1413": "Q1",   # Journal of Intelligent Information Systems
    "1469-7688": "Q1",   # Quantitative Finance
    "1613-9372": "Q2",   # Crime Science
    "2363-7501": "Q2",   # Crime Science (alt ISSN)
    # ── Wiley journals ───────────────────────────────────────────────────────
    "1097-0258": "Q1",   # Statistics in Medicine
    "1099-1425": "Q1",   # Journal of Scheduling
    "0012-9682": "Q1",   # Econometrica
    # ── ACM journals ─────────────────────────────────────────────────────────
    "1557-7341": "Q1",   # ACM Transactions on Information Systems
    "1550-4832": "Q1",   # ACM Transactions on Embedded Computing Systems
    "1049-331X": "Q1",   # ACM Transactions on Software Engineering and Methodology
    "1094-9224": "Q1",   # ACM Transactions on Information and System Security
    # ── Taylor & Francis / Routledge ─────────────────────────────────────────
    "1463-5240": "Q1",   # Journal of Financial Crime
    "1472-6718": "Q1",   # Information Technology for Development
    "1097-198X": "Q1",   # Journal of Information Technology
    "0268-1102": "Q1",   # Journal of Strategic Information Systems
    "1350-1917": "Q1",   # European Journal of Information Systems
    "0960-085X": "Q1",   # European Journal of Information Systems alt
    "1476-7279": "Q1",   # Information Technology & People
    "0959-3845": "Q1",   # Information Technology & People alt
    "1464-9535": "Q2",   # Journal of Financial Regulation and Compliance
    # ── IS / MIS premier journals ────────────────────────────────────────────
    "0276-7783": "Q1",   # MIS Quarterly
    "1536-9323": "Q1",   # MIS Quarterly Executive
    "1047-7047": "Q1",   # Information Systems Research
    "1041-4347": "Q1",   # IEEE Transactions on Knowledge and Data Engineering
    "0960-3085": "Q1",   # Computers & Chemical Engineering (Elsevier)
    "1550-1329": "Q1",   # ACM/IEEE Transactions on Networking
    # ── Finance & Accounting ─────────────────────────────────────────────────
    "1057-5219": "Q1",   # International Review of Financial Analysis
    "0378-4266": "Q1",   # Journal of Banking & Finance
    "0304-405X": "Q1",   # Journal of Financial Economics
    "0022-1082": "Q1",   # Journal of Finance
    "0893-9454": "Q1",   # Review of Financial Studies
    "1042-9573": "Q1",   # Journal of Financial Intermediation
    "1573-9031": "Q2",   # Review of Accounting Studies
    "0165-4101": "Q1",   # Journal of Accounting and Economics
    # ── Public Administration / Governance ──────────────────────────────────
    "0033-3352": "Q1",   # Public Administration Review
    "0952-1895": "Q1",   # Governance
    "1749-5679": "Q2",   # Public Administration and Development
    "0027-0490": "Q1",   # Midwest Journal of Political Science / American J of Political Science
    "0003-0554": "Q1",   # American Political Science Review
    "1537-5927": "Q1",   # American Political Science Review (online)
    # ── Cybersecurity / Digital forensics ───────────────────────────────────
    "2093-4327": "Q2",   # Journal of Internet Services and Information Security
    "2692-4188": "Q2",   # IEEE Security & Privacy
    "2372-0204": "Q2",   # IEEE Transactions on Information Forensics (new ISSN)
    # ── Journal of Industrial Information Integration ────────────────────────
    "2452-414X": "Q1",   # Journal of Industrial Information Integration
}

# Journal display-name → SJR quartile (for fuzzy name matching)
NAME_TO_SJR: dict[str, str] = {
    "ieee access": "Q1",
    "electronics": "Q2",
    "applied sciences": "Q2",
    "big data and cognitive computing": "Q2",
    "mathematics": "Q2",
    "sustainability": "Q2",
    "computation": "Q2",
    "future internet": "Q2",
    "economies": "Q2",
    "journal of risk and financial management": "Q3",
    "artificial intelligence review": "Q1",
    "expert systems with applications": "Q1",
    "computers & security": "Q1",
    "knowledge-based systems": "Q1",
    "information sciences": "Q1",
    "information & management": "Q1",
    "information systems": "Q1",
    "decision support systems": "Q1",
    "future generation computer systems": "Q1",
    "neurocomputing": "Q1",
    "neural networks": "Q1",
    "computers in human behavior": "Q1",
    "mis quarterly": "Q1",
    "information systems research": "Q1",
    "journal of information technology": "Q1",
    "european journal of information systems": "Q1",
    "journal of strategic information systems": "Q1",
    "crime science": "Q2",
    "journal of financial crime": "Q2",
    "american political science review": "Q1",
    "journal of industrial information integration": "Q1",
    "applied soft computing": "Q1",
    "engineering applications of artificial intelligence": "Q1",
    # Known Q3/Q4 or unverified (assign conservatively)
    "finance & accounting research journal": "Q3",
    "journal of corporate accounting & finance": "Q3",
}

# Journals that are definitively low-quality / non-indexed (stay unranked)
UNVERIFIED_INDICATORS = [
    "multidisciplinary research", "futuristic development", "universal studies",
    "ijmrge", "asian journal of research", "computer science & it research",
    "islamic business", "edelweiss", "sustainable development", "law and sustainable",
    "dayasaing", "akuntansiku", "jurnal akademi", "eduvest", "dinasti",
]

# ─────────────────────────────────────────────────────────────────────────────
# OpenAlex lookup helpers
# ─────────────────────────────────────────────────────────────────────────────

def _get(url: str, params: dict | None = None) -> dict | None:
    """GET with polite delay and error handling."""
    try:
        resp = requests.get(
            url,
            params={**(params or {}), "mailto": "researcher@binus.ac.id"},
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json()
        log.debug("HTTP %s for %s", resp.status_code, url)
    except Exception as e:
        log.debug("Request error: %s", e)
    return None


def openalex_source_by_issn(issn: str) -> dict | None:
    """Query OpenAlex Sources endpoint by ISSN."""
    if not issn:
        return None
    data = _get(f"https://api.openalex.org/sources/issn:{issn}")
    return data


def openalex_work_by_doi(doi: str) -> dict | None:
    """Query OpenAlex Works endpoint by DOI."""
    if not doi:
        return None
    doi = doi.strip()
    if not doi.startswith("10."):
        return None
    data = _get(f"https://api.openalex.org/works/doi:{doi}",
                params={"select": "primary_location"})
    return data


def get_issn_from_doi(doi: str) -> str | None:
    """Extract source ISSN from OpenAlex via DOI lookup."""
    data = openalex_work_by_doi(doi)
    if not data:
        return None
    try:
        source = data.get("primary_location", {}).get("source", {})
        issn_l = source.get("issn_l") or ""
        return issn_l.replace("-", "").strip() or None
    except Exception:
        return None


def citedness_to_quartile(citedness: float) -> str | None:
    """Map 2-year mean citedness (from OpenAlex) to approximate SJR quartile."""
    if citedness >= 8.0:
        return "Q1"
    if citedness >= 3.0:
        return "Q2"
    if citedness >= 0.5:
        return "Q3"
    return None   # too low to assign confidently


def enrich_from_openalex(issn: str) -> str | None:
    """Query OpenAlex Source by ISSN → infer quartile from citation metrics."""
    if not issn:
        return None
    # Normalise ISSN format (add hyphen if missing)
    issn_fmt = f"{issn[:4]}-{issn[4:]}" if len(issn) == 8 and "-" not in issn else issn
    data = openalex_source_by_issn(issn_fmt)
    if not data:
        return None
    stats = data.get("summary_stats", {})
    citedness = stats.get("2yr_mean_citedness", 0) or 0
    return citedness_to_quartile(float(citedness))


# ─────────────────────────────────────────────────────────────────────────────
# Main enrichment logic
# ─────────────────────────────────────────────────────────────────────────────

def is_unverified(journal_name: str) -> bool:
    """Return True if the journal name matches a known unverified/low-quality pattern."""
    jl = journal_name.lower()
    return any(kw in jl for kw in UNVERIFIED_INDICATORS)


def lookup_journal(journal_name: str, issn: str | None, doi: str | None,
                   do_doi_lookup: bool) -> str | None:
    """
    Resolve SJR quartile for a single paper using tiered strategy.
    Returns quartile string ('Q1'/'Q2'/'Q3'/'Q4') or None.
    """
    # Guard: don't assign quartile to likely-unverified journals
    if is_unverified(journal_name):
        return None

    # Tier 1a: ISSN direct lookup
    if issn:
        issn_clean = issn.replace("-", "").strip()
        for candidate in [issn, issn_clean, f"{issn_clean[:4]}-{issn_clean[4:]}"] if len(issn_clean) == 8 else [issn]:
            if candidate in ISSN_TO_SJR:
                return ISSN_TO_SJR[candidate]
            # Try without hyphen
            key = candidate.replace("-", "")
            for k, v in ISSN_TO_SJR.items():
                if k.replace("-", "") == key:
                    return v

    # Tier 1b: Journal name exact / substring match
    jl = journal_name.lower().strip()
    if not jl:
        return None   # empty journal name — no match
    if jl in NAME_TO_SJR:
        return NAME_TO_SJR[jl]
    # Substring match only when both sides are substantial (≥15 chars) to avoid
    # accidental matches like "computers" matching "computers & security"
    for name_key, q in NAME_TO_SJR.items():
        if len(name_key) >= 15 and len(jl) >= 15:
            if name_key in jl or jl in name_key:
                return q

    # Tier 2: DOI → ISSN → OpenAlex Source (if --doi-lookup enabled)
    if do_doi_lookup and doi:
        time.sleep(DELAY_SEC)
        resolved_issn = get_issn_from_doi(doi)
        if resolved_issn:
            # Re-check Tier 1a with resolved ISSN
            for k, v in ISSN_TO_SJR.items():
                if k.replace("-", "") == resolved_issn.replace("-", ""):
                    return v
            # Query OpenAlex Source by ISSN for citation metrics
            time.sleep(DELAY_SEC)
            q = enrich_from_openalex(resolved_issn)
            if q:
                return q

    return None   # Cannot determine; leave blank


def run(dry_run: bool = False, do_doi_lookup: bool = False) -> None:
    if not INPUT_CSV.exists():
        log.error("Input file not found: %s", INPUT_CSV)
        sys.exit(1)

    log.info("Loading %s ...", INPUT_CSV)
    df = pd.read_csv(INPUT_CSV, dtype=str)
    df = df.where(df.notna(), other="")   # NaN → empty string

    # Identify rows that need enrichment
    needs_sjr = df["sjr_quartile"].str.strip() == ""
    total_need = needs_sjr.sum()
    log.info("Rows needing sjr_quartile enrichment: %d / %d", total_need, len(df))

    if total_need == 0:
        log.info("All rows already have sjr_quartile — nothing to do.")
        return

    updates: dict[int, str] = {}   # index → new sjr_quartile

    for idx, row in df[needs_sjr].iterrows():
        journal = str(row.get("journal", "")).strip()
        issn    = ""          # OpenAlex records don't carry ISSN — resolved via DOI
        doi     = str(row.get("doi", "")).strip()

        q = lookup_journal(journal, issn, doi, do_doi_lookup)
        if q:
            updates[idx] = q
            log.info("  [%d] %-60s → %s", idx, journal[:60], q)
        else:
            log.debug("  [%d] %-60s → (no match)", idx, journal[:60])

    found = len(updates)
    log.info("")
    log.info("Enrichment summary: %d / %d rows resolved.", found, total_need)

    if dry_run:
        log.info("DRY RUN — no files written.")
        return

    if found == 0:
        log.info("No new data to write.")
        return

    # Backup original
    shutil.copy2(INPUT_CSV, BACKUP_CSV)
    log.info("Backup saved to %s", BACKUP_CSV)

    # Apply updates
    for idx, q in updates.items():
        df.at[idx, "sjr_quartile"] = q

    df.to_csv(INPUT_CSV, index=False)
    log.info("Updated papers_raw.csv written (%d rows enriched).", found)
    log.info("")
    log.info("Next step: rerun quality_filter_slr.py — already-downloaded PDFs")
    log.info("will be SKIPPED automatically (skip logic in Stage 3).")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enrich sjr_quartile / core_rank fields in papers_raw.csv"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview enrichment without writing files")
    parser.add_argument("--doi-lookup", action="store_true",
                        help="Enable DOI→ISSN→OpenAlex lookup for unknown journals "
                             "(slower, ~1-2 sec per paper, requires internet)")
    args = parser.parse_args()
    run(dry_run=args.dry_run, do_doi_lookup=args.doi_lookup)
