import pandas as pd, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
corpus = pd.read_csv(os.path.join(BASE,"scripts","output","coded_corpus.csv"))
codes  = pd.read_csv(os.path.join(BASE,"analysis","themes","open_codes_master.csv"))
fm     = pd.read_csv(os.path.join(BASE,"scripts","output","framework_synthesis_matrix.csv"))
cluster= pd.read_csv(os.path.join(BASE,"analysis","bibliometric","cluster_separation.csv"))
inc    = corpus[corpus["irr_resolution"].isin(["CONSENSUS","DOMAIN_OVERRIDE"])]
ids_inc  = set(inc["paper_id"].unique())
ids_code = set(codes["paper_id"].unique())
ids_fm   = set(fm["paper_id"].unique())
ids_cl   = set(cluster["paper_id"].unique())
years = pd.to_numeric(inc["year"], errors="coerce").dropna().astype(int)
qs    = pd.to_numeric(inc["quality_score"], errors="coerce")
print("=== CONSISTENCY CHECKS ===")
print(f"Corpus INCLUDE:    {len(inc)}")
print(f"Codes unique IDs:  {len(ids_code)}")
print(f"FM unique IDs:     {len(ids_fm)}")
print(f"Cluster unique IDs:{len(ids_cl)}")
print(f"Year range:        {years.min()} - {years.max()}")
print()
print("IDs in codes NOT in corpus:", ids_code - ids_inc)
print("IDs in FM NOT in corpus:   ", ids_fm - ids_inc)
print("Corpus IDs NOT in codes:   ", ids_inc - ids_code)
print("Corpus IDs NOT in FM:      ", ids_inc - ids_fm)
print("Corpus IDs NOT in cluster: ", ids_inc - ids_cl)
print()
bridging = ["P001","P016","P037","P043","P050","P065","P089","P093","P096"]
print("AT1 bridging papers in corpus:")
for pid in bridging:
    print(f"  {pid}: {'YES' if pid in ids_inc else 'NOT IN CORPUS'}")
print()
print(f"quality_score: min={qs.min():.2f} max={qs.max():.2f} mean={qs.mean():.2f}")
print(f"  >=4.0:{(qs>=4.0).sum()}  >=4.5:{(qs>=4.5).sum()}  >=5.0:{(qs>=5.0).sum()}")
print()
print("DSR cycle dist (from FM, inc papers only):")
inc_fm = fm[fm["paper_id"].isin(ids_inc)]
print(inc_fm["dsr_cycle_primary"].value_counts().to_string())
print()
# Check AT3 claim: 28/45 IST-NONE
ist_none = codes[codes["code"]=="IST-NONE"]["paper_id"].nunique()
print(f"IST-NONE papers in codes: {ist_none} (claimed: 28)")
# Check AT1 cluster sizes claimed in text
ml_codes  = ["MC-IF","MC-LOF","MC-AE","MC-GNN","MC-DL","MC-RF","MC-GBM","MC-SVM","MC-LSTM","MC-UNSUP"]
gov_codes = ["CTX-VILLAGE","DS-DANDES","IST-AT","IST-IT","CTX-GOVPUB","CTX-PROCU","DS-GOVERN"]
ml_pids  = set(codes[codes["code"].isin(ml_codes)]["paper_id"].unique()) & ids_inc
gov_pids = set(codes[codes["code"].isin(gov_codes)]["paper_id"].unique()) & ids_inc
brg_pids = ml_pids & gov_pids
print(f"ML cluster:  {len(ml_pids)} (claimed: 23)")
print(f"Gov cluster: {len(gov_pids)} (claimed: 26)")
print(f"Bridging:    {len(brg_pids)} (claimed: 9)")
print(f"Bridging IDs: {sorted(brg_pids)}")
print()
# DT5 count
dt_csv = pd.read_csv(os.path.join(BASE,"analysis","themes","descriptive_themes_matrix.csv"))
dt5 = dt_csv[dt_csv["dt_id"]=="DT5"]
if len(dt5):
    pids5 = [p for p in str(dt5.iloc[0]["paper_ids"]).split("|") if p]
    print(f"DT5 papers: {len(pids5)} (claimed: 26)")
# Sensitivity: DT5 drops at T2 threshold (critical finding)
print()
print("Sensitivity concern — DT5 at T2 (>=4.5):")
inc45 = inc[qs >= 4.5]["paper_id"].tolist()
dt5_at_t2 = set(pids5) & set(inc45)
print(f"  DT5 papers surviving T2: {len(dt5_at_t2)} (report says: 4)")
print(f"  IDs: {sorted(dt5_at_t2)}")
