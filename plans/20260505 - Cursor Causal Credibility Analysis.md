# Causal Credibility Analysis — Cursor Chapter

**Status:** Draft plan, pending author review
**Target file:** `analysis-cursor.tex`
**Placement:** Between Results (Section 4, including Robustness Checks) and Discussion (Section 5)

---

## Tasks

- [x] Literature review to justify each DAG node (citations populated below; all keys verified to exist in `references-cursor.bib`)
- [ ] Draft a single TikZ DAG inline within `analysis-cursor.tex` (matching the `analysis-pinning.tex` style) that simultaneously visualises the DiD identification structure and the GMM feedback loop
- [ ] Write Step 1 — Causal Theory (single DAG, two identification problems on the same node set)
- [ ] Write Step 2 — Causal Estimands and Identifying Assumptions
- [ ] Write Step 3 — Limitations and Known Caveats (causal credibility threats only)
- [ ] Write Step 4 — Alternative Explanations (most candidates already addressed by existing robustness checks; cross-reference rather than re-litigate)
- [ ] Add `\input{analysis-cursor}` to `main-cursor.tex` before the Discussion section
- [ ] Cross-reference (rather than supersede) the existing `Limitations and Threats to Validity` (Section~\ref{sec:cursor-limitations}) and `Robustness Checks` (Section~\ref{sec:robustness}); external and measurement validity remain there
- [x] Figure-consolidation decision: a single new TikZ DAG inside the credibility section; `figs-cursor/Theory.pdf` (mechanism schematic) stays in the Discussion. The two figures answer different questions (identification vs.\ mechanism) and are not redundant.
- [x] GMM diagnostics (Sargan/AR(2)) decision: already reported in Table~\ref{tab:causal-paths}; the credibility section will reference them rather than reproduce them.

---

## Step 1 — Explicit Causal Theory

**Goal:** Make the assumed causal structure visible and auditable for both the DiD estimand (effect of Cursor adoption on velocity and quality) and the GMM estimand (dynamic feedback between velocity and quality). Each node and edge in the DAG must be justified from existing literature.

### Node Inventory with Literature Justifications

All citation keys below have been verified to exist in `references-cursor.bib`. Where the existing chapter already discusses a node empirically, the discussion is referenced rather than reproduced.

#### Treatment

**$D_{it}$ — Cursor adoption.** Operationalised as the first month a `.cursorrules` file or `.cursor/` directory appears on the default branch. The treatment definition is justified in the existing chapter (Section~\ref{sec:find-cursor-repo}); Cursor's documentation establishes that configuration files are the visible and durable adoption signal~\cite{cursor-rules}. The same identification approach has been used for adjacent agentic tools, e.g.\ `\citet{watanabe2025use}` for Claude Code.

#### Outcomes

**Velocity outcomes** — commits and lines added, logged. Both are standard panel productivity proxies in software engineering~\cite{DBLP:journals/ese/ScholtesMS16, DBLP:journals/ese/OliveiraFSCCG20, DBLP:journals/tse/Murphy-HillJSSP21} and form the velocity dimension of the SPACE framework~\cite{DBLP:journals/queue/ForsgrenSMZHB21}.

**Quality outcomes** — SonarQube static-analysis warnings, cognitive complexity, duplicate-line density, all logged. Each is a maintainability proxy with established usage in panel studies of software quality~\cite{DBLP:conf/sigsoft/ChengMCJGKZ022, besker2018technical}; complexity in particular is the closest available proxy for the technical-debt mechanism the chapter argues for.

#### Mediators

**Code production rate.** AI assistance increases the rate at which new code enters the repository; this is the consensus finding across small-scale RCTs~\cite{DBLP:journals/corr/abs-2302-06590}, large-scale field experiments~\cite{cui2024effects, DBLP:journals/corr/abs-2406-17910, hoffmann2024generative}, observational analyses of Copilot~\cite{DBLP:conf/icis/YeverechyahuMO24, DBLP:journals/corr/abs-2410-02091}, and ecosystem-level analysis~\cite{daniotti2025using}.

**Per-line cognitive complexity of generated code.** A separate channel: even at fixed velocity, AI-generated code may be inherently more complex than human-written code. Direct evidence is mixed but increasingly tilts toward higher complexity for ChatGPT-style and chat-assisted code~\cite{DBLP:journals/tse/LiuTLZZ24}; reviewer-side overhead of AI-generated multi-file diffs has been documented qualitatively~\cite{DBLP:conf/icse/Liang0M24}.

**Developer review effort per line.** AI-generated patches are larger and more diffuse than hand-written ones, raising per-line review cost and potentially lowering review rigor~\cite{DBLP:conf/icse/Liang0M24, DBLP:journals/corr/abs-2507-08149, DBLP:conf/ccs/PerryS0B23}. This channel mediates the path from velocity to quality (warnings and complexity).

#### Time-Invariant Confounders (Absorbed by Repository Fixed Effects $\mu_i$)

**Project type and domain.** Different domains use AI tools differently~\cite{DBLP:journals/corr/abs-2410-02091, daniotti2025using}, and domain shapes the structural baseline for warnings and complexity~\cite{DBLP:conf/sigsoft/ChengMCJGKZ022}.

**Primary programming language.** LLM performance varies systematically across languages~\cite{DBLP:journals/pacmpl/CassanoGLSFAF0J24, DBLP:journals/corr/abs-2503-17181}, which correlates with both adoption probability and outcome levels. Already enforced by exact same-language matching (Section~\ref{sec:matching}).

**Team composition and contributor expertise.** Heterogeneous treatment effects on developers of different skill levels are well documented for prior generations of AI tools~\cite{DBLP:journals/jss/DakhelMNKDJ23, DBLP:journals/corr/abs-2302-06590, cui2024effects}.

**Governance maturity and review practice.** Quality assurance processes shape both willingness to adopt new tools and the post-adoption quality trajectory~\cite{DBLP:conf/sigsoft/ChengMCJGKZ022, besker2018technical}.

**Pre-existing project lifecycle stage.** OSS projects exhibit characteristic activity decay regardless of any specific event~\cite{DBLP:journals/ese/KalliamvakouGBS16, DBLP:journals/corr/abs-2412-13459, DBLP:journals/ese/MunaiahKCN17}. Repositories that adopted Cursor may be at systematically different lifecycle stages from random non-adopters; the propensity-score model on six-month dynamics (Section~\ref{sec:matching}) addresses observable lifecycle differences.

#### Time-Varying Confounders (Absorbed by Month Fixed Effects $\lambda_t$ and Covariates $Z_{it}$)

**Frontier-model release cycle and ecosystem shocks.** The 2024–2025 study window spans Claude 3.5 Sonnet, GPT-4o, Claude 3.7 Sonnet, and GPT-5 releases, plus rapid evolution of Cursor itself; calendar-time variation in tool capability is a common shock that affects all repositories simultaneously and is absorbed by $\lambda_t$~\cite{DBLP:journals/corr/abs-2507-09089, kumar2025intuition}.

**General growth in AI-tool adoption.** AI-tool prevalence rose substantially during the window~\cite{stackoverflow-survey-ai, daniotti2025using}; this lifts the velocity baseline for the control group as well as the treatment group, so $\lambda_t$ differences this out.

**Repository scale dynamics.** Larger codebases mechanically accrue more warnings and complexity; $Z_{it}$ controls explicitly for lines of code, age, contributors, stars, and issues opened (Section~\ref{sec:covariates}).

#### Residual Threats (Not Absorbed by FE)

**Other AI-tool adoption that changes within the window.** Copilot, Claude Code, Windsurf, Cline, and OpenHands are all in active circulation during the study period~\cite{DBLP:journals/corr/abs-2507-09089, watanabe2025use, kumar2025intuition}. Project fixed effects absorb a control group that always uses (or never uses) Copilot; they do not absorb a control project that adopts Copilot mid-window. Section~\ref{sec:robustness} mitigates this with the *Cursor and Others* / *Only Cursor* split, but configuration-file-based detection underestimates real usage.

**Anticipation through pre-commit Cursor use.** Developers can experiment with Cursor locally for weeks before committing a `.cursorrules` file. The estimator drops $h=-1$, which absorbs one month of anticipation but not earlier experimentation~\cite{borusyak2024revisiting}.

**Time-varying unobservables coincident with adoption.** A new senior contributor joining a project who simultaneously brings Cursor and a different coding style cannot be separated from the treatment effect by any observational design~\cite{DBLP:journals/corr/abs-2410-02091}. This is the canonical residual threat to DiD parallel trends.

### Two Causal Sub-Theories on the Same DAG

The DAG should make visible *two* distinct identification problems on the same node set:

1. **Direct effect of $D$ on velocity and quality** — identified by the DiD design under parallel trends. Back-door paths run through repository-invariant characteristics (absorbed by $\mu_i$), calendar-time shocks (absorbed by $\lambda_t$), and observable scale dynamics (absorbed by $Z_{it}$); selection on observable pre-adoption trajectory is mitigated by propensity-score matching.
2. **Dynamic feedback between velocity and quality** — identified by panel GMM. The estimand is the causal effect of contemporaneous quality (or velocity) on next-period velocity (or quality), conditional on $D_{it}$. The DAG shows the feedback arrows $\text{Quality}_t \to \text{Velocity}_{t+1}$ and $\text{Velocity}_t \to \text{Quality}_t$, with lagged outcomes serving as instruments.

### Critical Argument

Unlike the pinning study, identification here is *not* by construction (no counterfactual simulation produces $Y_{it}(0)$ for treated units). The DiD design imputes $Y_{it}(0)$ from a model fit on the untreated sample. The credibility of the estimate therefore depends on the plausibility of parallel trends, the quality of the matching on pre-adoption dynamics, and the appropriateness of the Borusyak imputation estimator under treatment-effect heterogeneity. The DAG should make each of these dependencies visible.

For the GMM estimand, identification rests on the validity of lagged outcomes as instruments for contemporaneous regressors. The required diagnostics — Sargan/Hansen overidentification and Arellano-Bond AR(2) — are already reported in Table~\ref{tab:causal-paths}; the credibility section will reference those rows rather than reproduce them.

### Proposed DAG (TikZ draft, inline within `analysis-cursor.tex`)

The figure follows the same `confbox` / `tnode` / `mnode` / `gnode` / `ynode` / `rbox` style as Figure~\ref{fig:dag-pinning}. The DiD identification problem is shown by the gray confounder box, the green treatment node, the yellow mediators, the orange LoC moderator (mirroring graph size $G$ in the pinning DAG), and the blue outcome cluster. The GMM feedback structure is shown by two explicitly directed dashed arrows: a contemporaneous $V_t \to Q_t$ arrow and a lagged $Q_t \to V_{t+1}$ arrow into a separate $V_{t+1}$ node. The two-arrow form is more faithful to the GMM specification than a single bidirectional arrow; the visual balance can be reviewed against the rendered PDF.

```latex
\begin{figure}[t]
    \centering
    \begin{tikzpicture}[
        >=latex, font=\scriptsize,
        confbox/.style={draw, rounded corners, fill=gray!12, align=left, text width=4.6cm, inner sep=4pt},
        tnode/.style={draw, rounded corners, fill=green!20, very thick, minimum height=0.7cm, minimum width=2.6cm, align=center, font=\bfseries\scriptsize},
        mnode/.style={draw, rounded corners, fill=yellow!25, minimum height=0.6cm, minimum width=2.6cm, align=center, font=\scriptsize},
        gnode/.style={draw, rounded corners, fill=orange!15, minimum height=0.55cm, minimum width=2.4cm, align=center, font=\scriptsize},
        ynode/.style={draw, rounded corners, fill=blue!10, minimum height=0.5cm, minimum width=2.6cm, align=center, inner sep=2pt},
        ynodeQ/.style={draw, rounded corners, fill=blue!18, minimum height=0.5cm, minimum width=2.6cm, align=center, inner sep=2pt},
        ynodeF/.style={draw, rounded corners, dashed, fill=blue!10, minimum height=0.5cm, minimum width=2.6cm, align=center, inner sep=2pt},
        rbox/.style={draw, rounded corners, dashed, fill=red!8, align=left, text width=4.6cm, inner sep=4pt},
        cedge/.style={->, gray, dashed, semithick},
        medge/.style={->, black, semithick},
        gmmedge/.style={->, blue!55!black, dashed, thick},
    ]
    % --- Confounders absorbed by FE / matching / covariates ---
    \node[confbox] (Conf) {%
        \textbf{Absorbed by $\mu_i$, $\lambda_t$, $Z_{it}$, matching}\\[1pt]
        $\bullet$ Project type, domain, language\\
        $\bullet$ Team composition, expertise\\
        $\bullet$ Governance and review practice\\
        $\bullet$ Repo lifecycle stage (matched on)\\
        $\bullet$ Frontier-model release cycle\\
        $\bullet$ General AI-tool prevalence\\
        $\bullet$ Repo age, stars, contributors, \dots
    };
    % --- Treatment ---
    \node[tnode, right=2.0cm of Conf] (D) {Treatment $D_{it}$\\ Cursor adoption};
    % --- Mediators ---
    \node[mnode, below=0.9cm of D] (Mprod) {Code production rate};
    \node[mnode, below=0.3cm of Mprod] (Mcompl) {Per-line complexity};
    % --- Velocity outcomes (top right) ---
    \node[ynode, right=2.0cm of D] (V1) {$Y_1$: commits$_{it}$};
    \node[ynode, below=4pt of V1] (V2) {$Y_2$: lines added$_{it}$};
    % --- LoC moderator (between V and Q clusters) ---
    \node[gnode, below=0.6cm of V2] (LoC) {Lines of code$_{it}$\\(cumulative)};
    % --- Quality outcomes (below LoC) ---
    \node[ynodeQ, below=0.6cm of LoC] (Q1) {$Y_3$: SonarQube warnings$_{it}$};
    \node[ynodeQ, below=4pt of Q1] (Q2) {$Y_4$: cognitive complexity$_{it}$};
    \node[ynodeQ, below=4pt of Q2] (Q3) {$Y_5$: dup.\ line density$_{it}$};
    % --- Lagged velocity outcome for GMM Q -> V_{t+1} ---
    \node[ynodeF, right=0.9cm of Q2] (Vnext) {$Y_2$: lines added$_{i,t+1}$};
    % --- Residual threats ---
    \node[rbox, below=0.9cm of Mcompl] (Resid) {%
        \textbf{Residual threats (not absorbed)}\\[1pt]
        $\bullet$ Time-varying other-AI-tool adoption\\
        $\bullet$ Anticipation pre-$h{=}{-}1$ experimentation\\
        $\bullet$ Time-varying unobservables coincident\\
        \quad with adoption (e.g., new contributor)
    };
    % --- DiD edges ---
    \draw[cedge] (Conf.east) -- (D.west) node[midway, above, font=\tiny\itshape] {(blocked by FE/matching)};
    \draw[medge] (D.south) -- (Mprod.north);
    \draw[medge] (Mprod.east) to[bend left=5] (V1.west);
    \draw[medge] (Mprod.east) to[bend left=2] (V2.west);
    \draw[medge] (Mcompl.east) to[bend right=8] (Q2.west);
    % Volume-mediated path: V2 -> LoC -> Q1, Q2, Q3
    \draw[medge] (V2.south) -- (LoC.north);
    \draw[medge] (LoC.south) -- (Q1.north);
    \draw[medge] (LoC.south west) to[bend right=10] (Q2.west);
    \draw[medge] (LoC.south east) to[bend left=10] (Q3.east);
    % Residual threats touch the outcomes directly
    \draw[cedge] (Resid.east) to[bend right=5] (Q1.west);
    \draw[cedge] (Resid.east) to[bend right=10] (Q2.west);
    % --- GMM arrows (two explicitly directed) ---
    \draw[gmmedge] (V2.east) to[bend left=40] node[right, font=\tiny\itshape] {GMM contemp.\ $L_t{\to}C_t$} (Q2.east);
    \draw[gmmedge] (Q2.east) to[bend right=15] node[below, font=\tiny\itshape] {GMM lag $C_t{\to}L_{t+1}$} (Vnext.west);
    \end{tikzpicture}
    \caption{Causal DAG for the effect of Cursor adoption on five velocity and quality outcomes.
    Repository-invariant characteristics, calendar-time shocks, and observable scale dynamics (gray box) are absorbed by repository fixed effects $\mu_i$, month fixed effects $\lambda_t$, and time-varying covariates $Z_{it}$; selection on observable six-month pre-adoption trajectory is mitigated by propensity-score matching (Section~\ref{sec:matching}).
    Cumulative codebase size (lines of code, orange) is promoted to an explicit moderator: the chapter's GMM analysis (Section~\ref{sec:finding-interaction}, Table~\ref{tab:causal-paths}) shows that the volume-mediated path $V_t \to \mathrm{LoC}_t \to Q_t$ absorbs most of the warnings effect and a large share of the complexity effect, while a direct $D \to$ per-line-complexity $\to C_t$ path remains after this control.
    The DiD estimand identifies the marginal effect of $D$ on each outcome through these paths.
    The GMM estimand identifies two further causal arrows beyond DiD's reach (dashed blue): the contemporaneous within-period feedback $L_t \to C_t$ and the lagged feedback $C_t \to L_{t+1}$ from quality back to next-period velocity. The required Sargan and AR(2) diagnostics are already reported in Table~\ref{tab:causal-paths}.
    Three residual threats remain after FE and matching: time-varying other-AI-tool adoption, anticipatory pre-commit experimentation earlier than $h{=}{-}1$, and time-varying unobservables coincident with adoption.
    The principal load-bearing assumptions are A1 (parallel trends) for the DiD estimand and B1 (sequential exogeneity) for the GMM estimand.}
    \label{fig:dag-cursor}
\end{figure}
```

Layout decisions made (per author direction):
- **GMM rendered as two explicitly directed dashed arrows**: $L_t \to C_t$ (contemporaneous) and $C_t \to L_{t+1}$ (lagged), with a separate dashed-border `lines added$_{i,t+1}$` node on the right. Visual balance to be reviewed against the rendered PDF and adjusted if the right-hand cluster looks crowded.
- **LoC promoted to an explicit `gnode` moderator** between the velocity column and the quality column, mirroring how Figure~\ref{fig:dag-pinning} foregrounds graph size $G$. This makes the chapter's main GMM finding visible at a glance: the volume-mediated $V \to \mathrm{LoC} \to Q$ path captures most of the warnings effect, while the direct $D \to$ per-line-complexity $\to C$ path is what survives the LoC control and yields the +9% Cursor coefficient on complexity in Table~\ref{tab:causal-paths}.

For tractability, the figure draws the GMM arrows only on the complexity outcome ($C$), since complexity is the GMM finding that survives controls and motivates the chapter's headline interpretation; the warnings ($W$) GMM arrows are mentioned in the caption rather than drawn, to avoid visual clutter. If the author prefers the four-arrow variant ($L_t \to W_t$, $L_t \to C_t$, $W_t \to L_{t+1}$, $C_t \to L_{t+1}$), the additional arrows are easy to add at the cost of density.

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

The existing Cursor chapter already engages with several reviewer-grade alternatives through dedicated robustness checks (Section~\ref{sec:robustness}, Figure~\ref{fig:robustness-checks}, Figure~\ref{fig:robustness-checks-all}) and the Discussion (Section~\ref{sec:cursor-discussion}). The credibility section therefore *cross-references* those passages rather than re-litigating them, and adds two further alternatives that the existing chapter does not explicitly canvass.

### Alternatives Already Addressed in the Existing Chapter

For each of the following, the credibility section will name the alternative and pointer to the existing analysis in one or two sentences. Authoring as a numbered table:

| # | Alternative | Already addressed by | Status |
|---|---|---|---|
| 1 | The transient velocity finding is an artefact of OSS repository mortality | Active-Months ($>0$ commits) and Very-Active ($\geq 10$ commits) subset robustness checks (Section~\ref{sec:robustness}, Figure~\ref{fig:robustness-checks-all} Row 2) | Addressed; transient pattern persists in active sample. |
| 2 | The pattern reflects an excitement–frustration–abandonment cycle, not a sustained Cursor effect | High Contributor Adoption / Cursor Configuration Changes subsets (Section~\ref{sec:robustness}, Figure~\ref{fig:robustness-checks-all} Row 1); explicit treatment in Section~\ref{sec:cursor-discussion} | Addressed; velocity gain *persists* under sustained usage, while the abandonment dynamic explains the transient pattern in the full ITT sample. |
| 3 | The quality degradation is a mechanical consequence of increased code volume rather than a per-line effect | Dynamic panel GMM with explicit lines-of-code control (Section~\ref{sec:finding-interaction}, Table~\ref{tab:causal-paths}); Discussion paragraph 5.1.2 distinguishing proportional warnings from per-line complexity | Addressed; complexity increases survive controls for velocity and codebase size, supporting a per-line interpretation. The decomposition still rests on the GMM identifying assumptions named in B1–B3. |
| 4 | Contamination from other AI tools (Copilot, Claude Code, Windsurf, Cline, OpenHands) is the true driver | *Cursor and Other* / *Only Cursor* subset robustness checks (Section~\ref{sec:robustness}, Figure~\ref{fig:robustness-checks-all} Row 3) | Addressed; main findings amplify in the *Only Cursor* subset. The subset construction is conservative — it relies on observable detection signatures that may understate true other-AI usage, leaving a residual threat already noted in Section~\ref{sec:cursor-limitations}. |
| 5 | The findings are driven by particular programming languages or cohort-specific effects | Per-language robustness panels (Section~\ref{sec:robustness}, Figure~\ref{fig:robustness-checks-all} Row 4); cross-estimator comparison with Callaway–Sant'Anna and TWFE (Section~\ref{sec:appendix-alternative-estimators}) | Addressed for languages; partially addressed for cohorts (the Callaway–Sant'Anna estimator diverges on quality outcomes, and the chapter discusses why honestly in Section~\ref{sec:estimator-comp}). |

### Remaining Alternatives Not Yet Canvassed

Two further alternatives are worth raising explicitly in the credibility section because they target identification specifically and are not already absorbed by the existing robustness-check argument.

**Alternative 6 — Selection on time-varying unobservables coincident with adoption.**
A senior contributor or an organisational shift that simultaneously brings Cursor *and* a more aggressive coding style cannot be separated from the treatment effect by any observational design. Repository fixed effects absorb all time-invariant project characteristics, and the propensity-score model on six-month pre-adoption dynamics absorbs observable trajectories, but neither absorbs an unobserved shock occurring exactly at the adoption month. *This is the canonical residual threat to A1 (parallel trends), is irreducible without an experimental design, and should be named as the principal load-bearing assumption rather than glossed over.* Direction of bias depends on the confounder; the most plausible scenario (a "modernisation push" that bundles tool adoption with pace acceleration) would reinforce the velocity-up / quality-down pattern, so the central finding is robust in sign but possibly inflated in magnitude.

**Alternative 7 — SonarQube warning increases reflect a measurement-side change in coding style rather than a quality decline.**
LLM-generated code may trigger SonarQube rules that human-written code triggers less often (e.g., naming-convention violations, leftover scaffolding, or verbose patterns) without a corresponding change in *defect proneness*. Under this reading, the warnings outcome would shift mechanically with style rather than quality. The existing appendix (Section~\ref{tab:warnings-by-category}) breaks down the increase by warning category and shows that the largest contributors are Naming Conventions, Code Hygiene, Code Complexity, and Code Style — categories consistent with both the per-line-quality-decline interpretation *and* with this style-shift interpretation. *The two readings cannot be fully disambiguated by static analysis alone.* This alternative is properly framed as a measurement-validity concern (already noted in Section~\ref{sec:cursor-limitations} under the construct-validity discussion) rather than as an internal-validity threat to the DiD estimate, but the credibility section should mention it briefly so the reader can locate the boundary between identification and measurement.

---

## Open Questions Before Drafting

- [x] **Literature review scope:** Completed in Step 1; all citation keys verified against `references-cursor.bib`.
- [x] **Figure consolidation:** A single combined TikZ DAG drawn inline within the credibility section, showing the DiD identification structure and the GMM feedback loop on the same node set. The existing `figs-cursor/Theory.pdf` (mechanism schematic) stays in the Discussion — the two figures answer different questions.
- [x] **GMM diagnostic placement:** Sargan and AR(2) diagnostics are already reported in Table~\ref{tab:causal-paths}; the credibility section will cite that table rather than reproduce the results.

### Remaining for Author Review

- [x] GMM feedback rendered as two explicitly directed arrows ($L_t \to C_t$ and $C_t \to L_{t+1}$); visual effect to be reviewed against the rendered PDF.
- [x] Lines of code promoted to an explicit `gnode` moderator between the velocity and quality columns, mirroring how Figure~\ref{fig:dag-pinning} foregrounds graph size $G$.
- [ ] After the figure renders, decide whether to add the two warnings-side GMM arrows ($L_t \to W_t$ and $W_t \to L_{t+1}$) for completeness, or keep the figure focused on the complexity-side feedback that survives the LoC control.
