# Conclusion Chapter Plan

**Status:** Draft plan, pending author review
**Target file:** New `chap-conclusion.tex`, `\include`d from `main.tex` after Chapter~\ref{chp:cursor}
**Replaces:** The author's existing skeleton notes in `main.tex` (lines 327--343), which already include a Cursor design-strength paragraph that should be relocated into Section~2 of the conclusion below

---

## Source Material Anchoring This Plan

Two pieces of authorial guidance left in `main.tex` lines 329--337 must drive the conclusion's content rather than be paraphrased away:

1. **Author's structural skeleton (lines 329--331).** The conclusion has three sections: (1) Summary of Contributions, (2) Revisiting the Thesis Statement, (3) Final Thoughts.
2. **Final-thoughts seed notes (lines 333--337).** Three substantive points the author wants the conclusion to make:
   - The downstream-misuse worry: "where does it leave us? is it credible? how do you envision somebody downstream uses this information better than how they misscited Ray?"
   - The author's own ranking of the three studies: pinning strongest, Cursor close to strong, fake stars weakest but informative because the policy claim is not overturned.
   - The pragmatic stance: all causal inference rests on assumptions (RCTs included); cynics will reject any study and uninformed readers will misread descriptive results as causal; the field's path forward is iterative refinement of designs through credibility analysis, not certainty.

The plan below preserves the author's structure, voice, and substantive claims rather than rewriting them.

---

## Section 1 — Summary of Contributions

**Goal:** Recap what each chapter contributes, with deliberate parallelism so a reader can see the four-step framework operating across three substantively different studies. This is not a re-summary of findings (the chapter abstracts already do that); it is a framing that sets up Section~2's cross-chapter comparison.

### 1.1 The Tutorial (Chapter~\ref{chp:background})

- The literature-review evidence: 29\% of empirical SE papers at ICSE/FSE/ASE 2015--2025 are motivated by a causal question; only 1.9\% use a recognised causal inference method; the ratio has been flat for a decade.
- The tutorial's contribution: a self-contained primer on potential outcomes, DAGs, and design-based identification (DiD, IV, RDD, FE) with a worked AI-coding-tool example showing how progressively stronger designs collapse a +911\% naive estimate to a credible +32--52\% DiD estimate.
- Frame this chapter as the *methodological infrastructure* the three empirical chapters build on, not as a standalone literature review.

### 1.2 Pinning (Chapter~\ref{chp:pinning})

- The myth: pinning improves project security against malicious package updates.
- The design: counterfactual simulation of pinning vs.\ floating on 10{,}000 npm packages and 10{,}000 GitHub repositories, with both potential outcomes simulated for every project from the same `package.json`.
- The finding: pinning is futile or counter-productive in large dependency graphs ($\geq$498 nodes), and ecosystem-level coordinated pinning at $\sim$100 critical packages reduces malicious-update spread by up to 75\%.
- The methodological contribution: identification by construction is achievable in observational software-engineering data when an underlying simulator is faithful enough.

### 1.3 Fake Stars (Chapter~\ref{chp:fake-stars})

- The myth: buying fake GitHub stars provides sustainable promotional benefit.
- The design: \SystemName mines GitHub events for two signatures of inauthentic starring, identifies $\sim$6M fake stars across 26{,}254 repositories, and uses panel autoregression with repository fixed effects to estimate the promotional and penalty effects.
- The finding: short-run promotional bump $<$2 months, then a long-run penalty; majority of campaigns target phishing/malware repositories.
- The methodological contribution: even when the maintainer's decision is endogenous and identification cannot be by construction, a panel-FE design paired with three targeted robustness checks (R1: survivor stratification; R2: topic stratification; R3: lead-lag swap) can discipline the directions of residual biases, even if it cannot eliminate them.

### 1.4 Cursor (Chapter~\ref{chp:cursor})

- The myth: AI coding tools unambiguously improve developer productivity.
- The design: \citet{borusyak2024revisiting} DiD with propensity-score matching on six-month pre-adoption dynamics, plus a panel GMM analysis decomposing the velocity-quality feedback.
- The finding: large transient velocity gains for $\sim$1--2 months, then a persistent increase in static-analysis warnings and cognitive complexity that subsequently dampens velocity.
- The methodological contribution: a quasi-experimental design hits a "close-to-strong" credibility level when the assignment mechanism cannot be controlled but matching, an estimator robust to heterogeneous treatment effects, and cross-direction GMM agreement substitute for missing experimental variation.

---

## Section 2 — Comparing the Three Studies on Causal Credibility

**Goal:** Make the cross-study comparison the author has already begun (lines 339--343 of `main.tex`) the load-bearing analytical contribution of the conclusion. This is where the conclusion earns its keep beyond a recap. The author's existing paragraph (now in `main.tex`) is the kernel; this section expands it into a structured comparison.

### 2.1 Lift the existing paragraph into the conclusion

Move `main.tex` lines 339--343 verbatim into this section as its opening paragraph. It already says: pinning achieves identification by construction; fake-stars is fully observational with three residual threats bounded only by post-hoc robustness checks; Cursor sits in between because matching, the Borusyak imputation, and cross-direction GMM agreement substitute for missing experimental variation.

### 2.2 Add a comparison table

A compact table makes the ordering inspectable at a glance. Suggested columns:

| Chapter | Treatment assignment | Load-bearing assumptions | Diagnostic / robustness device | Author's credibility ranking |
|---|---|---|---|---|
| Pinning | Imposed by simulator | A1 (simulation fidelity) only | Resolution-failure analysis; npm semantics validation | Strongest |
| Cursor (DiD) | Maintainer choice; matched on 6-month trajectories | A1 (parallel trends), B1 (sequential exogeneity for GMM) | Pre-trend Wald test; AR(2)/Sargan; cross-estimator appendix | Close to strong |
| Fake stars | Endogenous purchase | A1 (strict exogeneity), A2 (no time-varying topic confounders), A5 (panel completeness) | R1 (survivor stratification), R2 (topic stratification), R3 (lead-lag swap) | Weakest but informative |

The table's columns deliberately mirror the four-step framework: DAG-justified treatment, named identifying assumptions, the design or robustness device that addresses each, and a final qualitative ranking the author is willing to defend.

### 2.3 Articulate the ordering

State the author's ranking from `main.tex` line 335 directly. The pragmatic argument: identification by construction (pinning) is preferable when the data-generating process can be simulated faithfully; design-based identification with targeted matching and an estimator robust to heterogeneous effects (Cursor) is the next-best option when the treatment is observed but not controlled; panel FE with explicit robustness checks on the residual biases (fake stars) is the fallback when even matching is infeasible because the treatment proxy is endogenous and noisy.

### 2.4 Argue that policy survival is orthogonal to design strength

A surprise of the cross-study comparison: the chapter with the *weakest* design (fake stars) yields a policy claim that survives *most easily*, because the residual biases on the short-run estimate point upward and would only strengthen the recommendation against buying fake stars. The pinning chapter's policy claim survives because the identification is strong by construction. The Cursor chapter's policy claim survives because the most plausible residual confounders bias in the direction the policy already advocates for. Design strength and policy survival are therefore distinct dimensions, and the conclusion should resist the temptation to equate them.

---

## Section 3 — Revisiting the Thesis Statement

**Goal:** Return to the framed thesis statement on `chap-intro.tex` line 70 and assess whether the three studies, taken together, support it. The thesis statement is:

> *Causal credibility assessments are feasible in empirical software engineering through an explicit articulation of causal theory and assumptions.*

### 3.1 Restate the four-step framework

Briefly recap the four steps (DAG, estimand + assumptions, limitations, alternative explanations) introduced in Chapter~\ref{chp:background} (`chap-intro.tex` lines 75--80) so that the assessment is self-contained.

### 3.2 Show the framework operating in practice

For each empirical chapter, point to the section that instantiates each of the four steps. This is a one-paragraph cross-reference, not a re-summary:

- **Pinning:** Causal Theory~\ref{sec:pinning-credibility-theory}, Estimand~\ref{sec:pinning-credibility-estimand}, Limitations~\ref{sec:pinning-credibility-limitations}, Alternatives~\ref{sec:pinning-credibility-alternatives}, Summary~\ref{sec:pinning-credibility-summary}.
- **Fake stars:** Causal Theory~\ref{sec:fake-stars-credibility-theory}, Estimand~\ref{sec:fake-stars-credibility-estimand}, Limitations~\ref{sec:fake-stars-credibility-limitations}, Alternatives~\ref{sec:fake-stars-credibility-alternatives}, Summary~\ref{sec:fake-stars-credibility-summary}.
- **Cursor:** Causal Theory~\ref{sec:cursor-credibility-theory}, Estimand~\ref{sec:cursor-credibility-estimand}, Limitations~\ref{sec:cursor-credibility-limitations}, Alternatives~\ref{sec:cursor-credibility-alternatives}, Summary~\ref{sec:cursor-credibility-summary}.

### 3.3 The verdict

The thesis statement claims *feasibility*, not *certainty*. The three empirical chapters demonstrate feasibility along three different design tracks (simulation, DiD, panel FE), at three different credibility levels, with three different residual-bias profiles. The fact that the framework operates uniformly across designs that differ this much is the argument that the feasibility claim is broadly applicable rather than design-specific.

What the thesis does *not* claim, and the conclusion should not overclaim:
- That the four-step framework eliminates causal uncertainty (it does not---each chapter still has load-bearing assumptions that require empirical argument).
- That every empirical SE study should adopt the full framework (the Chapter~\ref{chp:background} literature review establishes that 29\% of empirical SE papers are causal in nature; for the other 71\%, the framework is unnecessary).
- That the framework resolves the measurement-validity challenges that AGENTS.md flags as orthogonal (e.g., whether bug-fix commits are valid proxies for defect proneness).

---

## Section 4 — Final Thoughts

**Goal:** Convert the author's seed notes (`main.tex` lines 333--337) into prose. The notes already contain three substantive ideas; the conclusion should preserve all three rather than dilute or generalise them.

### 4.1 The downstream-misuse problem (from the note: "how do you envision somebody downstream uses this information better than how they misscited Ray?")

`chap-intro.tex` lines 33--40 already documents the Ray et al.\ controversy and its counter-rebuttal. The conclusion should connect the seed note to that introduction passage: a causally hedged study (Ray et al.) was misread downstream as a causal claim because the field lacks a shared framework for evaluating causal credibility. The four-step framework offers a partial answer:

- *For producers of empirical work,* the framework provides a discipline that forces the load-bearing assumptions into the open before the study reaches downstream readers.
- *For consumers of empirical work,* the framework provides a checklist for distinguishing studies whose authors have stress-tested their identification (and reported what survived) from studies that have not.
- *For misciting downstream readers,* the framework cannot prevent miscitation, but it can make the gap between what a study claims and what a downstream reader infers visible and challengeable.

The fake-stars chapter's worked example---where the policy recommendation survives even though the design is weakest---is the clearest illustration of this asymmetry. A downstream reader who reads only the abstract still gets the policy claim; a downstream reader who engages with the credibility section understands *why* the policy claim survives and at what cost.

### 4.2 The pragmatic stance (from the note: "all causal inference papers will rest on some assumptions (this applies to controlled experiments too!)")

This is the most important rhetorical commitment of the conclusion. Three sub-points to make explicitly:

- **Assumptions are universal, not a flaw of observational work.** Even RCTs rest on assumptions: SUTVA, compliance, no spillover, construct validity of the outcome metric, generalisability beyond the trial population. The novelty of the four-step framework is not that it makes assumptions visible (every method does), but that it makes them visible *uniformly* across observational designs that the field has historically treated as if they had no assumptions to articulate.
- **Cynics and uninformed readers are bounding cases.** Per the seed note: a fully cynical critic can refuse to believe any study, and an uninformed reader can misread any descriptive result as causal. Neither failure mode is the framework's responsibility to solve; the framework's value is for the practitioner in between, who is willing to engage with the evidence but needs a structured way to calibrate confidence.
- **Iterative refinement is the path forward.** The pinning study's identification by construction was made possible by an experimental npm resolver feature that did not exist a decade ago. The Cursor study's matching procedure depends on six-month pre-adoption trajectories that became observable only after dense repository event logging matured. Each generation of empirical SE work that engages with the framework hands the next generation a stronger toolkit.

### 4.3 The author's ranking, stated plainly

Reproduce the author's ranking from the seed note: pinning strongest (only simulation fidelity), Cursor close to strong (parallel trends + sequential exogeneity), fake stars weakest but informative because the policy recommendation survives. The ranking is the author's honest assessment of what the three studies achieve, and the conclusion should not soften it into a more uniform "all three are credible." Reviewers, downstream researchers, and future PhD students benefit more from a calibrated ranking than from rhetorical evenness.

### 4.4 Closing posture

End with the pragmatic stance the abstract and `chap-intro.tex` both gesture at. The thesis does not claim to resolve the empirical SE field's disconnect between causal ambition and methodological practice. It claims that the disconnect is bridgeable through explicit articulation of causal theory and assumptions, and that the four-step framework is one operationalisation of that bridge.

---

## Tasks

- [ ] Create `chap-conclusion.tex` with three sections (Summary of Contributions, Revisiting the Thesis Statement, Final Thoughts) plus the cross-study comparison as Section~2.
- [ ] Move `main.tex` lines 339--343 (the existing Cursor cross-study paragraph) into Section~2.1 of the new file; remove the comment-only skeleton on lines 327--337 once their content has been incorporated.
- [ ] Update `main.tex` to `\include{chap-conclusion}` after Chapter~\ref{chp:cursor}.
- [ ] Add cross-study comparison table to Section~2.2 (treat the suggested table above as a starting point; verify column count and final formatting match thesis style).
- [ ] Add `\label{sec:pinning-credibility-summary}`, `\label{sec:fake-stars-credibility-summary}`, `\label{sec:cursor-credibility-summary}` to the existing `Causal Credibility Summary` subsections in the three analysis files so Section~3.2 can cross-reference them. (None of the three currently have an explicit label.)
- [ ] Verify all `\ref{}` targets used in the conclusion exist before final compile.
- [ ] Pass the final draft through the AGENTS.md style rules: one sentence per line, em-dashes without spaces, declarative tone, no superlatives or hedging.

---

## Out-of-Scope

- Re-summarising the three chapter findings beyond a one-paragraph recap each. The chapter abstracts and `summary-rq` boxes already do this work.
- Litigating measurement-validity concerns. Per AGENTS.md, the thesis addresses identification, not measurement; the conclusion should reaffirm this scope rather than expand it.
- Adding new related-work positioning. The thesis statement and the introduction already place the work relative to Bradford Hill, the credibility revolution in econometrics, and Rosenbaum sensitivity analysis (`chap-intro.tex` line 73); the conclusion does not need to re-position.
