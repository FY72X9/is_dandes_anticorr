# Chapter 6: Conclusion

> **Draft Status**: v3.0 — July 2026 (Final synthesis & research directions)  
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Target**: ~500 words  
> **Citation Format**: IEEE (continuous numbering per references.md)  

---

## 6. Conclusion

This study developed and evaluated an unsupervised Dual-Path Machine Learning artifact (`v3-run`), framed within Design Science Research (DSR) [10], for detecting expenditure anomalies in village fund absorption records. Applied to 96,778 activity-level entries across 1,363 villages in Jambi Province (FY 2023–2025), empirical results resolve all three research questions:

1. **RQ1 — Feature Discriminating Power**: Seven engineered feature constructs incorporating kabupaten-stratified z-score baseline centering (`cost_deviation_by_category`) provide strong discriminating power. Autoencoder loss decomposition confirms that within-category unit cost deviation and unit price inflation represent the primary statistical drivers of financial distortion in Siskeudes records.
2. **RQ2 — Algorithmic Performance & Ensemble Gating**: LOF isolates extreme heavy-tailed local density anomalies (Sarle BC = 0.957), while Isolation Forest (BC = 0.335) and Deep Autoencoder (BC = 0.703) partition global multi-feature outliers. The Dual-Path Consensus Framework ($\text{LOF} \lor (\text{IF} \land \text{RDA})$) resolves the mutual cancellation limitation of traditional majority voting, outperforming individual algorithms on an ex-ante 10,000-record synthetic benchmark with **Precision = 0.846, Recall = 0.846, F1-Score = 0.846, and AUC-ROC = 0.912**.
3. **RQ3 — Typology Mapping & Operational XAI**: An Operational Policy Mapping Layer translates mathematical anomalies into seven corruption typologies dominated by **T2: Ghost Activities (58.1%)** and **T5: Procurement Irregularities (32.8%)**, identifying **Rp 642.85 Miliar** in realized expenditure exposure. Instance-level XAI feature contribution rankings translate abstract reconstruction MSE into actionable audit checklists for field inspectors.

The artifact operationalises the DeLone and McLean information-quality-to-organisational-impact pathway [10]: at the **activity level**, 96,778 records are filtered to 7,153 consensus anomalies (a 92.6% search space reduction); at the **entity level**, longitudinal persistence scoring isolates **702 villages (51.5%)** flagged continuously across all three fiscal years, providing an operationally feasible priority pool for district APIP inspectorates.

### Future Research Directions

Future research will expand this work along four main trajectories:
1. **Semi-Supervised Graph Neural Networks (GNNs)**: Implementing GNN architectures (GraphSAGE / GAT) on transaction network graphs to automatically discover latent compound corruption topologies, resolving the 17.2% Unclassified sub-threshold anomaly subspace.
2. **Multi-Province Panel Extension**: Scaling the longitudinal pipeline to additional Indonesian provinces (e.g., Sumatera Utara, Jawa Timur) to evaluate national generalisability across diverse fiscal contexts.
3. **Real-Time API Dashboard Integration**: Deploying the artifact as an automated streaming microservice integrated with BPKP Siskeudes API endpoints for pre-disbursement alert triggering.
4. **Ex-Post Impact Assessment**: Conducting empirical field research measuring APIP audit referral conversion rates and recovered state financial losses (*Kerugian Negara*).
