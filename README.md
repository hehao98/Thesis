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

| File | Description |
|------|-------------|
| `main.tex` | Main document entry point |
| `chap-intro.tex` | Introduction, thesis statement, and contributions |
| `chap-background.tex` | A Primer on Causal Credibility |
| `chap-finished-work.tex` | Completed empirical studies |
| `chap-proposed-work.tex` | Proposed work |
| `main-pinning.tex` | Full paper: Dependency Pinning study |
| `main-fake-stars.tex` | Full paper: Fake GitHub Stars study |
| `main-cursor.tex` | Full paper: Cursor AI study |
| `references*.bib` | Bibliography files |
| `cmuthesis.cls` | CMU thesis document class |

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
