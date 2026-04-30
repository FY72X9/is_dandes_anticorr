# 6. Conclusion

## 6.1 Summary of Findings

This systematic literature review mapped 45 peer-reviewed papers to produce a structured
evidence base for ML-based financial anomaly detection in decentralised public governance.
The review answers its three research questions directly:

**RQ1** (ML methods): Unsupervised methods — particularly Isolation Forest, LOF, and
Autoencoder — demonstrate the strongest methodological fit for the unlabelled, low-volume
data conditions that characterise village fund governance. Supervised methods dominate
the existing literature but require labelled training data unavailable in the Dana Desa
context. Graph neural networks offer superior relational detection but presuppose
transaction-graph infrastructure that village governance systems do not currently provide.

**RQ2** (Feature engineering): Five validated feature categories exist in the procurement
and public finance fraud literature (single-bidder ratios, amendment frequencies, price
escalation, timing concentration, vendor diversity). Two additional categories specific
to village fund governance (budget absorption rate anomalies, disbursement timing
irregularities) emerge from the DT5 governance cluster. No prior study integrates these
into a unified village fund detection framework.

**RQ3** (Structural gaps): Three CRITICAL gaps preclude direct application of existing
methods to Dana Desa data: the complete absence of any ML detection artifact designed for
village-level public governance (G1); the absence of a validated feature engineering
framework for village fund corruption typology (G3); and the structural constraint of
label scarcity that eliminates supervised approaches (G2). Two secondary gaps — IS theory
absence (G4) and deployment/explainability limitations (G5) — require explicit framing
rather than full resolution.

## 6.2 Significance of the Operationalization Chasm

The review's primary contribution — beyond gap enumeration — is characterising the
nature of the divide between the ML detection and IS governance traditions. The
Operationalization Chasm (AT1) is not merely a practical gap waiting to be filled by
a single study. It reflects a genuine conceptual problem: the two traditions do not
share a common definition of what financial corruption is as a computable quantity.
Resolving this requires constructing a theoretically grounded bridge between sociological
corruption typology (documented by governance scholars) and computational feature design
(required by ML practitioners). This conceptual bridge is the primary theoretical
contribution that a primary study grounded in this SLR must deliver.

## 6.3 Limitations

Four limitations qualify the review's scope and conclusions.

**Protocol pre-registration**: The review protocol was not registered with PROSPERO or
an equivalent registry prior to commencing searches. This is a methodological limitation
that reduces protection against post-hoc adjustment, though all decisions are
version-controlled and documented in the execution plan.

**Database coverage**: Automated retrieval via OpenAlex API captured approximately 60%
of the expected corpus prior to Scopus and IEEE manual exports. Some papers accessible
only through institutional Scopus access may not have been retrieved in the automated
stage. Sensitivity analysis across quality thresholds mitigates but does not eliminate
this risk.

**Language boundary**: Inclusion criteria encompassed English and Indonesian papers.
Papers in other languages (particularly Chinese-language ML detection literature) were
excluded. This creates potential under-representation of GNN-based detection methods
primarily published in Chinese venues.

**DT5 quality instability**: Village fund governance papers predominantly appear in
unranked Indonesian journals, creating scoring disadvantages in the composite quality
metric. The domain-override protocol addresses this, but DT5-based conclusions should
be read as resting on a corpus subset with lower quality scores than the ML detection
cluster.

## 6.4 Future Research Directions

The five identified gaps directly inform a primary empirical research agenda:

1. **Immediate (primary study)**: Apply unsupervised ensemble (IF, LOF, Autoencoder) to
   Jambi Province Dana Desa disbursement data (2023–2025), implementing the 12-feature
   taxonomy derived from the KPK corruption typology, with expert validation against
   KPK/BPK audit records as surrogate ground truth evaluation.

2. **Medium-term**: Develop and validate a Dana Desa–specific quality assessment framework
   for ML detection artifacts incorporating IS Success Model dimensions — information
   quality (score interpretability), system quality (batch processing reliability), and
   net benefits (audit targeting efficiency improvement).

3. **Long-term**: Extend the detection framework to real-time monitoring integration with
   SiKPA/SIMDA village financial information systems, addressing G5's deployment gap
   through streaming architecture design and edge computation for village-level data.

4. **Comparative**: Replicate the primary study in other Indonesian provinces and
   subsequently in comparable fiscal decentralization programmes (Philippines, Bangladesh)
   to establish generalizability boundaries for the feature engineering framework.

## 6.5 Closing Statement

This review demonstrates that the convergence of ML capabilities and governance data
availability creates conditions for a technically achievable and institutionally valuable
contribution to Indonesian anti-corruption practice. The specific value of the primary
study is not algorithmic novelty — the methods it applies are established — but
contextual and theoretical novelty: being the first study to ask, and empirically answer,
what village fund corruption looks like as a machine-detectable pattern in real
government financial data. The five-gap synthesis reported here provides the justification,
design parameters, and theoretical grounding that makes that contribution rigorous.
