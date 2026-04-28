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
| **D** | Filter & Acquire — Run pipeline → corpus + PDFs | ✅ COMPLETED — 2026-04-29 | `papers/`, `scripts/output/` |
| **D+** | Cross-check — `crosscheck_papers.py` → PDF vs pipeline audit | ✅ COMPLETED — 2026-04-28 | `scripts/output/crosscheck_report.md`, `scripts/output/crosscheck_detail.csv` |
| **E** | IRR & Coding — Co-author screening + domain-override adjudication | ⏳ NOT STARTED | `scripts/output/irr_pilot_results.csv`, `scripts/output/coded_corpus.csv` |
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

**Status**: ✅ COMPLETED — April 30, 2026 (pipeline v2 with journal metadata enrichment complete; Scopus/IEEE/WoS merge pending)

**Steps**:
1. ✅ Pipeline v1 (April 29) — 1,001 OpenAlex records; 3 included (all `sjr_quartile` empty → quality scores depressed)
2. ✅ Root cause diagnosed: OpenAlex does not populate `sjr_quartile`/`core_rank`; `score_journal_quality()` defaults to 2.0 for unranked → depresses composite by 2.0 per paper
3. ✅ `enrich_journal_metadata.py` built — 3-tier ISSN/name lookup; hardcoded SCImago-verified Q1/Q2/Q3 mapping for 100+ journals; blank-journal guard and 15-char minimum substring protection
4. ✅ Enrichment executed (April 30) — 194/1001 rows updated (95 Q1, 91 Q2, 8 Q3); backup saved as `papers_raw.csv.bak`
5. ✅ Pipeline v2 re-run — enriched `papers_raw.csv`; existing PDFs skipped (skip logic lines 662–664); 7-min 47-sec runtime
6. ⚠️ Corpus 23 < 40 target; borderline pool holds 73 additional candidates
7. ⚠️ Manually download 45 papers listed in `manual_download_log.txt`; place in `papers/`
8. ⚠️ After Scopus/IEEE/WoS export + metadata merge → re-run pipeline for final corpus

**Pipeline summary (v2 — enriched `papers_raw.csv`, OpenAlex-only input)**:

| Stage | Metric | v1 Count | v2 Count |
|---|---|---|---|
| Input records | Total loaded from `papers_raw.csv` | 1,001 | 1,001 |
| `sjr_quartile` enriched | Rows resolved by `enrich_journal_metadata.py` | 0 | **194** |
| Stage 1 Passed | IC/EC filter | 113 | 113 |
| Stage 1 Excluded | IC/EC filter | 888 | 888 |
| Stage 2 Included | Quality score ≥ 6.0 | 3 | **23** |
| Stage 2 Borderline | Quality score 4.0–5.9 | 93 | **73** |
| Stage 2 Excluded | Quality score < 4.0 | 17 | 17 |
| Stage 3 Auto-downloaded | OA PDF acquired | 51 | 51 (all existing, 0 new) |
| Stage 3 Manual required | No OA version found | 45 | 45 |
| Total excluded (all stages) | Stage 1 + Stage 2 | 905 | 905 |

**Included corpus v2 (23 papers, score ≥ 6.0) — representative selection**:

| # | Title (truncated) | Journal | Score | Quartile | PDF |
|---|---|---|---|---|---|
| 1 | Online Payment Fraud Detection Model Using ML Techniques | IEEE Access | 8.25 | Q1 | ✅ Downloaded |
| 2 | Edge-FLGuard: A Federated Learning Framework for Anomaly Detection | Applied Sciences | 7.90 | Q2 | ⚠️ Manual |
| 3 | Research trends in DL/ML for network intrusion detection | Artificial Intelligence Review | 7.65 | Q1 | ✅ Downloaded |
| 4 | Anomaly Detection of IoT Cyberattacks (Federated + Split Learning) | Big Data and Cognitive Computing | 7.30 | Q2 | ⚠️ Manual |
| 5 | A Review of Large Language Models for Energy Systems | IEEE Access | 7.20 | Q1 | ⚠️ Manual |
| 6 | Blockchain and AI-Empowered Healthcare Insurance Fraud Detection | IEEE Access | 7.05 | Q1 | ⚠️ Manual |
| 7 | Securing the digital world: smart infrastructures protection | J. Industrial Information Integration | 7.05 | Q1 | ⚠️ Manual |
| 8 | Generative AI revolution in cybersecurity | Artificial Intelligence Review | 7.05 | Q1 | ✅ Downloaded |
| 9 | … 15 additional papers (score 6.0–6.90) | IEEE Access / Electronics / Applied Sciences | 6.0–6.9 | Q1/Q2 | mix |

**Journal breakdown (included corpus)**:

| Journal | Count | Quartile |
|---|---|---|
| IEEE Access | 7 | Q1 |
| Electronics | 4 | Q2 |
| Applied Sciences | 3 | Q2 |
| Artificial Intelligence Review | 2 | Q1 |
| Journal of Industrial Information Integration | 1 | Q1 |
| American Political Science Review | 1 | Q1 |
| Finance & Accounting Research Journal | 1 | Q3 |
| Big Data and Cognitive Computing | 1 | Q2 |
| Mathematics | 1 | Q2 |
| International Journal of Information Technology | 1 | Q1 |
| Information Systems | 1 | Q1 |

**Borderline score distribution (73 papers)**:

| Score band | Count | Action |
|---|---|---|
| (5.5, 6.0] | 8 | Candidates for threshold sensitivity run at 5.5 |
| (5.0, 5.5] | 14 | Human adjudication — high-quality abstract screening |
| (4.5, 5.0] | 19 | Human adjudication — discard unless IS-specific |
| (4.0, 4.5] | 28 | Likely exclude; review titles only |

**⚠️ WARNING — Corpus size 23 < 40 target minimum**:
Pipeline exited with code 1 (non-fatal). Three resolution paths available:

**Path 1 (Recommended)**: Scopus / IEEE Xplore / WoS manual export + merge
- Export CSVs using strings from `docs/draft/search_strings.md`
- Expected additional unique papers: 100–300 with proper `sjr_quartile` from Scopus export metadata
- Re-run `quality_filter_slr.py` → expected final included corpus: 40–70 papers

**Path 2**: Threshold sensitivity at 5.5
- Lowers `SCORE_INCLUDE` from 6.0 → 5.5 in `quality_filter_slr.py`
- Adds 8 borderline papers from (5.5, 6.0] band → total 31 included
- Acceptable for conference papers where corpus depth > breadth trade-off is documented

**Path 3**: Extend `enrich_journal_metadata.py` with `--doi-lookup` flag
- Activates OpenAlex Source API per-DOI lookup for the 73 borderline NaN papers
- May resolve 10–20 additional quartile values → push some borderline papers to ≥ 6.0
- Runtime ~3–5 min additional; requires `--doi-lookup` flag

**Produced outputs** (`scripts/output/`):
- `slr_included_corpus.csv` — 23 papers (score ≥ 6.0) with full score breakdown per dimension
- `slr_borderline.csv` — 73 papers (score 4.0–5.9; primary adjudication pool)
- `slr_excluded_log.csv` — 905 papers with exclusion reason codes
- `manual_download_log.txt` — 45 papers requiring manual PDF retrieval
- `papers/` — 51 validated OA PDFs (≥ 8 KB, %PDF magic bytes verified)
- `papers_raw.csv.bak` — backup of unenriched `papers_raw.csv` (pre-enrichment rollback point)

---

## Phase E — IRR & Coding

**Goal**: Dual-coder screening + quality calibration + domain-relevance override protocol.

**Status**: ⏳ NOT STARTED (depends on Phase D)

**Stage 0 — Domain-Relevance Override (NEW — pre-IRR)**:
- Cross-check of 52 PDFs in `papers/` against pipeline outputs completed: `scripts/output/crosscheck_report.md`
- **27 BORDERLINE papers identified as PRIORITY REVIEW** — scored low due to journal tier, not low relevance
- 12 are HIGH-relevance village fund / Dana Desa / Indonesian corruption papers (RQ2/RQ3 direct evidence)
- Action: Coder 1 reads abstract of each priority paper; if domain criteria met → override quality_score to 6.0
- Document in `coded_corpus.csv` column `adjudication_note` with reason code `DOMAIN_OVERRIDE_RQ2` or `DOMAIN_OVERRIDE_RQ3`
- **Rationale**: Pipeline scoring systematically undervalues developing-country IS journals (unranked → score_journal_quality defaults to 2.0/10). Dana Desa governance papers represent the primary evidence base for RQ2 and cannot be excluded on journal-tier grounds alone. Precedent: Petticrew & Roberts (2006) advocate purposive sampling alongside systematic search when domain-specific evidence bases are thin.

**Stage 1 — Title + Abstract Screening IRR**:
- Both Coder 1 + Coder 2 independently screen 100% of Stage 1 candidates
- Target: Cohen's κ ≥ 0.75
- Disagreements → consensus discussion; persistent → third adjudicator

**Stage 2 — Quality Score Calibration**:
- Both coders independently score 20% pilot sample
- Compute per-dimension κ; revise coding guide for any dimension κ < 0.70
- Coder 2 reviews all borderline papers (4.0–5.4 range)
- Priority review papers (domain override candidates) assessed separately

**Cross-check findings summary** (`crosscheck_papers.py` — April 28, 2026):
| Finding | Value |
|---|---|
| Total PDFs in `papers/` | 52 |
| INCLUDED (pipeline score ≥ 5.5) | 11 |
| BORDERLINE (4.0–5.4) | 41 |
| MANUAL_ONLY (not in pipeline) | 0 |
| PRIORITY REVIEW (borderline + HIGH/MEDIUM relevance) | 27 |
| RQ1 coverage (INCLUDED + priority borderline) | 21 |
| RQ2 coverage (INCLUDED + priority borderline) | 18 |
| RQ3 coverage (INCLUDED + priority borderline) | 14 |

**Critical bias finding**: Pipeline quality score systematically undervalues Dana Desa / village fund papers:
- `score_journal_quality` = 2.0 for unranked Indonesian journals → composite depressed by ~2 pts
- Result: All village-fund governance papers cluster at score 4.15 (hardfloor from unranked journal + low citations)
- Net: If domain override applied to all 12 HIGH village-fund papers → effective corpus = 23 + 12 = 35 papers
- Still below 40 target → Scopus/IEEE/WoS export remains required

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
| 2026-04-28 | `crosscheck_papers.py` built → cross-checks 52 PDFs in `papers/` against pipeline | Identifies 27 priority-review borderline papers; RQ2/RQ3 coverage confirmed viable |
| 2026-04-28 | Domain-relevance override protocol added to Phase E | Pipeline scoring bias against developing-country IS journals confirmed; village-fund governance papers (4.15 score) excluded by composite metric despite HIGH RQ2/RQ3 relevance |
| 2026-04-28 | Effective estimated corpus after domain override: ~35 papers | 23 pipeline-included + 12 HIGH village-fund overrides; below 40 target → Scopus/IEEE/WoS export still required |
