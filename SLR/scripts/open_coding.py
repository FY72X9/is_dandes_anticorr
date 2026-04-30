"""
Phase F2.1 — Line-by-Line Open Coding (Thomas & Harden 2008 Stage 1)
Reads extracted .md files for all 45 INCLUDE papers.
Applies pattern-based + context-window coding to assign taxonomy codes.
Produces:
  - SLR/analysis/coding/[paper_id]_codes.md  (per-paper workbook with codes + evidence quotes)
  - SLR/analysis/themes/open_codes_master.csv (aggregated master table)

Code taxonomy categories:
  MC  — Method claim
  FE  — Feature engineering
  DS  — Data source
  AC  — Applicability condition
  LIM — Limitation stated
  GAP — Gap stated
  IST — IS theory used
  CTX — Context/domain
"""

import os
import re
import csv
import pandas as pd
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTED_DIR = os.path.join(BASE_DIR, "analysis", "extracted")
CODING_DIR    = os.path.join(BASE_DIR, "analysis", "coding")
THEMES_DIR    = os.path.join(BASE_DIR, "analysis", "themes")
CORPUS_CSV    = os.path.join(BASE_DIR, "scripts", "output", "coded_corpus.csv")
MASTER_CSV    = os.path.join(THEMES_DIR, "open_codes_master.csv")

os.makedirs(CODING_DIR, exist_ok=True)
os.makedirs(THEMES_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# CODE PATTERNS — (code_label, category, description, patterns)
# Each pattern is a regex; if matched, code is assigned.
# We extract up to 3 evidence quotes (sentence containing match).
# ─────────────────────────────────────────────────────────────────────────────

CODE_PATTERNS = [
    # ── Method Claims ────────────────────────────────────────────────────────
    ("MC-RF",    "MC", "Random Forest used/evaluated",
        [r"\brandom\s*forest\b", r"\bRF\b(?!\s*frequency)"]),
    ("MC-GBM",   "MC", "Gradient Boosting / XGBoost / LightGBM",
        [r"\bgradient\s*boost", r"\bXGBoost\b", r"\bLightGBM\b", r"\bCatBoost\b", r"\bAdaBoost\b"]),
    ("MC-IF",    "MC", "Isolation Forest used/evaluated",
        [r"\bisolation\s*forest\b"]),
    ("MC-LOF",   "MC", "Local Outlier Factor (LOF) used/evaluated",
        [r"\blocal\s*outlier\s*factor\b", r"\bLOF\b"]),
    ("MC-SVM",   "MC", "SVM / kernel methods",
        [r"\bsupport\s*vector\s*machine\b", r"\bSVM\b", r"\bSVR\b"]),
    ("MC-LSTM",  "MC", "LSTM / GRU / RNN used/evaluated",
        [r"\bLSTM\b", r"\bGRU\b", r"\brecurrent\s*neural\b", r"\bRNN\b"]),
    ("MC-CNN",   "MC", "CNN / convolutional methods",
        [r"\bconvolutional\s*neural\b", r"\bCNN\b"]),
    ("MC-AE",    "MC", "Autoencoder / VAE for anomaly detection",
        [r"\bautoencoder\b", r"\bvariational\s*autoencoder\b", r"\bVAE\b"]),
    ("MC-GNN",   "MC", "Graph Neural Network / GCN / GAT",
        [r"\bgraph\s*(neural|convolutional|attention)\b", r"\bGNN\b", r"\bGCN\b", r"\bGAT\b"]),
    ("MC-BERT",  "MC", "Transformer / BERT / LLM applied",
        [r"\bBERT\b", r"\bGPT\b", r"\btransformer\b", r"\blarge\s*language\s*model\b", r"\bLLM\b"]),
    ("MC-FL",    "MC", "Federated Learning applied",
        [r"\bfederated\s*learn"]),
    ("MC-ENS",   "MC", "Ensemble method as top performer",
        [r"\bensemble\b.*\b(outperform|superior|best|top)\b",
         r"\b(outperform|superior|best)\b.*\bensemble\b"]),
    ("MC-UNSUP", "MC", "Unsupervised anomaly detection claimed",
        [r"\bunsupervised\b.*\b(anomaly|fraud|detection)\b",
         r"\b(anomaly|fraud)\s*detection\b.*\bunsupervised\b"]),
    ("MC-PERF",  "MC", "High performance claim (AUC/F1/accuracy reported)",
        [r"\b(AUC|F1|F-measure|accuracy|precision|recall)\b.*\b(0\.\d{2,}|\d{2,}\s*%)\b",
         r"\b(0\.9[0-9]|99\s*%|98\s*%|97\s*%)\b.*\b(AUC|F1|accuracy)\b"]),
    ("MC-COMP",  "MC", "Comparative evaluation of multiple ML methods",
        [r"\bcompar(e|ed|ison|ative)\b.*\b(algorithm|method|model|approach|baseline)\b",
         r"\bbaseline\b.*\bcompar"]),
    ("MC-SEMI",  "MC", "Semi-supervised learning applied",
        [r"\bsemi.supervised\b"]),
    ("MC-DL",    "MC", "Deep learning as primary method",
        [r"\bdeep\s*learn", r"\bneural\s*network\b"]),

    # ── Feature Engineering ───────────────────────────────────────────────────
    ("FE-RFLAG", "FE", "Red flag / indicator-based feature operationalization",
        [r"\bred\s*flag", r"\bwarning\s*sign", r"\bfraud\s*indicator"]),
    ("FE-BID",   "FE", "Single bidder / collusion signal as feature",
        [r"\bsingle\s*bidder", r"\bsole\s*source", r"\bbid\s*(rigg|manipul|collus)"]),
    ("FE-AMEND", "FE", "Contract amendment / change order as feature",
        [r"\bcontract\s*amendment", r"\bchange\s*order", r"\bprice\s*modif"]),
    ("FE-TRAN",  "FE", "Transaction amount / volume features",
        [r"\btransaction\s*(amount|volume|pattern|featur)",
         r"\b(unusual|abnormal|anomalous)\s*transaction"]),
    ("FE-NETW",  "FE", "Network / graph features (vendor relationships, entities)",
        [r"\bnetwork\s*analy", r"\bgraph\s*featur", r"\bbipartite\b",
         r"\bbeneficial\s*owner", r"\bentity\s*relationship"]),
    ("FE-BUDGET","FE", "Budget absorption / spending pattern feature",
        [r"\bbudget\s*absorpt", r"\bspending\s*pattern", r"\bpagu\b",
         r"\bpenyerapan\b", r"\brealisasi\b"]),
    ("FE-BEHAV", "FE", "Behavioral features (user behavior, employee)",
        [r"\buser\s*behav", r"\bemployee\s*behav", r"\binside[r]?\s*trad"]),
    ("FE-TEXTM", "FE", "Text mining / NLP features from documents",
        [r"\btext\s*min", r"\bNLP\s*featur", r"\bdocument\s*(classification|analysis)",
         r"\b(contract|audit|report)\s*text"]),
    ("FE-TEMPORAL","FE","Temporal / time-series features",
        [r"\btime\s*series\b", r"\btemporal\s*featur", r"\bsequential\s*(pattern|featur)"]),

    # ── Data Sources ──────────────────────────────────────────────────────────
    ("DS-PROC",  "DS", "Procurement / e-procurement database",
        [r"\bprocurement\s*(data|database|system|record)",
         r"\be-procurement\b", r"\bSIKAP\b", r"\bLPSE\b", r"\bSIPP\b"]),
    ("DS-AUDIT", "DS", "Audit reports / BPK / BPKP data",
        [r"\baudit\s*report", r"\bBPK\b", r"\bBPKP\b",
         r"\bsupreme\s*audit", r"\binspectorate"]),
    ("DS-LEDGER","DS", "Financial ledger / accounting records",
        [r"\baccounting\s*record", r"\bfinancial\s*ledger", r"\bgeneral\s*ledger",
         r"\bjournal\s*entr"]),
    ("DS-TRANS", "DS", "Banking / payment transaction data",
        [r"\bbank\s*(transaction|record|data)", r"\bpayment\s*(data|record|transaction)"]),
    ("DS-DANDES","DS", "Dana Desa / village fund data",
        [r"\bdana\s*desa\b", r"\bvillage\s*fund", r"\bAPBDes\b", r"\bsiskeudes\b",
         r"\bfund\s*village", r"\bkelurahan\b.*\bfund\b"]),
    ("DS-GOVERN","DS", "Government / public sector financial data",
        [r"\bgovernment\s*(financial|expenditure|budget|data)",
         r"\bpublic\s*(financial|expenditure|budget|sector)\s*(data|record)",
         r"\bAPBD\b", r"\bAPBN\b"]),
    ("DS-JUDIC", "DS", "Judicial / court / KPK verdict data",
        [r"\bKPK\b", r"\bcourt\s*(decision|verdict|record)",
         r"\bjudicial\s*record", r"\bconviction\s*record", r"\bprosecution\s*data"]),
    ("DS-SYNTH", "DS", "Synthetic / simulated data used",
        [r"\bsynthetic\s*(data|dataset)", r"\bsimulated\s*data",
         r"\bdata\s*generat", r"\bsmote\b"]),
    ("DS-PRIVATE","DS","Private sector / commercial dataset",
        [r"\bcredit\s*card\s*dataset", r"\bbank\s*fraud\s*dataset",
         r"\bIEEE.CIS\b", r"\bKaggle\b.*\bfraud\b",
         r"\bPaySim\b", r"\bUCI\b.*\bfraud"]),

    # ── Applicability Conditions ───────────────────────────────────────────────
    ("AC-LABEL", "AC", "Requires labeled training data (ground truth dependency)",
        [r"\blabeled\s*(data|dataset|sample)", r"\bground\s*truth\b",
         r"\bannotated\s*(data|sample)", r"\bsupervised\b.*\brequire"]),
    ("AC-CENTRAL","AC","Assumes centralized / well-maintained database",
        [r"\bcentralized\s*(database|system|data)",
         r"\bwell.maintained\s*data", r"\bintegrated\s*database",
         r"\bdata\s*warehouse"]),
    ("AC-ENGLISH","AC","English-language or Western-country context assumed",
        [r"\bUnited\s*States\b", r"\bUK\b.*\bfinancial\b",
         r"\bEuropean\b.*\bfinancial", r"\bWestern\b.*\bcontext"]),
    ("AC-SCALE", "AC", "Requires large-scale data to function",
        [r"\blarge.scale\s*(data|dataset)", r"\bbig\s*data\b",
         r"\bhigh.volume\s*transaction"]),
    ("AC-INFRA", "AC", "Requires advanced computing infrastructure",
        [r"\bGPU\b.*\btraining", r"\bcloud\s*computing\b.*\bmodel",
         r"\bhigh.performance\s*computing"]),

    # ── Limitations Stated ────────────────────────────────────────────────────
    ("LIM-NOLABEL","LIM","No ground truth / label scarcity acknowledged",
        [r"\bno\s*ground\s*truth", r"\black\s*of\s*labeled", r"\bunlabeled\b",
         r"\bimbalanced\s*(data|dataset|class)",
         r"\blabel\s*scarcit", r"\bground.truth\s*(unavail|absent|lack)"]),
    ("LIM-SMALLN","LIM","Small sample / dataset size limitation acknowledged",
        [r"\bsmall\s*(sample|dataset|n\b)", r"\blimited\s*(sample|data\s*size)",
         r"\bsample\s*size\s*(is\s*small|limit)", r"\binsufficient\s*data"]),
    ("LIM-SINGLE","LIM","Single country / organization generalizability limit",
        [r"\bsingle\s*(country|organization|institution|case|dataset)",
         r"\bgeneraliz(e|ation|ability)\b.*\blimit",
         r"\blimited\s*generalizab"]),
    ("LIM-STATIC","LIM","Static dataset / no real-time validation",
        [r"\bstatic\s*dataset", r"\bhistorical\s*data\s*only",
         r"\bnot\s*(tested|validated)\b.*\breal.time",
         r"\blimited\s*to\s*historical"]),
    ("LIM-INTERP","LIM","Interpretability / explainability limitation",
        [r"\bblack\s*box\b", r"\black\s*of\s*explainab",
         r"\binterpretab\w+\s*challenge", r"\bexplainab\w+\s*limit"]),
    ("LIM-CONTEXT","LIM","Context-specificity / external validity concern",
        [r"\bcontext.specific", r"\bexternal\s*validity",
         r"\bcannot\s*be\s*generalized", r"\blimited\s*to\s*(specific|this)\s*context"]),
    ("LIM-DATA",  "LIM","Data quality / availability limitation",
        [r"\bdata\s*quality\b.*\b(issue|problem|challenge|concern)",
         r"\bincomplete\s*data", r"\bmissing\s*(value|data)",
         r"\bdata\s*availability\b.*\b(limit|challenge)"]),

    # ── Gaps Stated ────────────────────────────────────────────────────────────
    ("GAP-DC",   "GAP","Future work / gap: developing-country application",
        [r"\bdeveloping\s*(country|nation|world)\b.*\b(future|apply|test|gap)\b",
         r"\b(future|further)\s*(work|research|study)\b.*\bdeveloping\s*countr"]),
    ("GAP-VILLAGE","GAP","Gap: no village-level / sub-national test conducted",
        [r"\bvillage\s*(level|fund|government)\b.*\b(future|gap|not\s*tested)\b",
         r"\bsub.national\b", r"\blocal\s*government\b.*\b(future|gap|not\s*address)"]),
    ("GAP-RT",   "GAP","Gap: real-time detection not addressed",
        [r"\breal.time\b.*\b(not\s*(address|test|implement)|future|gap)\b",
         r"\bfuture\b.*\breal.time\b"]),
    ("GAP-FW",   "GAP","General future work statement",
        [r"\bfuture\s*(work|research|study|direction)",
         r"\bfurther\s*(work|research|investigation)",
         r"\bremain(s)?\s*for\s*future"]),
    ("GAP-INTER","GAP","Gap: cross-institutional / inter-agency integration not addressed",
        [r"\bcross.institutional", r"\binter.agency\b",
         r"\bdata\s*shar(e|ing)\b.*\b(future|challenge|gap)"]),
    ("GAP-EXPLAIN","GAP","Gap: explainability / transparency for practitioners",
        [r"\bexplainab\w+\b.*\b(future|gap|need(ed)?|practitioner)",
         r"\btransparency\b.*\b(future|gap|need(ed)?|audit)"]),

    # ── IS Theory Used ────────────────────────────────────────────────────────
    ("IST-TAM",  "IST","Technology Acceptance Model (TAM/TAM2/TAM3)",
        [r"\btechnology\s*acceptance\s*model\b", r"\bTAM\b(?!\s*score)",
         r"\bperceived\s*usefulness\b", r"\bperceived\s*ease\s*of\s*use\b"]),
    ("IST-TTF",  "IST","Task-Technology Fit (TTF)",
        [r"\btask.technology\s*fit\b", r"\bTTF\b"]),
    ("IST-DM",   "IST","DeLone & McLean IS Success Model",
        [r"\bDeLone\b", r"\bMcLean\b", r"\bIS\s*success\s*model\b"]),
    ("IST-IT",   "IST","Institutional Theory",
        [r"\binstitutional\s*theory\b", r"\bneo.institutional\b",
         r"\bisomorphism\b", r"\binstitutional\s*pressure"]),
    ("IST-AT",   "IST","Agency Theory",
        [r"\bagency\s*theory\b", r"\bprincipal.agent\b"]),
    ("IST-DSR",  "IST","Design Science Research (DSR) framing",
        [r"\bdesign\s*science\b", r"\bHevner\b", r"\bartifact\b.*\bIS\s*(research|science)",
         r"\bdesign\s*artifact\b"]),
    ("IST-FRAUD","IST","Fraud Triangle / Hexagon / Diamond theory",
        [r"\bfraud\s*triangle\b", r"\bfraud\s*hexagon\b", r"\bfraud\s*diamond\b",
         r"\bCressey\b", r"\bpressure.opportunity.rationalization\b"]),
    ("IST-NONE", "IST","No IS theory — purely technical/computational framing",
        [r"\b(no|without)\s*(theoretical|IS)\s*frame",
         r"\bpurely\s*(technical|computational)\s*(approach|method)"]),
    ("IST-UTAUT","IST","UTAUT / UTAUT2",
        [r"\bUTAUT\b", r"\bunified\s*theory\s*of\s*acceptance\b"]),
    ("IST-GRC",  "IST","Governance, Risk, Compliance (GRC) framework",
        [r"\bgovernance.risk.compliance\b", r"\bGRC\b",
         r"\brisk\s*governance\b.*\bcompli"]),

    # ── Context / Domain ──────────────────────────────────────────────────────
    ("CTX-GOVPUB","CTX","Government / public sector financial fraud context",
        [r"\bpublic\s*(sector|financial|fund|expenditure)\s*fraud",
         r"\bgovernment\s*(corruption|fraud|financial\s*crime)",
         r"\bcorruption\s*(in|of)\s*(public|government)"]),
    ("CTX-PROCU","CTX","Public procurement fraud / corruption context",
        [r"\bprocurement\s*(fraud|corruption|irregularit|manipulat)",
         r"\bbid\s*(rigg|fraud|manipulat|collus)",
         r"\bpublic\s*contracting\s*fraud"]),
    ("CTX-VILLAGE","CTX","Village fund / Dana Desa / sub-national governance context",
        [r"\bdana\s*desa\b", r"\bvillage\s*(fund|government|finance)",
         r"\bdesa\b.*\b(dana|korupsi|fraud)\b"]),
    ("CTX-BANK", "CTX","Banking / credit card / payment fraud (private)",
        [r"\bcredit\s*card\s*fraud", r"\bonline\s*payment\s*fraud",
         r"\bbank(ing)?\s*fraud", r"\bfinancial\s*institution\s*fraud"]),
    ("CTX-AML",  "CTX","Anti-Money Laundering (AML) context",
        [r"\banti.money.laundering\b", r"\bAML\b", r"\bmoney\s*laundering\b"]),
    ("CTX-TAX",  "CTX","Tax fraud / evasion context",
        [r"\btax\s*(fraud|evasion|compliance|avoidance)",
         r"\bfiscal\s*(fraud|crime)"]),
    ("CTX-INDO", "CTX","Indonesia-specific context",
        [r"\bIndonesia\b", r"\bIndonesian\b"]),
    ("CTX-DEV",  "CTX","Developing country / global south context",
        [r"\bdeveloping\s*countr", r"\bglobal\s*south\b",
         r"\blow.income\s*countr", r"\bemerging\s*econom"]),
    ("CTX-SLR",  "CTX","Systematic literature review / bibliometric meta-study",
        [r"\bsystematic\s*literature\s*review\b", r"\bSLR\b",
         r"\bbibliometric\s*analy", r"\bmeta.analy"]),
    ("CTX-SHELL","CTX","Shell company / beneficial ownership fraud context",
        [r"\bshell\s*compan", r"\bbeneficial\s*owner",
         r"\bsham\s*compan", r"\bfrontman\b"]),
]


def get_sentences(text):
    """Split text into sentences (rough)."""
    sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sents if len(s.strip()) > 20]


def extract_evidence(text, patterns, max_quotes=3):
    """
    Find up to max_quotes sentences that match any of the patterns.
    Returns list of evidence quote strings (truncated to 200 chars).
    """
    sentences = get_sentences(text)
    found = []
    seen = set()
    for sent in sentences:
        for pat in patterns:
            if re.search(pat, sent, re.IGNORECASE):
                clean = sent.replace("\n", " ").strip()[:200]
                if clean not in seen:
                    found.append(clean)
                    seen.add(clean)
                if len(found) >= max_quotes:
                    return found
                break
    return found


def code_paper(paper_id, text, rq_tags, theme_tags):
    """
    Apply all code patterns to paper text.
    Returns list of dicts: {paper_id, code, category, description, evidence[]}
    Also detects IST-NONE if no IS theory codes found.
    """
    results = []
    ist_found = False
    full_text_lower = text.lower()

    for code_label, cat, desc, patterns in CODE_PATTERNS:
        # Quick check: does any pattern appear in lowercased text?
        any_match = any(re.search(p, text, re.IGNORECASE) for p in patterns)
        if any_match:
            evidence = extract_evidence(text, patterns, max_quotes=3)
            if evidence:
                results.append({
                    "paper_id": paper_id,
                    "code": code_label,
                    "category": cat,
                    "description": desc,
                    "evidence_1": evidence[0] if len(evidence) > 0 else "",
                    "evidence_2": evidence[1] if len(evidence) > 1 else "",
                    "evidence_3": evidence[2] if len(evidence) > 2 else "",
                    "rq_tags": rq_tags,
                    "theme_tags": theme_tags,
                })
                if cat == "IST":
                    ist_found = True

    # Auto-assign IST-NONE if no IS theory detected
    if not ist_found:
        results.append({
            "paper_id": paper_id,
            "code": "IST-NONE",
            "category": "IST",
            "description": "No IS theory — purely technical/computational framing (inferred from absence)",
            "evidence_1": "(no IS theory patterns detected in full text)",
            "evidence_2": "",
            "evidence_3": "",
            "rq_tags": rq_tags,
            "theme_tags": theme_tags,
        })

    return results


def write_workbook(paper_id, title, year, authors, journal, doi, sjr, quality_score,
                   pipeline_status, irr_resolution, rq_tags, theme_tags,
                   codes, out_path):
    """Write per-paper coding workbook .md file."""
    lines = [
        f"---",
        f"paper_id: {paper_id}",
        f'title: "{title[:120].replace(chr(34), chr(39))}"',
        f"year: {year}",
        f"irr_resolution: {irr_resolution}",
        f"rq_tags: \"{rq_tags}\"",
        f"theme_tags: \"{theme_tags}\"",
        f"sjr_quartile: {sjr}",
        f"quality_score: {quality_score}",
        f"---",
        f"",
        f"# Coding Workbook: {paper_id}",
        f"",
        f"**Title**: {title}",
        f"**Authors**: {authors[:200]}",
        f"**Year**: {year} | **Journal**: {journal}",
        f"**DOI**: {doi}",
        f"**SJR**: {sjr} | **Quality Score**: {quality_score} | **Pipeline**: {pipeline_status}",
        f"**RQ Tags**: {rq_tags}",
        f"**Theme Tags**: {theme_tags}",
        f"",
        f"---",
        f"",
        f"## Open Codes",
        f"",
    ]

    # Group codes by category
    cat_order = ["MC", "FE", "DS", "AC", "LIM", "GAP", "IST", "CTX"]
    cat_names = {
        "MC": "Method Claims",
        "FE": "Feature Engineering",
        "DS": "Data Sources",
        "AC": "Applicability Conditions",
        "LIM": "Limitations Stated",
        "GAP": "Gaps Stated",
        "IST": "IS Theory Used",
        "CTX": "Context / Domain",
    }

    codes_by_cat = defaultdict(list)
    for c in codes:
        codes_by_cat[c["category"]].append(c)

    for cat in cat_order:
        cat_codes = codes_by_cat.get(cat, [])
        if not cat_codes:
            continue
        lines.append(f"### {cat}: {cat_names[cat]}")
        lines.append("")
        for c in cat_codes:
            lines.append(f"#### `{c['code']}` — {c['description']}")
            for i, ev_key in [("evidence_1", 1), ("evidence_2", 2), ("evidence_3", 3)]:
                # fix variable name
                pass
            evs = [c.get("evidence_1",""), c.get("evidence_2",""), c.get("evidence_3","")]
            for ev in evs:
                if ev:
                    lines.append(f"> \"{ev}\"")
            lines.append("")

    lines += [
        "---",
        "",
        "## Descriptive Theme Notes",
        "",
        "_(Filled in Phase F2.2 — descriptive theme aggregation)_",
        "",
        "## Inter-Paper Relation Notes",
        "",
        "_(Filled in Phase F2.3 — analytical themes)_",
        "",
        "## Coder Annotations",
        "",
        "- [ ] Full text read and codes verified",
        "- [ ] Descriptive theme assigned",
        "- [ ] Inter-paper relations mapped",
        "",
    ]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

df = pd.read_csv(CORPUS_CSV)
inc = df[df["irr_resolution"].isin(["CONSENSUS", "DOMAIN_OVERRIDE"])].copy()
inc = inc.sort_values("paper_id").reset_index(drop=True)

all_codes = []

print(f"Open coding {len(inc)} INCLUDE papers...")
print()

for _, row in inc.iterrows():
    pid = row["paper_id"]
    title    = str(row.get("title", "")).strip()
    year     = str(row.get("year", "")).replace(".0","")
    authors  = str(row.get("authors", "")).strip()
    journal  = str(row.get("journal", "")).strip()
    doi      = str(row.get("doi", "")).strip()
    sjr      = str(row.get("sjr_quartile", "")).strip()
    quality_score = str(row.get("quality_score", "")).strip()
    pipeline_status = str(row.get("pipeline_status","")).strip()
    irr      = str(row.get("irr_resolution","")).strip()
    rq_tags  = str(row.get("rq_tags","")).strip()
    theme_tags = str(row.get("theme_tags","")).strip()

    # Read extracted text
    extracted_path = os.path.join(EXTRACTED_DIR, f"{pid}.md")
    if os.path.exists(extracted_path):
        with open(extracted_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        # Remove YAML header from text for coding
        text = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
    else:
        text = title + " " + str(row.get("notes",""))

    codes = code_paper(pid, text, rq_tags, theme_tags)
    all_codes.extend(codes)

    # Write workbook
    workbook_path = os.path.join(CODING_DIR, f"{pid}_codes.md")
    write_workbook(pid, title, year, authors, journal, doi, sjr, quality_score,
                   pipeline_status, irr, rq_tags, theme_tags, codes, workbook_path)

    code_labels = [c["code"] for c in codes]
    print(f"  {pid}: {len(codes)} codes — {', '.join(code_labels[:8])}{'...' if len(code_labels)>8 else ''}")

# Save master CSV
master_df = pd.DataFrame(all_codes)
master_df.to_csv(MASTER_CSV, index=False)

print()
print("=" * 60)
print("OPEN CODING SUMMARY")
print("=" * 60)
print(f"Total code instances: {len(all_codes)}")
print(f"Papers coded: {master_df['paper_id'].nunique()}")
print()
print("Code frequency (top 30):")
freq = master_df["code"].value_counts().head(30)
for code, count in freq.items():
    print(f"  {code:<20} {count:>3} papers")

print()
print("Category distribution:")
cat_dist = master_df["category"].value_counts()
for cat, count in cat_dist.items():
    print(f"  {cat}: {count} code instances")

print()
print(f"Master CSV: {MASTER_CSV}")
print(f"Workbooks:  {CODING_DIR}")
