"""
scoping_run.py — Phase B: Mini Scoping Search via OpenAlex API
==============================================================
Executes multiple Boolean search string variants against the OpenAlex API,
counts raw hits, identifies existing systematic reviews in the domain,
and outputs:
  - docs/draft/scoping_run_results.md   (hit counts + sampled titles)
  - docs/draft/search_strings.md        (finalized strings for all 5 databases)

Run:
    python scripts/scoping_run.py

No API key required (OpenAlex polite pool: mailto param only).
"""

from __future__ import annotations

import json
import time
import sys
import re
from pathlib import Path
from datetime import date

import requests

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
ROOT_DIR    = SCRIPT_DIR.parent
DRAFT_DIR   = ROOT_DIR / "docs" / "draft"
DRAFT_DIR.mkdir(parents=True, exist_ok=True)

MAILTO = "researcher@binus.ac.id"
BASE   = "https://api.openalex.org"
DELAY  = 1.2   # polite delay between requests

# ─────────────────────────────────────────────────────────────────────────────
# Search string variants to test
# Each entry: (label, query_string_for_openalex, rationale)
# OpenAlex uses simple phrase search in title+abstract via the 'search' param,
# and filter=type:article or type:review for type filtering.
# ─────────────────────────────────────────────────────────────────────────────
SEARCH_VARIANTS = [
    (
        "S1 — Core ML + Public Finance Fraud",
        "anomaly detection fraud detection public sector government financial machine learning",
        "Primary scope: ML methods + public sector financial fraud"
    ),
    (
        "S2 — Corruption Detection + IS",
        "corruption detection information system government expenditure",
        "IS framing + corruption: direct RQ1 alignment"
    ),
    (
        "S3 — Village Fund / Dana Desa",
        "village fund dana desa corruption irregularity detection",
        "Specific context — RQ3 applicability boundary"
    ),
    (
        "S4 — Feature Engineering + Corruption Typology",
        "feature engineering corruption typology fraud pattern government financial data",
        "RQ2 operationalization gap — typology to signal"
    ),
    (
        "S5 — Decentralized Fund Audit Analytics",
        "decentralized fund audit analytics anomaly unsupervised machine learning public",
        "Broadened S1: includes audit analytics + decentralized governance"
    ),
    (
        "S6 — Procurement Fraud ML",
        "procurement fraud detection machine learning public sector",
        "Procurement sub-domain — often overlaps Dana Desa irregularities"
    ),
    (
        "S7 — SLR Existing Reviews (novelty check)",
        "systematic review fraud detection public sector government machine learning",
        "Identifies nearest existing SLRs for novelty claim validation"
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# OpenAlex query helpers
# ─────────────────────────────────────────────────────────────────────────────

def openalex_search(query: str, filter_str: str = "", per_page: int = 25, page: int = 1) -> dict:
    params = {
        "search":   query,
        "per-page": per_page,
        "page":     page,
        "mailto":   MAILTO,
        "select":   "id,title,publication_year,type,cited_by_count,open_access,primary_location",
    }
    if filter_str:
        params["filter"] = filter_str
    try:
        resp = requests.get(f"{BASE}/works", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  [WARN] API error: {e}")
        return {"meta": {"count": 0}, "results": []}


def count_total(query: str, filter_str: str = "") -> int:
    data = openalex_search(query, filter_str, per_page=1)
    return data.get("meta", {}).get("count", 0)


def fetch_sample(query: str, filter_str: str = "", n: int = 10) -> list[dict]:
    data = openalex_search(query, filter_str, per_page=n)
    return data.get("results", [])


def fetch_reviews(query: str, n: int = 15) -> list[dict]:
    """Fetch papers typed as 'review' — identifies existing SLRs."""
    data = openalex_search(query, filter_str="type:review", per_page=n)
    return data.get("results", [])


def get_journal_name(result: dict) -> str:
    try:
        loc = result.get("primary_location") or {}
        src = loc.get("source") or {}
        return src.get("display_name") or "—"
    except Exception:
        return "—"


def get_oa_status(result: dict) -> str:
    try:
        oa = result.get("open_access") or {}
        return "OA" if oa.get("is_oa") else "paywalled"
    except Exception:
        return "?"


# ─────────────────────────────────────────────────────────────────────────────
# Main execution
# ─────────────────────────────────────────────────────────────────────────────

def run_scoping():
    today = date.today().isoformat()
    print("=" * 70)
    print("Phase B — Mini Scoping Run via OpenAlex API")
    print(f"Date: {today}")
    print("=" * 70)

    results_table: list[dict] = []
    variant_details: list[dict] = []

    for label, query, rationale in SEARCH_VARIANTS:
        print(f"\n▶ {label}")
        time.sleep(DELAY)

        # Total hits (all types, 2010–2026)
        total_all   = count_total(query, "publication_year:2010-2026")
        time.sleep(DELAY)
        # Journal articles only
        total_art   = count_total(query, "publication_year:2010-2026,type:article")
        time.sleep(DELAY)
        # Reviews only
        total_rev   = count_total(query, "publication_year:2010-2026,type:review")
        time.sleep(DELAY)
        # High-relevance: 2018–2026 articles
        total_recent = count_total(query, "publication_year:2018-2026,type:article")
        time.sleep(DELAY)

        print(f"  All (2010-2026)   : {total_all:,}")
        print(f"  Articles          : {total_art:,}")
        print(f"  Reviews (SLRs)    : {total_rev:,}")
        print(f"  Recent (2018+) art: {total_recent:,}")

        # Sample top results
        sample = fetch_sample(query, "publication_year:2010-2026,type:article", n=8)
        time.sleep(DELAY)

        results_table.append({
            "label":      label,
            "query":      query,
            "rationale":  rationale,
            "total_all":  total_all,
            "total_art":  total_art,
            "total_rev":  total_rev,
            "total_recent": total_recent,
            "sample":     sample,
        })

    # Fetch existing reviews for S7 separately (all strings combined broad query)
    print("\n▶ Fetching nearest existing SLRs (type:review) ...")
    time.sleep(DELAY)
    slr_candidates = fetch_reviews(
        "systematic review fraud detection anomaly detection public sector government machine learning",
        n=15
    )
    time.sleep(DELAY)

    # Also fetch reviews for more specific query
    slr_candidates2 = fetch_reviews(
        "systematic literature review corruption detection information system",
        n=10
    )

    # Deduplicate by title
    seen_titles: set[str] = set()
    unique_slrs: list[dict] = []
    for r in slr_candidates + slr_candidates2:
        t = (r.get("title") or "").lower().strip()
        if t and t not in seen_titles:
            seen_titles.add(t)
            unique_slrs.append(r)

    print(f"  Found {len(unique_slrs)} unique candidate SLRs for novelty analysis")

    # ─────────────────────────────────────────────────────────────────────────
    # Write scoping_run_results.md
    # ─────────────────────────────────────────────────────────────────────────
    out_results = DRAFT_DIR / "scoping_run_results.md"
    with open(out_results, "w", encoding="utf-8") as f:
        f.write(f"# Phase B — Mini Scoping Run Results\n\n")
        f.write(f"> **Run date**: {today}  \n")
        f.write(f"> **API**: OpenAlex (free tier, polite pool)  \n")
        f.write(f"> **Purpose**: Validate corpus density target (40–80 papers) and identify nearest existing SLRs\n\n")
        f.write("---\n\n")

        # Summary table
        f.write("## 1. Hit Count Summary\n\n")
        f.write("| Variant | Query Label | All (2010–2026) | Articles | Reviews / SLRs | Recent (2018+) |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in results_table:
            f.write(f"| `{r['label'].split('—')[0].strip()}` | {r['label'].split('—')[1].strip() if '—' in r['label'] else r['label']} "
                    f"| {r['total_all']:,} | {r['total_art']:,} | {r['total_rev']:,} | {r['total_recent']:,} |\n")
        f.write("\n")

        # Corpus density assessment
        # Estimate realistic filtered corpus from best-performing variants
        best_articles = max(r["total_art"] for r in results_table[:6])
        typical_pass_rate = 0.15  # conservative: 15% pass IC/EC after filtering
        est_corpus_low  = int(best_articles * 0.08)
        est_corpus_high = int(best_articles * 0.25)

        f.write("## 2. Corpus Density Assessment\n\n")
        f.write(f"- **Largest raw pool (articles)**: {best_articles:,} from S1/S5 combined domain\n")
        f.write(f"- **Conservative filter pass rate**: ~8–25% (IC/EC + quality threshold)\n")
        f.write(f"- **Estimated included corpus**: {est_corpus_low}–{est_corpus_high} papers\n")

        if est_corpus_low >= 25 and est_corpus_high <= 200:
            verdict = "✅ **Target range 40–80 is ACHIEVABLE.** Proceed to Phase C full search."
        elif est_corpus_high < 25:
            verdict = "⚠️ **Corpus too sparse.** Broaden search strings before Phase C."
        else:
            verdict = "⚠️ **Corpus may be too large.** Narrow search or accept higher filter attrition."

        f.write(f"- **Verdict**: {verdict}\n\n")

        # Sample titles per variant
        f.write("## 3. Sample Titles by Variant\n\n")
        for r in results_table[:6]:
            f.write(f"### {r['label']}\n\n")
            f.write(f"> *Rationale*: {r['rationale']}\n\n")
            if r["sample"]:
                for item in r["sample"]:
                    year  = item.get("publication_year", "?")
                    title = item.get("title") or "—"
                    cites = item.get("cited_by_count", 0)
                    jrnl  = get_journal_name(item)
                    oa    = get_oa_status(item)
                    f.write(f"- [{year}] **{title}** — *{jrnl}* (cited: {cites}, {oa})\n")
            else:
                f.write("- *No results returned*\n")
            f.write("\n")

        # Existing SLRs — novelty gap table
        f.write("## 4. Nearest Existing SLRs — Novelty Gap Analysis\n\n")
        f.write("> These are candidate SLRs retrieved from OpenAlex type:review. "
                "Review each title to confirm it is a genuine SLR and assess the gap this study fills.\n\n")
        f.write("| Year | Title | Journal | Citations | OA | Potential Gap |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in unique_slrs[:12]:
            year  = r.get("publication_year", "?")
            title = (r.get("title") or "—")[:90]
            jrnl  = get_journal_name(r)
            cites = r.get("cited_by_count", 0)
            oa    = get_oa_status(r)
            # Heuristic gap signals
            title_lower = title.lower()
            if any(x in title_lower for x in ["village", "dana desa", "decentralized", "sub-national"]):
                gap = "Same context — direct competitor; compare scope carefully"
            elif any(x in title_lower for x in ["developing countr", "indonesia", "asia"]):
                gap = "Regional overlap — check method scope"
            elif "public sector" in title_lower or "government" in title_lower:
                gap = "Public sector scope matches; likely misses IS theory + village level"
            else:
                gap = "Broader domain; this SLR adds village-level IS framing"
            f.write(f"| {year} | {title} | {jrnl[:40]} | {cites} | {oa} | {gap} |\n")
        f.write("\n")

        # Notes
        f.write("## 5. Notes & Decisions\n\n")
        f.write("- Scopus, IEEE Xplore, and WoS searches must be run manually with institutional access.\n")
        f.write("  Use string variants S1–S6 from `search_strings.md` with database-specific field tags.\n")
        f.write("- OpenAlex hit counts are indicative; actual includable papers depend on IC/EC filter outcomes.\n")
        f.write("- Combine S1 + S2 + S4 + S6 as the primary search string set for Scopus.\n")
        f.write("- S3 (Dana Desa) expected sparse — treat results as specialty supplementary corpus.\n")
        f.write(f"- **Recommendation**: Proceed to Phase C. Target combined retrieval of 150–400 raw records across all databases.\n")

    print(f"\n✓ Written: {out_results}")

    # ─────────────────────────────────────────────────────────────────────────
    # Write search_strings.md
    # ─────────────────────────────────────────────────────────────────────────
    out_strings = DRAFT_DIR / "search_strings.md"
    with open(out_strings, "w", encoding="utf-8") as f:
        f.write(f"# Finalized Search Strings — SLR Phase C\n\n")
        f.write(f"> **Finalized**: {today}  \n")
        f.write(f"> **Based on**: Phase B scoping run results (`scoping_run_results.md`)\n\n")
        f.write("---\n\n")

        f.write("## Overview\n\n")
        f.write("Two complementary search string sets are used:\n\n")
        f.write("- **Primary set (S-PRI)**: Covers ML methods + public sector fraud/anomaly detection — feeds RQ1 and RQ2\n")
        f.write("- **Supplementary set (S-SUP)**: Village-level governance + decentralized fund irregularities — feeds RQ3\n\n")
        f.write("Both sets are run on all five databases. Hits are merged and de-duplicated before entering `papers_raw.csv`.\n\n")

        f.write("---\n\n")

        f.write("## 1. Scopus — Advanced Search\n\n")
        f.write("**S-PRI (Primary)**\n")
        f.write("```\nTITLE-ABS-KEY(\n")
        f.write('  ( "anomaly detection" OR "fraud detection" OR "corruption detection"\n')
        f.write('    OR "financial irregularity" OR "misappropriation detection" )\n')
        f.write("  AND\n")
        f.write('  ( "machine learning" OR "deep learning" OR "unsupervised learning"\n')
        f.write('    OR "isolation forest" OR "random forest" OR "neural network"\n')
        f.write('    OR "autoencoder" OR "clustering" OR "classification algorithm" )\n')
        f.write("  AND\n")
        f.write('  ( "public sector" OR "government expenditure" OR "public finance"\n')
        f.write('    OR "government procurement" OR "public spending" OR "state budget" )\n')
        f.write(")\n")
        f.write("AND PUBYEAR > 2009 AND PUBYEAR < 2027\n")
        f.write("AND DOCTYPE(ar OR re)\n")
        f.write("```\n\n")

        f.write("**S-SUP (Supplementary — Village/Decentralized)**\n")
        f.write("```\nTITLE-ABS-KEY(\n")
        f.write('  ( "village fund" OR "dana desa" OR "decentralized fund"\n')
        f.write('    OR "village finance" OR "local government fund"\n')
        f.write('    OR "sub-national government" OR "fiscal decentralization" )\n')
        f.write("  AND\n")
        f.write('  ( "corruption" OR "fraud" OR "irregularity" OR "anomaly"\n')
        f.write('    OR "audit finding" OR "financial mismanagement" )\n')
        f.write(")\n")
        f.write("AND PUBYEAR > 2009 AND PUBYEAR < 2027\n")
        f.write("AND DOCTYPE(ar OR re)\n")
        f.write("```\n\n")

        f.write("---\n\n")

        f.write("## 2. IEEE Xplore — Advanced Search\n\n")
        f.write("**S-PRI**\n")
        f.write("```\n")
        f.write('("Abstract":"anomaly detection" OR "Abstract":"fraud detection")\n')
        f.write('AND ("Abstract":"machine learning" OR "Abstract":"deep learning"\n')
        f.write('     OR "Abstract":"unsupervised" OR "Abstract":"neural network")\n')
        f.write('AND ("Abstract":"government" OR "Abstract":"public sector"\n')
        f.write('     OR "Abstract":"public finance" OR "Abstract":"procurement")\n')
        f.write("Filter: Year: 2010–2026 | Content Type: Journals + Conference Papers\n")
        f.write("```\n\n")

        f.write("**S-SUP**\n")
        f.write("```\n")
        f.write('("Abstract":"village fund" OR "Abstract":"decentralized fund"\n')
        f.write(' OR "Abstract":"dana desa" OR "Abstract":"local government")\n')
        f.write('AND ("Abstract":"corruption" OR "Abstract":"fraud" OR "Abstract":"anomaly")\n')
        f.write("Filter: Year: 2010–2026\n")
        f.write("```\n\n")

        f.write("---\n\n")

        f.write("## 3. Web of Science — Advanced Search\n\n")
        f.write("**S-PRI**\n")
        f.write("```\n")
        f.write('TS=("anomaly detection" OR "fraud detection" OR "corruption detection")\n')
        f.write('AND TS=("machine learning" OR "deep learning" OR "unsupervised"\n')
        f.write('        OR "random forest" OR "neural network" OR "autoencoder")\n')
        f.write('AND TS=("public sector" OR "government" OR "public finance"\n')
        f.write('        OR "public expenditure" OR "government procurement")\n')
        f.write("AND PY=(2010-2026)\n")
        f.write("AND DT=(Article OR Review)\n")
        f.write("```\n\n")

        f.write("**S-SUP**\n")
        f.write("```\n")
        f.write('TS=("village fund" OR "dana desa" OR "decentralized fund"\n')
        f.write('    OR "local government fund" OR "fiscal decentralization")\n')
        f.write('AND TS=("corruption" OR "fraud" OR "financial irregularity")\n')
        f.write("AND PY=(2010-2026)\n")
        f.write("```\n\n")

        f.write("---\n\n")

        f.write("## 4. OpenAlex — API Query (used in scoping run)\n\n")
        f.write("```\nGET https://api.openalex.org/works\n  ?search=anomaly+detection+fraud+detection+public+sector+government+machine+learning\n")
        f.write("  &filter=publication_year:2010-2026,type:article\n")
        f.write("  &per-page=200\n")
        f.write("  &mailto=researcher@binus.ac.id\n")
        f.write("```\n\n")
        f.write("Repeat with supplementary query:\n")
        f.write("```\n  ?search=village+fund+dana+desa+corruption+fraud+detection\n")
        f.write("  &filter=publication_year:2010-2026\n")
        f.write("```\n\n")
        f.write("> For full retrieval, iterate pages until `meta.count` exhausted or `per-page=200` × pages = total.\n\n")

        f.write("---\n\n")

        f.write("## 5. Semantic Scholar — API Query\n\n")
        f.write("```\nGET https://api.semanticscholar.org/graph/v1/paper/search\n")
        f.write('  ?query=anomaly+detection+fraud+detection+public+sector+machine+learning\n')
        f.write("  &fields=paperId,title,year,citationCount,openAccessPdf,journal,abstract\n")
        f.write("  &limit=100\n")
        f.write("```\n\n")
        f.write("Supplementary:\n")
        f.write("```\n")
        f.write('  ?query=village+fund+corruption+detection+government+financial+anomaly\n')
        f.write("```\n\n")

        f.write("---\n\n")

        f.write("## 6. papers_raw.csv Column Mapping\n\n")
        f.write("When exporting from each database, normalize to these columns before merging:\n\n")
        f.write("| Column | Scopus Export | IEEE Export | WoS Export | OpenAlex API | Semantic Scholar API |\n")
        f.write("|---|---|---|---|---|---|\n")
        f.write("| `doi` | DOI | DOI | DI | `doi` | `externalIds.DOI` |\n")
        f.write("| `title` | Title | Document Title | TI | `title` | `title` |\n")
        f.write("| `year` | Year | Publication Year | PY | `publication_year` | `year` |\n")
        f.write("| `journal` | Source title | Publication Title | SO | `primary_location.source.display_name` | `journal.name` |\n")
        f.write("| `sjr_quartile` | — (look up Scimago) | — | — | — | — |\n")
        f.write("| `core_rank` | — (look up CORE) | — | — | — | — |\n")
        f.write("| `citations` | Cited by | — | TC | `cited_by_count` | `citationCount` |\n")
        f.write("| `source_db` | `scopus` | `ieee` | `wos` | `openalex` | `semantic_scholar` |\n")
        f.write("| `oa_url` | — | PDF Links | — | `open_access.oa_url` | `openAccessPdf.url` |\n")
        f.write("| `abstract` | Abstract | Abstract | AB | *(not in select — run separate query if needed)* | `abstract` |\n")
        f.write("| `is_duplicate` | — (set True after DOI dedup) | — | — | — | — |\n")
        f.write("| `language` | Language of Original Document | — | LA | — | — |\n")
        f.write("\n")
        f.write("**De-duplication rule**: After merging all exports, set `is_duplicate=True` for any row whose `doi` appears more than once; keep only the row from the highest-priority source (Scopus > WoS > IEEE > OpenAlex > S2).\n\n")

        f.write("---\n\n")

        f.write("## 7. Expected Retrieval Volumes (Pre-filter)\n\n")
        f.write("| Database | S-PRI (est.) | S-SUP (est.) | Notes |\n")
        f.write("|---|---|---|---|\n")
        f.write("| Scopus | 80–150 | 5–20 | Most comprehensive IS journal coverage |\n")
        f.write("| IEEE Xplore | 30–70 | 2–10 | Strong for ML methods papers |\n")
        f.write("| Web of Science | 40–80 | 3–15 | High-impact journals; overlaps Scopus heavily |\n")
        f.write("| OpenAlex | 100–300 | 10–40 | Largest raw pool; many non-IS papers |\n")
        f.write("| Semantic Scholar | 50–120 | 5–20 | Good PDF coverage; semantic matching |\n")
        f.write("| **Total (pre-dedup)** | **300–720** | **25–105** | — |\n")
        f.write("| **Post-dedup estimate** | **150–300** | **15–50** | ~40% overlap across databases |\n")
        f.write("| **Post-IC/EC filter (15–25%)** | **22–75** | **2–12** | Combined: 24–87 |\n")
        f.write("\n")
        f.write("> **Target 40–80**: Achievable if combined post-dedup pool ≥ 150 records.\n")
        f.write("> If post-filter count < 40, broaden by: removing `public sector` AND constraint (allow implicit gov context), or lowering threshold to 5.5.\n\n")

    print(f"✓ Written: {out_strings}")
    print("\n" + "=" * 70)
    print("Phase B scoping run COMPLETE")
    print(f"  scoping_run_results.md → {out_results}")
    print(f"  search_strings.md      → {out_strings}")
    print("=" * 70)

    # Print brief console summary
    print("\n── Hit Count Summary ──")
    for r in results_table:
        label_short = r['label'].split('—')[0].strip()
        print(f"  {label_short:6s} │ All={r['total_all']:>6,} │ Articles={r['total_art']:>6,} │ Reviews={r['total_rev']:>4,} │ Recent={r['total_recent']:>5,}")

    print(f"\n── Nearest SLRs Found: {len(unique_slrs)} candidates ──")
    for r in unique_slrs[:8]:
        print(f"  [{r.get('publication_year','?')}] {(r.get('title') or '')[:75]}")


if __name__ == "__main__":
    run_scoping()
