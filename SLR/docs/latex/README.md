# LaTeX Paper Compilation Guide

## Files

| File | Purpose |
|---|---|
| `main.tex` | Full SLR paper source |
| `references.bib` | BibTeX bibliography (30 entries) |
| `elsarticle.cls` | Elsevier article class (ICCSCI template) |
| `ecrc.sty` | Elsevier conference style file |
| `framed.sty` | Framed environment support |

## Compile Instructions

### Option 1 — Overleaf (recommended, no local install required)

1. Zip this entire `latex/` folder
2. Upload to [https://www.overleaf.com](https://www.overleaf.com) → New Project → Upload
3. Set compiler: **pdflatex**
4. Click Recompile

### Option 2 — Local TeX installation (MiKTeX or TeX Live)

```powershell
cd "d:\BINUS Works\Codes\research_banks\research\is_dandes_anticorr\SLR\docs\latex"
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Output: `main.pdf`

### Option 3 — Docker (no TeX install needed)

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
  bash -c "pdflatex main && bibtex main && pdflatex main && pdflatex main"
```

## Conference Submission Checklist (ICCSCI / Procedia Computer Science)

- [ ] Abstract ≤ 250 words (current: 248)
- [ ] Keywords: exactly 5 (current: 5 ✓)
- [ ] Author affiliations complete (restore after blind review)
- [ ] All figures referenced and captioned
- [ ] All tables referenced and captioned
- [ ] References in IEEE numeric format (elsarticle-num ✓)
- [ ] Page limit: 8–10 pages (verify in compiled PDF)
- [ ] No track changes or comments in final version
- [ ] Copyright transfer form completed at submission

## Structure

```
Section 1: Introduction          (~500 words)
Section 2: Related Work          (~400 words)
Section 3: Methodology           (~500 words)
Section 4: Results               (~700 words)
Section 5: Discussion            (~500 words)
Section 6: Conclusion            (~350 words)
References                       (30 entries)
```

**Estimated page count**: 8–9 pages in two-column elsarticle format.
