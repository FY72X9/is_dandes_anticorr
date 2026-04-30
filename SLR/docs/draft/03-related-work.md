# 2. Related Work

## 2.1 ML-Based Financial Fraud Detection: Current State

Financial fraud detection using ML methods has advanced substantially since the foundational
work of Phua et al. (2010) on imbalanced-class fraud classification [10]. Contemporary reviews
document three dominant method families: ensemble tree-based classifiers (Random Forest,
Gradient Boosting, XGBoost), deep learning architectures (LSTM, Autoencoder, Transformer),
and graph-based methods (Graph Neural Networks, network centrality features) [3, 11].
Unsupervised methods — Isolation Forest [12], Local Outlier Factor [13], and One-Class SVM
— have gained traction specifically in contexts where ground truth labels are unavailable,
a structural condition that characterises public sector financial data.

Existing SLRs in this domain (e.g., [3], [4], [11]) share a common boundary condition:
they evaluate method performance on private-sector, centralised financial datasets —
credit card transactions, banking ledgers, AML transaction graphs — and extrapolate
conclusions about "financial fraud detection" without distinguishing between private-sector
and public governance contexts. This boundary conflation is methodologically significant:
the data structures, institutional settings, transaction volumes, and ground truth
availability differ fundamentally between a commercial bank's transaction system and a
village government's disbursement ledger.

## 2.2 Village Fund Governance and Corruption in Indonesia

Dana Desa, established under UU No. 6/2014, allocates central government funds to village
governments based on a formula combining population, geographic area, and poverty index.
The KPK's Dana Desa monitoring programme has identified a consistent typology of
corruption patterns across documented cases: budget absorption manipulation (artificial
acceleration or suppression of expenditure rates to exploit monitoring blind spots),
fictitious procurement (single-bidder contracts and phantom vendors), and
administrative fraud (falsified accountability reports) [1, 15].

The IS governance literature on Dana Desa addresses these patterns primarily through
institutional and behavioural lenses — agency theory [16], fraud triangle [17], internal
control frameworks [18] — without proposing computational detection mechanisms.
Conversely, the ML detection literature does not reference this governance context.
No existing study bridges these two traditions.

## 2.3 Theoretical Framework: DSR and IS Governance

This SLR adopts Hevner et al.'s (2004) three-cycle DSR model as its organising framework
[8]. In DSR terms, the _relevance cycle_ frames the problem: village fund corruption
patterns constitute the governance requirement. The _design cycle_ produces the artifact:
an ML anomaly detection pipeline calibrated to village fund data features. The _rigor cycle_
grounds the design in prior knowledge: the validated methods, feature engineering
approaches, and IS theoretical frameworks that the existing literature has established.

Agency Theory [9] provides the micro-level governance mechanism: village heads (agents)
manage funds disbursed by central government and regency supervisors (principals), creating
information asymmetry that enables misappropriation when monitoring is periodic and
superficial. An automated anomaly detection layer reduces this asymmetry by continuously
screening disbursement patterns, generating early-warning signals for auditor attention.
The DeLone and McLean IS Success Model [19] provides the artifact evaluation framework:
the detection system must produce information quality (accurate anomaly scores), achieve
system quality (reliable processing of village-level batch data), and generate net benefits
(improved audit targeting) to constitute a successful IS intervention.

## 2.4 Gap in Existing Reviews

Four prior systematic reviews are most directly relevant: Ahmad et al. (2022) [3] on
ML fraud detection methods; West and Bhattacharya (2016) [11] on intelligent financial
fraud detection; Nicholls et al. (2021) [4] on unsupervised anomaly detection; and
Awotunde et al. (2021) [20] on AI in financial crime. None of these reviews addresses
a sub-national public governance context, none evaluates feature engineering for village
fund corruption typology, and none applies a DSR analytical lens to assess artifact
deployability. The most topically adjacent existing SLR is Wahyuni et al. (2023) [21],
which reviews digital governance of Dana Desa without engaging with ML detection methods.
This SLR fills the intersection none of these prior works has addressed.
