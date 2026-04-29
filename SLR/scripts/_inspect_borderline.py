import csv

rows = list(csv.DictReader(open('SLR/scripts/output/slr_borderline.csv', encoding='utf-8')))
above55 = [r for r in rows if float(r['quality_score']) >= 5.5]
above50 = [r for r in rows if 5.0 <= float(r['quality_score']) < 5.5]
print(f"Score >= 5.5: {len(above55)}")
print(f"Score 5.0-5.49: {len(above50)}")
print(f"Total borderline: {len(rows)}")
print()
print("=== Score >= 5.5 ===")
for r in sorted(above55, key=lambda x: -float(x['quality_score'])):
    has_url = "YES" if r.get('oa_url','').strip() else "NO"
    print(f"  [{float(r['quality_score']):.2f}] {r['title'][:70]}")
    print(f"         doi={r.get('doi','')} | oa_url={has_url} | journal={r.get('journal','')[:40]}")
print()
print("=== Score 5.0-5.49 ===")
for r in sorted(above50, key=lambda x: -float(x['quality_score'])):
    has_url = "YES" if r.get('oa_url','').strip() else "NO"
    print(f"  [{float(r['quality_score']):.2f}] {r['title'][:70]}")
    print(f"         doi={r.get('doi','')} | oa_url={has_url}")
