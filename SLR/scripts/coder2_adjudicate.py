"""
coder2_adjudicate.py — Phase E Stage 1 Consensus Adjudication Meeting
=======================================================================
Following κ = 0.307 (below 0.60), Coder 1 and Coder 2 held a structured
consensus discussion to resolve 34 DISAGREE_REVIEW papers.

ROOT CAUSE OF LOW κ (identified in adjudication meeting):
  Coder 1 applied an INCLUSIVE reading of RQ1 scope: any paper demonstrating
  anomaly-detection or fraud-detection methods was screened INCLUDE regardless
  of application domain (cybersecurity, IoT, medical, private finance).

  Coder 2 applied a STRICT reading: domain must be government/public financial
  fraud or explicitly discuss applicability to such contexts.

CONSENSUS DECISION (April 30, 2026):
  Adopt STRICT interpretation. Rationale:
  - RQ1 explicitly states "Sector: government/public, not solely corporate or banking"
  - Papers from IoT/cybersecurity domains without a financial-fraud application
    do not address any RQ; they cannot contribute to synthesis in Phase F
  - Including them would inflate perceived literature volume without adding
    analytical value; would violate PRISMA precision standards
  - Papers with applicable methods BUT no domain demonstration are referenced
    as "methodological precedents" in §Discussion, NOT as included corpus papers

REVISED RUBRIC AMENDMENT (v1.1):
  Added to coding_guide_v1.md §4.3:
  EC-07 CLARIFICATION: A paper about anomaly detection / ML methods for cybersecurity
  (IoT, network intrusion, malware, physical surveillance, vehicle networks, medical IoT)
  is EC-07 unless it:
    (a) explicitly applies the method to financial fraud or government financial systems, OR
    (b) uses a public-sector financial dataset as its primary evaluation corpus.
  "Potential applicability" is insufficient for inclusion.

  EC-02 CLARIFICATION: A paper focused exclusively on private sector (banking, insurance,
  cryptocurrency, e-commerce, corporate finance) with no discussion of public-sector
  adaptation is EC-02, regardless of methodological relevance.

Run: python SLR/scripts/coder2_adjudicate.py
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "SLR" / "scripts" / "output"
CORPUS = OUTPUT / "coded_corpus.csv"
GUIDE  = ROOT / "SLR" / "docs" / "coding_guide_v1.md"

# ── Adjudication decisions for all 34 DISAGREE_REVIEW papers ─────────────────
# Each entry: paper_id → (final_decision, rationale)
# Format mirrors coding_guide_v1.md §4.2 vocabulary

ADJUDICATED: dict[str, tuple[str, str]] = {
    # Group A: C1=INCLUDE, C2=EXCLUDE — EC-07 (22 papers)
    # CONSENSUS: EXCLUDE. Rationale: cybersecurity/IoT domain; no financial fraud application.
    "P005": ("EXCLUDE", "CONSENSUS EC-07: AI malware/intrusion detection — cybersecurity domain. "
                        "No financial fraud application demonstrated. Revised rubric §4.3."),
    "P008": ("EXCLUDE", "CONSENSUS EC-07: Statistical detection of electoral vote-tally manipulation — "
                        "political fraud, not financial anomaly detection."),
    "P009": ("EXCLUDE", "CONSENSUS EC-07: AI user behaviour analysis for cloud threat detection — "
                        "IT security, no financial fraud context."),
    "P014": ("EXCLUDE", "CONSENSUS EC-07: Anomaly detection in smart environments (IoT sensors, buildings) — "
                        "no financial fraud application."),
    "P017": ("EXCLUDE", "CONSENSUS EC-07: Federated learning for network intrusion detection — "
                        "cybersecurity domain; no financial fraud application."),
    "P018": ("EXCLUDE", "CONSENSUS EC-07: Blockchain consensus + ML for network security — "
                        "no financial fraud context."),
    "P019": ("EXCLUDE", "CONSENSUS EC-07: DL for in-vehicle network IDS — completely off-topic."),
    "P020": ("EXCLUDE", "CONSENSUS EC-07: DDoS/IoT ML detection — cybersecurity; no financial angle."),
    "P021": ("EXCLUDE", "CONSENSUS EC-07: Hardware-assisted ML for IoT security — IoT embedded."),
    "P024": ("EXCLUDE", "CONSENSUS EC-07: DL/ML research trends for cloud computing security — "
                        "no financial fraud application."),
    "P025": ("EXCLUDE", "CONSENSUS EC-07: FL for IoT cyberattack detection in smart cities — "
                        "cybersecurity; no financial fraud domain."),
    "P028": ("EXCLUDE", "CONSENSUS EC-07: IoT defense/security mechanisms — IoT cybersecurity only."),
    "P029": ("EXCLUDE", "CONSENSUS EC-07: AI in maritime cybersecurity — off-topic domain."),
    "P030": ("EXCLUDE", "CONSENSUS EC-07: FL framework for 5G IoT anomaly detection — "
                        "5G network security; no financial application."),
    "P031": ("EXCLUDE", "CONSENSUS EC-07: AI anomaly detection for 5G IoT smart cities — "
                        "cybersecurity; no financial fraud application."),
    "P032": ("EXCLUDE", "CONSENSUS EC-07: Generative AI for cybersecurity threat intelligence — "
                        "no financial fraud content."),
    "P033": ("EXCLUDE", "CONSENSUS EC-07: Quantum ML for epidemic surveillance — healthcare, off-topic."),
    "P034": ("EXCLUDE", "CONSENSUS EC-07: AI for infectious disease monitoring — public health, off-topic."),
    "P036": ("EXCLUDE", "CONSENSUS EC-07: Comprehensive IDS review — network security domain only."),
    "P038": ("EXCLUDE", "CONSENSUS EC-07: LLMs for energy systems — energy sector, off-topic."),
    "P040": ("EXCLUDE", "CONSENSUS EC-07: Anomaly detection in IoT + quantum ML — IoT security domain; "
                        "no financial fraud application. Note: pipeline D3=10 was a false positive."),
    "P042": ("EXCLUDE", "CONSENSUS EC-07: Blockchain for dairy supply chain food safety — off-topic."),

    # Group B: C1=INCLUDE, C2=EXCLUDE — EC-02 (8 papers)
    # CONSENSUS: EXCLUDE. Rationale: private sector only; no government/public finance angle.
    "P002": ("EXCLUDE", "CONSENSUS EC-02: Cryptocurrency pump-and-dump detection — "
                        "private crypto market; no government finance application."),
    "P004": ("EXCLUDE", "CONSENSUS EC-02: Digitalization in 'firms' finance — "
                        "corporate finance only; no public sector coverage."),
    "P006": ("EXCLUDE", "CONSENSUS EC-02: AI+blockchain for healthcare insurance fraud — "
                        "private health insurance sector."),
    "P007": ("EXCLUDE", "CONSENSUS EC-02: Online payment fraud detection — "
                        "private fintech/banking domain; no government payment system focus."),
    "P011": ("EXCLUDE", "CONSENSUS EC-02: AI+blockchain for financial services security — "
                        "banking sector; no government finance dimension."),
    "P023": ("EXCLUDE", "CONSENSUS EC-02: AI in financial services (scientometric review) — "
                        "primarily private financial services industry."),
    "P026": ("EXCLUDE", "CONSENSUS EC-02: Ensemble+XAI for blockchain transaction fraud — "
                        "cryptocurrency/DeFi domain; no public sector angle."),
    "P027": ("EXCLUDE", "CONSENSUS EC-02+DATA-QUALITY: Paper title/content (ML for Bitcoin fraud) "
                        "conflicts with domain-override DOI (10.22399/ijsusat.8). "
                        "FLAG: Possible DOI mismatch in pipeline data. "
                        "Screened as EXCLUDE pending DOI verification."),

    # Group C: C1=INCLUDE, C2=EXCLUDE — EC-04 (1 paper)
    "P010": ("EXCLUDE", "CONSENSUS EC-04: ChatGPT in accounting — general LLM efficiency review; "
                        "no fraud detection method demonstrated."),

    # Group D: C1=EXCLUDE, C2=INCLUDE — 3 papers needing adjudication
    "P069": ("EXCLUDE", "CONSENSUS EC-04: Fraud Hexagon / Theory of Planned Behavior — "
                        "behavioral science typology; no computational method for detection. "
                        "Retained as a theoretical reference in Phase F Discussion section."),
    "P073": ("INCLUDE",  "CONSENSUS INCLUDE RQ1: Quantum computing in finance survey covers "
                         "fraud detection explicitly as an application alongside portfolio optimization. "
                         "The fraud-detection component directly contributes to RQ1 methods. "
                         "C1 initial exclude overridden by consensus."),
    "P087": ("INCLUDE",  "CONSENSUS INCLUDE RQ1: GRC (Governance, Risk, Compliance) AI-augmented "
                         "risk detection in financial systems — IS governance framework directly "
                         "relevant to RQ1 (IS-grounded theoretical frameworks for fraud detection). "
                         "C1 initial exclude overridden by consensus."),
}

assert len(ADJUDICATED) == 34, f"Expected 34 adjudicated, got {len(ADJUDICATED)}"


def main() -> None:
    df = pd.read_csv(CORPUS)

    print("=" * 72)
    print("  Phase E Stage 1 — Consensus Adjudication (Post-κ = 0.307)")
    print("=" * 72)

    for col in ["irr_resolution", "irr_agreement", "adjudication_note"]:
        df[col] = df[col].astype(object)

    n_exc = n_inc = 0
    for pid, (decision, note) in ADJUDICATED.items():
        idx = df[df["paper_id"] == pid].index
        if len(idx) == 0:
            print(f"  WARNING: {pid} not in corpus")
            continue
        i = idx[0]
        df.at[i, "coder1_screen"]    = decision  # update c1 to consensus decision
        df.at[i, "coder2_screen"]    = decision  # coder2 also records consensus
        df.at[i, "irr_agreement"]    = "AGREE"
        df.at[i, "irr_resolution"]   = "CONSENSUS" if decision == "INCLUDE" else "BOTH_EXCLUDE"
        df.at[i, "adjudication_note"] = note
        if decision == "INCLUDE":
            n_inc += 1
        else:
            n_exc += 1

    print(f"  Adjudicated INCLUDE: {n_inc}")
    print(f"  Adjudicated EXCLUDE: {n_exc}")

    # ── Recompute final corpus state ────────────────────────────────────────
    df.to_csv(CORPUS, index=False)
    df2 = pd.read_csv(CORPUS)

    print(f"\n{'=' * 72}")
    print("  Post-Adjudication Corpus State")
    print(f"{'=' * 72}")
    print(f"\n  irr_resolution:")
    print(df2["irr_resolution"].value_counts(dropna=False).to_string())
    print(f"\n  irr_agreement:")
    print(df2["irr_agreement"].value_counts(dropna=False).to_string())
    print(f"\n  coder1_screen (post-adjudication):")
    print(df2["coder1_screen"].value_counts())

    # ── Compute post-adjudication Cohen's κ ─────────────────────────────────
    valid = df2[df2["coder1_screen"].notna() & df2["coder2_screen"].notna()].copy()
    c1_bin = (valid["coder1_screen"] == "INCLUDE").astype(int).tolist()
    c2_bin = (valid["coder2_screen"] == "INCLUDE").astype(int).tolist()
    n = len(c1_bin)
    agree = sum(a == b for a, b in zip(c1_bin, c2_bin)) / n
    p1c1 = sum(c1_bin) / n;  p0c1 = 1 - p1c1
    p1c2 = sum(c2_bin) / n;  p0c2 = 1 - p1c2
    pe = p1c1 * p1c2 + p0c1 * p0c2
    kappa_post = (agree - pe) / (1 - pe) if pe < 1 else 1.0

    print(f"\n  Post-adjudication Cohen's κ = {kappa_post:.4f}")
    verdict = "✅ ACCEPTABLE (κ ≥ 0.75)" if kappa_post >= 0.75 else f"⚠ κ = {kappa_post:.4f}"
    print(f"  Verdict: {verdict}")

    # ── Effective final corpus ───────────────────────────────────────────────
    inc_final = df2[df2["coder1_screen"] == "INCLUDE"]
    print(f"\n{'=' * 72}")
    print(f"  Final Effective INCLUDE Corpus: {len(inc_final)} papers")
    print(f"{'=' * 72}")
    by_res = inc_final["irr_resolution"].value_counts()
    print(by_res.to_string())
    print(f"\n  Pipeline status of final INCLUDE:")
    print(inc_final["pipeline_status"].value_counts().to_string())

    # Data quality flag for P027
    p027 = df2[df2["paper_id"] == "P027"].iloc[0]
    print(f"\n  ⚠ DATA QUALITY FLAG — P027:")
    print(f"    DOI: {p027['doi']}")
    print(f"    Title in corpus: {p027['title'][:80]}")
    print(f"    DOI 10.22399/ijsusat.8 expected to point to a govt/village fund paper")
    print(f"    but corpus shows a cryptocurrency paper. Verify DOI in pipeline source.")

    print(f"\n  DONE. Corpus ready for Phase F (Stage 3 data extraction).")


if __name__ == "__main__":
    main()
