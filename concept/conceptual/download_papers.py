"""
download_papers.py — Dynamic Mode
==================================
Parses references.md (or any path given as CLI argument) to extract paper
entries and their OA PDF URLs.  For every paper with a resolvable URL it
attempts a download, then validates the result is a genuine PDF file—not a
corrupt HTML error page, a 403 redirect, or a near-empty stub.

Key improvements over the previous hard-coded catalogue:
  • No static PAPERS list — every entry is read from references.md at runtime
  • Pre-flight HEAD check to detect HTML responses before wasting bandwidth
  • PDF magic-byte validation (%PDF header) after every download
  • Minimum file-size guard (< 8 KB almost certainly means an error page)
  • arXiv /abs/ → /pdf/ URL normalisation
  • When a line contains multiple URLs, the best (most likely direct PDF) is
    selected automatically
  • Stale files (exist but invalid) are deleted and re-attempted
  • Comprehensive summary report with manual-download list

Usage:
    python download_papers.py                  # uses references.md in same dir
    python download_papers.py /path/to/refs.md # custom references file

Requirements:
    pip install requests
"""

from __future__ import annotations

import re
import sys
import time
import requests
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR         = Path(__file__).parent
DEFAULT_REFS_FILE  = SCRIPT_DIR / "references.md"
OUTPUT_DIR         = SCRIPT_DIR / "papers-literatures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REQUEST_TIMEOUT    = 30     # seconds per request
DELAY_BETWEEN      = 2      # polite delay between requests (seconds)
MIN_PDF_BYTES      = 8_000  # files smaller than this are treated as error pages

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,*/*;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
}

# Values in OA PDF / OA URL fields that signal the paper is not downloadable
SKIP_PHRASES = (
    "not available",
    "not openly available",
    "institutional access",
    "institutional login",
    "institutional subscription",
    "download manually",
    "requires login",
    "requires institutional",
)


# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------

def clean_url(raw: str) -> str:
    """Strip trailing punctuation and markdown artefacts from a raw URL."""
    return raw.strip().rstrip(".,;)]\\/ ")


def normalise_url(url: str) -> str:
    """Convert known redirect / landing-page URLs to direct PDF equivalents."""
    url = clean_url(url)
    # arXiv: /abs/XXXX.YYYY  ->  /pdf/XXXX.YYYY.pdf
    if "arxiv.org/abs/" in url:
        url = url.replace("arxiv.org/abs/", "arxiv.org/pdf/")
        if not url.endswith(".pdf"):
            url += ".pdf"
    return url


def is_likely_pdf_url(url: str) -> bool:
    """Heuristic: does this URL pattern suggest a direct PDF download?"""
    lower = url.lower()
    return (
        lower.endswith(".pdf")
        or "/pdf/" in lower
        or "downloadpdf" in lower
        or "citation-pdf-url" in lower
        or "arxiv.org/pdf/" in lower
        or "/article/download/" in lower
    )


def extract_best_url(text: str) -> "str | None":
    """
    Extract the most useful URL from a text fragment.
    Prefers direct PDF links; falls back to the first URL if none found.
    """
    raw_urls = re.findall(r"https?://[^\s\)\]\|]+", text)
    if not raw_urls:
        return None
    urls = [normalise_url(u) for u in raw_urls]
    pdf_candidates = [u for u in urls if is_likely_pdf_url(u)]
    return pdf_candidates[0] if pdf_candidates else urls[0]


# ---------------------------------------------------------------------------
# PDF validation
# ---------------------------------------------------------------------------

def is_valid_pdf(path: Path) -> bool:
    """Return True only if the file begins with the PDF magic bytes %PDF."""
    try:
        with open(path, "rb") as fh:
            return fh.read(4) == b"%PDF"
    except Exception:
        return False


def file_size_ok(path: Path) -> bool:
    """Return True if the file exceeds the minimum size threshold."""
    try:
        return path.stat().st_size >= MIN_PDF_BYTES
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

def parse_references(filepath: Path) -> list:
    """
    Parse a references.md file and return a list of paper dicts.

    Each dict contains:
        id       : int
        title    : str
        slug     : str   (filesystem-safe filename fragment)
        pdf_url  : str|None  (**OA PDF** line — preferred direct download)
        oa_url   : str|None  (**OA URL** line — may be a landing page)

    Parsing rules
    -------------
    - Entries are delimited by lines beginning with [N] (IEEE citation format).
    - **OA PDF**: lines supply preferred direct-download targets.
    - **OA URL**: lines supply fallback URLs.
    - Lines containing a SKIP_PHRASE are treated as no PDF available.
    - When a line contains multiple URLs the most direct-PDF-looking one wins.
    """
    if not filepath.exists():
        raise FileNotFoundError("References file not found: {}".format(filepath))

    text = filepath.read_text(encoding="utf-8")
    papers = []

    # Split into per-entry blocks at lines beginning with [N]
    blocks = re.split(r"(?m)^(?=\[\d+\]\s)", text)

    for block in blocks:
        block = block.strip()
        m_id = re.match(r"\[(\d+)\]", block)
        if not m_id:
            continue  # preamble or section headings

        ref_id = int(m_id.group(1))
        first_line = block.split("\n")[0]

        # Title: first quoted string on the first line
        m_title = re.search(r'"([^"]+)"', first_line)
        if m_title:
            title = m_title.group(1)
        else:
            title = first_line[len(m_id.group(0)):].strip()[:80]

        # Filesystem-safe slug
        slug = re.sub(r"[^\w\s-]", "", title.lower())
        slug = re.sub(r"\s+", "_", slug.strip())[:60].rstrip("_")

        # OA PDF URL (direct download preferred)
        pdf_url = None
        m_pdf = re.search(r"\*\*OA PDF\*\*:\s*(.+)", block)
        if m_pdf:
            candidate = m_pdf.group(1).strip()
            if not any(p in candidate.lower() for p in SKIP_PHRASES):
                pdf_url = extract_best_url(candidate)

        # OA URL (general fallback)
        oa_url = None
        m_oa = re.search(r"\*\*OA URL\*\*:\s*(.+)", block)
        if m_oa:
            candidate = m_oa.group(1).strip()
            if not any(p in candidate.lower() for p in SKIP_PHRASES):
                oa_url = extract_best_url(candidate)

        papers.append(
            {
                "id":      ref_id,
                "title":   title,
                "slug":    slug,
                "pdf_url": pdf_url,
                "oa_url":  oa_url,
            }
        )

    return sorted(papers, key=lambda p: p["id"])


# ---------------------------------------------------------------------------
# Downloader
# ---------------------------------------------------------------------------

def download_and_validate(url: str, dest: Path):
    """
    Download url to dest.  Validates the result is a genuine PDF.

    Returns
    -------
    (True,  "OK (N KB)")       on success
    (False, "<reason string>") on failure — also deletes any partial file
    """
    # 1. Pre-flight HEAD check
    try:
        head = requests.head(
            url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True
        )
        ct = head.headers.get("Content-Type", "")
        if head.status_code >= 400:
            return False, "HEAD returned HTTP {}".format(head.status_code)
        if "html" in ct.lower() and not is_likely_pdf_url(url):
            return False, "Server reports Content-Type: {!r} — likely HTML error page".format(ct)
    except Exception:
        pass  # HEAD not supported by all servers; proceed to GET

    # 2. GET download
    try:
        resp = requests.get(
            url, headers=HEADERS, timeout=REQUEST_TIMEOUT, stream=True
        )
        resp.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=8192):
                fh.write(chunk)
    except requests.exceptions.HTTPError as exc:
        dest.unlink(missing_ok=True)
        return False, "HTTP {}".format(exc.response.status_code)
    except requests.exceptions.ConnectionError:
        dest.unlink(missing_ok=True)
        return False, "Connection error"
    except requests.exceptions.Timeout:
        dest.unlink(missing_ok=True)
        return False, "Timeout after {} s".format(REQUEST_TIMEOUT)
    except Exception as exc:
        dest.unlink(missing_ok=True)
        return False, "Unexpected error: {}".format(exc)

    # 3. Validate PDF magic bytes
    if not is_valid_pdf(dest):
        size = dest.stat().st_size
        dest.unlink(missing_ok=True)
        return False, "Not a valid PDF (magic bytes wrong; {} bytes)".format(size)

    # 4. Validate minimum file size
    if not file_size_ok(dest):
        size = dest.stat().st_size
        dest.unlink(missing_ok=True)
        return False, "File too small ({} bytes) — likely an error page".format(size)

    size_kb = dest.stat().st_size / 1024
    return True, "OK ({:.1f} KB)".format(size_kb)


def attempt_paper(paper: dict):
    """
    Attempt to download a paper, trying OA PDF first, then OA URL if it
    looks like a direct PDF link.

    Returns
    -------
    ("downloaded",     None)      on success
    ("skipped_exists", None)      already valid on disk
    ("no_url",         str|None)  no usable URL found
    ("failed",         str)       all attempts failed
    """
    pdf_url = paper["pdf_url"]
    oa_url  = paper["oa_url"]

    urls_to_try = []
    if pdf_url:
        urls_to_try.append((pdf_url, "OA PDF"))
    if oa_url and is_likely_pdf_url(oa_url) and oa_url != pdf_url:
        urls_to_try.append((oa_url, "OA URL (direct PDF)"))

    if not urls_to_try:
        reason = "No direct PDF URL available"
        if oa_url:
            reason += " — OA URL is a landing page: {}".format(oa_url)
        return "no_url", reason

    dest = OUTPUT_DIR / "[{:02d}] {}.pdf".format(paper["id"], paper["slug"])

    # Check for existing valid file
    if dest.exists():
        if is_valid_pdf(dest) and file_size_ok(dest):
            size_kb = dest.stat().st_size / 1024
            print("   [EXISTS] Already downloaded and valid ({:.1f} KB)".format(size_kb))
            return "skipped_exists", None
        print("   [STALE]  Existing file is invalid/corrupt — deleting and re-downloading")
        dest.unlink(missing_ok=True)

    last_reason = "no attempts made"
    for url, label in urls_to_try:
        print("   [TRY] {}: {}".format(label, url))
        success, msg = download_and_validate(url, dest)
        if success:
            print("   [OK]  {}".format(msg))
            return "downloaded", None
        print("   [FAIL] {}".format(msg))
        last_reason = msg
        time.sleep(DELAY_BETWEEN)

    return "failed", "All {} attempt(s) failed — last error: {}".format(
        len(urls_to_try), last_reason
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(refs_path: Path) -> None:
    print("=" * 72)
    print("  Research Paper Downloader — Dynamic Mode")
    print("  Source : {}".format(refs_path))
    print("  Output : {}".format(OUTPUT_DIR))
    print("=" * 72)

    papers = parse_references(refs_path)
    print("\n  Parsed {} reference entries from {}\n".format(
        len(papers), refs_path.name
    ))

    results = {
        "downloaded":     [],
        "skipped_exists": [],
        "no_url":         [],
        "failed":         [],
    }

    for paper in papers:
        print("\n[{:02d}] {}".format(paper["id"], paper["title"][:72]))
        status, note = attempt_paper(paper)
        results[status].append(paper["id"])
        if note:
            print("   [INFO] {}".format(note))
        if status not in ("skipped_exists", "no_url"):
            time.sleep(DELAY_BETWEEN)

    # Summary
    print("\n" + "=" * 72)
    print("  DOWNLOAD SUMMARY")
    print("=" * 72)
    print("  Successfully downloaded  : {:3d}  {}".format(
        len(results["downloaded"]), results["downloaded"]
    ))
    print("  Already valid (skipped)  : {:3d}".format(len(results["skipped_exists"])))
    print("  No PDF URL available     : {:3d}  {}".format(
        len(results["no_url"]), results["no_url"]
    ))
    print("  Failed / invalid PDF     : {:3d}  {}".format(
        len(results["failed"]), results["failed"]
    ))
    print("\n  Files saved to: {}".format(OUTPUT_DIR))
    print("=" * 72)

    manual_ids = sorted(set(results["no_url"] + results["failed"]))
    if manual_ids:
        print("\n  Papers requiring manual download:")
        for paper in papers:
            if paper["id"] in manual_ids:
                print("    [{:02d}] {}".format(paper["id"], paper["title"][:60]))
                if paper["oa_url"]:
                    print("         URL: {}".format(paper["oa_url"]))


if __name__ == "__main__":
    refs_file = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_REFS_FILE
    run(refs_file)
