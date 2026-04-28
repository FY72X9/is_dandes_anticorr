# SLR Execution Plan — ML-Based Financial Anomaly Detection for Anti-Corruption IS

> **Study**: Systematic Literature Review (SLR) — prerequisite for Phase 1 empirical study
> **Target venue**: PACIS or AMCIS (decision pending Phase B scoping run)
> **Target corpus**: 40–80 papers
> **Last updated**: April 29, 2026

---

## Phase Status Overview

| Phase | Name | Status | Output |
|---|---|---|---|
| **A** | Infrastructure — Build `quality_filter_slr.py` | ✅ COMPLETED — 2026-04-28 | `scripts/quality_filter_slr.py` |
| **B** | Search Design — Mini scoping run + search strings | ✅ COMPLETED — 2026-04-28 | `docs/draft/scoping_run_results.md`, `docs/draft/search_strings.md` |
| **C** | Retrieval — Full database search → `papers_raw.csv` | ✅ COMPLETED — 2026-04-28 | `scripts/papers_raw.csv` |
| **D** | Filter & Acquire — Run pipeline → corpus + PDFs | ✅ COMPLETED — 2026-04-29 | `papers/`, `scripts/output/` |
| **E** | IRR & Coding — Co-author screening + quality calibration | ⏳ NOT STARTED | `scripts/output/irr_pilot_results.csv`, `scripts/output/coded_corpus.csv` |
| **F** | Analysis — Sensitivity + bibliometric + synthesis | ⏳ NOT STARTED | `docs/draft/bibliometric_report.md`, `docs/draft/framework_synthesis_matrix.csv` |
| **G** | Writing — Draft paper + gap matrix + submit | ⏳ NOT STARTED | `docs/draft/`, `docs/latex/` |

---

## Phase A — Infrastructure

**Goal**: Build `quality_filter_slr.py` as a fully executable 3-stage pipeline (Filter → Score → Acquire).

**Status**: ✅ COMPLETED — April 28, 2026

**Deliverable**: `scripts/quality_filter_slr.py`

**What it does**:
- Stage 1: Applies IC-01–IC-06 and EC-01–EC-06 inclusion/exclusion logic against `papers_raw.csv`
- Stage 2: Computes weighted composite quality score (0–10) across 5 dimensions; splits corpus into included (≥6.0), borderline (4.0–5.9), excluded (<4.0)
- Stage 3: Cascading OA download — OpenAlex → Unpaywall → Semantic Scholar → Direct URL → arXiv normalization; invalid PDFs logged for manual download

**Outputs**:
- `scripts/output/slr_included_corpus.csv` — final included set with scores
- `scripts/output/slr_borderline.csv` — borderline papers for human adjudication
- `scripts/output/slr_excluded_log.csv` — excluded papers with reason codes
- `papers/` — validated PDF downloads (≥8 KB, %PDF magic bytes)
- `scripts/output/manual_download_log.txt` — papers requiring manual retrieval

---

## Phase B — Search Design

**Goal**: Validate corpus density (40–80 papers reachable) and finalize Boolean search strings.

**Status**: ✅ COMPLETED — April 28, 2026

**Deliverables**:
- `docs/draft/scoping_run_results.md` — OpenAlex hit counts + sample titles + nearest SLR candidates
- `docs/draft/search_strings.md` — Finalized Boolean strings for all 5 databases (Scopus, IEEE, WoS, OpenAlex, Semantic Scholar) + `papers_raw.csv` column mapping guide

**Key findings from scoping run**:

| Finding | Implication |
|---|---|
| S3 (Dana Desa): **57 articles, 0 existing SLRs** | **Novelty confirmed.** No prior SLR covers village-level IS corruption detection. |
| S4 (Feature Engineering + Typology): 249 articles | RQ2 has sparse literature — gap is real and documentable |
| S1/S6 (broad ML + fraud): 3,000–5,000+ raw hits | OpenAlex semantic search is noisy. Scopus Boolean will yield ~80–150 targeted hits |
| 25 SLR candidates retrieved | None cover Dana Desa / village-level IS specifically — novelty claim holds |
| Estimated post-dedup raw pool: 150–300 | Post IC/EC filter (15–25%): 24–87 included — target range **achievable** |

**Verdict**: ✅ Proceed to Phase C. Corpus density target 40–80 is achievable with Scopus+IEEE+WoS Boolean searches.

---

## Phase C — Retrieval

**Goal**: Execute full search across 5 databases → export unified `papers_raw.csv`.

**Status**: ✅ COMPLETED 2026-04-28 (auto-retrieval from OpenAlex; Scopus/IEEE/WoS pending manual export)

**Databases**: Scopus (institutional BINUS), IEEE Xplore, WoS (institutional BINUS), OpenAlex (free API), Semantic Scholar (free API)

**Steps**:
1. ✅ `retrieve_apis.py` built and executed → automated retrieval from OpenAlex (5 queries, paginated)
2. ✅ Semantic Scholar 429 rate-limit (no key) → 0 records from S2 (OpenAlex compensates adequately)
3. ✅ `papers_raw.csv` written with 1,001 rows; 945 unique after DOI+title dedup
4. ✅ `papers_manual_template.csv` written for Scopus/IEEE/WoS manual merge
5. ⚠️ Scopus / IEEE Xplore / WoS: must be exported manually (institutional login)
   → Use strings from `docs/draft/search_strings.md`; append rows to `papers_raw.csv`
6. ✅ `retrieval_report.txt` written with per-query counts

**Key findings**:
- OpenAlex S3 (Dana Desa): 60 records retrieved (ALL available)
- OpenAlex S4 (Typology): 300/515 available (top by relevance, capped)
- OpenAlex S5 (Decentralized): 300/897 available (capped)
- OpenAlex S1 (Broad ML): 200/4,336 available (top cited, capped)
- OpenAlex S6 (Procurement): 150/2,389 available (top cited, capped)
- Duplicates flagged: 56 (5.6%)
- Unique records: 945

**Verdict**: Proceed to manual export from Scopus/IEEE/WoS, then Phase D.
After manual merge, expected raw pool ~1,100–1,300; IC/EC filter will yield 40–80 included.

**Output**: `scripts/papers_raw.csv` (1,001 rows / 945 unique; partial — add Scopus/IEEE/WoS before Phase D)

---

## Phase D — Filter & Acquire

**Goal**: Run `quality_filter_slr.py` on `papers_raw.csv`; download all available OA PDFs.

**Status**: ✅ COMPLETED — April 29, 2026 (auto-retrieval pass complete; Scopus/IEEE/WoS merge + re-run pending)

**Steps**:
1. ✅ Activated `.venv` and ran: `python scripts/quality_filter_slr.py`
2. ✅ Stage 1 filtering complete — IC/EC applied to 1,001 records
3. ✅ Stage 2 quality scoring complete — weighted composite (0–10) across 5 dimensions
4. ✅ Stage 3 OA acquisition complete — 51 PDFs auto-downloaded; 45 require manual retrieval
5. ⚠️ Review `slr_borderline.csv` — 93 papers for human adjudication (primary working corpus)
6. ⚠️ Manually download 45 papers listed in `manual_download_log.txt`; place in `papers/`
7. ⚠️ After Scopus/IEEE/WoS export + metadata merge → re-run pipeline for final corpus

**Pipeline summary (auto-run — OpenAlex-only input)**:

| Stage | Metric | Count |
|---|---|---|
| Input records | Total loaded from `papers_raw.csv` | 1,001 |
| Stage 1 Passed | IC/EC filter | 113 |
| Stage 1 Excluded | IC/EC filter | 888 |
| Stage 2 Included | Quality score ≥ 6.0 | **3** |
| Stage 2 Borderline | Quality score 4.0–5.9 | **93** |
| Stage 2 Excluded | Quality score < 4.0 | 17 |
| Stage 3 Auto-downloaded | OA PDF acquired | **51** |
| Stage 3 Manual required | No OA version found | **45** |
| Total excluded (all stages) | Stage 1 + Stage 2 | 905 |

**Included corpus (3 papers, score ≥ 6.0)**:

| # | Title (truncated) | Journal | Score | PDF |
|---|---|---|---|---|
| 1 | Online Payment Fraud Detection Model Using Machine Learning Techniques | IEEE Access | 6.25 | ✅ Downloaded |
| 2 | Anomaly Detection of IoT Cyberattacks in Smart Cities Using Federated Learning and Split Learning | Big Data and Cognitive Computing | 6.05 | ⚠️ Manual |
| 3 | Edge-FLGuard: A Federated Learning Framework for Real-Time Anomaly Detection in 5G-Enabled IoT Ecosystems | Applied Sciences | 6.65 | ⚠️ Manual |

**Critical architectural note — why only 3 included papers**:
All 1,001 records in `papers_raw.csv` originate from OpenAlex; `sjr_quartile` and `core_rank` fields are empty for these records. The `score_journal_quality()` function assigns a default of 2.0/5.0 for unranked journals, depressing all composite scores. This is **expected, not a bug**. After Scopus/IEEE/WoS records are appended with proper `sjr_quartile`/`core_rank` values, a significant portion of the 93 borderline papers will migrate into the included tier (≥ 6.0).

**⚠️ WARNING — Corpus size 3 < 40 target minimum**:
The pipeline flagged this condition. Resolution path:
1. Export Scopus/IEEE/WoS CSVs using strings from `docs/draft/search_strings.md`
2. Fill `sjr_quartile` (Q1/Q2/Q3/Q4) and `core_rank` (A*/A/B/C) from SCImago + CORE
3. Append rows to `papers_raw.csv` using `papers_manual_template.csv` format
4. Re-run `quality_filter_slr.py` → expected included corpus: 40–80 papers
5. Alternatively: lower threshold to 5.5 (sensitivity lower bound) to expand corpus

**Produced outputs** (`scripts/output/`):
- `slr_included_corpus.csv` — 3 papers (score ≥ 6.0) with full score breakdown
- `slr_borderline.csv` — 93 papers (score 4.0–5.9; primary adjudication pool)
- `slr_excluded_log.csv` — 905 papers with exclusion reason codes
- `manual_download_log.txt` — 45 papers requiring manual PDF retrieval
- `papers/` — 51 validated OA PDFs (≥ 8 KB, %PDF magic bytes verified)

---

## Phase E — IRR & Coding

**Goal**: Dual-coder screening + quality calibration to ensure replicability.

**Status**: ⏳ NOT STARTED (depends on Phase D)

**Stage 1 — Title + Abstract Screening IRR**:
- Both Coder 1 + Coder 2 independently screen 100% of Stage 1 candidates
- Target: Cohen's κ ≥ 0.75
- Disagreements → consensus discussion; persistent → third adjudicator

**Stage 2 — Quality Score Calibration**:
- Both coders independently score 20% pilot sample
- Compute per-dimension κ; revise coding guide for any dimension κ < 0.70
- Coder 2 reviews all borderline papers (4.0–5.9 range)

**Output**: `scripts/output/irr_pilot_results.csv`, `docs/draft/coding_guide_v1.md`, `scripts/output/coded_corpus.csv`

---

## Phase F — Analysis

**Goal**: Quantitative (bibliometric) + qualitative (synthesis) analysis of included corpus.

**Status**: ⏳ NOT STARTED (depends on Phase E)

**Sub-tasks**:
- [ ] Sensitivity analysis: rerun scoring at threshold 5.5 and 6.5; document stability → `docs/draft/sensitivity_analysis.md`
- [ ] Bibliometric analysis: VOSviewer or Bibliometrix (R) on included corpus → co-citation map, keyword clusters → `docs/draft/bibliometric_report.md`
- [ ] Framework synthesis (DSR-aligned): map each paper to DSR three-cycle model → `scripts/output/framework_synthesis_matrix.csv`
- [ ] Thematic synthesis: line-by-line coding → descriptive → analytical themes
- [ ] Narrative synthesis: logic model of detection-as-IS-intervention

---

## Phase G — Writing & Submission

**Goal**: Draft full SLR paper; adapt to target venue format; submit.

**Status**: ⏳ NOT STARTED (depends on Phase F)

**Sub-tasks**:
- [ ] Abstract (≤200 words PACIS / ≤150 AMCIS)
- [ ] Section 1 — Introduction + problem statement
- [ ] Section 2 — Methodology (PRISMA 2020 flow diagram with actual N values)
- [ ] Section 3 — Literature analysis (themes + evidence table)
- [ ] Section 4 — Discussion (gap matrix answering RQ1–RQ3)
- [ ] Section 5 — Conclusion + future research agenda
- [ ] Finalize venue (PACIS vs AMCIS) and adapt format
- [ ] Limitations section (language bias, database coverage, publication bias, single-context validity)
- [ ] Conflict of interest statement

**Submission-readiness checklist**: See `concept/conceptual/research_concept_slr.md` Section 10.3

---

## Dependency Chain

```
A (script ready)
    ↓
B (scoping run + search strings)
    ↓
C (full retrieval → papers_raw.csv)
    ↓
D (pipeline run → corpus + PDFs)
    ↓
E (IRR + coding → coded_corpus.csv)
    ↓
F (analysis → synthesis outputs)
    ↓
G (writing → submission)
```

B can begin concurrently with A.
All other phases are strictly sequential.

---

## Notes & Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-28 | IC-06 expanded to include Bahasa Indonesia papers with English abstract + findings | Capture KPK/BPKP institutional literature |
| 2026-04-28 | Conference scoring: CORE A*=10, A=7, B=5, C/Unranked=2 (separate from SJR quartile) | Prevent under-scoring of CORE A* IS conferences |
| 2026-04-28 | Pre-2010 anchor criteria: ≥300 citations + post-2020 active citation + fundamental claim | Balances seminal work inclusion against recency bias |
| 2026-04-28 | Sensitivity analysis at 5.5 and 6.5 (not 5.0/7.0) | Conservative range; minimizes corpus volatility |
| 2026-04-28 | Cressey (1953) cited via Dorminey et al. (2012) DOI 10.2308/iace-50131 | No primary DOI for 1953 monograph |
| 2026-04-28 | DiMaggio & Powell (1983) DOI 10.2307/2095101 confirmed (JSTOR) | Primary source accessible |
| 2026-04-28 | PACIS provisionally preferred over AMCIS | Stronger regional fit; IS theory depth expected |
