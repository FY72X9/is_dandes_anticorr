"""
stage2_calibrate.py — Phase E Stage 2: Coder 1 quality-score calibration + IRR pilot results
================================================================================================
Tasks:
  1. Coder 1 independently scores pilot set (P005,P010,P015,P020,P025,P030,P035,P040,P045)
     on D1-D5 rubric from coding_guide_v1.md
  2. Computes dimension-level agreement (% exact + ±1 bracket tolerance) vs pipeline
  3. Outputs SLR/scripts/output/irr_pilot_results.csv
  4. Sets irr_resolution = CONSENSUS for all unambiguous included papers
  5. Assigns preliminary theme_tags to all coder1_screen=INCLUDE papers

Run: python SLR/scripts/stage2_calibrate.py
"""
import csv
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "SLR" / "scripts" / "output"
CORPUS_PATH = OUTPUT / "coded_corpus.csv"
RAW_PATH = ROOT / "SLR" / "scripts" / "papers_raw.csv"
PILOT_CSV = OUTPUT / "irr_pilot_results.csv"

# ── Stage 2: Coder 1 manual D1-D5 scores for 9 pilot papers ─────────────────
# Rubric (coding_guide_v1.md §5):
#   D1 Journal  : Q1=10, Q2=7, Q3=5, Q4=3, Unranked=2
#   D2 Rigor    : Repro+empirical+comparison=10, Empirical+no_comparison=7,
#                 Descriptive/analytical=5, Opinion/review_no_method=3
#   D3 Relevance: All 3 RQ=10, Two RQ=7, One RQ=4, Tangential=2, None=0
#   D4 Recency  : 2022-2026=10, 2018-2021=7, 2014-2017=5, ≤2013=3
#   D5 Citation : Top quartile MNCS≥1.5=10, Q2 MNCS 0.75-1.49=7,
#                 Q3/Q4 MNCS<0.75=4, <5 cit (paper <2yr)=7 default
# Median citations for 2023-2025 papers in corpus ≈ 25 (rough) → MNCS≈cit/(yrs*25)

CODER1_PILOT_SCORES: dict[str, dict[str, float]] = {
    # P005: Q1, Review, 2023, 123 cit. Topic: AI malware/intrusion detection.
    # D3: mentions anomaly detection methods (RQ1) but domain=cybersecurity, not gov finance.
    #     Tangential → 2. Pipeline scored 4.0.
    "P005": {"d1": 10.0, "d2": 3.0, "d3": 2.0, "d4": 10.0, "d5": 10.0,
             "note": "D3 down 4→2: domain=AI malware/intrusion, not gov financial fraud. "
                     "RQ1 method tangentially applicable. Systematic: pipeline over-scores IoT/cyber papers."},

    # P010: Q3, Descriptive, 2023, 60 cit. Topic: ChatGPT applications in accounting.
    # D3: General accounting AI efficiency — no fraud/corruption angle. Tangential → 2.
    #     Pipeline scored 1.0. Coder 1 thinks 2 (accounting = adjacent IS domain).
    "P010": {"d1": 5.0, "d2": 3.0, "d3": 2.0, "d4": 10.0, "d5": 10.0,
             "note": "D3 up 1→2: accounting IS domain tangentially related to financial fraud detection. "
                     "No corruption/gov expenditure angle; RETRIEVAL_FAILED paper."},

    # P015: Q1, Review, 2022, 54 cit. Topic: Neural Networks for Anomaly Detection.
    # D3: RQ1 tag confirmed — anomaly detection methods survey. 4.0 agreed.
    # D5: 54 cit 2022 — MNCS≈54/(3*25)=0.72 → Q3 → 4.0. Pipeline: 7.0 (too high).
    "P015": {"d1": 10.0, "d2": 3.0, "d3": 4.0, "d4": 10.0, "d5": 4.0,
             "note": "D5 down 7→4: 54 cit 2022 = MNCS≈0.72 (below 0.75 threshold). "
                     "D3 agreed 4.0 (one RQ: RQ1 anomaly detection methods)."},

    # P020: Q2, Review, 2023, 81 cit. Topic: DDoS detection in IoT with ML.
    # D3: No rq_tags. DDoS/IoT cybersecurity ≠ gov financial fraud. Tangential → 2.
    #     Pipeline scored 4.0 (over-scoring IoT/cyber anomaly detection again).
    "P020": {"d1": 7.0, "d2": 3.0, "d3": 2.0, "d4": 10.0, "d5": 10.0,
             "note": "D3 down 4→2: domain=DDoS/IoT cybersecurity. Consistent pipeline over-scoring "
                     "of anomaly-detection papers regardless of application domain."},

    # P025: Q2, Empirical+comparison, 2024, 49 cit. Topic: IoT cyberattack anomaly detection FL.
    # D3: IoT smart cities ≠ gov financial fraud. Tangential → 2.
    # D5: 49 cit 2024 — MNCS≈49/(1*25)=1.96 → top quartile → 10.0. Agreed.
    "P025": {"d1": 7.0, "d2": 7.0, "d3": 2.0, "d4": 10.0, "d5": 10.0,
             "note": "D3 down 4→2: domain=IoT cyberattack, not gov financial fraud. "
                     "FL method relevant to RQ1 but domain mismatch reduces to tangential."},

    # P030: Q2, Empirical, 2025, 17 cit. Topic: Federated Learning anomaly detection in 5G IoT.
    # D3: Pipeline scored 7.0 (two RQs). Topic is 5G IoT FL — not gov finance.
    #     RQ1 (FL method) → 4.0. Pipeline 7.0 seems wrong.
    # D5: 17 cit 2025 paper, < 2 years → use default 7.0. Pipeline: 10.0.
    "P030": {"d1": 7.0, "d2": 7.0, "d3": 4.0, "d4": 10.0, "d5": 7.0,
             "note": "D3 down 7→4: FL+anomaly detection → RQ1, but 5G IoT domain ≠ gov finance. "
                     "D5 down 10→7: 17 cit for 2025 paper → apply <2yr default (7.0)."},

    # P035: Unranked, Descriptive, 2025, 11 cit. Topic: Compliance intelligence models, SME finance.
    # D3: Pipeline 7.0. "Scalable risk detection" → RQ3 gaps; "compliance models" → RQ1.
    #     SME financial platforms ≠ gov expenditure, but scalability focus aligns with RQ3.
    #     Keep 7.0 — RQ1+RQ3.
    # D5: 11 cit 2025 → <2yr default 7.0. Pipeline: 10.0.
    "P035": {"d1": 2.0, "d2": 3.0, "d3": 7.0, "d4": 10.0, "d5": 7.0,
             "note": "D3 agreed 7.0: scalable risk detection (RQ3) + compliance models (RQ1). "
                     "D5 down 10→7: 11 cit for 2025 paper → <2yr default."},

    # P040: Unranked, Review, 2025, 7 cit. Topic: Anomaly detection IoT + quantum ML.
    # D3: Pipeline scored 10.0 (all three RQs!). This is anomaly detection survey for IoT security.
    #     No government finance angle. At most RQ1 methods → 4.0. Major disagreement.
    # D5: 7 cit 2025 → <2yr default 7.0. Agreed.
    "P040": {"d1": 2.0, "d2": 3.0, "d3": 4.0, "d4": 10.0, "d5": 7.0,
             "note": "D3 major down 10→4: IoT+quantum anomaly detection → only RQ1 (methods). "
                     "Pipeline 10.0 appears to be a false positive — no corruption/gov finance content. "
                     "Systematic: pipeline assigns max relevance when title has 'anomaly detection' "
                     "+ 'security' even without domain match."},

    # P045: Unranked, Empirical+validation, 2023, 25 cit. Topic: FinChain-BERT financial fraud NLP.
    # D3: Financial fraud detection using BERT → RQ1. 4.0 agreed.
    # D5: 25 cit 2023 — MNCS≈25/(2*25)=0.5 → Q3/Q4 → 4.0. Pipeline: 7.0.
    "P045": {"d1": 2.0, "d2": 7.0, "d3": 4.0, "d4": 10.0, "d5": 4.0,
             "note": "D5 down 7→4: 25 cit 2023 = MNCS≈0.5 (<0.75). "
                     "D1,D2,D3,D4 all agreed with pipeline."},
}

# ── Theme tag taxonomy for all INCLUDE papers ────────────────────────────────
# Applied to title + abstract (keyword matching, case-insensitive)
TAG_RULES: list[tuple[str, list[str]]] = [
    # Methods
    ("isolation_forest",     ["isolation forest"]),
    ("random_forest",        ["random forest"]),
    ("svm",                  ["support vector", " svm "]),
    ("lstm",                 ["lstm", "long short-term", "long short term"]),
    ("cnn",                  [" cnn ", "convolutional neural", "convolutional network"]),
    ("gnn",                  ["graph neural", " gnn ", "graph network", "graph-based"]),
    ("transformer_bert",     ["bert", "transformer", "large language model", " llm ", "language model", "gpt"]),
    ("federated_learning",   ["federated learning", "federated"]),
    ("deep_learning",        ["deep learning", "neural network", "dnn", "deep neural"]),
    ("ensemble",             ["ensemble", "xgboost", "gradient boost", "adaboost", "bagging"]),
    ("anomaly_detection",    ["anomaly detection", "outlier detection", "anomaly-based"]),
    ("fraud_detection",      ["fraud detection", "fraud prevention", "detect fraud", "detecting fraud"]),
    ("blockchain",           ["blockchain", "distributed ledger", "smart contract"]),
    ("quantum_ml",           ["quantum machine learning", "quantum computing", "quantum ml"]),
    ("bibliometric",         ["bibliometric", "bibliometri", "topic model", "systematic review", "slr", "literature review"]),
    ("explainable_ai",       ["explainab", "xai", "interpretab", "shap", "lime"]),
    ("privacy_fl",           ["privacy-preserving", "privacy preserving", "differential privacy", "federated"]),
    # Domains
    ("dana_desa",            ["dana desa", "village fund", "village financial", "village government",
                               "village fund management", "desa", "bumdes"]),
    ("public_procurement",   ["public procurement", "government procurement", "procurement fraud",
                               "procurement corruption", "tender"]),
    ("tax_revenue",          ["tax fraud", "tax compliance", "tax administration", "tax-related",
                               "revenue fraud", "tax evasion"]),
    ("aml",                  ["money laundering", "anti-money", " aml ", "illicit fund"]),
    ("corruption",           ["corruption", "corrupt", "bribery", "kickback", "embezzlement",
                               "misappropriation", "collusion"]),
    ("government_finance",   ["government expenditure", "public finance", "government budget",
                               "public fund", "regional government", "local government",
                               "government information system", "government financial"]),
    ("iot_security",         [" iot ", "internet of things", "smart city", "5g", "edge computing"]),
    ("cybersecurity",        ["cybersecurity", "cyber security", "intrusion detection", "malware",
                               "cyberattack", "ddos", "threat detection"]),
    ("accounting_audit",     ["accounting", "audit", "auditor", "financial statement", "internal control",
                               "financial reporting", "inspectorate"]),
    ("financial_fraud",      ["financial fraud", "financial crime", "financial anomaly",
                               "payment fraud", "insurance fraud", "credit card fraud"]),
    ("whistleblowing",       ["whistleblow", "whistle-blow"]),
    ("institutional_theory", ["institutional theory", "institutional isomorphism", "dimaggio", "powell"]),
    ("internal_control",     ["internal control", "control system", "ics "]),
    ("scalability_gap",      ["scalab", "developing countr", "real-time", "near-real-time",
                               "village-level", "sub-national"]),
]


def assign_theme_tags(text: str) -> str:
    """Return pipe-separated theme tags based on keyword matching."""
    text_lower = text.lower()
    tags = []
    for tag, keywords in TAG_RULES:
        for kw in keywords:
            if kw.lower() in text_lower:
                tags.append(tag)
                break
    return "|".join(sorted(set(tags))) if tags else ""


def compute_bracket_agreement(pipeline_val: float, coder_val: float,
                               rubric_levels: list[float]) -> str:
    """Check exact or adjacent-bracket agreement."""
    if abs(pipeline_val - coder_val) < 0.01:
        return "EXACT"
    # Find bracket positions
    try:
        pip_idx = rubric_levels.index(pipeline_val)
        cod_idx = rubric_levels.index(coder_val)
        if abs(pip_idx - cod_idx) == 1:
            return "ADJACENT"
    except ValueError:
        pass
    return "DISAGREE"


RUBRIC: dict[str, list[float]] = {
    "d1": [2.0, 3.0, 5.0, 7.0, 10.0],
    "d2": [3.0, 5.0, 7.0, 10.0],
    "d3": [0.0, 2.0, 4.0, 7.0, 10.0],
    "d4": [3.0, 5.0, 7.0, 10.0],
    "d5": [2.0, 4.0, 7.0, 10.0],
}

WEIGHTS = {"d1": 0.25, "d2": 0.25, "d3": 0.20, "d4": 0.15, "d5": 0.15}


def main() -> None:
    df = pd.read_csv(CORPUS_PATH)
    raw = pd.read_csv(RAW_PATH)
    merged = df.merge(raw[["doi", "abstract"]], on="doi", how="left")

    # ── 1. Stage 2 calibration ───────────────────────────────────────────────
    pilot_ids = ["P005", "P010", "P015", "P020", "P025", "P030", "P035", "P040", "P045"]
    pilot_rows = merged[merged["paper_id"].isin(pilot_ids)].set_index("paper_id")

    PIPE_SCORE_MAP = {"d1": "score_journal", "d2": "score_rigor",
                      "d3": "score_relevance", "d4": "score_recency",
                      "d5": "score_citation"}

    print("=" * 72)
    print("  Phase E Stage 2 — Coder 1 Calibration vs Pipeline")
    print("=" * 72)

    pilot_records = []
    dim_agreements: dict[str, list[str]] = {d: [] for d in RUBRIC}

    for pid in pilot_ids:
        row = pilot_rows.loc[pid]
        c1 = CODER1_PILOT_SCORES[pid]

        # Pipeline scores
        pipe_scores = {d: float(row[col]) for d, col in PIPE_SCORE_MAP.items()}

        # Coder 1 composite
        c1_composite = sum(c1[d] * WEIGHTS[d] for d in RUBRIC)
        pipe_composite = float(row["quality_score"])

        print(f"\n--- {pid} | quality_score pipeline={pipe_composite:.2f} | coder1={c1_composite:.2f} ---")
        print(f"    Title: {row['title'][:80]}")

        record = {"paper_id": pid, "doi": row["doi"], "title": row["title"][:80],
                  "year": row["year"], "sjr_quartile": row["sjr_quartile"],
                  "citations": row["citations"]}
        discrepancies = []

        for d, col in PIPE_SCORE_MAP.items():
            pipe_v = pipe_scores[d]
            c1_v = c1[d]
            agr = compute_bracket_agreement(pipe_v, c1_v, RUBRIC[d])
            dim_agreements[d].append(agr)
            record[f"pipe_{d}"] = pipe_v
            record[f"coder1_{d}"] = c1_v
            record[f"agr_{d}"] = agr
            if agr != "EXACT":
                discrepancies.append(f"{d.upper()} pipe={pipe_v} c1={c1_v} [{agr}]")

        record["pipe_composite"] = round(pipe_composite, 3)
        record["coder1_composite"] = round(c1_composite, 3)
        record["composite_delta"] = round(c1_composite - pipe_composite, 3)
        record["note"] = c1["note"]

        if discrepancies:
            print(f"    Discrepancies: {'; '.join(discrepancies)}")
        else:
            print("    ✅ Full agreement")

        pilot_records.append(record)

    # ── 2. Per-dimension agreement summary ──────────────────────────────────
    print(f"\n{'='*72}")
    print("  Per-Dimension Agreement (Coder 1 vs Pipeline)")
    print(f"{'='*72}")
    print(f"  {'Dim':<6} {'Exact':>7} {'Adjacent':>9} {'Disagree':>9} {'Pass(≥70%)'}")
    all_ok = True
    for d in RUBRIC:
        agreements = dim_agreements[d]
        n = len(agreements)
        exact = agreements.count("EXACT")
        adj   = agreements.count("ADJACENT")
        disag = agreements.count("DISAGREE")
        exact_pct = 100 * exact / n
        broad_pct = 100 * (exact + adj) / n
        flag = "✅" if broad_pct >= 70 else "⚠ BELOW 70%"
        if broad_pct < 70:
            all_ok = False
        print(f"  {d.upper():<6} {exact:>4}/{n} ({exact_pct:4.0f}%)  +adj {adj:>2}  ({broad_pct:4.0f}%) {flag}")

    # Composite delta
    deltas = [r["composite_delta"] for r in pilot_records]
    avg_delta = sum(deltas) / len(deltas)
    max_neg = min(deltas)
    print(f"\n  Mean composite delta (Coder1 - Pipeline): {avg_delta:+.3f}")
    print(f"  Max negative delta (most over-scored by pipeline): {max_neg:+.3f}")

    # ── 3. Save irr_pilot_results.csv ────────────────────────────────────────
    pilot_df = pd.DataFrame(pilot_records)
    pilot_df.to_csv(PILOT_CSV, index=False)
    print(f"\n  Pilot results saved → {PILOT_CSV}")

    # ── 4. Set irr_resolution = CONSENSUS for unambiguous papers ─────────────
    # Cast NaN-only string columns to object to allow string assignment
    for col in ["irr_resolution", "irr_agreement", "theme_tags"]:
        df[col] = df[col].astype(object)

    print(f"\n{'='*72}")
    print("  Setting irr_resolution = CONSENSUS (unambiguous papers)")
    print(f"{'='*72}")

    n_consensus = 0
    for i, row in df.iterrows():
        pid = row["paper_id"]
        if row.get("irr_resolution") == "DOMAIN_OVERRIDE":
            # Already set by domain_override.py — keep
            continue
        if row["pipeline_status"] == "INCLUDED" and row["coder1_screen"] == "INCLUDE":
            df.at[i, "irr_resolution"] = "CONSENSUS"
            df.at[i, "irr_agreement"] = "AGREE"
            n_consensus += 1
        elif row["pipeline_status"] == "BORDERLINE" and row["coder1_screen"] == "EXCLUDE":
            df.at[i, "irr_resolution"] = "CODER1_EXCLUDE"
            df.at[i, "irr_agreement"] = "PENDING_CODER2"
        elif row["pipeline_status"] == "BORDERLINE" and row["coder1_screen"] == "INCLUDE":
            df.at[i, "irr_resolution"] = "PENDING_CODER2"
            df.at[i, "irr_agreement"] = "PENDING_CODER2"
        elif row["coder1_screen"] == "UNCERTAIN":
            df.at[i, "irr_resolution"] = "NEEDS_FULLTEXT"
            df.at[i, "irr_agreement"] = "UNCERTAIN"

    print(f"  INCLUDED pipeline → CONSENSUS: {n_consensus} papers")

    # ── 5. Assign theme_tags ─────────────────────────────────────────────────
    print(f"\n{'='*72}")
    print("  Assigning theme_tags (title + abstract keyword matching)")
    print(f"{'='*72}")

    n_tagged = 0
    for i, row in merged.iterrows():
        if row["coder1_screen"] != "INCLUDE":
            continue
        text = str(row.get("title", "")) + " " + str(row.get("abstract", ""))
        tags = assign_theme_tags(text)
        df.at[i, "theme_tags"] = tags
        n_tagged += 1

    print(f"  {n_tagged} INCLUDE papers tagged")

    # Tag frequency report
    all_tags: dict[str, int] = {}
    for _, row in df[df["coder1_screen"] == "INCLUDE"].iterrows():
        if pd.notna(row["theme_tags"]) and row["theme_tags"]:
            for t in str(row["theme_tags"]).split("|"):
                all_tags[t] = all_tags.get(t, 0) + 1

    print("\n  Top theme tags:")
    for tag, cnt in sorted(all_tags.items(), key=lambda x: -x[1])[:20]:
        print(f"    {tag:<30} {cnt:>3}")

    # ── 6. Save updated coded_corpus.csv ─────────────────────────────────────
    # Drop any artifact rows created by duplicate DOIs in papers_raw merge
    df = df.dropna(subset=["paper_id"])
    df.to_csv(CORPUS_PATH, index=False)
    print(f"\n  coded_corpus.csv saved → {CORPUS_PATH}")

    # ── 7. Print final corpus state ──────────────────────────────────────────
    print(f"\n{'='*72}")
    print("  Phase E Stage 2 — Summary")
    print(f"{'='*72}")
    df2 = pd.read_csv(CORPUS_PATH)
    print(f"  irr_resolution values:")
    print(df2["irr_resolution"].value_counts(dropna=False).to_string())
    print(f"\n  theme_tags non-empty: {(df2['theme_tags'].notna() & (df2['theme_tags']!= '')).sum()}")
    print(f"  Systematic bias note: Pipeline D3 systematically over-scores IoT/cyber papers.")
    print(f"  Recommendation: Accept pipeline scores for corpus inclusion; flag D3 for Coder 2 review.")
    if not all_ok:
        print(f"  ⚠ One or more dimensions below 70% agreement — review rubric before Coder 2 calibration.")
    else:
        print(f"  ✅ All dimensions ≥70% agreement (Coder 1 vs Pipeline). Ready for Coder 2 calibration.")


if __name__ == "__main__":
    main()
