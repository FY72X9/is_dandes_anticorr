# SLR Coding Guide v1.0

> **Study**: ML-Based Financial Anomaly Detection for Anti-Corruption IS — Systematic Literature Review
> **Guide version**: 1.0
> **Effective from**: Phase E Stage 0 (April 2026)
> **Applies to**: `coded_corpus.csv` (96 papers: 45 INCLUDED + 51 BORDERLINE)
> **Coders**: Coder 1 (primary researcher) + Coder 2 (co-author)

---

## 1. Purpose and Scope

This guide governs all coding decisions during Phase E (IRR & Coding). It defines:
- Inclusion/exclusion screening criteria (Stage 1 IRR)
- Quality score calibration rubric (Stage 2 IRR)
- Domain override protocol (Stage 0, solo)
- Data extraction schema (Stage 3, Phase F preparation)
- Conflict resolution procedure

All decisions are recorded in `SLR/scripts/output/coded_corpus.csv`. No verbal decisions — every judgment must be written in the appropriate column before the next paper is coded.

---

## 2. Research Questions (Reference)

| Code | Research Question | Scope Boundary |
|---|---|---|
| **RQ1** | What computational methods and IS-grounded theoretical frameworks have been applied to detect financial anomalies indicative of corruption in government expenditure systems? | Methods: supervised, unsupervised, hybrid ML; audit analytics; rule-based. Sector: government/public, not solely corporate or banking. |
| **RQ2** | How have existing studies operationalized corruption typologies and modus operandi as computationally detectable feature signals? | Translation of corruption behavior (mark-up, fictitious projects, procurement irregularities, fund diversion) into quantifiable variables or detection rules. |
| **RQ3** | What methodological, contextual, and theoretical gaps prevent scalable, near-real-time corruption detection applicable to village-level financial governance in developing countries? | Gap analysis: developing-country IS coverage, label scarcity, IS-theoretical evaluation criteria, detection lag. |

---

## 3. Stage 0 — Domain Override Protocol (Coder 1 Solo)

### 3.1 Who applies this

Coder 1 only. Stage 0 runs **before** Stage 1 IRR and does not require co-author review.

### 3.2 Which papers to review

Papers with `domain_override_candidate = TRUE` in `coded_corpus.csv`. There are **12 such papers** (P027, P047–P060 range — see column filter). All currently have `pipeline_status = BORDERLINE` and `quality_score = 4.15`.

### 3.3 Decision criteria

Read the abstract of each paper. Apply override if the paper meets **any one** of the following:

| Criterion | Override code |
|---|---|
| Paper addresses village fund (Dana Desa) / sub-national Indonesian fiscal governance empirically | `DOMAIN_OVERRIDE_RQ2` |
| Paper addresses applicability gaps, institutional barriers, or developing-country IS implementation challenges | `DOMAIN_OVERRIDE_RQ3` |
| Paper uses data-driven or IS-theoretic methods to detect corruption/fraud specifically in government expenditure | `DOMAIN_OVERRIDE_RQ1_RQ2` |
| Paper provides KPK/BPKP audit evidence, judicial verdict analysis, or corruption typology from Indonesian context | `DOMAIN_OVERRIDE_RQ2` |

### 3.4 How to record override

In `coded_corpus.csv`:
1. Set `adjudication_note` = appropriate override code (e.g. `DOMAIN_OVERRIDE_RQ2`)
2. Do NOT change `quality_score` column — preserve pipeline score for transparency
3. Set `irr_resolution` = `DOMAIN_OVERRIDE`
4. Set `coder1_screen` = `INCLUDE`

### 3.5 What NOT to override

- Papers whose low score reflects genuinely low methodological rigor (no validation, no empirical data)
- Papers that merely mention Dana Desa in passing without substantive analysis
- Papers from predatory journals (check Beall's list if uncertain)

### 3.6 Rationale

The pipeline quality score assigns `score_journal_quality = 2.0` to all unranked journals — a 30%-weight dimension. This systematically subtracts ~0.6 from composite for any paper in a developing-country IS journal not indexed in SCImago or JCR. For papers that are the *only available evidence* for RQ2/RQ3, this is a measurement artifact, not a quality signal. Precedent: Petticrew & Roberts (2006) advocate purposive sampling supplementary to systematic search when domain-specific evidence bases are structurally thin.

---

## 4. Stage 1 — Title + Abstract Screening IRR

### 4.1 Applies to

All 113 papers that passed Stage 1 IC/EC filter in the pipeline (reflected in `coded_corpus.csv` as the 96 papers with `quality_score ≥ 4.0`; plus 17 that scored < 4.0 which may be spot-checked for false exclusions).

### 4.2 Screening procedure

1. Coder 1 and Coder 2 independently open `coded_corpus.csv`
2. Read **title + abstract** only (do not read full text at this stage)
3. Record decision in `coder1_screen` or `coder2_screen` respectively
4. Use only these three values:

| Value | Meaning |
|---|---|
| `INCLUDE` | Paper clearly addresses at least one RQ; proceed to quality scoring |
| `EXCLUDE` | Paper clearly does not address any RQ; record reason in `notes` column |
| `UNCERTAIN` | Title/abstract insufficient to decide; flag for full-text check |

### 4.3 Exclusion reasons (for `notes` column)

Use these codes in the `notes` column when recording `EXCLUDE`:

| Code | Reason |
|---|---|
| EC-01 | Year out of scope (pre-2010 without anchor justification) |
| EC-02 | Domain: private sector / banking only (no public sector coverage) |
| EC-03 | Non-indexed conference proceedings / predatory venue |
| EC-04 | No computational or IS-theoretic method |
| EC-05 | Duplicate (same dataset or substantially overlapping findings as another included paper) |
| EC-06 | Language: non-English without accessible English abstract |
| EC-07 | Off-topic: no connection to fraud, corruption, or anomaly detection |

### 4.4 IRR calculation

After both coders complete independent screening:
1. Export `coder1_screen` and `coder2_screen` columns
2. Compute Cohen's κ on INCLUDE/EXCLUDE binary (treat UNCERTAIN as EXCLUDE for κ calculation)
3. Target: **κ ≥ 0.75**
4. If κ < 0.75: review all DISAGREE cases together; revise this guide; re-screen the disagreement subset

### 4.5 Disagreement resolution

| Scenario | Action |
|---|---|
| One says INCLUDE, other says EXCLUDE | Consensus discussion; write resolution in `irr_resolution` |
| Both say UNCERTAIN | Both read full text; re-screen |
| Consensus not reached after discussion | Third-party adjudicator (supervisor / department head) |

---

## 5. Stage 2 — Quality Score Calibration

### 5.1 Pilot sample

Both coders independently score the **same 20% random sample** (~9 papers from the 45 included set). Select by: `paper_id` ending in 0 or 5 (P005, P010, P015, P020, P025, P030, P035, P040, P045).

### 5.2 Scoring rubric

Score each dimension on the scale provided. Do not round — use exact values from the rubric. The pipeline already computed scores; coders validate and may *revise* pipeline scores if they disagree.

#### D1 — Journal / Venue Quality (weight: 25%)

| Value | Criterion |
|---|---|
| 10 | SJR Q1 journal OR CORE A* IS conference |
| 7 | SJR Q2 journal OR CORE A conference |
| 5 | SJR Q3 journal OR CORE B conference |
| 3 | SJR Q4 journal OR CORE C conference |
| 2 | Unranked journal / no venue metadata |
| *Override* | Domain-override papers: treat as 5.0 for scoring purposes after Stage 0 |

#### D2 — Methodological Rigor (weight: 25%)

| Value | Criterion |
|---|---|
| 10 | Reproducible method + empirical validation + comparison baseline |
| 7 | Empirical validation present; no comparison baseline |
| 5 | Descriptive/analytical; no empirical validation |
| 3 | Opinion, review, or position paper without systematic method |

#### D3 — Relevance to RQ (weight: 20%)

| Value | Criterion |
|---|---|
| 10 | Directly addresses all three RQs |
| 7 | Addresses two RQs substantively |
| 4 | Addresses one RQ substantively |
| 2 | Tangential connection to any RQ |
| 0 | No connection |

#### D4 — Recency (weight: 15%)

| Value | Year |
|---|---|
| 10 | 2022–2026 |
| 7 | 2018–2021 |
| 5 | 2014–2017 |
| 3 | ≤ 2013 (non-anchor) |

#### D5 — Citation Impact (weight: 15%)

| Value | Criterion |
|---|---|
| 10 | Top quartile by year-normalized citations (MNCS ≥ 1.5) |
| 7 | Second quartile (MNCS 0.75–1.49) |
| 4 | Third/fourth quartile (MNCS < 0.75) |
| 2 | < 5 citations total (for papers < 2 years old: use 7 as default) |

*MNCS approximation*: divide raw citation count by mean citations for papers of same year in same discipline. For pragmatic scoring without per-discipline data, use: (citations / years_since_pub) relative to median of the full 45-paper included corpus.

### 5.3 Composite formula

```
quality_score = (D1 × 0.25) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.15)
```

### 5.4 Per-dimension κ targets

| Dimension | Minimum κ | Action if below |
|---|---|---|
| D1 Journal Quality | 0.80 | Review SCImago/CORE lookup procedure |
| D2 Methodological Rigor | 0.70 | Re-define boundary between 7 and 5; add examples |
| D3 Relevance | 0.70 | Sharpen RQ scope boundary descriptions; add anchor examples |
| D4 Recency | 0.90 | Purely year-based; low κ indicates data entry error |
| D5 Citation Impact | 0.75 | Agree on MNCS approximation procedure |

---

## 6. Column Definitions — `coded_corpus.csv`

| Column | Coder fills? | Values / Format | Notes |
|---|---|---|---|
| `paper_id` | No (auto) | P001–P096 | Sequential; do not change |
| `doi` | No (auto) | DOI string | From pipeline |
| `title` | No (auto) | Free text | From pipeline |
| `authors` | No (auto) | Free text | From pipeline |
| `year` | No (auto) | Integer | From pipeline |
| `journal` | No (auto) | Free text | From pipeline |
| `sjr_quartile` | No (auto) | Q1/Q2/Q3/Q4/nan | From `enrich_journal_metadata.py` |
| `citations` | No (auto) | Integer | From pipeline (OpenAlex) |
| `quality_score` | No (auto) | Float 0–10 | Pipeline score; **do not overwrite**; use `adjudication_note` if override |
| `score_journal` | No (auto) | Float | Pipeline D1 |
| `score_rigor` | No (auto) | Float | Pipeline D2 |
| `score_relevance` | No (auto) | Float | Pipeline D3 |
| `score_recency` | No (auto) | Float | Pipeline D4 |
| `score_citation` | No (auto) | Float | Pipeline D5 |
| `pipeline_status` | No (auto) | INCLUDED / BORDERLINE | From pipeline |
| `pdf_filename` | No (auto) | filename.pdf / NaN | From pipeline |
| `acquisition_status` | No (auto) | Free text | From pipeline Stage 3 |
| `relevance_tier` | No (auto) | HIGH/MEDIUM/LOW/OFF_TOPIC | From crosscheck_papers.py |
| `rq_tags` | No (auto) | RQ1,RQ2,RQ3 combinations | From crosscheck_papers.py |
| `domain_override_candidate` | No (auto) | TRUE / blank | Pre-flagged: 12 papers |
| `adjudication_note` | **CODER 1** | See §3.4 / §4.5 | Record override or IRR decision code |
| `coder1_screen` | **CODER 1** | INCLUDE / EXCLUDE / UNCERTAIN | Stage 1 independent screen |
| `coder2_screen` | **CODER 2** | INCLUDE / EXCLUDE / UNCERTAIN | Stage 1 independent screen |
| `irr_agreement` | Post-IRR | AGREE / DISAGREE | Computed after both coders finish |
| `irr_resolution` | Post-IRR | CONSENSUS / ADJUDICATED / EXCLUDED / DOMAIN_OVERRIDE | Final decision |
| `anchor` | CODER 1 | TRUE / blank | For pre-2010 seminal papers only |
| `theme_tags` | Phase F | pipe-separated tags | e.g. `isolation_forest\|dana_desa\|feature_engineering` |
| `full_text_extracted` | Phase F | TRUE / blank | Set after full-text data extraction |
| `notes` | CODER 1/2 | Free text | Exclusion codes, disagreement notes, observations |

---

## 7. Theoretical Anchor Tagging

Papers published before 2010 may qualify as **Theoretical Anchors** if they meet all three criteria:

1. ≥ 300 total citations (Scopus or OpenAlex, April 2026 count)
2. Cited in ≥ 3 peer-reviewed papers published 2020–2026
3. Makes a foundational theoretical claim still active in IS literature

If a pre-2010 paper meets these criteria: set `anchor = TRUE` and `adjudication_note = ANCHOR_SEMINAL`.
Anchor papers are included in the narrative synthesis but **excluded from bibliometric cluster analysis**.

Known anchors confirmed (add `anchor = TRUE` manually):
- Cressey (1953) Fraud Triangle — cited via Dorminey et al. (2012) DOI: 10.2308/iace-50131
- DiMaggio & Powell (1983) Institutional Theory — DOI: 10.2307/2095101

---

## 8. Conflict Resolution Ladder

| Level | Mechanism | Timeframe |
|---|---|---|
| L1 | Asynchronous: coders review each other's reasoning in `notes` column | 2 days |
| L2 | Synchronous: 30-min consensus call; write joint decision in `irr_resolution` | 1 week |
| L3 | Third adjudicator reads abstract + writes binding decision | 2 weeks |

Disagreements that reach L3 are documented in the SLR paper limitations section.

---

## 9. Workflow Summary for Each Phase E Stage

```
Stage 0 (Coder 1 solo, ~2–3 hours)
  For each of P027, P047–P060:
    1. Open PDF or abstract
    2. Apply criteria from §3.3
    3. Fill: adjudication_note, irr_resolution=DOMAIN_OVERRIDE, coder1_screen=INCLUDE
    4. Add rq_tags if missing

Stage 1 (Both coders, ~4–6 hours each)
  For each of P001–P096:
    1. Read title + abstract
    2. Fill: coder1_screen OR coder2_screen
    3. If EXCLUDE: add EC code to notes
  After both done:
    4. Compute Cohen's κ → document in irr_pilot_results.csv
    5. If κ < 0.75: consensus round

Stage 2 (Both coders, ~3 hours)
  Pilot set: P005, P010, P015, P020, P025, P030, P035, P040, P045
    1. Score each D1–D5 independently
    2. Compute per-dimension κ
    3. If any dimension κ < 0.70: revise rubric, re-score
  Remaining corpus:
    4. Coder 1 scores all; Coder 2 audits BORDERLINE + override papers
```

---

## 10. Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-29 | Initial release — Phase E Stage 0/1/2 protocol; scoring rubric v1 |
