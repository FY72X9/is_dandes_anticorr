"""
Phase F1 — PDF Text Extraction
Extracts full text from all 45 INCLUDE corpus PDFs using pymupdf (fitz).
Writes per-paper .md files to SLR/analysis/extracted/
Logs extraction quality to SLR/analysis/extraction_quality_log.csv

For the 5 papers with no PDF, writes abstract-only .md files from coded_corpus.csv.
"""

import os
import re
import csv
import pandas as pd
import fitz  # pymupdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS_DIR = os.path.join(BASE_DIR, "papers")
CORPUS_CSV = os.path.join(BASE_DIR, "scripts", "output", "coded_corpus.csv")
OUT_DIR = os.path.join(BASE_DIR, "analysis", "extracted")
LOG_CSV = os.path.join(BASE_DIR, "analysis", "extraction_quality_log.csv")

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CORPUS_CSV)
inc = df[df["irr_resolution"].isin(["CONSENSUS", "DOMAIN_OVERRIDE"])].copy()
inc = inc.sort_values("paper_id").reset_index(drop=True)

print(f"Processing {len(inc)} INCLUDE papers...")

quality_log = []

def find_pdf(paper_id, pdf_filename, papers_dir):
    """Locate PDF by paper_id prefix or pdf_filename."""
    # Try pdf_filename first
    if pd.notna(pdf_filename) and str(pdf_filename).strip():
        candidate = os.path.join(papers_dir, str(pdf_filename).strip())
        if os.path.exists(candidate):
            return candidate
    # Try paper_id prefix
    for fname in os.listdir(papers_dir):
        if fname.startswith(paper_id + "_") or fname.startswith(paper_id + "."):
            return os.path.join(papers_dir, fname)
    return None

def clean_text(raw):
    """Basic cleaning: collapse excess whitespace, remove null bytes."""
    text = raw.replace("\x00", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{3,}", " ", text)
    return text.strip()

def extract_text_fitz(pdf_path):
    """Extract text from PDF using pymupdf."""
    try:
        doc = fitz.open(pdf_path)
        pages_text = []
        for page_num, page in enumerate(doc, 1):
            text = page.get_text("text")
            if text.strip():
                pages_text.append(f"<!-- PAGE {page_num} -->\n{text}")
        doc.close()
        full_text = "\n\n".join(pages_text)
        char_count = len(full_text)
        page_count = len(pages_text)
        return full_text, char_count, page_count, "ok"
    except Exception as e:
        return "", 0, 0, f"error: {e}"

for _, row in inc.iterrows():
    pid = row["paper_id"]
    title = str(row.get("title", "")).strip()
    year = str(row.get("year", "")).replace(".0", "")
    authors = str(row.get("authors", "")).strip()
    journal = str(row.get("journal", "")).strip()
    doi = str(row.get("doi", "")).strip()
    abstract = str(row.get("notes", "")).strip()  # 'notes' sometimes has abstract
    sjr = str(row.get("sjr_quartile", "")).strip()
    quality_score = str(row.get("quality_score", "")).strip()
    rq_tags = str(row.get("rq_tags", "")).strip()
    theme_tags = str(row.get("theme_tags", "")).strip()
    irr = str(row.get("irr_resolution", "")).strip()
    pipeline_status = str(row.get("pipeline_status", "")).strip()
    pdf_filename = row.get("pdf_filename", "")

    pdf_path = find_pdf(pid, pdf_filename, PAPERS_DIR)

    out_path = os.path.join(OUT_DIR, f"{pid}.md")

    # YAML header
    header = f"""---
paper_id: {pid}
title: "{title.replace('"', "'")}"
authors: "{authors[:200]}"
year: {year}
journal: "{journal[:120]}"
doi: {doi}
sjr_quartile: {sjr}
quality_score: {quality_score}
pipeline_status: {pipeline_status}
irr_resolution: {irr}
rq_tags: "{rq_tags}"
theme_tags: "{theme_tags}"
---

# {title}

**Authors**: {authors[:200]}
**Year**: {year}
**Journal**: {journal}
**DOI**: {doi}
**SJR**: {sjr} | **Quality Score**: {quality_score}
**RQ Tags**: {rq_tags}
**Theme Tags**: {theme_tags}

"""

    if pdf_path:
        full_text, char_count, page_count, status = extract_text_fitz(pdf_path)
        if char_count > 500:
            content = header + f"## Full Text\n\n{clean_text(full_text)}\n"
            source = "pdf_full_text"
        else:
            # Fallback: too short — may be image-based PDF
            content = header + f"## Abstract / Notes\n\n{abstract}\n\n<!-- PDF EXTRACTION FAILED OR EMPTY: char_count={char_count} -->\n"
            status = f"low_quality (chars={char_count})"
            source = "abstract_only_ocr_fail"
            char_count = len(abstract)
            page_count = 0
    else:
        # No PDF — abstract only
        content = header + f"## Abstract / Notes\n\n{abstract}\n\n<!-- NO PDF AVAILABLE — ABSTRACT ONLY -->\n"
        char_count = len(abstract)
        page_count = 0
        status = "no_pdf"
        source = "abstract_only"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    quality_log.append({
        "paper_id": pid,
        "title": title[:80],
        "source": source,
        "char_count": char_count,
        "page_count": page_count,
        "status": status,
        "pdf_path": pdf_path or "N/A"
    })

    symbol = "✓" if source == "pdf_full_text" else "~"
    print(f"  [{symbol}] {pid} — {source} ({char_count:,} chars)")

# Write quality log
log_df = pd.DataFrame(quality_log)
log_df.to_csv(LOG_CSV, index=False)
print()
print("=== EXTRACTION SUMMARY ===")
print(log_df["source"].value_counts().to_string())
print(f"\nMean char count (PDF papers): {log_df[log_df['source']=='pdf_full_text']['char_count'].mean():.0f}")
print(f"\nLog written to: {LOG_CSV}")
print(f"Extracted .md files: {len(quality_log)} → {OUT_DIR}")
