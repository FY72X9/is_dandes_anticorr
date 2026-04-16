# Chapter 5: Discussion

> **Draft Status**: v1.0 — April 2026
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~900 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 5. Discussion

### 5.1 Algorithm Selection: Why LOF's Superiority Is Theoretically Predicted

LOF's bimodality coefficient of 0.957 — the highest among the three methods — is not an empirical surprise. It is a theoretically predictable consequence of how corruption manifests structurally in Siskeudes activity records. Village fund activities within the same Kode_Output prefix code form natural local density clusters: all PAUD operational expense records, all road construction activities, all BLT disbursement entries share similar cost ranges, procurement types, and disbursement stage structures. When a fraudulent record occupies such a cluster — for instance, a road construction activity with `cost_per_unit` at 42.42 standard deviations above its category mean — LOF's local density comparison correctly identifies it as a local outlier (LOF >> 1.0) even if it appears globally unremarkable to Isolation Forest's path-partitioning mechanism, which compares the record against the global feature distribution rather than its Kode_Output peer group.

This finding empirically demonstrates that LOF identifies a structurally distinct anomaly subset from Isolation Forest on government spending data — a direct consequence of LOF's local density architecture [25] operating on within-category peer groups rather than the global feature space. The implication for APIP inspection design is consequential: an audit prioritisation system relying solely on IF would structurally miss the 3,951 records that LOF's local density mechanism uniquely identifies — activities whose cost structure is abnormal relative to their specific programme category but unremarkable in the global expenditure distribution.

IF's unimodal score distribution (BC = 0.335) reflects an architecture misalignment with the fraud structure: village fund corruption clusters systematically by activity type rather than manifesting as globally random sparsity, suppressing the score variance that IF's path-partitioning needs to produce clean bimodal separation. This does not invalidate IF's detections — it means IF's 7,974 flagged records include genuine anomalies that should carry lower individual weight and higher weight when corroborated by LOF or RDA.

The consensus framework — requiring convergence from at least two methodologically independent algorithms — resolves this architectural heterogeneity. Records in the IF∩RDA intersection (50.3% overlap) represent globally extreme anomalies confirmed by two independent global paradigms; records in the LOF-unique population represent locally deviant within-category anomalies; triple-consensus records (n = 156) represent the highest-confidence fraud signals across all three detection modalities.

### 5.2 The Fraud Triangle in the Data

The three Fraud Triangle conditions — Pressure, Opportunity, and Rationalisation — each find quantitative expression in the empirical results.

**Pressure** manifests in the fiscal expansion trajectory: Isolation Forest's elevated 2023 anomaly rate (10.5% versus 6.5–7.1% in subsequent years) coincides with post-COVID-era village budget expansion, when disbursement targets created stronger incentives for inflated claims to fully absorb enlarged allocations. The high-value Swakelola prevalence (24.7% of all activities) constrains the feasible range of procurement manipulation to self-managed activities, concentrating Pressure on the activity types where competitive controls are absent.

**Opportunity** is confirmed most directly by the 98.8% Swakelola procurement dominance — the structural condition Søreide [9] identifies as the primary enabler of procurement-stage corruption. The 642 Tier-1 villages exhibiting multi-year anomaly persistence (47.1% of all villages) demonstrate that Opportunity is not incidental but entrenched: the same villages display irregular patterns across consecutive fiscal years, consistent with a stable accountability vacuum rather than isolated administrative error.

**Rationalisation** does not produce directly observable quantitative signals — it operates within the cognitive domain of perpetrators. However, the typology analysis offers indirect evidence: the dominance of T1 (Mark-up, n = 1,571) and T7 (Cross-Category Dump, n = 1,568) over more operationally complex schemes (T3 Volume Padding = 38, T5 Procurement Irregularity = 26) suggests that low-detection-risk, high-frequency forms predominate. This is consistent with a rationalisation environment where mark-up and cross-category budget migration are perceived as administratively ambiguous enough to evade detection — rather than involving the elaborate construction of completely fictitious activities (T2, n = 774).

### 5.3 Principal-Agent Information Asymmetry: Where the Gap Operates

The principal-agent relationship in village fund governance positions the village head (agent) with substantial information advantages relative to the principal chain (kabupaten inspectorate, BPKP, KPK). The empirical detection results locate where this asymmetry operates with greatest consequence: `avg_completion` as the primary RDA error feature — dominant in 43.5% of Tier-1 village reconstructions — reveals that completion percentage reporting is the most exploited information gap. Agents report T1 disbursement at or near 100% while T2 and T3 realisations approach zero, creating a completion profile that the autoencoder reconstructed with maximum error precisely because no legitimate fund absorption behaviour produces this pattern.

This finding carries a direct operational implication: APIP inspection procedures should prioritise cross-checking reported stage completion percentages against physical output documentation as the first analytical step, before any cost or procurement analysis, because the completion reporting channel is where information asymmetry operates most intensively.

### 5.4 The Subthreshold Masking Problem

The 708 unclassified records (22.8% of consensus flags) represent a methodological limitation that warrants explicit analytical attention. These records satisfy the multi-paradigm anomaly threshold — they are confirmed anomalous by at least two independent detection methods — but simultaneously fail to meet any single typology rule's feature threshold. The most plausible explanation is compound fraud: schemes that combine moderate mark-up with partial completion manipulation across multiple features simultaneously, such that no single feature exceeds its individual typology threshold while the joint feature profile is nonetheless statistically anomalous. Single-threshold rule-based typology assignment is structurally inadequate for compound patterns. Future work should replace the rule-based typology module with a multi-label classifier trained on expert-validated samples that explicitly models feature interaction effects.

### 5.5 DeLone and McLean IS Success: Evaluating the Pipeline as an IS Artefact

The DeLone and McLean IS Success Model assesses systems along three quality dimensions (Information Quality, System Quality, Service Quality) leading to use, individual impact, and organisational impact [10]. Applied to this pipeline:

- **Information Quality**: The consensus anomaly scores, typology labels, and village priority tiers constitute information outputs whose quality is validated by (a) multi-paradigm convergence, (b) alignment with documented modus operandi from judicial records [13, 14], and (c) the four Jambi prosecution cases confirming that the exact financial patterns this pipeline targets were present in verified fraud cases [30–33].
- **Individual Impact**: The ranked village priority list and typology-labelled activity records convert an undifferentiated population of 99,692 records into a targeted inspection workplan covering 642 Tier-1 villages — a 93.5% reduction in the inspection search space.
- **Organisational Impact**: APIP operational coverage gap closure depends on whether inspectorates adopt ranked pipeline outputs as inspection inputs. This study does not measure adoption rates (an inherent limitation of technical research without implementation evaluation), but the inspection search space reduction directly addresses the staffing constraint Srirejeki and Faturokhman [12] document.

The pipeline satisfies the DeLone and McLean success pathway from information quality to organisational impact provided that inspectorates operationalise ranked outputs as inspection inputs — a governance and institutional design challenge outside the scope of technical detection research but constituting the central imperative for Phase 2 implementation evaluation.
