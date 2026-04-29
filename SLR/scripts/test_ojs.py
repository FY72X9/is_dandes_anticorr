"""Download remaining fixable papers."""
import re
import requests
from pathlib import Path
from curl_cffi import requests as cf

PDF_DIR = Path(__file__).parent.parent / "papers"


def save(name, content, slug):
    dest = PDF_DIR / f"{slug}.pdf"
    if content[:4] == b"%PDF" and len(content) > 8000:
        dest.write_bytes(content)
        print(f"  SAVED {name}: {len(content)//1024} KB -> {dest.name}")
        return True
    print(f"  NOT PDF {name}: size={len(content)}, head={content[:8]!r}")
    return False


# --- Test 1: Emerald (OpenAlex URL confirmed 200 OK PDF) ---
print("\n[20] Emerald JOPP bibliometric")
emerald_url = "https://www.emerald.com/insight/content/doi/10.1108/JOPP-06-2022-0031/full/pdf?title=the-landscape-of-public-procurement-research-a-bibliometric-analysis-and-topic-modelling-based-on-scopus"
r = cf.get(emerald_url, impersonate="chrome", timeout=20)
save("Emerald JOPP", r.content, "The_landscape_of_public_procurement_research__a_b")


# --- Test 2: UMM ejournal.umm.ac.id - find galley ID from HTML then try download ---
print("\n[18] UMM JAA fraud determinants")
r2 = cf.get("https://ejournal.umm.ac.id/index.php/jaa/article/view/36914", impersonate="chrome", timeout=12)
# Find download link in HTML
matches = re.findall(r'href=["\']([^"\']*(?:download|/pdf)[^"\']*36914[^"\']*)["\'\s]', r2.text, re.I)
print(f"  Found links: {matches[:5]}")
# Try common OJS3 download patterns
for suffix in ["/36914/15606", "/36914/15607", "/36914/15608", "/36914/0"]:
    base = "https://ejournal.umm.ac.id/index.php/jaa/article/download"
    r3 = cf.get(base + suffix, impersonate="chrome", timeout=10, allow_redirects=True)
    if r3.content[:4] == b"%PDF" and len(r3.content) > 8000:
        save("UMM JAA", r3.content, "Determinants_of_fraud_in_the_village_government__t")
        break
    else:
        print(f"  {suffix}: HTTP {r3.status_code}, size={len(r3.content)}, head={r3.content[:6]!r}")


# --- Test 3: ijcat.com - SSL self-signed, try requests verify=False ---
print("\n[22] ijcat.com Securing Government Revenue")
try:
    import urllib3
    urllib3.disable_warnings()
    r4 = requests.get(
        "https://ijcat.com/archieve/volume14/issue5/ijcatr14051008.pdf",
        verify=False, timeout=15,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    save("ijcat", r4.content, "Securing_Government_Revenue__A_Cloud-Based_AI_Mode")
except Exception as e:
    print(f"  ERROR: {e}")


# --- Test 4: nblformosa - check correct article URL from DOI ---
print("\n[19] nblformosa ijbae")
try:
    r5 = requests.get("https://doi.org/10.55927/ijbae.v4i3.150", verify=False, timeout=12, allow_redirects=True)
    print(f"  DOI resolved to: {r5.url}")
    # Try download link from HTML
    m = re.findall(r'href=["\']([^"\']*(?:download|\.pdf)[^"\']*)["\']', r5.text, re.I)
    print(f"  PDF/download links: {m[:4]}")
except Exception as e:
    print(f"  ERROR: {e}")




def find_pdf_links(html, base_url=""):
    """Find PDF/download links in HTML."""
    results = []
    for pat in [
        r'href=["\']([^"\']*download[^"\']*)["\']',
        r'href=["\']([^"\']*\.pdf[^"\']*)["\']',
        r'href=["\']([^"\']*galley[^"\']*)["\']',
        r'href=["\']([^"\']*article/view[^"\']*)["\']',
    ]:
        matches = re.findall(pat, html, re.I)
        results.extend(matches)
    # dedupe
    seen = set()
    out = []
    for r in results:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out[:8]


# Test 1: UMM journal (200 OK but no PDF link found previously)
print("=== UMM ac.id ===")
r = cf.get("https://ejournal.umm.ac.id/index.php/jaa/article/view/36914", impersonate="chrome", timeout=12)
links = find_pdf_links(r.text)
print(f"HTTP {r.status_code}, links: {links}")
# Check common OJS download path
for suffix in ["/36914/pdf", "/36914/26519", "/36914/26520"]:
    direct = "https://ejournal.umm.ac.id/index.php/jaa/article/download" + suffix
    r2 = cf.get(direct, impersonate="chrome", timeout=10)
    print(f"  direct {suffix}: HTTP {r2.status_code}, size={len(r2.content)}, head={r2.content[:5]!r}")

# Test 2: ijcat.com (SSL error) - try with verify=False
print("\n=== ijcat.com ===")
try:
    r3 = stdlib_req.get("https://doi.org/10.7753/ijcatr1405.1007", verify=False, timeout=10, allow_redirects=True)
    print(f"doi redirect: HTTP {r3.status_code} -> {r3.url[:80]}")
    links3 = find_pdf_links(r3.text)
    print(f"  PDF links: {links3}")
except Exception as e:
    print(f"  ERROR: {e}")

# Test 3: OpenAlex for paywalled papers - check if any have OA copy
print("\n=== OpenAlex OA check for paywalled ===")
paywall_dois = [
    ("Elsevier IS procurement", "10.1016/j.is.2023.102284"),
    ("Wiley JCAF ChatGPT", "10.1002/jcaf.22663"),
    ("Emerald JOPP bibliometric", "10.1108/jopp-06-2022-0031"),
    ("IGI JCIT AML graph", "10.4018/jcit.316665"),
    ("Elsevier JEconC shell co", "10.1016/j.jeconc.2024.100123"),
]
for name, doi in paywall_dois:
    r4 = stdlib_req.get(f"https://api.openalex.org/works/https://doi.org/{doi}", timeout=8)
    if r4.status_code == 200:
        d = r4.json()
        oa = d.get("open_access", {})
        best = d.get("best_oa_location") or {}
        pdf = best.get("pdf_url") or oa.get("oa_url")
        print(f"  {name}: {pdf}")
    else:
        print(f"  {name}: OpenAlex HTTP {r4.status_code}")

