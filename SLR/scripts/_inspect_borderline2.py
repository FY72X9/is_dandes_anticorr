import csv, os
from pathlib import Path

PAPERS_DIR = Path('SLR/papers')
rows = list(csv.DictReader(open('SLR/scripts/output/slr_borderline.csv', encoding='utf-8')))
above50 = [r for r in rows if float(r['quality_score']) >= 5.0]

print(f"Borderline >= 5.0: {len(above50)} papers\n")
print(f"{'Score':>6}  {'On Disk':>7}  {'Acq Status':>15}  Title / DOI")
print("-"*110)

existing_pdfs = {p.stem.lower(): p.name for p in PAPERS_DIR.glob("*.pdf")}

for r in sorted(above50, key=lambda x: -float(x['quality_score'])):
    score = float(r['quality_score'])
    pdf_fn = r.get('pdf_filename','').strip()
    acq = r.get('acquisition_status','').strip()
    
    # check if on disk by pdf_filename or by title match
    on_disk = "NO"
    if pdf_fn and (PAPERS_DIR / pdf_fn).exists():
        on_disk = "YES(fn)"
    else:
        # fuzzy: check if any existing PDF starts with first 20 chars of title sanitized
        title_frag = r['title'][:25].lower().replace(' ','_')
        title_frag = ''.join(c if c.isalnum() or c=='_' else '_' for c in title_frag)
        for stem in existing_pdfs:
            if stem[:25].lower().startswith(title_frag[:15]):
                on_disk = f"YES({existing_pdfs[stem][:35]})"
                break
    
    oa = r.get('oa_url','').strip()
    url_preview = oa[:60] if oa else "(none)"
    
    print(f"  {score:.2f}  {on_disk:>7}  {acq[:15]:>15}")
    print(f"         Title: {r['title'][:80]}")
    print(f"         DOI  : {r.get('doi','')}")
    print(f"         URL  : {url_preview}")
    print()
