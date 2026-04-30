# Section 5: Discussion

> **Basis**: Synthesis of SLR F2–F7 findings — 45 papers, 4 analytical themes,
> 5 structured gaps, DSR framework, narrative logic model

---

## 5.1 Principal Findings

This systematic literature review synthesized 45 empirical studies on ML-based financial
anomaly detection and IS governance of public funds to establish the state of knowledge
at the intersection of these two research traditions. Four analytical themes emerge from
the cross-paper analysis.

### AT1: The Operationalization Chasm

The corpus divides structurally into two non-communicating research traditions: an ML
detection cluster (23 papers) that has developed high-performing computational methods
without application to village governance contexts, and an IS governance cluster
(26 papers) that has documented corruption mechanisms in detail without computational
operationalization. Only nine papers span both clusters, and none of these bridge papers
test detection artifacts on Dana Desa or equivalent sub-national village fund data.

The bibliometric cluster analysis (F4) confirms this structure: ML and governance
keywords exhibit near-zero co-occurrence across clusters, despite both literatures
claiming to address 'public fund corruption'. This is not a minor gap — it represents
the complete absence of a research tradition that this study initiates.

### AT2: The Scalability Illusion

Performance claims in the ML detection literature are systematically inflated by
evaluation conditions that do not generalize to decentralized governance contexts.
The four papers assuming centralized databases (AC-CENTRAL) achieve AUC scores that
cannot be replicated in settings where data is fragmented across 74,000 village
governments. The twelve papers using synthetic training data create a circular validation
problem: high performance on synthetic data does not evidence detection capability on
real corrupt transactions, which by definition were designed to evade detection.

### AT3: The Absence of IS Theory

Sixty-two percent of included papers (28/45) apply no IS theory. This rate exceeds what
would be expected for interdisciplinary research bridging computer science and information
systems; it indicates that the ML detection strand treats fraud detection as a purely
computational rather than socio-institutional phenomenon. The governance strand, while
more theoretically grounded, applies IS theory to institutional analysis rather than to
computational artifact design. No paper applies Agency Theory to motivate detection
feature selection; no paper uses the IS Success Model to evaluate deployment effectiveness.

### AT4: The Ground Truth Paradox

The label scarcity problem identified in 17 papers is not merely a practical constraint —
it is an epistemological paradox specific to governance contexts. In private sector fraud
detection, historical labeled datasets exist (successful prosecutions, confirmed fraud
cases). In village fund governance, corruption is often undetected or unprosecuted,
meaning the absence of labels reflects the severity of the problem rather than the
absence of fraudulent activity. Supervised methods claiming high F1 scores on labeled
village datasets are detecting the corruption that was already discovered, not the
corruption that remains hidden.

---

## 5.2 Research Gap Analysis

**Table 3: Structured Gap Matrix**

| Gap ID | Gap Statement (abbreviated) | Severity | Evidence Basis | Primary Study Response |
|---|---|---|---|---|
| G1 | No existing study applies ML anomaly detection to Dana Desa (village fund) financial trans... | **CRITICAL** | Literature void — confirmed by keyword search, clu... | Design and evaluate ML anomaly detection artifact using real... |
| G2 | Ground truth unavailability for village fraud labels creates an epistemological paradox: s... | **CRITICAL** | LIM-NOLABEL (17 papers), DS-SYNTH (12 papers), cir... | Adopt unsupervised ensemble approach (no labels required). U... |
| G3 | No validated feature engineering methodology exists for village fund fraud detection. The ... | **CRITICAL** | FE category thin (<5 papers on budget absorption);... | Construct 12-feature taxonomy for Dana Desa fraud detection ... |
| G4 | IS theoretical grounding is absent from 62% of included papers. The ML detection literatur... | **PARTIAL** | IST-NONE: 28/45 (62%); 0 D&M IS Success Model appl... | Ground primary study in Agency Theory (principal-agent corru... |
| G5 | All validated ML detection methods require batch processing of historical transaction data... | **METHODOLOGICAL** | GAP-RT (4 papers explicitly note real-time gap); D... | Explicitly scope primary study as audit-support tool (post-p... |

**Table 4: DSR Framework — Empty Quadrant Analysis**

| DSR Cycle | Context Level | N Papers | Research Status |
|---|---|---|---|
| DESIGN | cross-national (developed) | 4 | N=4 |
| DESIGN | cross-national (developing) | 0 | Empty |
| DESIGN | national | 2 | N=2 |
| DESIGN | sub-national | 0 | **EMPTY — Primary contribution** |
| DESIGN | unspecified | 5 | N=5 |
| DESIGN | village | 0 | **EMPTY — Primary contribution** |
| RELEVANCE | cross-national (developed) | 0 | Empty |
| RELEVANCE | cross-national (developing) | 0 | Empty |
| RELEVANCE | national | 1 | N=1 |
| RELEVANCE | sub-national | 0 | Empty |
| RELEVANCE | unspecified | 2 | N=2 |
| RELEVANCE | village | 12 | N=12 |
| RIGOR | cross-national (developed) | 4 | N=4 |
| RIGOR | cross-national (developing) | 5 | N=5 |
| RIGOR | national | 5 | N=5 |
| RIGOR | sub-national | 2 | N=2 |
| RIGOR | unspecified | 1 | N=1 |
| RIGOR | village | 2 | N=2 |

The most consequential empty cell in Table 4 is the intersection of DESIGN cycle
and village-level context. Hevner et al. [ref] define the design cycle as the
iterative construction and evaluation of IS artifacts within their intended use context.
Eleven papers operate in the DESIGN cycle, but none targets the village/sub-national
governance context. This structural absence motivates the primary study's DSR framing:
its contribution is precisely the artifact produced by filling this empty cell.

---

## 5.3 Theoretical Implications

**For IS theory**: This review demonstrates that IS theory remains systematically
disconnected from computational methods in the fraud detection domain. This is
not a failure of individual researchers — it reflects the structural absence of
interdisciplinary venue conventions that would require ML papers to theorize their
governance implications. The primary study models an alternative approach: grounding
feature engineering choices in Agency Theory principal-agent dynamics, rather than
treating feature selection as a purely statistical optimization problem.

**For design science research**: The DSR three-cycle model predicts that artifacts
developed in isolation from their relevance environments will fail in deployment.
The Scalability Illusion (AT2) and Ground Truth Paradox (AT4) are exactly the
failures predicted by DSR: when design-cycle work proceeds without relevance-cycle
grounding, the resulting artifacts perform well in lab conditions but inadequately
in real governance environments.

**For development informatics**: The concentration of 21 papers in high-capacity
institutional contexts (banking, federal systems) and the near-absence of papers
addressing decentralized, low-capacity governance confirms the development informatics
critique that IS research systematically underserves the institutional conditions of
the Global South. The village fund governance context — characterized by 74,000
fragmented administrative units, limited data infrastructure, and enforcement gaps —
represents exactly the institutional environment that development informatics demands
IS researchers to address.

---

## 5.4 Practical Implications

The review findings carry direct implications for Indonesian government agencies:

**For KPK (Corruption Eradication Commission)**: The absence of a validated ML
detection methodology for Dana Desa means that current fraud screening relies on
manual audit sampling with inherently limited coverage. The primary study's contribution
provides a prototype methodology that could be integrated into JAGA (KPK's anti-corruption
monitoring platform) to prioritize village-level audits based on anomaly score rankings.

**For Kemendesa**: The feature engineering taxonomy constructed for this study identifies
six operationally actionable fraud indicators derived from budget realization data already
collected in SISKEUDES. Automated flag generation requires no new data collection —
only algorithmic analysis of existing administrative records.

**For BPK/BPKP**: The logic model (F5) identifies the 'last mile' gap between ML
anomaly output and audit work product. Future research should focus on designing
the human-AI interaction interface that translates anomaly scores into investigation
referrals compatible with BPK/BPKP evidentiary standards.

---

## 5.5 Limitations of the Review

Several limitations constrain the scope of this review's conclusions:

**Language bias**: The search strategy retrieved only English-language publications.
Indonesian-language research on Dana Desa governance (published in national journals)
was not systematically captured, potentially underrepresenting governance-specific
feature engineering knowledge.

**Publication bias**: Null results and failed ML deployments are underreported in the
corpus. The high AUC scores in the ML cluster may reflect publication bias toward
positive technical results.

**Temporal limitation**: The corpus covers 2018–2025. The rapid pace of LLM and
foundation model development means detection methods based on transformer architectures
(emerging 2023–2025) may be underrepresented relative to their actual capability level.

**Sensitivity analysis caveat**: The three-tier sensitivity analysis (F6) reveals that
6 of 10 descriptive themes show proportional shifts when quality thresholds are raised.
This indicates that medium-quality papers (quality score 4.0–4.5) contribute substantially
to the thematic picture; researchers requiring a higher-confidence sub-corpus should
apply the T2 threshold (≥4.5, N=23) for replication studies.

---

_This discussion section was generated by Phase F7 gap matrix synthesis._
_All analytical claims are traceable to specific codes, papers, and quantitative evidence in the SLR analysis files._