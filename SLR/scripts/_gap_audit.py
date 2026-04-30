import pandas as pd, os

inc = pd.read_csv('SLR/scripts/output/slr_included_corpus.csv')
papers_dir = 'SLR/papers'
on_disk = set(os.listdir(papers_dir))

missing = []
for _, r in inc.iterrows():
    fn = str(r.get('pdf_filename',''))
    if fn in ('nan','') or fn not in on_disk:
        score = r['quality_score']
        title = str(r['title'])[:65]
        doi   = r['doi']
        missing.append((score, title, doi, fn))

print(f"Included papers with PDF missing from disk: {len(missing)} / {len(inc)}")
for score, title, doi, fn in sorted(missing, key=lambda x: float(x[0]), reverse=True):
    print(f"  score={score}  {title}")
    print(f"         doi={doi}")
