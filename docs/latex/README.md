# Compilation Instructions — `main.tex`

## Required File Support

The LaTeX paper uses the Elsevier Procedia CRC template, which requires two support files not included here:
- `elsarticle.cls` — Elsevier article document class
- `ecrc.sty` — Procedia CRC extension package

### Download from Elsevier (Official Source)
1. Go to: https://www.elsevier.com/authors/tools-and-resources/latex/latex-instructions
2. Download the "Procedia" LaTeX package ZIP
3. Extract `elsarticle.cls` and `ecrc.sty` into this folder (`docs/latex/`)

### Alternative: Install via TeX Distribution
If you have TeX Live:
```
tlmgr install elsarticle
```
MiKTeX: search for `elsarticle` in the package manager.

---

## Figure Path Setup

Charts are loaded with:
```latex
\graphicspath{{../../src/output_v1/charts/}}
```

This path is **relative to wherever you run pdflatex from**. Compile from the `docs/latex/` directory:
```
cd "docs/latex"
pdflatex main.tex
pdflatex main.tex   # run twice for cross-references
```

If compiling from another directory, update `\graphicspath` accordingly or copy the charts folder.

---

## Compilation

```bash
# From docs/latex/ with elsarticle.cls and ecrc.sty in same folder:
pdflatex main.tex
pdflatex main.tex
```

No BibTeX step is needed — references use inline `thebibliography`.

---

## Pre-Submission Checklist

- [ ] Fill author names and affiliation (replace [BLINDED FOR REVIEW] placeholders)
- [ ] Verify [28] = [12] duplicate — collapse to [12] citation in final revision
- [ ] Remove [18] "removed" placeholder entry from bibliography if no longer needed
- [ ] Confirm all 9 chart `.png` files are accessible at `../../src/output_v1/charts/`
- [ ] Check similarity index (target ≤ 20%)
- [ ] Confirm reference count ratio: ≥ 60% from last 5 years (2021–2026)
- [ ] Verify page count falls within 3–10 pages after compilation

---

## Chart Files Expected

| Figure in Paper | File Name |
|---|---|
| Fig. 1 — Research Framework | TikZ (embedded in main.tex) |
| Fig. 2 — Feature Distributions | `feature_distributions.png` |
| Fig. 3 — Feature Correlation Heatmap | `feature_correlation_heatmap.png` |
| Fig. 4 — Anomaly Rate Consistency | `anomaly_rate_consistency.png` |
| Fig. 5 — Score Distributions | `score_distributions.png` |
| Fig. 6 — Typology Distribution | `typology_distribution.png` |
| Fig. 7 — RDA Error Decomposition | `rda_error_decomposition.png` |
| Fig. 8 — Village Priority Tiers | `village_persistence_tiers.png` |
| Fig. 9 — PCA Projection | `pca_projection.png` |
| Fig. 10 — t-SNE Projection | `tsne_projection.png` |
