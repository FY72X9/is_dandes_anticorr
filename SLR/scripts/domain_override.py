"""
domain_override.py — Phase E Stage 0: Apply Domain-Relevance Override to coded_corpus.csv
===========================================================================================
Usage:
    python SLR/scripts/domain_override.py            # dry-run (show what would change)
    python SLR/scripts/domain_override.py --apply    # write changes to coded_corpus.csv

What it does:
    For each paper in coded_corpus.csv where domain_override_candidate == TRUE:
      - Prompts user to confirm override (unless --auto flag used)
      - Sets adjudication_note, irr_resolution, coder1_screen
      - Reports RQ coverage gain

After running --apply:
    Re-run crosscheck_papers.py to regenerate crosscheck_report.md with updated state.
"""

import argparse
import csv
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = ROOT / "SLR" / "scripts" / "output" / "coded_corpus.csv"

# Hardcoded override decisions per DOI
# Format: doi -> (override_code, rq_tags_if_missing)
# These 12 papers were identified by crosscheck_papers.py as HIGH-relevance borderline
OVERRIDES = {
    "10.55214/25768484.v8i5.1969": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.23917/dayasaing.v27i2.12296": ("DOMAIN_OVERRIDE_RQ2", "RQ2"),
    "10.52152/1fvmny20": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.54957/akuntansiku.v5i1.2004": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.54099/ijibmr.v2i1.136": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.32697/integritas.v8i2.940": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.55908/sdgs.v11i12.1930": ("DOMAIN_OVERRIDE_RQ2", "RQ1,RQ2,RQ3"),
    "10.25041/cepalo.v7no1.2814": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.38035/dijefa.v6i6.5934": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.61132/ijema.v2i3.768": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.38035/jafm.v6i3.2109": ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"),
    "10.22399/ijsusat.8": ("DOMAIN_OVERRIDE_RQ1_RQ2", "RQ1"),   # ML methods paper
}


def load_corpus(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_corpus(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Phase E Stage 0 — Domain Override")
    parser.add_argument("--apply", action="store_true",
                        help="Write overrides to coded_corpus.csv (default: dry-run)")
    parser.add_argument("--auto", action="store_true",
                        help="Apply all overrides without per-paper confirmation")
    args = parser.parse_args()

    if not CORPUS_PATH.exists():
        print(f"ERROR: {CORPUS_PATH} not found. Run quality_filter_slr.py first.")
        sys.exit(1)

    rows = load_corpus(CORPUS_PATH)
    fieldnames = list(rows[0].keys())

    candidates = [r for r in rows if str(r.get("domain_override_candidate", "")).strip().upper() == "TRUE"]
    print(f"\n{'='*70}")
    print(f"  Phase E Stage 0 — Domain Override")
    print(f"  Corpus: {CORPUS_PATH.name}  ({len(rows)} total papers)")
    print(f"  Override candidates: {len(candidates)}")
    print(f"  Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"{'='*70}\n")

    applied = 0
    skipped = 0

    for row in rows:
        if str(row.get("domain_override_candidate", "")).strip().upper() != "TRUE":
            continue

        doi = row.get("doi", "").strip()
        title = row.get("title", "")[:70]
        score = row.get("quality_score", "")
        current_note = row.get("adjudication_note", "").strip()
        override_code, rq_fallback = OVERRIDES.get(doi, ("DOMAIN_OVERRIDE_RQ2", "RQ2,RQ3"))

        # Already processed — skip
        if current_note.startswith("DOMAIN_OVERRIDE"):
            print(f"  [SKIP — already applied]  {row['paper_id']}  {title}")
            skipped += 1
            continue

        print(f"\n  [{row['paper_id']}] score={score}  doi={doi}")
        print(f"  Title: {title}")
        print(f"  Journal: {row.get('journal','')}")
        print(f"  RQ tags: {row.get('rq_tags','') or rq_fallback}")
        print(f"  Override code: {override_code}")

        if not args.auto and args.apply:
            answer = input("  Apply override? [Y/n]: ").strip().lower()
            if answer == "n":
                print("  → Skipped by user.")
                skipped += 1
                continue

        if args.apply:
            row["adjudication_note"] = override_code
            row["irr_resolution"] = "DOMAIN_OVERRIDE"
            row["coder1_screen"] = "INCLUDE"
            if not row.get("rq_tags", "").strip():
                row["rq_tags"] = rq_fallback
            print(f"  → Override applied.")
        else:
            print(f"  → [DRY-RUN] Would apply: adjudication_note={override_code}, "
                  f"irr_resolution=DOMAIN_OVERRIDE, coder1_screen=INCLUDE")

        applied += 1

    print(f"\n{'='*70}")
    print(f"  Summary")
    print(f"  Applied  : {applied}")
    print(f"  Skipped  : {skipped}")
    print(f"  Remaining: {len(candidates) - applied - skipped}")

    if args.apply and applied > 0:
        save_corpus(CORPUS_PATH, rows, fieldnames)
        print(f"\n  ✓ Saved: {CORPUS_PATH}")
        print(f"\n  Next step: re-run crosscheck_papers.py to regenerate crosscheck_report.md")
        print(f"  Command  : python SLR/scripts/crosscheck_papers.py")
    elif not args.apply:
        print(f"\n  Run with --apply to write changes.")
        print(f"  Run with --apply --auto to apply all without confirmation.")

    print(f"{'='*70}\n")

    # RQ coverage summary
    if args.apply:
        rows_after = load_corpus(CORPUS_PATH)
        effective_included = [
            r for r in rows_after
            if r.get("pipeline_status") == "INCLUDED"
            or r.get("irr_resolution") == "DOMAIN_OVERRIDE"
        ]
        rq_counts = {"RQ1": 0, "RQ2": 0, "RQ3": 0}
        for r in effective_included:
            tags = r.get("rq_tags", "")
            for rq in ["RQ1", "RQ2", "RQ3"]:
                if rq in tags:
                    rq_counts[rq] += 1
        print(f"  Effective corpus after override: {len(effective_included)} papers")
        print(f"  RQ1 coverage: {rq_counts['RQ1']} papers")
        print(f"  RQ2 coverage: {rq_counts['RQ2']} papers")
        print(f"  RQ3 coverage: {rq_counts['RQ3']} papers")
        print()


if __name__ == "__main__":
    main()
