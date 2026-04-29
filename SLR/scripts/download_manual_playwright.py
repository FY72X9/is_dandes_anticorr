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
import shutil
import logging
import requests
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
            # Title line: "[N] [score=X] Title here"  (space before score tag)
            m = re.match(r'^\[(\d+)\]\s+(?:\[score=[^\]]+\]\s+)?(.+)$', line)
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

    # OJS journals (Open Journal Systems) — fepbl.com, ejournal.umm.ac.id, nblformosapublisher.org, ajrcos.com, etc.
    # OJS 3.x uses a.obj_galley_link; download URL pattern: /article/download/{id}/{galley_id}
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        for selector in [
            "a.obj_galley_link",
            "a[href*='/article/download/']",
            "a[href*='/download/'][href*='pdf']",
            ".galley-link a",
            ".download a",
        ]:
            links = page.locator(selector).all()
            for link in links:
                href = link.get_attribute("href") or ""
                text = (link.text_content() or "").strip().lower()
                if "pdf" in text or "pdf" in href.lower() or "/download/" in href:
                    if href.startswith("http"):
                        return href
                    if href.startswith("/"):
                        return f"{base_url}{href}"
    except Exception:
        pass

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
# curl_cffi helpers (non-Playwright strategies)
# ─────────────────────────────────────────────────────────────────────────────

def _try_mdpi_curl_cffi(doi: str, dest: Path) -> tuple[bool, str]:
    """
    Download MDPI OA paper without Playwright:
    1. Query OpenAlex for versioned PDF URL (e.g. /2076-3417/12/19/9637/pdf?version=...)
       — the versioned URL works; the /doi/pdf shortcut returns 404.
    2. Fetch with curl_cffi impersonating Chrome TLS fingerprint — bypasses Cloudflare.
    """
    try:
        from curl_cffi import requests as cf_req
    except ImportError:
        return False, "curl_cffi not installed (pip install curl_cffi)"

    # Step 1: versioned PDF URL from OpenAlex
    pdf_url: str | None = None
    try:
        r = requests.get(
            f"https://api.openalex.org/works/https://doi.org/{doi}",
            timeout=10,
        )
        if r.status_code == 200:
            d = r.json()
            best = d.get("best_oa_location") or {}
            pdf_url = best.get("pdf_url") or (d.get("open_access") or {}).get("oa_url")
    except Exception as exc:
        log.debug(f"    OpenAlex lookup failed: {exc}")

    if not pdf_url:
        return False, "MDPI: no OA URL from OpenAlex"

    log.debug(f"    MDPI curl_cffi URL: {pdf_url[:90]}")

    # Step 2: fetch with Chrome TLS fingerprint
    try:
        r2 = cf_req.get(pdf_url, impersonate="chrome", timeout=30)
        body = r2.content
        if r2.status_code == 200 and body[:4] == b"%PDF" and len(body) >= MIN_PDF_BYTES:
            dest.write_bytes(body)
            return True, f"curl_cffi ({len(body)//1024} KB)"
        log.debug(f"    curl_cffi: HTTP {r2.status_code}, size={len(body)}, head={body[:6]!r}")
    except Exception as exc:
        log.debug(f"    curl_cffi failed: {exc}")

    return False, "MDPI curl_cffi failed"


def _try_oa_curl_cffi(doi: str, url: str, dest: Path) -> tuple[bool, str]:
    """
    Generic curl_cffi strategy for non-MDPI open-access publishers:
    1. Emerald Insight — OpenAlex provides a direct /full/pdf URL that works with Chrome TLS.
    2. OJS3 journals (ejournal.umm.ac.id, etc.) — fetch HTML with curl_cffi,
       find /article/view/{id}/{galley} link, convert to /article/download/{id}/{galley}.
    """
    try:
        from curl_cffi import requests as cf_req
    except ImportError:
        return False, "curl_cffi not installed"

    # ── Emerald Insight ────────────────────────────────────────────────────
    if "emerald.com" in url or "10.1108/" in doi:
        try:
            r_oa = requests.get(
                f"https://api.openalex.org/works/https://doi.org/{doi}", timeout=8
            )
            if r_oa.status_code == 200:
                best = (r_oa.json().get("best_oa_location") or {})
                pdf_url = best.get("pdf_url")
                if pdf_url and "emerald.com" in pdf_url:
                    r2 = cf_req.get(pdf_url, impersonate="chrome", timeout=30)
                    body = r2.content
                    if r2.status_code == 200 and body[:4] == b"%PDF" and len(body) >= MIN_PDF_BYTES:
                        dest.write_bytes(body)
                        return True, f"Emerald curl_cffi ({len(body)//1024} KB)"
                    log.debug(f"    Emerald: HTTP {r2.status_code}, size={len(body)}")
        except Exception as exc:
            log.debug(f"    Emerald curl_cffi error: {exc}")
        return False, "Emerald curl_cffi failed"

    # ── OJS3 open journals ─────────────────────────────────────────────────
    # Strategy: fetch landing page, find /article/view/{id}/{galley}, re-fetch as /download/
    try:
        r_page = cf_req.get(url, impersonate="chrome", timeout=15, allow_redirects=True)
        if r_page.status_code == 200:
            import re as _re
            from urllib.parse import urlparse
            parsed = urlparse(r_page.url)
            base = f"{parsed.scheme}://{parsed.netloc}"
            # OJS3 galley link pattern: /article/view/{article_id}/{galley_id}
            matches = _re.findall(
                r'href=["\']([^"\']*article/view/\d+/\d+)["\']', r_page.text, _re.I
            )
            for href in matches:
                dl_url = href.replace("/article/view/", "/article/download/")
                if not dl_url.startswith("http"):
                    dl_url = base + dl_url
                r_dl = cf_req.get(dl_url, impersonate="chrome", timeout=20, allow_redirects=True)
                body = r_dl.content
                if r_dl.status_code == 200 and body[:4] == b"%PDF" and len(body) >= MIN_PDF_BYTES:
                    dest.write_bytes(body)
                    return True, f"OJS3 curl_cffi ({len(body)//1024} KB)"
                log.debug(f"    OJS3 dl {dl_url[-40:]}: HTTP {r_dl.status_code}, {len(body)}b")
        else:
            log.debug(f"    OJS3 page: HTTP {r_page.status_code}")
    except Exception as exc:
        log.debug(f"    OJS3 curl_cffi error: {exc}")

    return False, "OJS3 curl_cffi failed"


# ─────────────────────────────────────────────────────────────────────────────
# PDF download strategies
# ─────────────────────────────────────────────────────────────────────────────

def _try_download_pdf(page, context, pdf_url: str, dest: Path) -> tuple[bool, str]:
    """
    PDF download strategies (tried in order):
    1. APIRequestContext — reuses browser session cookies; fast for non-CF-protected sites.
    2. expect_download + shutil.move — browser-triggered download (IEEE stamp.jsp, etc.).
    shutil.move() handles cross-drive moves (C: → D:).
    Note: MDPI papers are handled separately by _try_mdpi_curl_cffi() before this function.
    """
    # Strategy 1: APIRequest (shares cookies already set by page.goto() above)
    try:
        resp = context.request.get(
            pdf_url,
            headers={"Accept": "application/pdf,*/*"},
            timeout=30_000,
        )
        if resp.status == 200:
            body = resp.body()
            if body[:4] == b"%PDF" and len(body) >= MIN_PDF_BYTES:
                dest.write_bytes(body)
                log.debug(f"    APIRequest OK: {len(body)//1024} KB")
                return True, f"APIRequest ({len(body)//1024} KB)"
            log.debug(f"    APIRequest: not a valid PDF (size={len(body)}, header={body[:8]!r})")
        else:
            log.debug(f"    APIRequest: HTTP {resp.status}")
    except Exception as exc:
        log.debug(f"    APIRequest failed: {exc}")

    # Strategy 2: expect_download (browser-triggered download event)
    try:
        with page.expect_download(timeout=30_000) as dl_info:
            page.goto(pdf_url, timeout=LOAD_TIMEOUT)
        dl = dl_info.value
        temp = dl.path()
        if temp:
            shutil.move(temp, str(dest))  # shutil.move works across drive letters
            if is_valid_pdf(dest) and dest.stat().st_size >= MIN_PDF_BYTES:
                return True, f"Download ({dest.stat().st_size//1024} KB)"
            dest.unlink(missing_ok=True)
            log.debug("    expect_download: file not valid PDF after move")
    except Exception as exc:
        log.debug(f"    expect_download failed: {exc}")

    return False, "all strategies failed"


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
            ignore_https_errors=True,
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

            # ── MDPI shortcut: curl_cffi + OpenAlex (no Playwright needed) ────
            if doi and doi.startswith("10.3390/"):
                ok, msg = _try_mdpi_curl_cffi(doi, dest)
                if ok:
                    log.info(f"  ✓ {msg}")
                    counters["success"] += 1
                else:
                    log.warning(f"  ✗ {msg}")
                    counters["failed"] += 1
                time.sleep(DELAY_SEC)
                continue

            # ── Emerald / OJS3 shortcut: curl_cffi (no Playwright needed) ────
            if doi and ("10.1108/" in doi):
                ok, msg = _try_oa_curl_cffi(doi, url, dest)
                if ok:
                    log.info(f"  ✓ {msg}")
                    counters["success"] += 1
                else:
                    log.warning(f"  ✗ {msg}")
                    counters["failed"] += 1
                time.sleep(DELAY_SEC)
                continue

            try:
                # Step 1: Navigate to landing page so browser sets session cookies
                page.goto(url, wait_until="domcontentloaded", timeout=LOAD_TIMEOUT)
                time.sleep(2.0)  # let JS / Cloudflare challenge render

                pdf_url = _get_pdf_url_from_page(page, doi)
                log.debug(f"  Extracted PDF URL: {pdf_url}")

                if not pdf_url:
                    # Fallback: try OJS3 curl_cffi strategy (works when Playwright can't
                    # extract link from page but curl_cffi can read the HTML directly)
                    log.debug(f"  Trying OJS3 curl_cffi fallback for {page.url[:60]}")
                    ok, msg = _try_oa_curl_cffi(doi, url, dest)
                    if ok:
                        log.info(f"  ✓ {msg}")
                        counters["success"] += 1
                    else:
                        log.warning(f"  ✗ Could not extract PDF URL from page ({page.url[:60]})")
                        counters["failed"] += 1
                    continue

                # Step 2: Download using APIRequest (cookies) then expect_download fallback
                ok, msg = _try_download_pdf(page, context, pdf_url, dest)
                if ok:
                    log.info(f"  ✓ {msg}")
                    counters["success"] += 1
                else:
                    log.warning(f"  ✗ {msg}")
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
