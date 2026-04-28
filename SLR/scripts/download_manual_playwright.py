"""
download_manual_playwright.py — Headless Browser PDF Downloader
================================================================
Downloads the papers listed in manual_download_log.txt using Playwright
(Chromium headless browser), bypassing Cloudflare / bot detection that
blocks plain `requests`-based downloads.

This is a ONE-TIME helper script, separate from the main pipeline.

Setup (run once):
    pip install playwright
    playwright install chromium

Usage:
    python download_manual_playwright.py

Output:
    PDFs saved to SLR/papers/  (same directory as pipeline)
    Results logged to: output/playwright_download.log
"""

from __future__ import annotations

import re
import sys
import time
import logging
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
ROOT_DIR     = SCRIPT_DIR.parent
PDF_DIR      = ROOT_DIR / "papers"
OUTPUT_DIR   = SCRIPT_DIR / "output"
MANUAL_LOG   = OUTPUT_DIR / "manual_download_log.txt"
PW_LOG_FILE  = OUTPUT_DIR / "playwright_download.log"

PDF_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(PW_LOG_FILE, mode="a", encoding="utf-8"),
    ],
)
logging.getLogger().handlers[0].setLevel(logging.INFO)
logging.getLogger().handlers[1].setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

MIN_PDF_BYTES = 8_000
DELAY_SEC     = 2.0   # wait between pages (polite)
LOAD_TIMEOUT  = 30_000  # ms for page load


def sanitize_filename(name: str, max_len: int = 80) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:max_len].rstrip("_")


def is_valid_pdf(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"%PDF"
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# Parse manual_download_log.txt
# ─────────────────────────────────────────────────────────────────────────────

def parse_manual_log(path: Path) -> list[dict]:
    """Extract title + DOI pairs from manual_download_log.txt."""
    if not path.exists():
        log.error(f"manual_download_log.txt not found: {path}")
        return []

    papers = []
    current: dict = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            # Title line: "[N][score=X] Title here"
            m = re.match(r'^\[(\d+)\](?:\[score=[^\]]+\])?\s+(.+)$', line)
            if m:
                if current:
                    papers.append(current)
                current = {"title": m.group(2).strip(), "doi": "", "url": ""}
            elif line.strip().startswith("DOI") and current:
                doi = line.split(":", 1)[-1].strip()
                current["doi"] = doi
            elif line.strip().startswith("Publisher") and current:
                url = line.split(":", 1)[-1].strip()
                current["url"] = url
    if current:
        papers.append(current)
    log.info(f"Parsed {len(papers)} entries from manual_download_log.txt")
    return papers


# ─────────────────────────────────────────────────────────────────────────────
# Publisher-specific PDF extraction strategies
# ─────────────────────────────────────────────────────────────────────────────

def _get_pdf_url_from_page(page, doi: str) -> str | None:
    """Try to find a PDF download URL on the currently loaded page."""
    url = page.url

    # IEEE Xplore: look for PDF download button link
    if "ieeexplore.ieee.org" in url:
        try:
            # The PDF download link has class containing 'pdf-btn-link' or 'xpl-btn-primary'
            links = page.locator("a[href*='/stamp/stamp.jsp']").all()
            if links:
                href = links[0].get_attribute("href")
                if href:
                    return f"https://ieeexplore.ieee.org{href}" if href.startswith("/") else href
        except Exception:
            pass

    # MDPI: look for PDF link
    if "mdpi.com" in url:
        try:
            links = page.locator("a[href$='/pdf']").all()
            if links:
                href = links[0].get_attribute("href")
                if href:
                    return f"https://www.mdpi.com{href}" if href.startswith("/") else href
        except Exception:
            pass
        # Try constructing from DOI
        if doi and doi.startswith("10.3390/"):
            return f"https://www.mdpi.com/{doi}/pdf"

    # Generic: look for any PDF link
    try:
        links = page.locator("a[href$='.pdf']").all()
        if links:
            href = links[0].get_attribute("href")
            if href and href.startswith("http"):
                return href
    except Exception:
        pass

    return None


# ─────────────────────────────────────────────────────────────────────────────
# Main download loop
# ─────────────────────────────────────────────────────────────────────────────

def run_playwright_downloads(papers: list[dict]) -> dict[str, int]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log.error("Playwright not installed. Run:")
        log.error("    pip install playwright")
        log.error("    playwright install chromium")
        sys.exit(1)

    counters = {"success": 0, "failed": 0, "skipped": 0}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            accept_downloads=True,
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        for i, paper in enumerate(papers, 1):
            title  = paper["title"]
            doi    = paper["doi"]
            url    = paper["url"] or (f"https://doi.org/{doi}" if doi else "")

            slug = sanitize_filename(title[:60])
            dest = PDF_DIR / f"{slug}.pdf"

            log.info(f"[{i}/{len(papers)}] {title[:60]}")

            # Skip if already exists
            if dest.exists() and is_valid_pdf(dest) and dest.stat().st_size >= MIN_PDF_BYTES:
                log.info(f"  ✓ Already exists — skipping")
                counters["skipped"] += 1
                continue

            if not url:
                log.warning(f"  ✗ No URL or DOI — cannot fetch")
                counters["failed"] += 1
                continue

            try:
                # Navigate to the paper landing page
                page.goto(url, wait_until="domcontentloaded", timeout=LOAD_TIMEOUT)
                time.sleep(1.5)  # let JS render

                pdf_url = _get_pdf_url_from_page(page, doi)
                log.debug(f"  Extracted PDF URL: {pdf_url}")

                if pdf_url:
                    # Try download via Playwright (handles auth + cookies)
                    with page.expect_download(timeout=30_000) as dl_info:
                        page.goto(pdf_url, timeout=LOAD_TIMEOUT)
                    download = dl_info.value
                    temp_path = Path(download.path())
                    if temp_path and temp_path.exists():
                        temp_path.rename(dest)
                        if is_valid_pdf(dest) and dest.stat().st_size >= MIN_PDF_BYTES:
                            log.info(f"  ✓ Downloaded via Playwright ({dest.stat().st_size//1024} KB)")
                            counters["success"] += 1
                            time.sleep(DELAY_SEC)
                            continue
                        else:
                            dest.unlink(missing_ok=True)

                # Fallback: try direct navigation to a PDF URL if page IS already PDF
                ct = page.evaluate("() => document.contentType")
                if "pdf" in str(ct).lower():
                    content = page.content()
                    dest.write_bytes(content.encode())
                    log.info(f"  ✓ Saved page PDF content")
                    counters["success"] += 1
                else:
                    log.warning(f"  ✗ Could not extract PDF URL from page")
                    counters["failed"] += 1

            except Exception as exc:
                log.warning(f"  ✗ Exception: {exc}")
                counters["failed"] += 1

            time.sleep(DELAY_SEC)

        browser.close()

    return counters


def main():
    log.info("=" * 60)
    log.info("Playwright Manual PDF Downloader")
    log.info("=" * 60)
    log.info(f"Manual log : {MANUAL_LOG}")
    log.info(f"PDF output : {PDF_DIR}")

    papers = parse_manual_log(MANUAL_LOG)
    if not papers:
        log.error("No papers to process. Check manual_download_log.txt exists.")
        sys.exit(1)

    # Filter: skip papers already on disk
    remaining = []
    for p in papers:
        slug = sanitize_filename(p["title"][:60])
        dest = PDF_DIR / f"{slug}.pdf"
        if dest.exists() and is_valid_pdf(dest) and dest.stat().st_size >= MIN_PDF_BYTES:
            continue
        remaining.append(p)

    log.info(f"Papers remaining (not yet downloaded): {len(remaining)}")

    if not remaining:
        log.info("All manual papers already downloaded!")
        return

    counters = run_playwright_downloads(remaining)

    log.info("\n" + "=" * 60)
    log.info("DONE")
    log.info(f"  Success  : {counters['success']}")
    log.info(f"  Skipped  : {counters['skipped']}")
    log.info(f"  Failed   : {counters['failed']}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
