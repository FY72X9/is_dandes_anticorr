# 1. Introduction

Village fund governance in Indonesia operates at a scale that makes it both critical and
vulnerable. The Village Law (UU No. 6/2014) channels fiscal allocations to more than 74,000
village governments annually — a programme exceeding IDR 70 trillion per fiscal year by 2023.
This decentralisation ambition has delivered measurable development gains, yet it has
simultaneously created conditions conducive to financial mismanagement. The Corruption
Eradication Commission (KPK) recorded 601 Dana Desa corruption cases between 2015 and 2023,
implicating village heads, secretaries, and local officials in embezzlement, fictitious
project expenditure, and budget absorption manipulation [1]. The Supreme Audit Board (BPK)
consistently identifies village fund irregularities as a top-five public finance risk in its
annual national audit reports [2].

The governance response to date relies primarily on ex-post audit cycles — BPK annual reviews,
BPKP oversight, and KPK case referrals — which by design detect fraud after disbursement has
already occurred. These mechanisms lack the analytical granularity to distinguish statistical
anomalies in real-time disbursement patterns from legitimate expenditure variation across 74,000
heterogeneous village contexts. Information technology offers a potential complementary layer:
if financial transaction data can be transformed into machine-readable anomaly signals, then
automated detection could serve as an early-warning instrument alongside traditional audit,
enabling more targeted and timely investigative resource allocation.

Machine learning (ML)-based financial fraud detection has accumulated a substantial literature
over the past decade. Isolation Forest, Local Outlier Factor (LOF), graph neural networks
(GNNs), and autoencoder-based anomaly detection methods all report AUC-ROC values exceeding
0.90 on benchmark financial datasets [3, 4, 5]. Bibliometric analyses confirm accelerating
output — 15 papers in 2025 alone, up from six in 2022 [6]. This technical literature,
however, addresses a fundamentally different problem domain: centralised commercial banking
systems with labelled transaction data, high transaction volume, and institutional capacity
for rapid anomaly response. Whether these methods can be adapted to the conditions of
Indonesian village fund governance — fragmented paper-based records, unlabelled expenditure
data, sub-national institutional variation, and annual audit cycles — remains an open question
that no existing study addresses.

This gap defines the scope and motivation of this systematic literature review (SLR).

## 1.1 Research Questions

This SLR pursues three research questions derived from the governance-detection gap:

- **RQ1**: What ML-based anomaly and fraud detection methods have been proposed in the
  financial domain, and what performance characteristics do they demonstrate across different
  data and institutional contexts?
- **RQ2**: What feature engineering frameworks operationalize corruption or financial
  irregularity as machine-detectable computational signals, and how transferable are these
  frameworks to public-sector governance contexts?
- **RQ3**: What structural gaps in the existing literature prevent direct application of
  ML detection methods to decentralised village fund governance, and what design requirements
  does a primary study need to address to fill those gaps?

## 1.2 Theoretical Positioning

This review adopts an Information Systems (IS) perspective that frames ML anomaly detection
not as a purely algorithmic problem but as an IS governance intervention: a designed artifact
intended to operate within institutional processes, support human decision-making, and improve
governance outcomes [7]. This framing — anchored in Hevner et al.'s (2004) Design Science
Research (DSR) framework — distinguishes this SLR from existing technical reviews that evaluate
methods solely by laboratory performance metrics [8]. It implies that a complete evaluation of
any detection artifact must assess not only predictive accuracy but also institutional
deployability, interpretability for auditor use, and theoretical alignment with the governance
context's principal-agent corruption dynamics [9].

## 1.3 Significance and Scope

This SLR makes three contributions. First, it provides the first systematic mapping of ML
fraud detection methods against the specific institutional requirements of decentralised
public fund governance. Second, it identifies and validates five structural research gaps
through a formal gap matrix integrating thematic synthesis, bibliometric evidence, and DSR
framework analysis. Third, it produces a synthesis-derived design blueprint — feature
engineering requirements, method selection criteria, and evaluation framework — that directly
informs the primary empirical study applying an unsupervised detection ensemble to real
Jambi Province Dana Desa data (2023–2025).

The review covers the period 2018–2026, reflecting the post-deep-learning methodological shift
in anomaly detection and the post-2014 Village Law policy context. Non-financial anomaly
detection, cybersecurity intrusion detection, and medical anomaly detection lie outside scope.
