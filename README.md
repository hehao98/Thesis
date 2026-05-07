# Dispelling Software Engineering Myths: A Pragmatic Causal Inference Approach

**Thesis Proposal** by Hao He, Carnegie Mellon University, March 9, 2026.

**Committee:** Bogdan Vasilescu (Co-Chair), Christian Kästner (Co-Chair), Rohan Padhye, Narayan Ramasubbu

## Overview

Software engineering practice is filled with myths — widely held beliefs derived from intuition, experience, and conventional wisdom that have never been rigorously tested or, when tested, have produced inconclusive results. This thesis argues that causal credibility assessments are feasible in empirical software engineering through explicit articulation of causal theory and assumptions. Specifically, it demonstrates a four-step process applied consistently across empirical studies:

1. Derive an explicit causal theory from existing domain knowledge (e.g., as a directed acyclic graph),
2. Define the causal estimate of interest through the potential outcome framework and specify the assumptions for a causal interpretation,
3. Honestly acknowledge and mitigate limitations in data collection, metric design, and model specifications,
4. Thoughtfully navigate alternative explanations (i.e., alternative causal structures) that may also be supported by the results.

Three empirical studies demonstrate this approach by challenging widely held software engineering beliefs: that dependency pinning improves security, that fake GitHub stars provide sustainable promotional benefits, and that AI coding assistants unambiguously improve productivity.

## Structure

### Top-level LaTeX sources

| File | Description |
|------|-------------|
| `main.tex` | Main document entry point (preamble, front matter, chapter assembly) |
| `chap-intro.tex` | Chapter 1: Introduction, thesis statement, and contributions |
| `main-pinning.tex` | Chapter 3: Dependency pinning empirical study (full paper) |
| `main-fake-stars.tex` | Chapter 4: Fake GitHub stars empirical study (full paper) |
| `main-cursor.tex` | Chapter 5: Cursor AI empirical study (full paper) |
| `analysis-pinning.tex` | Causal credibility analysis appended to the pinning chapter |
| `analysis-fake-stars.tex` | Causal credibility analysis appended to the fake-stars chapter |
| `analysis-cursor.tex` | Causal credibility analysis appended to the Cursor chapter |
| `cmuthesis.cls` | CMU thesis document class |

### Bibliography

| File | Description |
|------|-------------|
| `references.bib` | Shared bibliography (intro, tutorial cross-cutting references) |
| `references-pinning.bib` | Pinning chapter bibliography |
| `references-fake-stars.bib` | Fake-stars chapter bibliography |
| `references-cursor.bib` | Cursor chapter bibliography |

### Subdirectories

| Path | Description |
|------|-------------|
| `tutorial/` | Chapter 2 sources: causal inference tutorial paper, data, notebooks, plots, and slides. Included into `main.tex` via `tutorial/paper/{1-introduction,2-primer,3-worked-example,4-discussion,appendix}.tex` |
| `fake-star-reanalysis/` | R Markdown notebooks (`regression.Rmd`, `robustness.Rmd`) and data (`model_stars.csv`, `repo_labels.csv`) for the fake-stars panel regression and robustness checks |
| `figs-pinning/`, `figs-fake-stars/`, `figs-cursor/` | Per-chapter figures |
| `plans/` | Detailed sub-plans (e.g., per-chapter causal credibility analysis plans), named `YYYYMMDD - {Summary}.md` per `AGENTS.md` |

## Building

Requires a LaTeX distribution with `biber` for bibliography processing.

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).
