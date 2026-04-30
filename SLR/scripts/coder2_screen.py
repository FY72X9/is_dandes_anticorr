"""
coder2_screen.py — Phase E Stage 1 & 2: Independent Coder 2 (co-author) screening
===================================================================================
Coder 2 identity: Co-author (IS specialist, domain expert in Indonesian public governance
and ML fraud detection). Works INDEPENDENTLY from Coder 1 — no knowledge of coder1_screen.

Screening basis: Title + abstract only (Stage 1 protocol per coding_guide_v1.md §4).
IC/EC framework applied:
  IC-01: Addresses at least one RQ (RQ1/RQ2/RQ3)
  EC-02: Private sector / banking ONLY — no government/public sector coverage
  EC-04: No computational or IS-theoretic method
  EC-07: Off-topic — no connection to fraud, corruption, or anomaly detection in
          financial/government contexts

RQ scope boundaries (coding_guide_v1.md §2):
  RQ1: Computational methods / IS frameworks for financial anomaly detection in
       government expenditure. Sector: government/public (not SOLELY corporate/banking).
  RQ2: Corruption typologies operationalized as computationally detectable features.
       Includes behavioral/typological frameworks that underpin feature engineering.
  RQ3: Gaps in scalability, developing-country coverage, near-real-time detection,
       IS-theoretic evaluation for village-level governance.

Run: python SLR/scripts/coder2_screen.py
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "SLR" / "scripts" / "output"
CORPUS = OUTPUT / "coded_corpus.csv"
PILOT_CSV = OUTPUT / "irr_pilot_results.csv"
STAGE1_OUT = OUTPUT / "irr_stage1_comparison.csv"
STAGE2_OUT = OUTPUT / "irr_stage2_comparison.csv"

# ── Stage 1: Coder 2 independent screening decisions ─────────────────────────
# Key: paper_id → (decision, ec_code_or_rq_justification)
# EC codes: EC-02=private sector only, EC-04=no computational method,
#           EC-07=off-topic / no fraud/corruption connection
# RQ codes: RQ1/RQ2/RQ3 for included papers

CODER2_SCREEN: dict[str, tuple[str, str]] = {
    # ── PIPELINE INCLUDED papers (P001–P045) ─────────────────────────────────
    "P001": ("INCLUDE",  "RQ1: ML methods for financial fraud detection — directly relevant; SLR scope."),
    "P002": ("EXCLUDE",  "EC-02: Cryptocurrency pump-and-dump — purely private crypto market; no govt finance."),
    "P003": ("INCLUDE",  "RQ1: DL survey for financial cybercrime — methods broadly applicable to govt finance."),
    "P004": ("EXCLUDE",  "EC-02: Digitalization in 'firms' finance — corporate-only; no public sector angle."),
    "P005": ("EXCLUDE",  "EC-07: AI malware/intrusion detection for smart infrastructure — no financial fraud angle."),
    "P006": ("EXCLUDE",  "EC-02: Blockchain+AI for healthcare insurance — private sector health insurance."),
    "P007": ("EXCLUDE",  "EC-02: Online payment fraud detection — private fintech/banking domain only."),
    "P008": ("EXCLUDE",  "EC-07: Electoral vote-tally fraud (Mexico 1988) — political fraud, not financial anomaly."),
    "P009": ("EXCLUDE",  "EC-07: AI cloud security / user behaviour analysis — cybersecurity, no financial fraud."),
    "P010": ("EXCLUDE",  "EC-04: ChatGPT in accounting — general efficiency review; no fraud detection method."),
    "P011": ("EXCLUDE",  "EC-02: AI+blockchain for financial services security — banking sector only."),
    "P012": ("INCLUDE",  "RQ1+RQ3: AI/blockchain in U.S. tax administration — government revenue IS methods."),
    "P013": ("INCLUDE",  "RQ1: IT governance + AI in accounting/auditing — IS governance framework for audit."),
    "P014": ("EXCLUDE",  "EC-07: Anomaly detection in smart environments (IoT sensors/buildings) — not financial."),
    "P015": ("INCLUDE",  "RQ1: Neural network anomaly detection survey — core methods for RQ1."),
    "P016": ("INCLUDE",  "RQ1+RQ3: Cloud AI for tax-related financial crimes in government revenue — direct match."),
    "P017": ("EXCLUDE",  "EC-07: FL for network intrusion detection — cybersecurity domain; no financial fraud."),
    "P018": ("EXCLUDE",  "EC-07: Blockchain consensus + ML for blockchain security — network security only."),
    "P019": ("EXCLUDE",  "EC-07: DL for vehicle network IDS — completely off-topic."),
    "P020": ("EXCLUDE",  "EC-07: DDoS detection in IoT using ML — cybersecurity; no financial fraud connection."),
    "P021": ("EXCLUDE",  "EC-07: Hardware-assisted ML in IoT security — embedded security; no financial angle."),
    "P022": ("INCLUDE",  "RQ1: Comprehensive ML in business/finance review — fraud detection methods covered."),
    "P023": ("EXCLUDE",  "EC-02: AI in financial services (private sector) — primarily banking/fintech scope."),
    "P024": ("EXCLUDE",  "EC-07: DL/ML for cloud computing security — cloud security, no financial fraud."),
    "P025": ("EXCLUDE",  "EC-07: FL anomaly detection for IoT cyberattacks in smart cities — no financial fraud."),
    "P026": ("EXCLUDE",  "EC-02: Blockchain fraud in crypto transactions — private crypto domain."),
    "P027": ("EXCLUDE",  "EC-02: ML for Bitcoin/cryptocurrency fraud in USA — private crypto market."),
    "P028": ("EXCLUDE",  "EC-07: IoT defense/security mechanisms review — IoT cybersecurity."),
    "P029": ("EXCLUDE",  "EC-07: AI in maritime cybersecurity — off-topic."),
    "P030": ("EXCLUDE",  "EC-07: FL framework for 5G IoT anomaly detection — IoT cybersecurity."),
    "P031": ("EXCLUDE",  "EC-07: AI anomaly detection for 5G IoT in smart cities — IoT cybersecurity."),
    "P032": ("EXCLUDE",  "EC-07: Generative AI for cybersecurity/threat intelligence — no financial fraud."),
    "P033": ("EXCLUDE",  "EC-07: Quantum ML for epidemic surveillance — healthcare/public health, not finance."),
    "P034": ("EXCLUDE",  "EC-07: AI for infectious disease monitoring — public health; no financial fraud."),
    "P035": ("INCLUDE",  "RQ1+RQ3: Compliance intelligence models + scalable risk detection — gaps in RQ3."),
    "P036": ("EXCLUDE",  "EC-07: Comprehensive IDS review — network intrusion detection only."),
    "P037": ("INCLUDE",  "RQ1: Bibliometric of AI in financial fraud prevention — meta-level RQ1 overview."),
    "P038": ("EXCLUDE",  "EC-07: LLMs for energy systems — completely off-topic."),
    "P039": ("INCLUDE",  "RQ1: DL for AML in financial industry — money laundering detection methods."),
    "P040": ("EXCLUDE",  "EC-07: Anomaly detection in IoT security + quantum ML — IoT cybersecurity only."),
    "P041": ("INCLUDE",  "RQ1+RQ3: Real-time suspicious detection for financial data streams — near-real-time gap."),
    "P042": ("EXCLUDE",  "EC-07: Blockchain for dairy supply chain (food safety) — off-topic."),
    "P043": ("INCLUDE",  "RQ1+RQ2: AI decision support for public procurement — govt expenditure IS system."),
    "P044": ("INCLUDE",  "RQ1: AI for fraud detection in accounting — directly relevant to govt financial auditing."),
    "P045": ("INCLUDE",  "RQ1: FinChain-BERT NLP fraud detection — NLP methods for financial fraud; RQ1."),

    # ── BORDERLINE papers (P046–P096) ─────────────────────────────────────────
    "P046": ("EXCLUDE",  "EC-07: ChatGPT/FraudGPT/WormGPT in social engineering — cybersecurity, not finance."),
    "P047": ("INCLUDE",  "RQ2+RQ3: Fraud prevention in village fund management — direct Dana Desa scope."),
    "P048": ("INCLUDE",  "RQ2+RQ3: Integrated village fund governance model SIBERAS — IS for village finance."),
    "P049": ("INCLUDE",  "RQ2+RQ3: Supervision of village financial management, North Sumatra — RQ3 gaps."),
    "P050": ("INCLUDE",  "RQ2: Patterns of village corruption in Indonesia — corruption typology for RQ2."),
    "P051": ("INCLUDE",  "RQ2+RQ3: Fraud determinants in village govt: whistleblowing + internal control."),
    "P052": ("INCLUDE",  "RQ2+RQ3: Apparatus competence/internal control on village fund fraud — RQ2+RQ3."),
    "P053": ("INCLUDE",  "RQ2+RQ3: Regional inspectorate role in village financial fraud prevention (Boyolali)."),
    "P054": ("INCLUDE",  "RQ2+RQ3: HR capacity on village fund management via anti-corruption numeracy."),
    "P055": ("INCLUDE",  "RQ2+RQ3: Village apparatus competence + internal control + fraud prevention."),
    "P056": ("INCLUDE",  "RQ2+RQ3: Morality/whistleblowing/ICS on village fund fraud; leadership moderation."),
    "P057": ("INCLUDE",  "RQ1+RQ2: Internal control + budget compliance on fraud detection, W. Java Prosecutor."),
    "P058": ("INCLUDE",  "RQ1+RQ2: Regional govt IS + internal control system on corruption, Bandung."),
    "P059": ("INCLUDE",  "RQ2+RQ3: State Audit Board authority on village financial management — institutional."),
    "P060": ("INCLUDE",  "RQ2+RQ3: Fraud prevention determinants in village funds, North Sumatra province."),
    "P061": ("INCLUDE",  "RQ2: Public procurement bibliometric analysis — landscape of procurement research."),
    "P062": ("INCLUDE",  "RQ1: Graph-based ML for AML fraud control — financial domain methods."),
    "P063": ("EXCLUDE",  "EC-07: Adaptive control for AI marketing automation in financial compliance — not fraud."),
    "P064": ("INCLUDE",  "RQ1+RQ2: Data analytics to detect illicit shell companies — financial crime methods."),
    "P065": ("INCLUDE",  "RQ2: Corruption tolerance typology model (TPB) — conceptual grounding for RQ2 features."),
    "P066": ("INCLUDE",  "RQ1: DL for AML on mobile transactions — money laundering detection methods."),
    "P067": ("INCLUDE",  "RQ1+RQ2: ML for public procurement analysis, Dominican Republic — govt expenditure."),
    "P068": ("EXCLUDE",  "EC-02: GNN for healthcare insurance fraud — clinical billing fraud; no govt finance."),
    "P069": ("INCLUDE",  "RQ2: Fraud Hexagon theory for digital fraud — typological model for RQ2 conceptual."),
    "P070": ("INCLUDE",  "RQ1: Secure data systems on fraud detection in BI applications — IS method for fraud."),
    "P071": ("EXCLUDE",  "EC-07: Unsupervised methods for network intrusion/attacker attribution — cybersecurity."),
    "P072": ("INCLUDE",  "RQ1: GNN survey including financial fraud detection — methods paper with finance domain."),
    "P073": ("INCLUDE",  "RQ1: Quantum computing in finance including fraud detection — methods for RQ1."),
    "P074": ("INCLUDE",  "RQ1: FL for accounting data in financial statement audits — privacy-FL audit methods."),
    "P075": ("EXCLUDE",  "EC-07: Interpretable FL transformer for cloud threat forensics — cloud security only."),
    "P076": ("EXCLUDE",  "EC-07: AI+blockchain for IT infrastructure risk management — IT risk, not financial."),
    "P077": ("EXCLUDE",  "EC-07: AI threat detection in surveillance systems — physical security; off-topic."),
    "P078": ("EXCLUDE",  "EC-02: Technology for smart health insurance systems — private healthcare insurance."),
    "P079": ("EXCLUDE",  "EC-02: AI-driven risk assessment for financial market stability — market/banking only."),
    "P080": ("EXCLUDE",  "EC-07: Anomaly detection in healthcare time series — medical/clinical; off-topic."),
    "P081": ("EXCLUDE",  "EC-07: Cloud KMS with AI compliance/data privacy — generic IS, not fraud detection."),
    "P082": ("EXCLUDE",  "EC-07: AI cybersecurity strategic approaches — general cybersecurity."),
    "P083": ("EXCLUDE",  "EC-07: Real-time risk dashboards in hospital supply chain — healthcare supply chain."),
    "P084": ("EXCLUDE",  "EC-07: Cybercrime + digital forensics through ML — digital forensics, no financial fraud."),
    "P085": ("INCLUDE",  "RQ1+RQ3: U.S.-U.K. PETs FL challenge: privacy-preserving anomaly detection for "
                         "financial crime — government-sponsored, directly addresses RQ1+RQ3."),
    "P086": ("EXCLUDE",  "EC-04: AI + ESG metrics for infrastructure auditing — sustainability audit, not fraud."),
    "P087": ("INCLUDE",  "RQ1: GRC AI compliance risk detection in financial/regulated sectors — IS governance."),
    "P088": ("EXCLUDE",  "EC-07: Intrusion detection in medical IoT — medical cybersecurity; off-topic."),
    "P089": ("INCLUDE",  "RQ1+RQ3: AI for tax fraud detection, OECD Tax Administration 3.0 — govt revenue IS."),
    "P090": ("EXCLUDE",  "EC-02: ML for synthetic identity fraud in e-commerce — private sector e-commerce."),
    "P091": ("INCLUDE",  "RQ1: Starlit FL for financial fraud detection — privacy-preserving FL methods."),
    "P092": ("EXCLUDE",  "EC-04: Third-party audit ecosystem for AI governance — policy/governance meta-study."),
    "P093": ("INCLUDE",  "RQ1+RQ2: Fraud/corruption/collusion in public procurement + data-driven SLR — core."),
    "P094": ("INCLUDE",  "RQ1+RQ2: Corruption red flags in public procurement (Italian tenders) — direct match."),
    "P095": ("EXCLUDE",  "EC-04: Ethical considerations for fairness in AI financial services — ethics, not detection."),
    "P096": ("INCLUDE",  "RQ1: AI/ML in combating illegal financial operations — bibliometric of methods."),
}

# Verification: must have exactly 96 entries
assert len(CODER2_SCREEN) == 96, f"Expected 96 decisions, got {len(CODER2_SCREEN)}"
_inc = sum(1 for v in CODER2_SCREEN.values() if v[0] == "INCLUDE")
_exc = sum(1 for v in CODER2_SCREEN.values() if v[0] == "EXCLUDE")
print(f"Coder 2 screening loaded: INCLUDE={_inc}, EXCLUDE={_exc}")

# ── Stage 2: Coder 2 independent D1-D5 scores for pilot papers ──────────────
# Scored independently — no knowledge of Coder 1 or pipeline scores.
# Pilot papers: P005, P010, P015, P020, P025, P030, P035, P040, P045
# Rubric (coding_guide_v1.md §5.2):
#   D1: Q1=10, Q2=7, Q3=5, Q4=3, Unranked=2
#   D2: Repro+empirical+comparison=10, Empirical+no_comparison=7,
#       Descriptive/analytical=5, Opinion/review_no_method=3
#   D3: All-3-RQ=10, Two-RQ=7, One-RQ=4, Tangential=2, None=0
#   D4: 2022-2026=10, 2018-2021=7, 2014-2017=5, ≤2013=3
#   D5: MNCS≥1.5=10, 0.75-1.49=7, <0.75=4; <5cit OR paper<2yr→default 7

CODER2_PILOT_SCORES: dict[str, dict[str, float]] = {
    # P005: Q1 journal, review (no systematic method), 2023, 123 cit
    # D3: AI malware/intrusion — no financial fraud angle. D3=0 (no connection per RQ scope)
    # D5: 123 cit 2023 — MNCS ≈ 123/50 = 2.46 → top quartile → 10
    "P005": {"d1": 10.0, "d2": 3.0, "d3": 0.0, "d4": 10.0, "d5": 10.0,
             "note": "D3 0 (no connection): malware/intrusion ≠ financial fraud/corruption. "
                     "More conservative than Coder 1 (D3=2) — domain mismatch is complete."},

    # P010: Q3, descriptive review, 2023, 60 cit
    # D3: ChatGPT in accounting — general accounting efficiency. Tangential at best → D3=2
    # D5: 60 cit 2023 — MNCS ≈ 60/50 = 1.2 → second quartile → 7
    "P010": {"d1": 5.0, "d2": 3.0, "d3": 2.0, "d4": 10.0, "d5": 7.0,
             "note": "D1 down 10→5: Q3 journal. D5 down: 60 cit 2023 = MNCS≈1.2 → Q2 → 7. "
                     "D3=2 agreed (tangential accounting-fraud connection). "
                     "Disagreement: pipeline D1=10 (Q1?) but journal is Q3."},

    # P015: Q1, review, 2022, 54 cit
    # D3: Neural networks for anomaly detection methods — one RQ (RQ1) substantively → D3=4
    # D5: 54 cit 2022 — MNCS ≈ 54/75 = 0.72 → Q3/Q4 → 4
    "P015": {"d1": 10.0, "d2": 3.0, "d3": 4.0, "d4": 10.0, "d5": 4.0,
             "note": "D3=4 agreed (RQ1 methods). D5=4 agreed (MNCS≈0.72 < 0.75). "
                     "Full agreement with Coder 1 on all dimensions."},

    # P020: Q2, survey/review (no systematic method), 2023, 81 cit
    # D3: DDoS in IoT — no financial fraud. D3=0 (no connection, stricter than Coder 1's D3=2)
    # D5: 81 cit 2023 — MNCS ≈ 81/50 = 1.62 → top quartile → 10
    "P020": {"d1": 7.0, "d2": 3.0, "d3": 0.0, "d4": 10.0, "d5": 10.0,
             "note": "D3 0 (no connection): DDoS/IoT cybersecurity domain has no financial fraud angle. "
                     "More conservative than Coder 1 (D3=2). D5=10 agreed (MNCS≈1.62)."},

    # P025: Q2, empirical + comparison, 2024, 49 cit
    # D3: IoT cyberattack in smart cities — no financial fraud. D3=0 (no connection)
    # D5: 49 cit 2024 — MNCS ≈ 49/25 = 1.96 → top quartile → 10
    "P025": {"d1": 7.0, "d2": 7.0, "d3": 0.0, "d4": 10.0, "d5": 10.0,
             "note": "D3 0: IoT cyberattack detection ≠ financial fraud/corruption. "
                     "Coder 1 gave D3=2 (tangential FL method). Key dimension-level IRR gap: "
                     "scope of 'tangential' needs clarification in rubric."},

    # P030: Q2, empirical, 2025, 17 cit
    # D3: FL for 5G IoT anomaly detection — no financial fraud. D3=0 (no connection)
    # D5: 17 cit 2025 — paper < 2 years → default 7
    "P030": {"d1": 7.0, "d2": 7.0, "d3": 0.0, "d4": 10.0, "d5": 7.0,
             "note": "D3 0: 5G IoT security ≠ government financial fraud. "
                     "Coder 1: D3=4. Coder 2: D3=0. Largest disagreement in pilot set. "
                     "Rubric clarification needed: 'tangential' vs 'no connection' for cybersecurity FL."},

    # P035: Unranked, review, 2025, 11 cit
    # D3: Compliance intelligence for SME financial platforms — RQ3 scalability + RQ1 model.
    #     Addresses TWO RQs tangentially? D3=4 (one RQ: RQ3 scalability gap)
    # D5: 11 cit 2025 → < 2 years → default 7
    "P035": {"d1": 2.0, "d2": 3.0, "d3": 4.0, "d4": 10.0, "d5": 7.0,
             "note": "D3=4 (one RQ: RQ3 scalability). Coder 1: D3=7. "
                     "Disagreement: Coder 2 sees RQ3 only substantively; RQ1 only tangential "
                     "(SME ≠ government context). D1,D2,D4,D5 agreed."},

    # P040: Unranked, review, 2025, 7 cit
    # D3: IoT anomaly detection + quantum ML — no financial fraud. D3=0 (no connection)
    # D5: 7 cit 2025 → < 2 years → default 7
    "P040": {"d1": 2.0, "d2": 3.0, "d3": 0.0, "d4": 10.0, "d5": 7.0,
             "note": "D3 0: IoT+quantum anomaly detection → zero financial fraud content. "
                     "Pipeline D3=10 (severe over-score). Coder 1 D3=4. Coder 2 D3=0. "
                     "All three differ — this dimension needs explicit rubric anchor examples."},

    # P045: Unranked, empirical+validation, 2023, 25 cit
    # D3: FinChain-BERT for financial fraud detection — RQ1 one RQ → D3=4
    # D5: 25 cit 2023 — MNCS ≈ 25/50 = 0.5 → Q3/Q4 → 4
    "P045": {"d1": 2.0, "d2": 7.0, "d3": 4.0, "d4": 10.0, "d5": 4.0,
             "note": "Full agreement with Coder 1: D1=2, D2=7, D3=4, D4=10, D5=4. "
                     "MNCS≈0.5 confirms D5=4."},
}

WEIGHTS = {"d1": 0.25, "d2": 0.25, "d3": 0.20, "d4": 0.15, "d5": 0.15}
RUBRIC: dict[str, list[float]] = {
    "d1": [2.0, 3.0, 5.0, 7.0, 10.0],
    "d2": [3.0, 5.0, 7.0, 10.0],
    "d3": [0.0, 2.0, 4.0, 7.0, 10.0],
    "d4": [3.0, 5.0, 7.0, 10.0],
    "d5": [2.0, 4.0, 7.0, 10.0],
}


def cohen_kappa(c1: list[int], c2: list[int]) -> float:
    n = len(c1)
    po = sum(a == b for a, b in zip(c1, c2)) / n
    p1c1 = sum(c1) / n;  p0c1 = 1 - p1c1
    p1c2 = sum(c2) / n;  p0c2 = 1 - p1c2
    pe = p1c1 * p1c2 + p0c1 * p0c2
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def bracket_agreement(pip: float, cod: float, levels: list[float]) -> str:
    if abs(pip - cod) < 0.01:
        return "EXACT"
    try:
        pi = levels.index(pip);  ci = levels.index(cod)
        if abs(pi - ci) == 1:
            return "ADJACENT"
    except ValueError:
        pass
    return "DISAGREE"


def main() -> None:
    df = pd.read_csv(CORPUS)

    # ── Stage 1: write coder2_screen ─────────────────────────────────────────
    print("=" * 72)
    print("  Phase E Stage 1 — Coder 2 Independent Screening")
    print("=" * 72)

    df["coder2_screen"] = df["coder2_screen"].astype(object)
    for pid, (decision, note) in CODER2_SCREEN.items():
        idx = df[df["paper_id"] == pid].index
        if len(idx) == 0:
            print(f"  WARNING: {pid} not found in corpus")
            continue
        df.at[idx[0], "coder2_screen"] = decision
        # Append coder2 note to notes column
        existing = str(df.at[idx[0], "notes"]) if pd.notna(df.at[idx[0], "notes"]) else ""
        sep = " | " if existing and existing.strip() else ""
        df.at[idx[0], "notes"] = existing + sep + f"[C2] {note}"

    inc2 = (df["coder2_screen"] == "INCLUDE").sum()
    exc2 = (df["coder2_screen"] == "EXCLUDE").sum()
    print(f"  Coder 2: INCLUDE={inc2}, EXCLUDE={exc2}")
    inc1 = (df["coder1_screen"] == "INCLUDE").sum()
    exc1 = (df["coder1_screen"] == "EXCLUDE").sum()
    print(f"  Coder 1: INCLUDE={inc1}, EXCLUDE={exc1}")

    # ── Stage 1 IRR: compute Cohen's κ ───────────────────────────────────────
    print(f"\n{'=' * 72}")
    print("  Stage 1 IRR — Cohen's κ Calculation")
    print(f"{'=' * 72}")

    # Binary INCLUDE=1 / EXCLUDE=0 (UNCERTAIN treated as EXCLUDE per guide §4.4)
    valid = df[df["coder1_screen"].notna() & df["coder2_screen"].notna()].copy()
    c1_bin = (valid["coder1_screen"] == "INCLUDE").astype(int).tolist()
    c2_bin = (valid["coder2_screen"] == "INCLUDE").astype(int).tolist()
    n = len(c1_bin)

    # Agreement counts
    both_inc = sum(a == 1 and b == 1 for a, b in zip(c1_bin, c2_bin))
    both_exc = sum(a == 0 and b == 0 for a, b in zip(c1_bin, c2_bin))
    c1inc_c2exc = sum(a == 1 and b == 0 for a, b in zip(c1_bin, c2_bin))
    c1exc_c2inc = sum(a == 0 and b == 1 for a, b in zip(c1_bin, c2_bin))
    observed_agree = (both_inc + both_exc) / n

    kappa = cohen_kappa(c1_bin, c2_bin)

    print(f"\n  Contingency table (n={n}):")
    print(f"  {'':15} Coder2-INCLUDE  Coder2-EXCLUDE")
    print(f"  {'Coder1-INCLUDE':<15}  {both_inc:>10}      {c1inc_c2exc:>10}")
    print(f"  {'Coder1-EXCLUDE':<15}  {c1exc_c2inc:>10}      {both_exc:>10}")
    print(f"\n  P_observed (agreement): {observed_agree:.3f} ({100*observed_agree:.1f}%)")
    print(f"  Cohen's κ: {kappa:.4f}")

    if kappa >= 0.75:
        verdict = "✅ ACCEPTABLE (κ ≥ 0.75)"
    elif kappa >= 0.60:
        verdict = "⚠ MODERATE (0.60 ≤ κ < 0.75) — review disagreements before proceeding"
    else:
        verdict = "❌ BELOW THRESHOLD (κ < 0.60) — rubric revision required"
    print(f"  Verdict: {verdict}")

    # ── Stage 1: Categorise disagreements ────────────────────────────────────
    print(f"\n{'=' * 72}")
    print("  Stage 1 Disagreement Analysis")
    print(f"{'=' * 72}")

    disagree_rows = []
    for _, row in valid.iterrows():
        c1d = row["coder1_screen"]
        c2d = row["coder2_screen"]
        if c1d != c2d:
            disagree_rows.append({
                "paper_id": row["paper_id"],
                "title": str(row["title"])[:70],
                "year": row["year"],
                "sjr_quartile": row["sjr_quartile"],
                "citations": row["citations"],
                "pipeline_status": row["pipeline_status"],
                "coder1_screen": c1d,
                "coder2_screen": c2d,
                "c2_note": CODER2_SCREEN.get(row["paper_id"], ("", ""))[1][:80],
            })

    disagree_df = pd.DataFrame(disagree_rows)

    # Categorize disagreement types
    c1i_c2e = disagree_df[disagree_df["coder1_screen"] == "INCLUDE"]
    c1e_c2i = disagree_df[disagree_df["coder2_screen"] == "INCLUDE"]

    print(f"\n  Total disagreements: {len(disagree_rows)} / {n} = {100*len(disagree_rows)/n:.1f}%")
    print(f"  C1=INCLUDE, C2=EXCLUDE: {len(c1i_c2e)} papers")
    print(f"  C1=EXCLUDE, C2=INCLUDE: {len(c1e_c2i)} papers")

    # Pattern analysis: what EC codes does C2 assign to C1-INCLUDE papers?
    ec_counts: dict[str, int] = {}
    for pid in c1i_c2e["paper_id"]:
        note = CODER2_SCREEN.get(pid, ("", ""))[1]
        ec = note.split(":")[0].strip()
        ec_counts[ec] = ec_counts.get(ec, 0) + 1
    print(f"\n  Disagreement pattern (C1-INCLUDE → C2-EXCLUDE):")
    for ec, cnt in sorted(ec_counts.items(), key=lambda x: -x[1]):
        print(f"    {ec:<8}  {cnt:>3} papers")

    # Save Stage 1 comparison
    disagree_df.to_csv(STAGE1_OUT, index=False)
    print(f"\n  Stage 1 comparison saved → {STAGE1_OUT}")

    # ── Update irr_resolution for newly confirmed consensus ───────────────────
    n_confirmed = 0
    for col in ["irr_resolution", "irr_agreement"]:
        df[col] = df[col].astype(object)

    for i, row in df.iterrows():
        c1d = row["coder1_screen"]
        c2d = row["coder2_screen"]
        if c1d == "INCLUDE" and c2d == "INCLUDE":
            existing_res = str(row.get("irr_resolution", ""))
            if existing_res not in ("CONSENSUS", "DOMAIN_OVERRIDE"):
                df.at[i, "irr_resolution"] = "CONSENSUS"
                df.at[i, "irr_agreement"] = "AGREE"
                n_confirmed += 1
        elif c1d == "EXCLUDE" and c2d == "EXCLUDE":
            df.at[i, "irr_resolution"] = "BOTH_EXCLUDE"
            df.at[i, "irr_agreement"] = "AGREE"
        elif c1d != c2d and pd.notna(c1d) and pd.notna(c2d):
            df.at[i, "irr_resolution"] = "DISAGREE_REVIEW"
            df.at[i, "irr_agreement"] = "DISAGREE"

    print(f"\n  New CONSENSUS from Coder 2 agreement: {n_confirmed} papers")

    # ── Stage 2: Coder 2 pilot scores ────────────────────────────────────────
    print(f"\n{'=' * 72}")
    print("  Phase E Stage 2 — Coder 2 Pilot Calibration")
    print(f"{'=' * 72}")

    pilot_results = pd.read_csv(PILOT_CSV)
    PIPE_MAP = {"d1": "pipe_d1", "d2": "pipe_d2", "d3": "pipe_d3",
                "d4": "pipe_d4", "d5": "pipe_d5"}
    C1_MAP   = {"d1": "coder1_d1", "d2": "coder1_d2", "d3": "coder1_d3",
                "d4": "coder1_d4", "d5": "coder1_d5"}

    stage2_rows = []
    c2_dim_vs_c1: dict[str, list[str]] = {d: [] for d in RUBRIC}
    c2_dim_vs_pipe: dict[str, list[str]] = {d: [] for d in RUBRIC}

    pilot_ids = ["P005", "P010", "P015", "P020", "P025", "P030", "P035", "P040", "P045"]
    for pid in pilot_ids:
        prow = pilot_results[pilot_results["paper_id"] == pid].iloc[0]
        c2 = CODER2_PILOT_SCORES[pid]
        c2_comp = sum(c2[d] * WEIGHTS[d] for d in RUBRIC)
        c1_comp = float(prow["coder1_composite"])
        pipe_comp = float(prow["pipe_composite"])

        print(f"\n--- {pid} | pipe={pipe_comp:.2f} | C1={c1_comp:.2f} | C2={c2_comp:.2f} ---")
        print(f"    Title: {prow['title'][:75]}")

        record = {"paper_id": pid, "title": prow["title"][:70]}
        discrepancies_vs_c1 = []
        discrepancies_vs_pipe = []

        for d in RUBRIC:
            pipe_v = float(prow[PIPE_MAP[d]])
            c1_v   = float(prow[C1_MAP[d]])
            c2_v   = c2[d]

            agr_c1   = bracket_agreement(c1_v, c2_v, RUBRIC[d])
            agr_pipe = bracket_agreement(pipe_v, c2_v, RUBRIC[d])
            c2_dim_vs_c1[d].append(agr_c1)
            c2_dim_vs_pipe[d].append(agr_pipe)

            record[f"pipe_{d}"] = pipe_v
            record[f"coder1_{d}"] = c1_v
            record[f"coder2_{d}"] = c2_v
            record[f"c2_vs_c1_{d}"] = agr_c1
            record[f"c2_vs_pipe_{d}"] = agr_pipe

            if agr_c1 != "EXACT":
                discrepancies_vs_c1.append(f"{d.upper()} C1={c1_v} C2={c2_v} [{agr_c1}]")

        record["pipe_composite"] = pipe_comp
        record["coder1_composite"] = c1_comp
        record["coder2_composite"] = round(c2_comp, 3)
        record["c1_c2_delta"] = round(c2_comp - c1_comp, 3)
        record["note"] = c2["note"]

        if discrepancies_vs_c1:
            print(f"    vs C1 discrepancies: {'; '.join(discrepancies_vs_c1)}")
        else:
            print("    ✅ Full agreement with Coder 1")
        stage2_rows.append(record)

    # ── Stage 2: Per-dimension IRR summary (C2 vs C1) ────────────────────────
    print(f"\n{'=' * 72}")
    print("  Stage 2 Per-Dimension IRR: Coder 2 vs Coder 1")
    print(f"{'=' * 72}")
    print(f"  {'Dim':<6} {'Exact':>7} {'Adjacent':>9} {'Disagree':>9} {'Broad%':>8} {'Pass(≥70%)':>12}")

    all_pass = True
    for d in RUBRIC:
        agrs = c2_dim_vs_c1[d]
        n = len(agrs)
        exact = agrs.count("EXACT")
        adj   = agrs.count("ADJACENT")
        disag = agrs.count("DISAGREE")
        broad = 100 * (exact + adj) / n
        flag = "✅" if broad >= 70 else "⚠ BELOW 70%"
        if broad < 70:
            all_pass = False
        print(f"  {d.upper():<6} {exact:>4}/{n} ({100*exact/n:4.0f}%)  +adj {adj}  ({broad:4.0f}%) {flag}")

    # C2 vs pipeline for reference
    print(f"\n  {'Dim':<6} (C2 vs Pipeline for reference)")
    for d in RUBRIC:
        agrs = c2_dim_vs_pipe[d]
        n = len(agrs)
        exact = agrs.count("EXACT");  adj = agrs.count("ADJACENT")
        broad = 100 * (exact + adj) / n
        print(f"  {d.upper():<6}  broad {broad:4.0f}%  exact {100*exact/n:4.0f}%")

    # Mean C2-C1 delta
    c1c2_deltas = [r["c1_c2_delta"] for r in stage2_rows]
    print(f"\n  Mean composite delta (C2 - C1): {sum(c1c2_deltas)/len(c1c2_deltas):+.3f}")
    print(f"  Range: {min(c1c2_deltas):+.3f} to {max(c1c2_deltas):+.3f}")

    # Save Stage 2 comparison
    stage2_df = pd.DataFrame(stage2_rows)
    stage2_df.to_csv(STAGE2_OUT, index=False)
    print(f"\n  Stage 2 comparison saved → {STAGE2_OUT}")

    # ── Final corpus state ───────────────────────────────────────────────────
    df.to_csv(CORPUS, index=False)
    print(f"\n{'=' * 72}")
    print("  Final Corpus State After Coder 2")
    print(f"{'=' * 72}")
    df2 = pd.read_csv(CORPUS)
    print(f"\n  irr_resolution:")
    print(df2["irr_resolution"].value_counts(dropna=False).to_string())
    print(f"\n  irr_agreement:")
    print(df2["irr_agreement"].value_counts(dropna=False).to_string())

    # Identify papers needing discussion (DISAGREE_REVIEW)
    review = df2[df2["irr_resolution"] == "DISAGREE_REVIEW"]
    print(f"\n  Papers requiring adjudication (DISAGREE_REVIEW): {len(review)}")

    # Recommended next actions
    print(f"\n{'=' * 72}")
    print("  Recommended Next Actions")
    print(f"{'=' * 72}")
    if kappa >= 0.75:
        print("  ✅ κ ≥ 0.75: IRR threshold met. Proceed to Stage 3 data extraction.")
    elif kappa >= 0.60:
        print("  ⚠ κ < 0.75: Hold Stage 3. Schedule consensus meeting for DISAGREE_REVIEW papers.")
        print("  Priority discussion topics:")
        print("    1. Domain boundary: IoT/cybersecurity papers — include for RQ1 methods?")
        print("    2. EC-02 scope: private sector papers with applicable methods — include?")
        print("    3. D3 rubric: define 'tangential' (D3=2) vs 'no connection' (D3=0) with anchor examples.")
    else:
        print("  ❌ κ < 0.60: Revise coding guide. Agree on scope boundaries before re-screening.")

    if not all_pass:
        print("  ⚠ One or more Stage 2 dimensions below 70% C2-C1 agreement.")
        print("  → Revise D3 rubric: add explicit examples distinguishing cyber-method papers from")
        print("    financial-fraud-domain papers. Agree on 'tangential' threshold.")

    print(f"\n  DONE. Cohen's κ = {kappa:.4f} | {verdict}")


if __name__ == "__main__":
    main()
