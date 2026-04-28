# Finalized Search Strings — SLR Phase C

> **Finalized**: 2026-04-28  
> **Based on**: Phase B scoping run results (`scoping_run_results.md`)

---

## Overview

Two complementary search string sets are used:

- **Primary set (S-PRI)**: Covers ML methods + public sector fraud/anomaly detection — feeds RQ1 and RQ2
- **Supplementary set (S-SUP)**: Village-level governance + decentralized fund irregularities — feeds RQ3

Both sets are run on all five databases. Hits are merged and de-duplicated before entering `papers_raw.csv`.

---

## 1. Scopus — Advanced Search

**S-PRI (Primary)**
```
TITLE-ABS-KEY(
  ( "anomaly detection" OR "fraud detection" OR "corruption detection"
    OR "financial irregularity" OR "misappropriation detection" )
  AND
  ( "machine learning" OR "deep learning" OR "unsupervised learning"
    OR "isolation forest" OR "random forest" OR "neural network"
    OR "autoencoder" OR "clustering" OR "classification algorithm" )
  AND
  ( "public sector" OR "government expenditure" OR "public finance"
    OR "government procurement" OR "public spending" OR "state budget" )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
AND DOCTYPE(ar OR re)
```

**S-SUP (Supplementary — Village/Decentralized)**
```
TITLE-ABS-KEY(
  ( "village fund" OR "dana desa" OR "decentralized fund"
    OR "village finance" OR "local government fund"
    OR "sub-national government" OR "fiscal decentralization" )
  AND
  ( "corruption" OR "fraud" OR "irregularity" OR "anomaly"
    OR "audit finding" OR "financial mismanagement" )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
AND DOCTYPE(ar OR re)
```

---

## 2. IEEE Xplore — Advanced Search

**S-PRI**
```
("Abstract":"anomaly detection" OR "Abstract":"fraud detection")
AND ("Abstract":"machine learning" OR "Abstract":"deep learning"
     OR "Abstract":"unsupervised" OR "Abstract":"neural network")
AND ("Abstract":"government" OR "Abstract":"public sector"
     OR "Abstract":"public finance" OR "Abstract":"procurement")
Filter: Year: 2010–2026 | Content Type: Journals + Conference Papers
```

**S-SUP**
```
("Abstract":"village fund" OR "Abstract":"decentralized fund"
 OR "Abstract":"dana desa" OR "Abstract":"local government")
AND ("Abstract":"corruption" OR "Abstract":"fraud" OR "Abstract":"anomaly")
Filter: Year: 2010–2026
```

---

## 3. Web of Science — Advanced Search

**S-PRI**
```
TS=("anomaly detection" OR "fraud detection" OR "corruption detection")
AND TS=("machine learning" OR "deep learning" OR "unsupervised"
        OR "random forest" OR "neural network" OR "autoencoder")
AND TS=("public sector" OR "government" OR "public finance"
        OR "public expenditure" OR "government procurement")
AND PY=(2010-2026)
AND DT=(Article OR Review)
```

**S-SUP**
```
TS=("village fund" OR "dana desa" OR "decentralized fund"
    OR "local government fund" OR "fiscal decentralization")
AND TS=("corruption" OR "fraud" OR "financial irregularity")
AND PY=(2010-2026)
```

---

## 4. OpenAlex — API Query (used in scoping run)

```
GET https://api.openalex.org/works
  ?search=anomaly+detection+fraud+detection+public+sector+government+machine+learning
  &filter=publication_year:2010-2026,type:article
  &per-page=200
  &mailto=researcher@binus.ac.id
```

Repeat with supplementary query:
```
  ?search=village+fund+dana+desa+corruption+fraud+detection
  &filter=publication_year:2010-2026
```

> For full retrieval, iterate pages until `meta.count` exhausted or `per-page=200` × pages = total.

---

## 5. Semantic Scholar — API Query

```
GET https://api.semanticscholar.org/graph/v1/paper/search
  ?query=anomaly+detection+fraud+detection+public+sector+machine+learning
  &fields=paperId,title,year,citationCount,openAccessPdf,journal,abstract
  &limit=100
```

Supplementary:
```
  ?query=village+fund+corruption+detection+government+financial+anomaly
```

---

## 6. papers_raw.csv Column Mapping

When exporting from each database, normalize to these columns before merging:

| Column | Scopus Export | IEEE Export | WoS Export | OpenAlex API | Semantic Scholar API |
|---|---|---|---|---|---|
| `doi` | DOI | DOI | DI | `doi` | `externalIds.DOI` |
| `title` | Title | Document Title | TI | `title` | `title` |
| `year` | Year | Publication Year | PY | `publication_year` | `year` |
| `journal` | Source title | Publication Title | SO | `primary_location.source.display_name` | `journal.name` |
| `sjr_quartile` | — (look up Scimago) | — | — | — | — |
| `core_rank` | — (look up CORE) | — | — | — | — |
| `citations` | Cited by | — | TC | `cited_by_count` | `citationCount` |
| `source_db` | `scopus` | `ieee` | `wos` | `openalex` | `semantic_scholar` |
| `oa_url` | — | PDF Links | — | `open_access.oa_url` | `openAccessPdf.url` |
| `abstract` | Abstract | Abstract | AB | *(not in select — run separate query if needed)* | `abstract` |
| `is_duplicate` | — (set True after DOI dedup) | — | — | — | — |
| `language` | Language of Original Document | — | LA | — | — |

**De-duplication rule**: After merging all exports, set `is_duplicate=True` for any row whose `doi` appears more than once; keep only the row from the highest-priority source (Scopus > WoS > IEEE > OpenAlex > S2).

---

## 7. Expected Retrieval Volumes (Pre-filter)

| Database | S-PRI (est.) | S-SUP (est.) | Notes |
|---|---|---|---|
| Scopus | 80–150 | 5–20 | Most comprehensive IS journal coverage |
| IEEE Xplore | 30–70 | 2–10 | Strong for ML methods papers |
| Web of Science | 40–80 | 3–15 | High-impact journals; overlaps Scopus heavily |
| OpenAlex | 100–300 | 10–40 | Largest raw pool; many non-IS papers |
| Semantic Scholar | 50–120 | 5–20 | Good PDF coverage; semantic matching |
| **Total (pre-dedup)** | **300–720** | **25–105** | — |
| **Post-dedup estimate** | **150–300** | **15–50** | ~40% overlap across databases |
| **Post-IC/EC filter (15–25%)** | **22–75** | **2–12** | Combined: 24–87 |

> **Target 40–80**: Achievable if combined post-dedup pool ≥ 150 records.
> If post-filter count < 40, broaden by: removing `public sector` AND constraint (allow implicit gov context), or lowering threshold to 5.5.

