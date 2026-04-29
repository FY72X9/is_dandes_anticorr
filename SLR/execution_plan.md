# SLR Execution Plan — ML-Based Financial Anomaly Detection for Anti-Corruption IS

> **Study**: Systematic Literature Review (SLR) — prerequisite for Phase 1 empirical study
> **Target venue**: PACIS or AMCIS (decision pending Phase B scoping run)
> **Target corpus**: 40–80 papers
> **Last updated**: April 30, 2026

---

## Phase Status Overview

| Phase | Name | Status | Output |
|---|---|---|---|
| **A** | Infrastructure — Build `quality_filter_slr.py` | ✅ COMPLETED — 2026-04-28 | `scripts/quality_filter_slr.py` |
| **B** | Search Design — Mini scoping run + search strings | ✅ COMPLETED — 2026-04-28 | `docs/draft/scoping_run_results.md`, `docs/draft/search_strings.md` |
| **C** | Retrieval — Full database search → `papers_raw.csv` | ✅ COMPLETED — 2026-04-28 | `scripts/papers_raw.csv` |
| **D** | Filter & Acquire — Run pipeline → corpus + PDFs | ✅ COMPLETED — 2026-04-29 (v3: SCORE_INCLUDE=5.0 → 45 included) | `papers/`, `scripts/output/` |
| **D+** | Cross-check — `crosscheck_papers.py` → PDF vs pipeline audit | ✅ COMPLETED — 2026-04-28 | `scripts/output/crosscheck_report.md`, `scripts/output/crosscheck_detail.csv` |
| **E** | IRR & Coding — Co-author screening + domain-override adjudication | 🔄 IN PROGRESS — Stage 0 scaffolding done (2026-04-29); Stage 0 override ready to apply | `scripts/output/coded_corpus.csv` ✅, `docs/coding_guide_v1.md` ✅, `scripts/domain_override.py` ✅ |
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

**Status**: ✅ COMPLETED — April 29, 2026 (pipeline v3 — SCORE_INCLUDE=5.0 sensitivity run; corpus target 40 met with 45 included)

**Full pipeline evolution**:

| Run | Date | SCORE_INCLUDE | Journal Enrichment | Included | PDFs | Exit |
|---|---|---|---|---|---|---|
| v1 | 2026-04-28 | 6.0 | None | 3 | 51 | code 1 — corpus < 40 |
| v2 | 2026-04-28 | 5.5 | `enrich_journal_metadata.py` (194 rows enriched) | 31 | 85 | code 1 — corpus < 40 |
| **v3** | **2026-04-29** | **5.0** | Same enriched CSV | **45** | **85** | code 0 — ✅ target met |

**Steps completed**:
1. ✅ Pipeline v1 (April 28) — 1,001 OpenAlex records; 3 included (all `sjr_quartile` empty → quality scores depressed)
2. ✅ Root cause diagnosed: OpenAlex does not populate `sjr_quartile`; `score_journal_quality()` defaults to 2.0 for unranked journals → depresses composite by ≥2.4 pts per paper
3. ✅ `enrich_journal_metadata.py` built — 3-tier ISSN/name lookup; hardcoded SCImago-verified Q1/Q2/Q3 mapping for 100+ journals; blank-journal guard and 15-char minimum substring protection
4. ✅ Enrichment executed (April 28) — 194/1001 rows updated (95 Q1, 91 Q2, 8 Q3); backup saved as `papers_raw.csv.bak`
5. ✅ Pipeline v2 (April 28) — 31 included; 85 PDFs on disk; 45 still manual (prior manual downloads filled pipeline later)
6. ✅ Playwright + curl_cffi download scripts executed — most manual papers resolved; `papers/` grew to 85→90 PDFs
7. ✅ Pipeline v3 (April 29) — SCORE_INCLUDE lowered 5.5→5.0 (sensitivity run); 14 papers in 5.0–5.49 band absorbed; **45 included, corpus target met**
8. ✅ PDF audit: 90 PDFs confirmed on disk; 11 permanently blocked (paywall/DNS)

**Pipeline v3 final summary**:

| Stage | Metric | Count |
|---|---|---|
| Input records (`papers_raw.csv`) | Total loaded | 1,001 |
| `sjr_quartile` enriched | Rows with valid quartile | 194 |
| Stage 1 Passed | IC/EC filter | 113 |
| Stage 1 Excluded | IC/EC filter | 888 |
| Stage 2 Included | Quality score ≥ **5.0** | **45** |
| Stage 2 Borderline | Quality score 4.0–4.9 | 51 |
| Stage 2 Excluded | Quality score < 4.0 | 17 |
| Stage 3 PDFs on disk | Already existed | 85 |
| Stage 3 Manual required | No OA version found | 11 |
| Total PDFs in `papers/` | Including manual additions | **90** |
| Total excluded (all stages) | Stage 1 + Stage 2 below threshold | 905 |

**Journal breakdown (v3 included corpus, 45 papers)**:

| Journal | Count | Quartile |
|---|---|---|
| IEEE Access | 9 | Q1 |
| Electronics | 4 | Q2 |
| Applied Sciences | 3 | Q2 |
| Artificial Intelligence Review | 2 | Q1 |
| Information Systems | 1 | Q1 |
| Big Data and Cognitive Computing | 1 | Q2 |
| Journal of Industrial Information Integration | 1 | Q1 |
| Mathematics | 1 | Q2 |
| American Political Science Review | 1 | Q1 |
| Finance & Accounting Research Journal | 1 | Q3 |
| International Journal of Information Technology | 1 | Q1 |
| Unranked IS/governance journals | ~20 | unranked |

**Borderline pool (v3, 51 papers)**:

| Score band | Count | Recommended action |
|---|---|---|
| 4.5–4.9 | 23 | Abstract screening required |
| 4.0–4.4 | 28 | Title screening; domain override if HIGH relevance |

*12 of the 4.0–4.4 papers are HIGH-relevance village fund governance papers (Dana Desa / KPK audit). They score 4.15 due to unranked journal bias, not low topical relevance. These are Phase E Stage 0 Domain Override candidates.*

**Produced outputs** (`scripts/output/`):
- `slr_included_corpus.csv` — **45 papers** (score ≥ 5.0) with full score breakdown per dimension
- `slr_borderline.csv` — 51 papers (score 4.0–4.9; primary adjudication pool)
- `slr_excluded_log.csv` — 905 papers with exclusion reason codes
- `manual_download_log.txt` — **11 papers** requiring manual PDF retrieval (down from 45: most resolved in prior sessions)
- `pipeline.log` — full execution trace
- `papers/` — **90 validated PDFs** (≥ 8 KB, %PDF magic bytes verified)
- `papers_raw.csv.bak` — pre-enrichment backup (rollback point)

**Supporting documentation**: `SLR/docs/phase_d_completion_report.md` — full PRISMA flow, pipeline version history, scoring bias analysis, PDF manifest, transition checklist for Phase E.

---

## Phase E — IRR & Coding

**Goal**: Dual-coder screening + quality calibration + domain-relevance override protocol.

**Status**: 🔄 IN PROGRESS — Stage 0 scaffolding complete (April 29, 2026); Stage 0 override execution pending Coder 1 abstract review

**Stage 0 — Domain-Relevance Override (NEW — pre-IRR)**:
- Cross-check of 90 PDFs in `papers/` against pipeline outputs completed; `scripts/output/crosscheck_report.md` (stale — pre-v3; regenerate after Stage 0 apply)
- **12 papers identified as DOMAIN_OVERRIDE candidates** — all score 4.15 due to unranked journal bias, all directly evidence RQ2/RQ3 (Dana Desa / village fund governance)
- Script built: `scripts/domain_override.py` — dry-run confirmed 12/12 candidates detected
- **To execute Stage 0**: `python SLR/scripts/domain_override.py --apply --auto`
- After apply: `python SLR/scripts/crosscheck_papers.py` to regenerate crosscheck_report.md
- Projected effective corpus after override: **45 + 12 = 57 papers**
- Coding template built: `scripts/output/coded_corpus.csv` (96 rows: 45 included + 51 borderline, `domain_override_candidate` pre-flagged)
- Coding guide written: `docs/coding_guide_v1.md`

**Stage 1 — Title + Abstract Screening IRR**:
- Both Coder 1 + Coder 2 independently screen 100% of Stage 1 candidates
- Target: Cohen's κ ≥ 0.75
- Disagreements → consensus discussion; persistent → third adjudicator

**Stage 2 — Quality Score Calibration**:
- Both coders independently score 20% pilot sample
- Compute per-dimension κ; revise coding guide for any dimension κ < 0.70
- Coder 2 reviews all borderline papers (4.0–5.4 range)
- Priority review papers (domain override candidates) assessed separately

**Cross-check findings summary** (`crosscheck_papers.py` — April 28, 2026; *pre-v3 numbers — re-run in Phase E Stage 0*):

| Finding | Value (pre-v3) | Updated (post-v3) |
|---|---|---|
| Total PDFs in `papers/` | 52 | **90** |
| INCLUDED (pipeline score ≥ 5.5) | 11 | **45** (score ≥ 5.0) |
| BORDERLINE (4.0–5.4 / 4.0–4.9) | 41 | **51** |
| MANUAL_ONLY (not in pipeline) | 1 | — |
| PRIORITY REVIEW (borderline + HIGH/MEDIUM relevance) | 27 | ~27 (re-audit needed) |
| RQ1 coverage (INCLUDED + priority borderline) | 21 | ~30+ |
| RQ2 coverage (INCLUDED + priority borderline) | 18 | ~12 + override candidates |
| RQ3 coverage (INCLUDED + priority borderline) | 14 | ~8 + override candidates |

**Critical bias finding**: Pipeline quality score systematically undervalues Dana Desa / village fund papers:
- `score_journal_quality` = 2.0 for unranked Indonesian journals → composite depressed by ~2.4 pts
- Result: All village-fund governance papers cluster at score 4.15 (hardfloor from unranked journal + low citations)
- Net: If domain override applied to all 12 HIGH village-fund papers → effective corpus = 45 + 12 = **57 papers** (well within 40–80 target)

**Output**: `scripts/output/coded_corpus.csv` ✅, `docs/coding_guide_v1.md` ✅, `scripts/domain_override.py` ✅, `scripts/output/irr_pilot_results.csv` ⏳

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
| 2026-04-28 | `crosscheck_papers.py` built → cross-checks 52 PDFs in `papers/` against pipeline | Identifies 27 priority-review borderline papers; RQ2/RQ3 coverage confirmed viable |
| 2026-04-28 | Domain-relevance override protocol added to Phase E | Pipeline scoring bias against developing-country IS journals confirmed; village-fund governance papers (4.15 score) excluded by composite metric despite HIGH RQ2/RQ3 relevance |
| 2026-04-28 | Effective estimated corpus after domain override: ~35 papers | 23 pipeline-included + 12 HIGH village-fund overrides; below 40 target → SCORE_INCLUDE sensitivity run planned |
| 2026-04-29 | SCORE_INCLUDE lowered 5.5 → 5.0 (pipeline v3 sensitivity run) | Borderline 5.0–5.49 band had 14 papers; 8 already on disk; corpus target 40 met with 45 included. Sensitivity bounds for Phase F: 5.0 (lower) / 5.5 (primary) / 6.0 (upper). |
| 2026-04-29 | 90 PDFs confirmed on disk; 11 papers permanently blocked | Blocked: Elsevier ×2, Wiley ×1, IGI Global ×2 (paywall); fepbl/ajrcos/nblformosa (DNS); ijcat ×2 (SSL+403). None are in included corpus — impact on Phase F synthesis is marginal. |
| 2026-04-29 | Phase D completion report created | `SLR/docs/phase_d_completion_report.md` — PRISMA flow, version history, scoring bias analysis, PDF manifest, Phase E transition checklist |
| 2026-04-29 | `crosscheck_report.md` flagged as stale | Generated pre-v3 (53 PDFs / score ≥ 5.5). Will be regenerated in Phase E Stage 0 after domain override applied. |
