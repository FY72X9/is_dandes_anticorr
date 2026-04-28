"""
rename_manual_papers.py
-----------------------
Renames manually-downloaded PDFs in SLR/papers/ to match the pipeline naming
convention:  sanitize_filename(title[:60]) + ".pdf"

Run with --dry-run (default) to preview, then without to apply.
"""

import re
import sys
import pathlib

PAPERS_DIR = pathlib.Path(__file__).parent.parent / "papers"


def sanitize(name: str, max_len: int = 80) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:max_len].rstrip("_")


# old_filename → (paper_no, title)  — confirmed matches only
RENAME_MAP = {
    "preprints202310.0571.v1.pdf": (
        29,
        "Machine Learning Analysis of Public Procurement in the Dominican Republic: Impacts on Economic Efficiency and Inclusive Sourcing",
    ),
    "Deep_Learning_in_the_Fast_Lane_A_Survey_on_Advanced_Intrusion_Detection_Systems_for_Intelligent_Vehicle_Networks.pdf": (
        30,
        "Deep Learning in the Fast Lane: A Survey on Advanced Intrusion Detection Systems for Intelligent Vehicle Networks",
    ),
    "risks-12-00206.pdf": (
        31,
        "riskAIchain: AI-Driven IT Infrastructure\u2014Blockchain-Backed Approach for Enhanced Risk Management",
    ),
    "healthcare-11-02257.pdf": (
        32,
        "Towards a Secure Technology-Driven Architecture for Smart Health Insurance Systems: An Empirical Study",
    ),
    "1-s2.0-S1386505624003599-main.pdf": (
        33,
        "Smart data-driven medical decisions through collective and individual anomaly detection in healthcare time series",
    ),
    "20260225125904_MFD-2025-1-047.1.pdf": (
        34,
        "Cloud-Based Knowledge Management Systems with AI-Enhanced Compliance and Data Privacy Safeguards",
    ),
    "jrfm-18-00323.pdf": (
        35,
        "AI and Financial Fraud Prevention: Mapping the Trends and Challenges Through a Bibliometric Lens",
    ),
    "1808-Article Text-3368-1-10-20250214.pdf": (
        36,
        "Exploring the role of Machine Learning and Deep Learning in Anti-Money Laundering (AML) strategies within U.S. Financial Industry: A systematic review of implementation, effectiveness, and challenges",
    ),
    "sensors-25-04720.pdf": (
        37,
        "Intrusion Detection and Real-Time Adaptive Security in Medical IoT Using a Cyber-Physical System Design",
    ),
    "jrfm-18-00502.pdf": (
        38,
        "Tax Fraud Detection Using Artificial Intelligence-Based Technologies: Trends and Implications",
    ),
    "0120131635_MGE-F-23-253.1.pdf": (
        39,
        "An Advanced Machine Learning Model for Detecting Synthetic Identity Fraud in E-Commerce Platforms",
    ),
}

# Papers not yet matched / file not found on disk — reported but not renamed
UNMATCHED = [
    (27, "Securing Government Revenue: A Cloud-Based AI Model for Predictive Detection of Tax-Related Financial Crimes", "10.7753/ijcatr1405.1007"),
    (40, "Blockchain-Enabled Supply Chain platform for Indian Dairy Industry: Safety and Traceability", "10.3390/foods11172716"),
]


def main(dry_run: bool = True) -> None:
    mode = "DRY RUN" if dry_run else "APPLYING RENAMES"
    print(f"\n{'='*60}")
    print(f"  {mode}")
    print(f"  Papers dir: {PAPERS_DIR}")
    print(f"{'='*60}\n")

    renamed = 0
    skipped = 0
    missing = 0
    conflict = 0

    for old_name, (num, title) in RENAME_MAP.items():
        new_name = sanitize(title[:60]) + ".pdf"
        old_path = PAPERS_DIR / old_name
        new_path = PAPERS_DIR / new_name

        if not old_path.exists():
            print(f"[{num}] MISSING — {old_name}")
            missing += 1
            continue

        if old_name == new_name:
            print(f"[{num}] OK (already correct name)")
            skipped += 1
            continue

        if new_path.exists():
            print(f"[{num}] CONFLICT — target already exists, skipping")
            print(f"       target : {new_name}")
            conflict += 1
            continue

        print(f"[{num}] RENAME")
        print(f"  FROM : {old_name}")
        print(f"    TO : {new_name}")

        if not dry_run:
            old_path.rename(new_path)
            print(f"       ✓ Done")

        renamed += 1

    print(f"\n{'─'*60}")
    print(f"  To rename : {renamed}")
    print(f"  Skipped   : {skipped}  (already correct)")
    print(f"  Conflict  : {conflict}")
    print(f"  Missing   : {missing}")

    print(f"\n{'─'*60}")
    print(f"  NOT YET MATCHED ({len(UNMATCHED)} papers — need manual lookup):")
    for num, title, doi in UNMATCHED:
        expected = sanitize(title[:60]) + ".pdf"
        found = (PAPERS_DIR / expected).exists()
        status = "ALREADY ON DISK" if found else "file not found in papers/"
        print(f"  [{num}] {status}")
        print(f"       Expected : {expected}")
        print(f"       DOI      : {doi}")

    if dry_run and renamed > 0:
        print(f"\nRun with --apply to execute the {renamed} rename(s).")
    print()


if __name__ == "__main__":
    dry = "--apply" not in sys.argv
    main(dry_run=dry)
