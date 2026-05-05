# Causal Credibility Analysis — Cursor Chapter

**Status:** Draft plan, pending author review
**Target file:** `analysis-cursor.tex`
**Placement:** Between Results (Section 4, including Robustness Checks) and Discussion (Section 5)

---

## Tasks

- [ ] Literature review to justify each DAG node (cite sources for each confounder, mediator, and treatment-effect channel; pinning-chapter review identified ~10 sources, similar effort expected here)
- [ ] Draw DAG figure (`figs-cursor/dag-cursor.pdf`) extending the existing `Theory.pdf` to make confounder structure explicit
- [ ] Write Step 1 — Causal Theory (separate panels for the DiD estimand and the GMM dynamic feedback estimand)
- [ ] Write Step 2 — Causal Estimands and Identifying Assumptions
- [ ] Write Step 3 — Limitations and Known Caveats (causal credibility threats only)
- [ ] Write Step 4 — Alternative Explanations
- [ ] Add `\input{analysis-cursor}` to `main-cursor.tex` before the Discussion section
- [ ] Cross-reference (rather than supersede) the existing `Limitations and Threats to Validity` (Section~\ref{sec:cursor-limitations}) and `Robustness Checks` (Section~\ref{sec:robustness}); external and measurement validity remain there
- [ ] Decide whether `figs-cursor/Theory.pdf` (mechanism diagram) and the new `dag-cursor.pdf` (identification diagram) are kept as separate figures or unified

---

## Step 1 — Explicit Causal Theory

**Goal:** Make the assumed causal structure visible and auditable for both the DiD estimand (effect of Cursor adoption on velocity and quality) and the GMM estimand (dynamic feedback between velocity and quality). Each node and edge in the DAG must be justified from existing literature.

### Node Inventory with Literature Justifications

**Literature review pending.** Each entry below lists what published evidence is required to support the node's inclusion. Bibliographic entries should be added during the literature review pass before drawing the DAG. Where the existing chapter already discusses a node empirically, that discussion can stand in for the literature support.

#### Treatment

**$D$ — Cursor adoption** (operationalized as the first month a `.cursorrules` file or `.cursor/` directory appears in the default branch)
- Definitional support: documentation of Cursor's configuration-file conventions.
- Validation support: any existing study using configuration-file-based identification of tool adoption; the chapter's own measurement-validation passages.

#### Outcomes

**Velocity** (commits, lines added, logged) and **Quality** (SonarQube static-analysis warnings, cognitive complexity, duplicate-line density, logged)
- Need: empirical software engineering literature establishing these as standard panel-data outcomes for productivity and quality respectively.

#### Mediators

**Code production rate, per-line quality, developer review effort per line**
- Need: literature on the productivity/quality trade-off in AI-assisted development. Plausible sources to consult: studies on Copilot acceptance and productivity, studies on code review under AI assistance, studies on multi-file vs. line-level diff comprehension.

#### Time-Invariant Confounders (Controlled by Repository Fixed Effects $\mu_i$)

**$U_i$ — Team and project characteristics** (domain, size, language distribution, contributor expertise, governance maturity)
- Need: literature linking team characteristics to both AI tool adoption and code quality outcomes.

**Selection on growth trajectory**
- Need: open-source lifecycle literature establishing that projects in particular growth phases differ systematically (repository-abandonment studies, community-evolution studies).

#### Time-Varying Confounders

**Industry trends and ecosystem shocks** (calendar-time effects: GitHub policy changes, LLM model releases, broader AI tooling rollouts)
- Need: documentation of significant 2024–2025 events affecting open-source activity. Controlled by month fixed effects $\lambda_t$.

**Other AI tool usage** (Copilot, Claude Code, Windsurf, Cline, OpenHands)
- Need: literature on the prevalence and effects of competing AI coding tools during the study window. Detection signatures (e.g., `.vscode/`, `.claude/`) cited from prior work or vendor documentation. Status: present in both treatment and control groups; estimates therefore reflect the *additional* effect of Cursor relative to the prevailing AI baseline.

**Repository activity decay**
- Need: literature documenting that repository activity decays even absent any external event. Baseline against which any treatment effect must be differenced.

#### Anticipation Channel

**Pre-commit Cursor use** — developers may experiment locally before pushing configuration
- Need: literature on tool adoption preceding artefact commit. Mitigated by dropping $h = -1$ from pre-trend tests.

### Two Causal Sub-Theories on the Same DAG

The DAG figure should make visible *two* distinct identification problems on the same node set:

1. **Direct effect of $D$ on velocity and quality** — identified by the DiD design under parallel trends. Back-door paths run through team/project characteristics and industry trends, blocked by $\mu_i$, $\lambda_t$, time-varying covariates $Z_{it}$, and propensity-score matching on six-month pre-adoption dynamics.
2. **Dynamic feedback between velocity and quality** — identified by panel GMM. The estimand is the causal effect of contemporaneous quality (or velocity) on next-period velocity (or quality), conditional on $D_{it}$. The DAG should show the dashed feedback arrow ($\text{Quality}_t \to \text{Velocity}_{t+1}$) and the lagged-instrument structure that identifies it.

### Critical Argument

Unlike the pinning study, identification here is *not* by construction (no counterfactual simulation produces $Y_{it}(0)$ for treated units). The DiD design imputes $Y_{it}(0)$ from a model fit on the untreated sample. The credibility of the estimate depends on the plausibility of parallel trends, the quality of the matching on pre-adoption dynamics, and the appropriateness of the Borusyak imputation estimator under treatment-effect heterogeneity. The DAG should make each of these dependencies visible.

For the GMM estimand, identification rests on the validity of lagged outcomes as instruments for contemporaneous regressors, which requires the absence of higher-order autocorrelation in the residuals (assessed via the Arellano-Bond AR(2) test) and joint exogeneity of the instrument set (assessed via the Hansen J test).

### Deliverable

A multi-panel DAG figure (`figs-cursor/dag-cursor.pdf`) showing:
- Panel (a): The DiD identification structure — back-door paths blocked by $\mu_i$, $\lambda_t$, $Z_{it}$, and matching.
- Panel (b): The GMM identification structure — the velocity $\leftrightarrow$ quality feedback loop and the lagged-instrument set.

TikZ recommended for consistency with the pinning DAG style.

---

## Step 2 — Causal Estimands and Identifying Assumptions

**Goal:** Define both estimands precisely. For each identifying assumption, state explicitly whether it is satisfied by the design's construction or requires empirical argument.

### DiD Estimands

For each outcome metric $M$, let $Y_{it}(d)$ denote the value of $M$ for repository $i$ in month $t$ under adoption status $d$. With $E_i$ denoting the adoption month (and $E_i = \infty$ for never-adopters), the study targets:

- **Average Treatment Effect on the Treated (ATT):** $\tau_{\text{ATT}} = E[Y_{it}(1) - Y_{it}(0) \mid \text{adopter}, t \geq E_i]$
- **Event-time CATT:** $\tau_{\text{ATT}}(h) = E[Y_{it}(1) - Y_{it}(0) \mid \text{adopter}, t = E_i + h]$ for $h \geq 0$, traced by the Borusyak imputation estimator.

### DiD Identifying Assumptions

**A1. Parallel trends.** *Requires empirical argument.* In the absence of treatment, the average trajectory of treated and matched-control repositories would have evolved in parallel. Untestable in the post-adoption period; pre-trend tests provide a placebo check on the pre-period; matching on six-month pre-adoption dynamics strengthens the plausibility of the assumption but does not prove it. Discussed in Step 3.

**A2. No anticipation.** *Partially satisfied by construction, partially requires empirical argument.* The Borusyak estimator drops $h = -1$ from the pre-trend specification, mechanically isolating the test from short-horizon anticipation. Anticipatory experimentation earlier than $h = -1$ cannot be ruled out by the design and must be argued empirically.

**A3. SUTVA / no interference.** *Requires empirical argument.* Most repositories are independent code bases without shared maintainers; ecosystem-level spillovers are partially absorbed by month fixed effects. Borderline cases (shared maintainers across repositories, organisation-level rollouts) are discussed in Step 3.

**A4. Stable treatment definition.** *Requires acknowledgment that the estimand is an averaged effect.* Adoption is heterogeneous in practice (different LLM backends, different versions, different engagement intensities). The estimate is best read as the ATT of "deliberate, visible adoption of Cursor as a development practice," averaged over realised heterogeneity. Generalisation to specific adoption intensities is an external validity concern handled in the existing Limitations subsection.

**A5. Treatment-effect heterogeneity correctly handled by the estimator.** *Satisfied by construction (subject to A1).* The Borusyak imputation estimator avoids the forbidden-comparison bias that would plague a TWFE estimator under heterogeneous, time-varying ATTs. The appendix already presents TWFE and Callaway-Sant'Anna as cross-checks; their consistency with the main results corroborates the appropriateness of the estimator.

### GMM Estimand and Assumptions

The GMM estimand is the contemporaneous causal effect of a quality (or velocity) variable on the next period's velocity (or quality), conditional on Cursor adoption status, repository identity, and calendar time. The reported estimator is panel system-GMM with lagged outcomes and lagged regressors as instruments.

**B1. Sequential exogeneity.** *Requires empirical argument.* Shocks to the outcome are uncorrelated with the history of regressors and the unobserved repository effect. This permits using lagged values as instruments; it fails if persistent unobserved shocks affect both the regressor and subsequent outcomes.

**B2. No serial correlation in residuals beyond AR(1).** *Tested by the Arellano-Bond AR(2) test.* If AR(2) is rejected, deeper lags must be used as instruments, with corresponding loss of efficiency.

**B3. Joint instrument validity.** *Tested by the Hansen J overidentification test.* Failure to reject is necessary but not sufficient; the test has known low power in finite samples and can be weakened by instrument proliferation. Mitigation: collapse the instrument matrix and limit lag depth.

**B4. Direction-of-causation justification.** *Satisfied by argument.* The temporal ordering encoded in the regression must be motivated by the DAG. The chapter tests both directions (quality $\to$ velocity and velocity $\to$ quality) to triangulate.

### What This Yields

The DiD identifies the *reduced-form* effect of Cursor adoption on each outcome separately. The GMM identifies the *mechanism* connecting outcomes — specifically, whether technical debt accumulation causally reduces future velocity, which the DiD alone cannot establish. The combination is what licenses the chapter's headline interpretation that initial velocity gains dissipate *because* they leave behind technical debt that throttles subsequent velocity, rather than for some other reason.

---

## Step 3 — Limitations and Known Caveats

**Goal:** Identify the residual threats to the *causal credibility* of the DiD and GMM estimates after the design's controls. Limitations that concern external validity, measurement validity, or treatment generalizability are not threats to causal identification and are covered in the existing "Limitations and Threats to Validity" subsection (Section~\ref{sec:cursor-limitations}); this section briefly notes them and refers the reader there.

### Causal Credibility Limitations (DiD)

| Limitation | Assumption Threatened | Direction of Bias | Analysis |
|---|---|---|---|
| Parallel trends untestable in the post-period | A1 | Direction depends on the unobserved confounder | Pre-trend tests pass for all outcomes at the 0.05 level; matching on six-month pre-adoption dynamics is the primary mitigation. Cohort-level pre-trend plots in the appendix should be inspected for systematic deviations. The assumption remains the principal load-bearing condition for the DiD estimate. |
| Anticipation effects (use before configuration commit) | A2 | Likely attenuates the immediate post-adoption ATT | Dropping $h = -1$ from the pre-trend test partially mitigates by removing the period most likely to contain anticipatory effects; remaining anticipatory use earlier than $h = -1$ cannot be ruled out from configuration-file evidence alone. |
| Shared maintainers and organisation-level rollouts | A3 | Direction unclear | Repositories with overlapping contributors may export practices across the unit boundary, partially violating no-interference. The magnitude is bounded by the small share of repositories with cross-repository contributor overlap. |
| Time-varying unobservable confounders coincident with adoption | A1 | Direction depends on the confounder | A developer joining a project who simultaneously brings Cursor and a different coding style cannot be separated from the treatment effect by any observational design. This is the core untestable assumption of DiD; the matching-plus-fixed-effects-plus-pre-trend triple is the strongest defence available without an experimental design. |

### Causal Credibility Limitations (GMM)

| Limitation | Assumption Threatened | Direction of Bias | Analysis |
|---|---|---|---|
| Sequential exogeneity violated by persistent unobserved shocks | B1 | Direction depends on the shock | If shocks to outcomes persist across periods (e.g., a maintainer's prolonged unavailability), lagged outcomes are no longer valid instruments. The Arellano-Bond AR(2) test is the principal diagnostic. |
| AR(2) test rejected | B2 | Bias of unknown direction; instrument set must be revised | If AR(2) is rejected, the chapter should report deeper-lag instruments and the corresponding loss of efficiency; failing that, the GMM estimates do not admit a causal interpretation. |
| Instrument proliferation | B3 | Weak Hansen test power; possibly biased point estimates | Number of instruments grows with $T$ in standard system-GMM. Collapsing the instrument matrix and limiting lag depth is recommended; both should be reported alongside the main GMM results. |

### Limitations Outside the Scope of Causal Credibility

The following concerns are not threats to internal causal identification of the DiD or GMM estimates and are addressed in Section~\ref{sec:cursor-limitations} of the paper:

- Treatment observability via committed configuration files (treatment definition; ITT estimate vs. usage-based effects).
- Usage intensity heterogeneity within the treatment group (treatment generalizability).
- Contamination from other AI tools in both groups (treatment definition and external validity to a no-AI counterfactual).
- Quality measured via static analysis only, with cognitive complexity as the per-line proxy (measurement validity / construct validity).
- Programming-language coverage (external validity).
- Rapidly evolving treatment over the observation window (external validity / time-bounded scope).
- OSS-specific patterns of adoption and abandonment (external validity to enterprise rollouts).

---

## Step 4 — Alternative Explanations

**Goal:** Identify the most threatening alternative causal structures and explain whether the design rules them out, partially addresses them, or leaves them open. Frame respectfully — these are alternative causal hypotheses an expert reviewer would raise.

### Alternative 1 — The Transient Velocity Finding Is Driven by OSS Repository Mortality, Not by Cursor

A well-known property of OSS repositories is that activity decays rapidly — many repositories become inactive within months of any salient event. The "transient velocity" finding could partly be an artefact of this baseline decay, with the matched control group decaying along the same trajectory but the treated group experiencing an adoption-induced spike that simply returns to a decaying baseline.

**Why the design is defensible:** The DiD design explicitly differences treatment and control trajectories, so common decay should net out. The robustness checks restricting to repository-months with $\geq 1$ commit and $\geq 10$ commits show the velocity-then-decay pattern persists in the active sample, weakening this alternative. Pre-trend tests further verify that treated and control repositories were on parallel trajectories before adoption.

**What remains unaddressed:** The activity threshold is observable but adoption-induced abandonment of *projects* is not separable from adoption-induced abandonment of *Cursor specifically*. The chapter's interpretation favours the latter; the data cannot fully disambiguate.

### Alternative 2 — Selection on Unobserved Project Quality or Developer Skill

Repositories adopting Cursor are not a random sample of GitHub. They may be systematically different in unobserved ways — more experimental teams, less stringent code review, lower baseline quality, different lifecycle stage — that drive both the adoption decision and the post-adoption outcomes.

**Why the design addresses this:** Repository fixed effects $\mu_i$ absorb all time-invariant differences. Propensity score matching on dynamic six-month pre-adoption trajectories addresses time-varying selection on observable growth, activity, and contributor patterns (AUC 0.83–0.91). Pre-trend tests pass for all outcomes, indicating that observable differences in trajectories are absent before adoption.

**What remains unaddressed:** Time-varying *unobservable* confounders that change exactly at adoption (e.g., a developer joining the project who simultaneously brings Cursor and a different coding style) cannot be separated from the treatment effect by any observational design. This is the core untestable assumption of DiD.

### Alternative 3 — The Quality Degradation Is a Mechanical Consequence of Increased Code Volume

A reviewer could argue that static analysis warnings and complexity scale roughly with codebase size, so any treatment that increases lines added will mechanically increase warning counts and total complexity, without implying that the *per-line* quality of AI-generated code is worse.

**Why the design partially addresses this:** The panel GMM analysis decomposes the quality effect into a velocity-mediated component and a direct component. The finding that complexity increases *even after* controlling for velocity dynamics provides positive evidence of a per-line complexity effect, distinct from a volume effect. Static analysis warnings, by contrast, are largely explained by the velocity-mediated path, which the chapter discusses honestly as a proportional rather than per-line effect.

**What remains unaddressed:** The decomposition relies on the GMM identifying assumptions; if these fail, the per-line interpretation is weakened.

### Alternative 4 — The Pattern Reflects Novelty Effects in Developer Behaviour, Not Sustained Cursor Effects

A natural alternative is the "excitement-frustration-abandonment" cycle the chapter itself raises: developers adopt Cursor, experience initial productivity from novelty effects on amenable tasks, hit limitations on harder tasks, and partially or fully abandon the tool — without any *sustained* causal effect of Cursor on the project's trajectory.

**Why the design partially addresses this:** This alternative is internally consistent with the chapter's transient-velocity finding and is openly entertained in the Discussion. The robustness check restricting to repositories with continued `.cursorrules` modification shows that velocity gains *persist* in the sustained-usage subset, providing evidence that the transient pattern is at least partially driven by abandonment rather than by an inherent ceiling on Cursor's productivity benefit.

**What remains unaddressed:** Persistent quality degradation in the full ITT sample does not require sustained usage — code introduced during the adoption phase remains in the codebase and continues to register in static analysis warnings. The chapter's framing should make clear that the quality finding is robust to abandonment, while the velocity finding is partly *about* abandonment patterns.

### Alternative 5 — Contamination from Other AI Tools Is the True Driver

A subtle alternative is that the observed effects are not driven by Cursor itself but by the broader AI tooling ecosystem that Cursor adopters disproportionately participate in.

**Why the design addresses this:** The "Only Cursor" robustness subset, restricted to repositories with no observable use of other AI tools, replicates the main findings with amplified magnitudes. This argues against the alternative that other AI tools are the true driver.

**What remains unaddressed:** Detection of other AI tools relies on observable artefacts which may underestimate true usage. Estimates should therefore be read as the marginal effect of Cursor on top of the prevailing baseline of partly-observed AI usage.

---

## Open Questions Before Drafting

- [ ] **Literature review scope:** Conduct a literature review pass before drawing the DAG to populate the citations flagged in Step 1.
- [ ] **Figure consolidation:** Single multi-panel DAG figure for both DiD and GMM identification, or two separate figures alongside the existing `Theory.pdf` mechanism diagram?
- [ ] **GMM diagnostic placement:** Should AR(2) and Hansen J test results be added to the GMM results table as part of the credibility argument, if not already there?
