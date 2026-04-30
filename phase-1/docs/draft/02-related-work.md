# Chapter 2: Related Work

> **Draft Status**: v1.0 — April 2026
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~700 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 2. Related Work

### 2.1 Corruption Typology Frameworks

Understanding the detection target requires a precise vocabulary of corruption forms. Bussell [1-book] proposes a pragmatic two-dimensional typology distinguishing corruption by access type (monetary vs. preferential) and governance level (bureaucratic vs. political), providing the foundational axis for empirical classification. Graycar's TASP framework — Types, Activities, Sectors, Places — extends this axis by demanding that corruption analysis specify not merely what form of corruption occurs, but in which programme activity and geographic context, making typology placement an essential precondition for designing targeted controls [7]. For Indonesia's village fund context, Siregar and Aminudin [13] provide the most directly applicable empirical classification: a multi-case analysis of East Java dana desa fraud identifying five modus operandi — mark-up of goods and services, fictitious budget items, double budgeting, procurement manipulation, and misuse of personnel funds. Kartadinata et al. [14] extend this taxonomy by analysing 200+ KPK prosecution cases (2015–2020), confirming mark-up (penggelembungan) and fictitious projects (proyek fiktif) as dominant recurring patterns. Medan et al. [15], reporting from a 2025 study in East Nusa Tenggara, document that these modus operandi patterns persist into the most recent fiscal period, validating the continuing relevance of typology-grounded detection.

### 2.2 Fraud Triangle and Principal-Agent Foundations

The Fraud Triangle (Cressey, 1953), operationalised in the dana desa context by Hidajat [6], provides a three-condition model: Pressure (disbursement targets creating perverse incentives), Opportunity (structural absence of competitive procurement and limited auditor reach), and Rationalisation (normalisa­tion of fund manipulation as low-risk). The 98.8% dominance of Swakelola procurement in Siskeudes records — documented in the present dataset — confirms Søreide's [9] argument that the absence of competitive bidding is the principal structural enabler of procurement-stage corruption. Principal-agent theory [26], applied specifically to village fund governance by Sutarna and Subandi [citation in phase1], frames the village head as an agent possessing information asymmetry relative to the principal (district government, BPKP, KPK). Unexplained deviations from expected spending patterns — the exact signal unsupervised anomaly detection targets — constitute proximate evidence of the information asymmetry exploitation the agent-principal model predicts.

### 2.3 Anomaly Detection in Public Financial Data

The anomaly detection literature applied to public financial management has converged on three methodologically distinct paradigms as complementary rather than substitutable. Isolation Forest (IF), introduced by Liu et al. [19], applies random partitioning path length as a global sparsity measure, performing optimally against globally extreme multi-feature outliers. Local Outlier Factor (LOF) operates on local density ratios, identifying records whose neighbourhood density differs substantially from their k-nearest peers [25] — an architecture that detects a distinct anomaly subset from IF, capturing within-category price inflation patterns that global methods miss. Deep autoencoders applied to anomaly detection learn a compressed representation of normal behaviour; records with anomalously high reconstruction error signal structural deviations from learned normality. The Robust Deep Autoencoder (RDA) variant, applied in this study, augments standard autoencoder training with a sparse noise decomposition matrix to prevent contaminating anomalous records from corrupting the learned normal representation [34].

Chandola et al.'s [24] comprehensive survey of anomaly detection methods establishes that multi-paradigm approaches consistently produce broader detection coverage than any single method, as each paradigm exploits a fundamentally different statistical signature of anomalous behaviour. Prior work on Indonesian public financial data has not yet applied this three-paradigm ensemble framework to Jambi Province village fund activity-level records — existing studies either address aggregate national procurement indicators or apply supervised classification requiring labelled ground truth unavailable in real-time monitoring [12, 16].

### 2.4 Information Systems Grounding

The DeLone and McLean IS Success Model [10] — in its updated 2003 formulation incorporating Service Quality alongside Information Quality and System Quality — provides the IS-level justification for deploying an anomaly detection pipeline as an institutional intervention. In this framework, the pipeline's output (anomaly scores, typology classifications, village priority tiers) constitutes the **information quality** dimension, whose accuracy drives **individual impact** (auditor attention allocation) and **organisational impact** (corruption deterrence and state loss prevention). Mutungi et al. [5] further demonstrate that digital anti-corruption tools fail in practice when their design does not map to specific corruption interaction points — validating the feature-engineering approach that operationalises each detector against a specific documented modus operandi rather than applying generic statistical filtering.

This study addresses the confluence of these three literatures: a typology-grounded, IS-theorised, multi-paradigm detection system applied to the first longitudinal activity-level village fund expenditure dataset in the existing fraud detection literature.
