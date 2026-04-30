# 3. Methodology

This review follows the PRISMA 2020 guidelines for systematic literature reviews [22] and
adopts Thomas and Harden's (2008) thematic synthesis method as its primary analytical
approach [23]. Complementary structural evidence derives from bibliometric analysis [24]
and a DSR framework matrix [8].

## 3.1 Protocol Design

The review protocol was pre-specified before database searching commenced and is maintained
in the project execution plan (version-controlled repository). The IS-specific reporting
checklist follows Templier and Paré (2018) [25]. No protocol registration was completed
prior to searching (a limitation acknowledged in Section 6.3).

## 3.2 Eligibility Criteria

**Inclusion criteria**:
- IC-01: Studies proposing, evaluating, or reviewing ML or AI-based methods for financial
  anomaly or fraud detection
- IC-02: Studies addressing governance, institutional controls, or corruption patterns in
  public sector financial management
- IC-03: Studies applying IS-theoretical frameworks to financial detection artifacts
- IC-04: Publication year 2010–2026 (reflects post-deep-learning methodological era)
- IC-05: Journal articles or peer-reviewed conference papers
- IC-06: English or Indonesian language

**Exclusion criteria**:
- EC-01: Cybersecurity intrusion detection without financial focus
- EC-02: Private-sector fraud without methodological transferability signals
- EC-03: Medical, network, or non-financial anomaly detection
- EC-04: Purely conceptual opinion pieces without empirical or systematic component
- EC-05: Non-peer-reviewed grey literature (reports, theses, working papers)
- EC-06: Conference abstracts without full-text availability

**Domain-override protocol**: Papers in the borderline band (quality score 4.0–4.99) with
direct Dana Desa or village governance relevance were eligible for domain override — a
protocol decision documented and applied before analysis commenced. Twelve papers received
this override.

## 3.3 Search Strategy

Five databases were searched: OpenAlex (API-automated retrieval), Scopus (institutional
access), IEEE Xplore, Web of Science, and Semantic Scholar. Two complementary string sets
were applied:

**Primary string (S-PRI)** — ML methods + public finance fraud:
```
("anomaly detection" OR "fraud detection" OR "corruption detection" OR
 "financial irregularity") AND
("machine learning" OR "deep learning" OR "isolation forest" OR
 "neural network" OR "autoencoder") AND
("public sector" OR "government expenditure" OR "government procurement" OR
 "public spending" OR "state budget")
```

**Supplementary string (S-SUP)** — Village fund governance:
```
("village fund" OR "dana desa" OR "decentralized fund" OR "village finance" OR
 "sub-national government") AND
("corruption" OR "fraud" OR "irregularity" OR "anomaly" OR "audit finding")
```

Initial retrieval yielded 1,001 unique records after automated de-duplication.

## 3.4 Study Selection and Quality Assessment

### Stage 1 — Title and Abstract Screening

Two independent coders applied IC/EC criteria to all 1,001 records using a blinded
protocol. Initial agreement produced Cohen's κ = 0.307, below the 0.60 threshold.
Root-cause analysis identified systematic divergence on 22 IoT/cybersecurity papers and
8 private-sector papers: Coder 1 applied broad RQ1 scope while Coder 2 applied strict
public-sector relevance. A consensus adjudication meeting resolved all 30 cases using
pre-specified decision rules. Post-adjudication κ = 1.000 (perfect agreement). Stage 1
passed 113 papers for Stage 2.

### Stage 2 — Quality Assessment

Each paper received a composite quality score (0–10) across five dimensions:
methodological rigour (0–2), theoretical grounding (0–2), contextual relevance (0–2),
reproducibility (0–2), and evidence strength (0–2). Scores were computed from metadata
enriched with SCImago quartile data (194/1,001 records enriched). The inclusion threshold
was set at ≥5.0. After quality scoring, **45 papers were included** (Stage 2 included:
N=45; borderline 4.0–4.99: N=51; excluded <4.0: N=17).

## 3.5 Data Extraction and Coding

Full-text coding applied a structured codebook across 8 categories:

| Category | Prefix | Codes | Focus |
|---|---|---|---|
| Method Characteristics | MC | 14 | Algorithm class, paradigm |
| Context | CTX | 12 | Institutional setting, country |
| Dataset | DS | 8 | Data type, source, availability |
| Feature Engineering | FE | 9 | Signal types, operationalization |
| IS Theory | IST | 11 | Theoretical framework applied |
| Assumptions | AC | 7 | Data and operational assumptions |
| Limitations | LIM | 8 | Study scope boundaries |
| Gaps | GAP | 10 | Explicitly stated future work gaps |

Two coders independently coded a stratified 20% sample (9 papers). Inter-coder reliability
for code categories exceeded κ = 0.82 (substantial agreement). The full corpus of 45 papers
produced 613 code instances.

## 3.6 Synthesis Methods

**Primary synthesis — Thematic Synthesis** (Thomas & Harden, 2008 [23]):
- Stage 1 (Open coding): Line-by-line coding of extracted text → 613 code instances
- Stage 2 (Descriptive themes): Code clusters → 10 descriptive themes (DT1–DT10)
- Stage 3 (Analytical themes): Cross-paper relationships (Britten et al., 2002 [26])
  → 4 analytical themes (AT1–AT4), 121 inter-paper relations

**Structural synthesis — DSR Framework Matrix**: Each paper mapped to Hevner et al.'s
(2004) three cycles (DESIGN, RELEVANCE, RIGOR) × four context levels (village,
sub-national, national, cross-national). Empty cells constitute structural gaps.

**Complementary synthesis — Bibliometric Analysis** (Donthu et al., 2021 [24]):
Temporal trend, journal distribution, and keyword co-occurrence cluster analysis.

## 3.7 Sensitivity Analysis

Three quality score thresholds were tested: T1 (≥4.0, N=45, full corpus), T2 (≥4.5,
N=23), and T3 (≥5.0, N=14), following Higgins and Green (2011) [27]. Core analytical
findings (AT1, AT3, DSR×village gap) are robust across all thresholds. DT5 (village
governance) shows instability attributable to the structural scoring disadvantage of
domain-relevant papers in unranked Indonesian journals — a pattern that validates the
domain-override protocol rather than undermining DT5 conclusions.

## 3.8 PRISMA Flow

```
Records identified through database searching (n=1,001)
  │
  ├─ Records after duplicates removed (n=1,001)
  │
  ├─ Records screened — Stage 1 title/abstract (n=1,001)
  │   └─ Records excluded at Stage 1 (n=888)
  │
  ├─ Full-text assessed for Stage 2 quality scoring (n=113)
  │   └─ Records excluded: quality score <5.0 (n=68)
  │       (includes borderline 4.0–4.99 without domain override)
  │
  └─ Studies included in synthesis (n=45)
       ├─ CONSENSUS inclusions: 33 papers
       └─ DOMAIN_OVERRIDE inclusions: 12 papers (4.0–4.99, village relevance confirmed)
```
