"""
Rename manually uploaded PDFs to pipeline-canonical filenames,
then update slr_included_corpus.csv and coded_corpus.csv.
"""
import re
import shutil
from pathlib import Path

import pandas as pd

PAPERS_DIR = Path(__file__).parent.parent / "papers"
OUTPUT_DIR = Path(__file__).parent / "output"


def sanitize_filename(name: str, max_len: int = 80) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:max_len].rstrip("_")


# Map DOI -> (current uploaded filename, paper title)
MANUAL_UPLOADS = {
    "10.1016/j.is.2023.102284": (
        "AI-based decision support system for public procurement.pdf",
        "AI-based decision support system for public procurement",
    ),
    "10.7753/ijcatr1405.1007": (
        "Securing Government Revenue_A Cloud-Based AI.pdf",
        "Securing Government Revenue: A Cloud-Based AI Model for Predictive Detection of Tax-Related Financial Crimes",
    ),
    "10.51594/farj.v6i6.1232": (
        "Enhancing_fraud_detection_in_accounting_through_AI.pdf",
        "Enhancing fraud detection in accounting through AI: Techniques and case studies",
    ),
    "10.9734/ajrcos/2024/v17i3424": (
        "AI-Driven Cloud Security-Examining the Impact of User Behavior Analysis on T...pdf",
        "AI-Driven Cloud Security: Examining the Impact of User Behavior Analysis on Threat Detection",
    ),
    "10.51594/csitrj.v5i2.759": (
        "EVOLVING_TAX_COMPLIANCE_IN_THE_DIGITAL_ERA_A_COMPA.pdf",
        "EVOLVING TAX COMPLIANCE IN THE DIGITAL ERA: A COMPARATIVE ANALYSIS OF AI-DRIVEN MODELS AND BLOCKCHAIN TECHNOLOGY IN U.S. TAX ADMINISTRATION",
    ),
}

# ── 1. Show plan ─────────────────────────────────────────────────────────────
print("=" * 72)
print("RENAME PLAN")
print("=" * 72)
renames: list[tuple[str, str, str]] = []   # (doi, old_name, new_name)
for doi, (current, title) in MANUAL_UPLOADS.items():
    canonical = sanitize_filename(title) + ".pdf"
    renames.append((doi, current, canonical))
    match = "✅ SAME" if current == canonical else "🔁 RENAME"
    print(f"{match}  {current!r}")
    if current != canonical:
        print(f"      →  {canonical!r}")
print()

# ── 2. Confirm existence of source files ─────────────────────────────────────
print("FILE CHECK")
print("-" * 72)
for doi, old, new in renames:
    # Try exact name first; fall back to glob for truncated names
    src = PAPERS_DIR / old
    if not src.exists():
        # The filename may be truncated in directory listing; try glob on stem
        stem = old.replace(".pdf", "")[:40]
        matches = list(PAPERS_DIR.glob(f"{stem}*.pdf"))
        if matches:
            src = matches[0]
            print(f"  ⚠  Resolved truncated name: {src.name!r}")
        else:
            print(f"  ❌  NOT FOUND on disk: {old!r}")
            continue
    dst = PAPERS_DIR / new
    if dst.exists() and dst != src:
        print(f"  ⚠  Target already exists, skipping: {new!r}")
    elif dst == src:
        print(f"  ✅ Already canonical: {new!r}")
    else:
        print(f"  ✅ Will rename: {src.name!r} → {new!r}")
print()

# ── 3. Execute renames ────────────────────────────────────────────────────────
print("EXECUTING RENAMES")
print("-" * 72)
renamed: dict[str, str] = {}   # doi -> canonical filename
for doi, old, new in renames:
    src = PAPERS_DIR / old
    if not src.exists():
        stem = old.replace(".pdf", "")[:40]
        matches = list(PAPERS_DIR.glob(f"{stem}*.pdf"))
        if matches:
            src = matches[0]
        else:
            print(f"  ❌  SKIP (not found): {old!r}")
            continue
    dst = PAPERS_DIR / new
    if dst == src:
        print(f"  ✅ Already canonical: {new!r}")
        renamed[doi] = new
    elif dst.exists():
        print(f"  ⚠  Target exists, skipping: {new!r}")
        renamed[doi] = new
    else:
        src.rename(dst)
        print(f"  🔁 Renamed → {new!r}")
        renamed[doi] = new
print()

# ── 4. Update slr_included_corpus.csv ────────────────────────────────────────
included_path = OUTPUT_DIR / "slr_included_corpus.csv"
df_inc = pd.read_csv(included_path)
updated = 0
for doi, canon_fn in renamed.items():
    mask = df_inc["doi"] == doi
    df_inc.loc[mask, "pdf_filename"] = canon_fn
    df_inc.loc[mask, "acquisition_status"] = "MANUAL_UPLOAD"
    updated += mask.sum()
df_inc.to_csv(included_path, index=False)
print(f"slr_included_corpus.csv  → updated {updated} rows")

# ── 5. Update coded_corpus.csv ───────────────────────────────────────────────
coded_path = OUTPUT_DIR / "coded_corpus.csv"
df_cod = pd.read_csv(coded_path)
updated_c = 0
for doi, canon_fn in renamed.items():
    mask = df_cod["doi"] == doi
    df_cod.loc[mask, "pdf_filename"] = canon_fn
    df_cod.loc[mask, "acquisition_status"] = "MANUAL_UPLOAD"
    updated_c += mask.sum()
df_cod.to_csv(coded_path, index=False)
print(f"coded_corpus.csv         → updated {updated_c} rows")

print()
print("DONE. Summary:")
for doi, canon_fn in renamed.items():
    print(f"  {doi}  →  {canon_fn}")
