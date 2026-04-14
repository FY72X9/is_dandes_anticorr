"""
download_papers.py
------------------
Downloads openly available PDFs of references listed in references.md.
Saves all files to: concept/conceptual/papers-literatures/

Usage:
    python download_papers.py

Requirements:
    pip install requests

Notes:
- Only attempts PDFs with verified direct-download URLs (from OpenAlex OA index).
- Papers without OA PDFs are listed but skipped with a clear log message.
- Implements a polite 2-second delay between requests.
- Skips re-downloading files that already exist.
"""

import os
import time
import requests
from pathlib import Path

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "papers-literatures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Request headers — polite browser identity
# ---------------------------------------------------------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

REQUEST_TIMEOUT = 30   # seconds
DELAY_BETWEEN    = 2    # seconds between requests (polite crawling)

# ---------------------------------------------------------------------------
# Paper catalogue
# Each entry:
#   id       : Citation number in references.md
#   key      : Short filename slug (no extension)
#   authors  : Abbreviated authors for display
#   year     : Publication year
#   title    : Full title
#   pdf_url  : Direct PDF URL (None if not openly available)
#   note     : Access note shown when pdf_url is None
# ---------------------------------------------------------------------------
PAPERS = [
    {
        "id": 1,
        "key": "bussell_2015_typologies_of_corruption",
        "authors": "Bussell, J.",
        "year": 2015,
        "title": "Typologies of corruption: a pragmatic approach",
        "pdf_url": None,
        "note": (
            "Elgaronline requires institutional login. "
            "DOI: https://doi.org/10.4337/9781784714703.00007  "
            "Access via institutional subscription or request from author."
        ),
    },
    {
        "id": 2,
        "key": "vargas_hernandez_2009_multiple_faces_corruption",
        "authors": "Vargas-Hernández, J.G.",
        "year": 2009,
        "title": "The Multiple Faces of Corruption: Typology, Forms and Levels",
        "pdf_url": None,
        "note": "SSRN page: https://doi.org/10.2139/ssrn.1413976  (download manually from SSRN)",
    },
    {
        "id": 3,
        "key": "suleiman_othman_2017_corruption_typology_review",
        "authors": "Suleiman, N. & Othman, Z.",
        "year": 2017,
        "title": "Corruption typology: a review of literature",
        "pdf_url": None,
        "note": (
            "UUM institutional repository requires login (HTTP 401). "
            "Repository: http://repo.uum.edu.my/26265/  "
            "Try CORE.ac.uk search: https://core.ac.uk/search?q=corruption+typology+suleiman+othman"
        ),
    },
    {
        "id": 4,
        "key": "albanese_artello_2019_empirical_typology_public_corruption",
        "authors": "Albanese, J.S. & Artello, K.",
        "year": 2019,
        "title": "The Behavior of Corruption: An Empirical Typology of Public Corruption by Objective and Method",
        "pdf_url": None,
        "note": "DOAJ record: https://doaj.org/article/f2ac0958521746d6881f94fe5db77279  (no direct PDF link available)",
    },
    {
        "id": 5,
        "key": "mutungi_et_al_2021_digital_anticorruption_typology",
        "authors": "Mutungi, F. et al.",
        "year": 2021,
        "title": "Digital Anti-Corruption Typology for Public Service Delivery",
        "pdf_url": "https://www.ijcaonline.org/archives/volume183/number5/31906-2021921089.pdf",
        "note": "Fallback: DOI landing page https://doi.org/10.5120/ijca2021921089",
    },
    {
        "id": 6,
        "key": "sommersguter_et_al_2018_corruption_typologies_healthcare",
        "authors": "Sommersguter-Reichmann, M. et al.",
        "year": 2018,
        "title": "Individual and Institutional Corruption in European and US Healthcare: Corruption Typologies",
        "pdf_url": "https://link.springer.com/content/pdf/10.1007%2Fs40258-018-0386-6.pdf",
        "note": None,
    },
    {
        "id": 7,
        "key": "vargas_hernandez_2014_polyfacetic_masks_corruption",
        "authors": "Vargas-Hernández, J.G.",
        "year": 2014,
        "title": "Polyfacetic Masks of Corruption: Typologies, Categories, Forms and Levels",
        "pdf_url": None,
        "note": "DOI: https://doi.org/10.7719/ijgc.v1i1.226  (no direct OA PDF; access via journal website)",
    },
    {
        "id": 8,
        "key": "tanzi_1998_corruption_around_the_world",
        "authors": "Tanzi, V.",
        "year": 1998,
        "title": "Corruption Around the World: Causes, Consequences, Scope, and Cures",
        "pdf_url": None,
        "note": "SSRN: https://doi.org/10.2139/ssrn.882334  (download manually from SSRN)",
    },
    {
        "id": 9,
        "key": "soreide_2002_corruption_public_procurement",
        "authors": "Søreide, T.",
        "year": 2002,
        "title": "Corruption in Public Procurement: Causes, Consequences and Cures",
        "pdf_url": None,
        "note": (
            "CMI server returns HTML redirect instead of PDF. "
            "Download manually from: https://hdl.handle.net/11250/2435744  "
            "Or try direct: https://www.cmi.no/publications/1458-corruption-in-public-procurement"
        ),
    },
    {
        "id": 10,
        "key": "sumah_2018_corruption_causes_consequences",
        "authors": "Šumah, Š.",
        "year": 2018,
        "title": "Corruption, Causes and Consequences",
        "pdf_url": "https://www.intechopen.com/citation-pdf-url/58969",
        "note": None,
    },
    {
        "id": 11,
        "key": "triyono_2020_framing_village_fund_corruption_indonesia",
        "authors": "Triyono, A.",
        "year": 2020,
        "title": "Framing Analysis of Village Funding Corruption in Media Suaramerdeka.com, Indonesia, 2019",
        "pdf_url": "https://lifescienceglobal.com/pms/index.php/ijcs/article/download/7830/4098",
        "note": None,
    },
    {
        "id": 12,
        "key": "srirejeki_faturokhman_2020_corruption_prevention_dana_desa",
        "authors": "Srirejeki, K. & Faturokhman, A.",
        "year": 2020,
        "title": "In Search of Corruption Prevention Model: Case Study from Indonesia Village Fund",
        "pdf_url": None,
        "note": "DOAJ/journal: http://dj.univ-danubius.ro/index.php/AUDOE/article/view/339/599  (download manually)",
    },
    {
        "id": 13,
        "key": "siregar_aminudin_2020_abuse_village_fund_east_java",
        "authors": "Siregar, R.K. & Aminudin, A.",
        "year": 2020,
        "title": "Abuse of Village Fund (VF) in Indonesia: Case Study of VF Corruption in East Java",
        "pdf_url": "https://www.grdspublishing.org/index.php/people/article/viewFile/2301/3751",
        "note": "Fallback DOI: https://doi.org/10.20319/pijss.2020.61.379396",
    },
    {
        "id": 14,
        "key": "kartadinata_et_al_2021_criminal_policy_village_fund",
        "authors": "Kartadinata, A. et al.",
        "year": 2021,
        "title": "Criminal Policy of Village Fund Corruption in Indonesia",
        "pdf_url": "http://eudl.eu/pdf/10.4108/eai.6-3-2021.2306470",
        "note": None,
    },
    {
        "id": 15,
        "key": "medan_et_al_2025_village_fund_corruption_patterns_kupang",
        "authors": "Medan, K.K. et al.",
        "year": 2025,
        "title": "Patterns of Village Fund Corruption Prevention Based on Fatuleu Local Wisdom in Kupang Regency",
        "pdf_url": "https://posthumanism.co.uk/jp/article/download/1810/965",
        "note": None,
    },
    {
        "id": 16,
        "key": "stripling_et_al_2018_isolation_based_fraud_detection_dss",
        "authors": "Stripling, E. et al.",
        "year": 2018,
        "title": "Isolation-based Conditional Anomaly Detection on Mixed-Attribute Data to Uncover Workers' Compensation Fraud",
        "pdf_url": None,
        "note": (
            "Bronze OA (Elsevier landing page, not directly downloadable). "
            "DOI: https://doi.org/10.1016/j.dss.2018.04.001  "
            "KU Leuven accepted version: https://lirias.kuleuven.be/handle/123456789/622527  "
            "Access via institutional subscription or ResearchGate author request."
        ),
    },
    {
        "id": 17,
        "key": "cressey_1953_other_peoples_money_fraud_triangle",
        "authors": "Cressey, D.R.",
        "year": 1953,
        "title": "Other People's Money: A Study in the Social Psychology of Embezzlement",
        "pdf_url": None,
        "note": "Pre-digital monograph — not openly available. Access via institutional library.",
    },
    {
        "id": 18,
        "key": "delone_mclean_2003_is_success_model",
        "authors": "DeLone, W.H. & McLean, E.R.",
        "year": 2003,
        "title": "The DeLone and McLean Model of Information Systems Success: A Ten-Year Update",
        "pdf_url": None,
        "note": (
            "DOI: https://doi.org/10.1080/07421222.2003.11045748  "
            "Available via Taylor & Francis / institutional subscription."
        ),
    },
    {
        "id": 19,
        "key": "liu_ting_zhou_2008_isolation_forest_icdm",
        "authors": "Liu, F.T., Ting, K.M. & Zhou, Z.-H.",
        "year": 2008,
        "title": "Isolation Forest",
        "pdf_url": None,
        "note": (
            "IEEE Xplore: https://doi.org/10.1109/ICDM.2008.17  "
            "Author copy often available on ResearchGate."
        ),
    },
    {
        "id": 20,
        "key": "liu_ting_zhou_2012_isolation_based_anomaly_detection_tkdd",
        "authors": "Liu, F.T., Ting, K.M. & Zhou, Z.-H.",
        "year": 2012,
        "title": "Isolation-Based Anomaly Detection",
        "pdf_url": None,
        "note": (
            "ACM DL: https://doi.org/10.1145/2133360.2133363  "
            "Author preprint may be available on ResearchGate."
        ),
    },
    # -----------------------------------------------------------------------
    # [21]-[26] Additions — sourced from cross-check with Referensi_laporan_korupsi.md
    # -----------------------------------------------------------------------
    {
        "id": 21,
        "key": "svensson_2005_eight_questions_corruption_jep",
        "authors": "Svensson, J.",
        "year": 2005,
        "title": "Eight Questions about Corruption",
        "pdf_url": None,
        "note": (
            "JEP DOI: https://doi.org/10.1257/089533005774357860  "
            "World Bank preprint (free): "
            "https://documents.worldbank.org/curated/en/486981468762385907/pdf/The-determinants-of-corruption-a-review.pdf"
        ),
    },
    {
        "id": 22,
        "key": "hidajat_2024_village_fund_corruption_mode_jfc",
        "authors": "Hidajat, T.",
        "year": 2024,
        "title": "Village Fund Corruption Mode: An Anti-Corruption Perspective in Indonesia",
        "pdf_url": None,
        "note": (
            "Emerald Journal of Financial Crime — institutional access required. "
            "DOI: https://doi.org/10.1108/jfc-01-2024-0042"
        ),
    },
    {
        "id": 23,
        "key": "alfada_2019_fiscal_decentralization_corruption_indonesia",
        "authors": "Alfada, A.",
        "year": 2019,
        "title": "Does Fiscal Decentralization Encourage Corruption in Local Governments? Evidence from Indonesia",
        "pdf_url": "https://www.mdpi.com/1911-8074/12/3/118/pdf",
        "note": "MDPI open-access article. If 403, download manually from: https://doi.org/10.3390/jrfm12030118",
    },
    {
        "id": 24,
        "key": "ester_et_al_1996_dbscan_kdd",
        "authors": "Ester, M., Kriegel, H.-P., Sander, J. & Xu, X.",
        "year": 1996,
        "title": "A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise",
        "pdf_url": "http://www2.cs.uh.edu/~ceick/7363/Papers/dbscan.pdf",
        "note": "CiteSeerX PDF mirror of original KDD-96 proceedings paper (19,132 citations).",
    },
    {
        "id": 25,
        "key": "kim_vasarhelyi_2024_dbscan_fraudulent_wire_transfers",
        "authors": "Kim, Y.-B. & Vasarhelyi, M.A.",
        "year": 2024,
        "title": "Anomaly Detection with DBSCAN to Detect Potentially Fraudulent Wire Transfers",
        "pdf_url": "http://dx.doi.org/10.4192/1577-8517-v24_3",
        "note": "IJDAR bronze OA — publisher PDF redirect via DOI.",
    },
    {
        "id": 26,
        "key": "groenendijk_1997_principal_agent_corruption",
        "authors": "Groenendijk, N.",
        "year": 1997,
        "title": "A Principal-Agent Model of Corruption",
        "pdf_url": "https://ris.utwente.nl/ws/files/6653794/principal-agent.pdf",
        "note": "University of Twente institutional repository (green OA).",
    },
]


# ---------------------------------------------------------------------------
# Downloader
# ---------------------------------------------------------------------------

def download_pdf(url: str, dest_path: Path, paper_title: str) -> bool:
    """Attempt to download a PDF from url to dest_path. Returns True on success."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        # Accept if content-type signals PDF, or if URL ends with .pdf
        is_pdf = (
            "pdf" in content_type.lower()
            or url.lower().endswith(".pdf")
            or url.lower().endswith(".pdf%2F")
        )
        if not is_pdf:
            # Try to detect PDF by magic bytes
            first_bytes = b""
            for chunk in response.iter_content(chunk_size=8):
                first_bytes = chunk
                break
            if not first_bytes.startswith(b"%PDF"):
                print(f"   [WARN] Response is not a PDF (Content-Type: {content_type}). Saving anyway.")

        # Write to file
        with open(dest_path, "wb") as f:
            # Write already-read first_bytes if we peeked
            try:
                if first_bytes:
                    f.write(first_bytes)
            except NameError:
                pass
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        size_kb = dest_path.stat().st_size / 1024
        print(f"   [OK] Saved ({size_kb:.1f} KB) → {dest_path.name}")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"   [FAIL] HTTP {e.response.status_code} — {url}")
    except requests.exceptions.ConnectionError:
        print(f"   [FAIL] Connection error — {url}")
    except requests.exceptions.Timeout:
        print(f"   [FAIL] Timeout after {REQUEST_TIMEOUT}s — {url}")
    except Exception as e:
        print(f"   [FAIL] Unexpected error: {e}")
    return False


def run():
    print("=" * 70)
    print("  Corruption Research — PDF Downloader")
    print(f"  Output directory: {OUTPUT_DIR}")
    print("=" * 70)

    results = {"downloaded": [], "skipped_exists": [], "no_url": [], "failed": []}

    for paper in PAPERS:
        ref_id  = paper["id"]
        key     = paper["key"]
        title   = paper["title"]
        authors = paper["authors"]
        year    = paper["year"]
        pdf_url = paper["pdf_url"]
        note    = paper["note"]

        print(f"\n[{ref_id:02d}] {authors} ({year})")
        print(f"      {title}")

        if pdf_url is None:
            print(f"   [SKIP] No OA PDF available.")
            if note:
                print(f"   [INFO] {note}")
            results["no_url"].append(ref_id)
            continue

        dest_path = OUTPUT_DIR / f"[{ref_id:02d}] {key}.pdf"

        if dest_path.exists():
            size_kb = dest_path.stat().st_size / 1024
            if size_kb < 1.0:
                print(f"   [STALE] Existing file is {size_kb:.1f} KB (likely empty/HTML). Deleting and re-trying.")
                dest_path.unlink()
            else:
                print(f"   [EXISTS] Already downloaded ({size_kb:.1f} KB) — skipping.")
                results["skipped_exists"].append(ref_id)
                continue
        success = download_pdf(pdf_url, dest_path, title)

        if success:
            results["downloaded"].append(ref_id)
        else:
            results["failed"].append(ref_id)
            if note:
                print(f"   [INFO] Manual access: {note}")

        time.sleep(DELAY_BETWEEN)

    # Summary
    print("\n" + "=" * 70)
    print("  DOWNLOAD SUMMARY")
    print("=" * 70)
    print(f"  Successfully downloaded : {len(results['downloaded'])} papers  {results['downloaded']}")
    print(f"  Already existed (skipped): {len(results['skipped_exists'])} papers")
    print(f"  No OA PDF available     : {len(results['no_url'])} papers  {results['no_url']}")
    print(f"  Download failed         : {len(results['failed'])} papers  {results['failed']}")
    print(f"\n  Files saved to: {OUTPUT_DIR}")
    print("=" * 70)

    if results["no_url"] or results["failed"]:
        print("\n  Papers requiring manual download:")
        ids_manual = sorted(set(results["no_url"] + results["failed"]))
        for paper in PAPERS:
            if paper["id"] in ids_manual:
                print(f"    [{paper['id']:02d}] {paper['authors']} ({paper['year']})")
                if paper["note"]:
                    print(f"         {paper['note']}")


if __name__ == "__main__":
    run()
