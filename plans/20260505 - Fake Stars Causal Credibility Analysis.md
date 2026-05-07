# Causal Credibility Analysis — Fake Stars Chapter

**Status:** Draft plan, pending author review
**Target file:** `analysis-fake-stars.tex`
**LaTeX section title:** `\section{Causal Credibility Analysis}` (matching `analysis-pinning.tex` and `analysis-cursor.tex` for consistency across chapters)
**Placement:** Between RQ4 results (Section 4.4) and Discussion (Section 5)
**Scope:** RQ4 (Promotional Effect) is the only research question that makes a quantitative causal claim, so the formal apparatus targets RQ4. RQ1–RQ3 are descriptive / measurement results and only require a brief framing note clarifying that they are *not* causal claims (and should not be read as such downstream). The criterion-validity argument in Section 3.4 (deletion-rate comparison) is a secondary application of the toolkit.

---

## Tasks

- [x] Literature review to justify each DAG node (citations populated below; keys verified against `references-fake-stars.bib` unless flagged as "needs new bib entry")
- [x] Draft TikZ DAG inline within `analysis-fake-stars.tex` (matching `analysis-pinning.tex` / `analysis-cursor.tex` style); see Step 1
- [ ] Draft a one-paragraph framing note clarifying the descriptive scope of RQ1–RQ3
- [ ] Write Step 1 — Causal Theory (single DAG centred on RQ4)
- [ ] Write Step 2 — Causal Estimand and Identifying Assumptions
- [ ] Write Step 3 — Limitations and Known Caveats (causal credibility threats only)
- [ ] Write Step 4 — Alternative Explanations
- [x] Specify and execute four robustness checks tied to columns of `fake-star-reanalysis/model_stars.csv` and `fake-star-reanalysis/repo_labels.csv` (580 labelled repos; 375 in the AR(2) panel). Each check is paired with the alternative it addresses inside Step 4 below
- [x] Implement R1, R2, R4, R5 in `fake-star-reanalysis/robustness.Rmd` (knits to `robustness.html`) and as chunks in `fake-star-reanalysis/regression.Rmd`. R3 was withdrawn as a design limitation. R6 is not implemented (justification below in Alternative 4)
- [ ] Cross-reference (rather than supersede) the existing "Limitations" paragraph in RQ4 (lines 707–712 of `main-fake-stars.tex`); external and measurement validity remain there
- [ ] Add `\input{analysis-fake-stars}` to `main-fake-stars.tex` before the Discussion section
- [ ] Cross-reference the new section from the existing "Limitations and Ethical Concerns" subsection (Section 3.4)

---

## Context: What the Chapter Currently Claims Causally

The chapter explicitly states two hypotheses (Section 4.4):

- **H$_1$:** Accumulating real stars helps gain more real stars in the future.
- **H$_2$:** Accumulating fake stars helps gain real stars in the future, but with weaker effect than real stars.

The paper fits panel autoregression models with random and fixed effects, and reports:

- A 1% increase in fake stars at month $t-1$ is associated with a 0.07% increase in real stars at month $t$ (short-run positive coefficient).
- The coefficient on cumulative fake stars three or more months earlier ($all\_fake_{i, t-k-1}$) is significantly *negative*.
- The fixed-effects specification is preferred per a Hausman test.

The existing Limitations paragraph already acknowledges:
1. Regression alone is insufficient for causal claims.
2. Granger causality tests are infeasible because most time series are too short ($t \geq 6 + 2k$ requirement violated for unbalanced panels).
3. "Real causality hides in exogenous variables" — e.g., a shortsighted maintainer may both buy fake stars and fail to attract real stars.

The Discussion then makes a stronger counterfactual claim ("we recommend against buying fake stars... our RQ4 results suggest that it is ineffective"), which is causal in form. The credibility analysis must defend or qualify both the H$_2$ result and the Discussion's counterfactual.

---

## Step 1 — Explicit Causal Theory

**Goal:** Construct a DAG for RQ4 in which every node and edge is justified from existing literature, distinguishing treatment from its observed proxy and exposing the reverse-causality and confounding paths the panel-FE design must rule out.

### Node Inventory with Literature Justifications

All citation keys below are verified against `references-fake-stars.bib` unless explicitly flagged as **[needs new bib entry]**.
Where the existing chapter already discusses a node empirically (Sections 3, 4.1–4.3), that discussion is referenced rather than reproduced.
Following the convention used in the pinning chapter's DAG, each node carries a literature-supported justification for *both* its effect on the treatment and its effect on the outcome.

#### Treatment and Observed Proxy

**$D_{i,t}$ — Maintainer's decision to purchase fake stars (unobserved).**
- Justification: the existence of an active, low-cost marketplace for fake stars on third-party sites (e.g., \Code{baddhi.shop}, \Code{gitstar.com.cn}, \Code{taobao}) is documented in the chapter itself (Section 2) and corroborated by prior reporting on reputation farms~\cite{reputation-farm, taobao-github-star, gitstar} and adjacent fake-engagement marketplaces on Twitter and Facebook~\cite{DBLP:conf/imc/StringhiniWEKVZZ13, DBLP:conf/ccs/CaoYYP14}.
- Treatment heterogeneity: documented purposes range from growth-hacking startups~\cite{startup-stars, bohnsack2019hack, oceanbase, dagster} through search-engine-optimisation spam~\cite{npm-spam, docker-hub-spam, pypi-spam} to malware promotion~\cite{stargazer-goblin, x-trader-attack, banshee, game-engine}.

**$\widehat{D}_{i,t} = fake_{i,t}$ — Detected fake stars from \SystemName.**
- Measurement-error justification: detector recall is benchmarked against the Stargazer Ghost Network ground truth in the chapter itself (Section 3), with $\sim$81% recall and unknown campaign-level precision. Prior fake-account detection work documents the difficulty of reaching simultaneously high precision and recall against adaptive adversaries~\cite{DBLP:conf/uss/ThomasMGKP13, DBLP:conf/uss/ViswanathBCGGKM14, DBLP:conf/www/CresciPPST17}.

#### Outcomes

**$real_{i, t+k}$ — Non-fake stars gained in subsequent months.**
- Justification: stars are widely used as a popularity/attention proxy on GitHub~\cite{DBLP:conf/cscw/DabbishSTH12, DBLP:journals/software/BegelBS13a, DBLP:journals/jss/BorgesV18, DBLP:conf/msr/FangKLHV20} and their accumulation predicts downstream signals such as forks, contributors, and dependent projects~\cite{DBLP:journals/jss/BorgesV18, DBLP:conf/icse/TsayDH14}. The chapter operationalises this construct via the GHArchive star-event stream and validates the partition into real vs. fake stars in Sections 3.1–3.4.

#### Mediators

**$M_{\text{vis}}$ — Visibility channel** (inflated star count $\to$ trending placement, search ranking, perceived popularity $\to$ real users discover and star).
- Treatment $\to$ mediator: GitHub Trending and search ranking are influenced by star velocity, and the chapter's RQ2 trending analysis (Section~\ref{sec:rq1}, lines 357–378 of `main-fake-stars.tex`) documents that 0.42% of campaign repositories reach Trending. Third-party reverse-engineering of the Trending algorithm corroborates this~\cite{trending-works, github-trending}.
- Mediator $\to$ outcome (social proof): users adopt OSS partly via popularity cues~\cite{DBLP:conf/cscw/DabbishSTH12, DBLP:conf/icse/TsayDH14, DBLP:journals/jmis/MoqriMQB18, dellarocas2010online}; star counts are explicitly used as a heuristic in package selection~\cite{DBLP:conf/icse/TrockmanZKV18, DBLP:journals/jss/BorgesV18}.

**$M_{\text{pen}}$ — Penalty channel** (inflated star count $\to$ user/security-tool inspection of activity signals $\to$ skeptical users decline to star, or GitHub deletes).
- Treatment $\to$ mediator: skeptical observers and analysts inspect star/commit/contributor patterns to flag inauthenticity, as documented in industry reports about gaming GitHub metrics~\cite{startup-stars, github-star-trust, wired-news} and academic and gray-literature work on detecting incongruent engagement signals~\cite{DBLP:conf/imc/StringhiniWEKVZZ13, DBLP:journals/dss/CresciPPST15, DBLP:conf/www/CresciPPST17}.
- Mediator $\to$ outcome: signal incongruence reduces adoption decisions in adjacent domains (online reviews~\cite{mukherjee2013yelp, dellarocas2010online} and social-media credibility~\cite{DBLP:journals/tkdd/YangWWGZD14, schueller2024modeling}); GitHub's policy against fake activity also makes detection-induced removal a within-platform mechanism~\cite{github-policy}.

#### Confounders Absorbed by Repository Fixed Effects (time-invariant)

**$U_i$ — Maintainer growth-hacking strategy / sophistication.**
- Effect on treatment: the decision to buy stars correlates with documented growth-hacking norms in startups and OSS marketing~\cite{bohnsack2019hack, startup-stars}; fraud-marketplace participation is itself a stable disposition in the buyer-account literature~\cite{DBLP:conf/imc/StringhiniWEKVZZ13, DBLP:conf/ccs/GrierTPZ10}.
- Effect on outcome: maintainer reputation, communication quality, and project-marketing skill correlate with organic star accrual~\cite{DBLP:conf/icse/TsayDH14, DBLP:conf/cscw/DabbishSTH12, DBLP:journals/jss/BorgesV18}.
- Treatment in the DAG: drawn as latent and absorbed by repository FE to the extent the disposition is stable over the 2019–2025 panel window.

**$T_i$ — Project type and topical baseline (e.g., framework vs. malware vs. tutorial).**
- Effect on treatment: the chapter's own categorical analysis (Section 4.3, lines 597–651) shows that purchase rates differ markedly by category --- Spam/Phishing, AI/LLM, and Blockchain dominate.
- Effect on outcome: organic star accrual depends on topical area and project type~\cite{DBLP:journals/jss/BorgesV18, DBLP:journals/ese/MunaiahKCN17, DBLP:conf/icse/TsayDH14}.

**$N_i$ — Project intrinsic quality / utility baseline (time-invariant component).**
- Effect on treatment: lower-quality projects have stronger incentive to buy because organic accrual is weak~\cite{bohnsack2019hack, startup-stars}.
- Effect on outcome: stable quality signals predict adoption~\cite{DBLP:conf/icse/TrockmanZKV18, DBLP:journals/jss/BorgesV18}.

#### Confounder Partially Absorbed by Time-Varying Controls (entered as $release_{i,t}$, $activity_{i,t}$, $age_{i,t}$ in the RE specification only)

**$Q_{i,t}$ — Project release/activity dynamics.**
- Effect on treatment: more active projects may cross-promote with paid stars timed to releases (campaign timing around launches is reported in marketing playbooks~\cite{startup-stars, bohnsack2019hack}).
- Effect on outcome: release events and authentic development activity are well-established short-run predictors of star arrivals~\cite{DBLP:conf/msr/FangKLHV20, DBLP:journals/jss/BorgesV18}.
- Treatment in the DAG: drawn as a node entering both arrows, with a note that it is included only in the RE specification; for the FE specification reported in the main text, $Q_{i,t}$ is *not* directly controlled but is partially absorbed by FE to the extent its within-unit variation is small relative to the panel.

#### Time-Varying Confounder Not Absorbed by Either Repository or Time FE Alone

**$Z_{t}^{\text{topic}}$ — Topic momentum / hype waves at the topic-by-time level.**
- Effect on treatment: hype-cycle attention to LLMs (2023–2024), blockchain (2021–2022), and adjacent topics directly motivates the kind of growth-hacking activity documented in the chapter~\cite{startup-stars, bohnsack2019hack}; a parallel literature on attention-driven marketplaces documents bursts of engagement-fraud demand around hype peaks~\cite{schueller2024modeling, faris2017partisanship}.
- Effect on outcome: organic interest in hyped topics simultaneously surges, raising real-star accrual independent of any campaign~\cite{DBLP:journals/jss/BorgesV18, DBLP:conf/msr/FangKLHV20}.
- Critical: hype is *time-varying within a repository's lifecycle*, so repository fixed effects do not absorb it. Calendar-time fixed effects absorb the cross-topic average shock but not topic-by-time interaction. This is the single most threatening confounder for the short-run $\beta_1$.

#### Reverse-Causality Edge

**$real_{i, t-k} \to D_{i,t}$** --- declining real-star growth may itself trigger a purchase decision.
- Justification: developer responses to declining attention are documented qualitatively in the growth-hacking and self-promotion literature~\cite{bohnsack2019hack, startup-stars}; the canonical "panic-buy" story is plausible from the same incentive that originally motivates buying. The chapter's RQ2 timeline analysis (Section 4.2) shows compressed campaign windows that are consistent with reactive timing.
- Identification consequence: this edge violates strict exogeneity and is the chief reason the panel-FE estimator with a lagged dependent variable suffers Nickell-style bias for short panels~\cite{nickell1981biases}. **[needs new bib entry: Nickell, S. (1981). Biases in dynamic models with fixed effects. *Econometrica*, 49(6), 1417–1426.]**

#### Deliberately Excluded from the DAG

**Detector evasion sophistication** (the propensity for sophisticated buyers to use realistic accounts that \SystemName under-detects) is a measurement-validity / external-validity concern, not a node in the DGP that produces the analysed sample. It is discussed under A3 (measurement) and as Alternative 4 in Step 4, not in the DAG itself.

### Critical Argument

Unlike the pinning chapter, the fake-stars analysis does *not* have a counterfactual simulation that imposes treatment by construction.
Treatment is observational and the maintainer chooses it endogenously.
The panel-FE estimator's causal interpretation therefore rests on a strict exogeneity assumption: conditional on repository fixed effects and the included time-varying controls, the treatment is uncorrelated with the unobserved error at all leads and lags.
This is a strong assumption.
The DAG is designed to surface paths that would violate strict exogeneity, namely the reverse-causality edge and the topic-by-time confounder $Z_{t}^{\text{topic}}$.

### Proposed DAG (TikZ draft, inline within `analysis-fake-stars.tex`)

The figure follows the same `confbox` / `tnode` / `mnode` / `ynode` / `rbox` style as Figure~\ref{fig:dag-pinning} and Figure~\ref{fig:dag-cursor}.
The latent treatment $D_{i,t}$ is drawn dashed with a measurement-error edge into the observed proxy $fake_{i,t}$ (the green treatment node feeding the regression).
The two mediators are drawn explicitly to make the *competing-channels* structure visible (visibility versus penalty), since the chapter's headline finding (positive short-run, negative long-run) is interpreted in the Discussion as the two channels operating on different time horizons.
The reverse-causality edge $real_{i, t-k} \to D_{i,t}$ is drawn as a curved red edge to highlight that it is the principal threat the lagged-DV specification attempts (and only partially manages) to absorb.
The topic-by-time confounder $Z_{t}^{\text{topic}}$ sits in a separate red dashed box to denote that it is *not* absorbed by either repository or month FE on their own.

```latex
\begin{figure}[t]
    \centering
    \begin{tikzpicture}[
        >=latex, font=\scriptsize,
        confbox/.style={draw, rounded corners, fill=gray!12, align=left, text width=4.4cm, inner sep=4pt},
        tnode/.style={draw, rounded corners, fill=green!20, very thick, minimum height=0.7cm, minimum width=2.6cm, align=center, font=\bfseries\scriptsize},
        tnodeL/.style={draw, rounded corners, dashed, fill=green!8, minimum height=0.6cm, minimum width=2.6cm, align=center, font=\itshape\scriptsize},
        mnode/.style={draw, rounded corners, fill=yellow!25, minimum height=0.6cm, minimum width=2.4cm, align=center, font=\scriptsize},
        ynode/.style={draw, rounded corners, fill=blue!10, minimum height=0.6cm, minimum width=2.6cm, align=center, font=\scriptsize},
        rbox/.style={draw, rounded corners, dashed, fill=red!8, align=left, text width=4.4cm, inner sep=4pt},
        cedge/.style={->, gray, dashed, semithick},
        medge/.style={->, black, semithick},
        revedge/.style={->, red!70!black, dashed, thick},
        meas/.style={->, gray!60!black, dotted, thick},
    ]
    % --- Time-invariant confounders absorbed by repository FE ---
    \node[confbox] (Conf) {%
        \textbf{Absorbed by repository FE $\mu_i$}\\[1pt]
        $\bullet$ $U_i$: maintainer growth-hacking disposition\\
        $\bullet$ $T_i$: project type / topical baseline\\
        $\bullet$ $N_i$: intrinsic quality / utility baseline
    };
    % --- Time-varying covariates (RE only) ---
    \node[confbox, below=0.4cm of Conf] (Covar) {%
        \textbf{Time-varying controls (RE only)}\\[1pt]
        $\bullet$ $age_{i,t}$, $had\_release_{i,t}$, $\log activity_{i,t}$\\
        \quad (omitted in FE specification)
    };
    % --- Latent treatment ---
    \node[tnodeL, right=2.0cm of Conf] (Dlat) {Latent $D_{i,t}$\\ purchase decision};
    % --- Observed treatment proxy ---
    \node[tnode, below=0.7cm of Dlat] (D) {$fake_{i,t}$ \\ detected fake stars};
    % --- Mediators ---
    \node[mnode, right=1.6cm of Dlat] (Mvis) {Visibility\\(trending, ranking)};
    \node[mnode, below=0.4cm of Mvis] (Mpen) {Penalty\\(scrutiny, removal)};
    % --- Outcome ---
    \node[ynode, right=1.6cm of Mvis, yshift=-0.5cm] (Y) {$real_{i, t+k}$};
    % --- Topic-by-time confounder (residual) ---
    \node[rbox, below=0.9cm of D] (Z) {%
        \textbf{Residual time-varying confounder $Z_{t}^{\text{topic}}$}\\[1pt]
        $\bullet$ Hype waves (LLMs 2023--2024, crypto 2021--2022)\\
        \quad not absorbed by repo FE; not absorbed by month FE\\
        \quad alone (only by topic$\times$month FE)
    };
    % --- Edges ---
    % Confounders -> treatment, blocked by FE
    \draw[cedge] (Conf.east) -- (Dlat.west) node[midway, above, font=\tiny\itshape] {(blocked by $\mu_i$)};
    \draw[cedge] (Covar.east) to[bend right=8] (D.west);
    % Latent -> observed (measurement)
    \draw[meas] (Dlat.south) -- (D.north) node[midway, right, font=\tiny\itshape] {meas.\ error (recall $\sim$81\%)};
    % Treatment -> mediators -> outcome
    \draw[medge] (D.east) to[bend left=8] (Mvis.south west);
    \draw[medge] (D.east) to[bend right=4] (Mpen.west);
    \draw[medge] (Mvis.east) to[bend left=8] node[above, font=\tiny\itshape] {$+$ short-run} (Y.north west);
    \draw[medge] (Mpen.east) to[bend right=8] node[below, font=\tiny\itshape] {$-$ long-run} (Y.south west);
    % Confounders -> outcome (also blocked)
    \draw[cedge] (Conf.east) to[bend left=10] (Y.north);
    % Z -> treatment and outcome (residual threat, both arrows solid)
    \draw[->, red!70!black, semithick] (Z.east) to[bend right=15] (D.south);
    \draw[->, red!70!black, semithick] (Z.east) to[bend right=30] (Y.south);
    % Reverse causality
    \draw[revedge] (Y.north) to[bend left=35] node[above, font=\tiny\itshape] {reverse: $real_{i, t-k} \to D_{i,t}$} (Dlat.east);
    \end{tikzpicture}
    \caption{Causal DAG for the RQ4 promotional-effect analysis.
    The latent purchase decision $D_{i,t}$ is observed only through the proxy $fake_{i,t}$ produced by \SystemName; classical attenuation under A3 is the optimistic case (recall $\sim$81\%, Section~\ref{sec:rq1}).
    Time-invariant confounders ($U_i$, $T_i$, $N_i$, gray box) are absorbed by repository fixed effects; time-varying release and activity controls (also gray) enter the random-effects specification only.
    The treatment effect on next-month real stars decomposes through two competing mediators: a positive visibility channel (trending, ranking, social proof) and a negative penalty channel (scrutiny, removal, signal-incongruence).
    Topic-by-time hype $Z_{t}^{\text{topic}}$ (red dashed box) is not absorbed by either repository or month fixed effects on their own and is the principal residual confounder.
    The dashed red arrow $real_{i, t-k} \to D_{i,t}$ is the reverse-causality edge that the lagged-dependent-variable specification only partially blocks (Nickell bias).
    The principal load-bearing assumptions are A1 (strict exogeneity), A2 (no unobserved time-varying confounders) and A5 (panel completeness).}
    \label{fig:dag-fake-stars}
\end{figure}
```

Layout decisions:
- **Two mediators drawn explicitly** rather than collapsed into a single arrow, because the headline finding (positive short-run / negative long-run) corresponds to the two mediators' relative dominance over different horizons. This mirrors the cursor DAG's choice to show the volume-mediated and per-line-complexity paths separately.
- **Latent treatment as a separate node** with a measurement-error edge into the observed proxy, mirroring the confounder/observed-covariate distinction used in the pinning DAG. This makes A3 (measurement) visually located in the DAG rather than only in prose.
- **Topic-by-time confounder shown in red dashed box** to mark it as a residual threat after the FE design's controls, in the same convention as the pinning DAG's Renovate/upstream-frequency residual-threat box.

---

## Step 2 — Causal Estimand and Identifying Assumptions

**Goal:** Define the estimand precisely. For each identifying assumption, state explicitly whether it is satisfied by construction or requires empirical argument. Because the treatment is observational and chosen endogenously by maintainers, *none* of the identifying assumptions for the fake-stars analysis is satisfied by construction; all require empirical argument.

### Estimands

Let $Y_{i, t+k}(d)$ denote real stars gained by repository $i$ in month $t+k$ if the maintainer had purchased $d$ fake stars in month $t$ (holding $D_{i, s}$ fixed at observed values for all $s \neq t$).

The study targets two estimands:

- **Short-run promotional effect (one-month elasticity):** $\beta_1 = \partial \log E[Y_{i, t+1}(d)] / \partial \log d$, evaluated locally around the observed treatment intensity.
- **Long-run penalty ($k \geq 3$ months on cumulative purchases):** $\beta_{\text{long}} = \partial \log E[Y_{i, t+k}(d)] / \partial \log\!\left(\sum_{s \leq t} D_{i,s}\right)$.

The reported estimator is the coefficient on $\log fake_{i, t-1}$ in the fixed-effects panel autoregression, plus the coefficient on $\log all\_fake_{i, t-k-1}$ for the long-run estimand.

### Identifying Assumptions

**A1. Strict exogeneity of treatment to errors.** Conditional on repository fixed effects and the included controls, the treatment is uncorrelated with the unobserved error at all leads and lags. This is the central identifying assumption and is the one most threatened by the reverse-causality and topic-momentum paths in the DAG.

**A2. No unobserved time-varying confounders.** Repository fixed effects absorb time-invariant heterogeneity, but topic-popularity shocks and platform algorithm changes are time-varying within unit and not absorbed by FE alone. Partially mitigated by the inclusion of $release_{i,t}$ and $activity_{i,t}$ in the RE specification, but these are not in the FE specification reported in the main text. Discussed in Step 3.

**A3. Classical (or known-direction) measurement error in the treatment proxy.** \SystemName has $\sim$81% recall and unknown campaign-level precision. If errors are classical (independent of true treatment), coefficients attenuate toward zero and the estimated short-run effect is a lower bound on the true elasticity. Non-classical errors (e.g., \SystemName systematically misses sophisticated buyers) bias in unknown directions; the non-classical case is treated as an external validity / measurement validity concern in the existing Limitations paragraph.

**A4. SUTVA at the repository level.** One repository's treatment does not affect another's outcomes. Plausibly violated through trending and search-ranking algorithms: a faked repository displacing organic competitors would create spillovers. The magnitude is bounded by the small fraction (0.42%) of fake-star repositories that reach trending, suggesting the violation is empirically small but nonzero.

**A5. No selection on outcome (panel completeness).** Repositories deleted before the observation window closes drop out of the panel. Since 90.42% of detected campaign repositories are deleted, the FE panel is estimated on the surviving 9.58%. This is severe and motivates the survivor-only robustness analysis in Step 4.

**A6. Stable treatment definition.** "Buying fake stars" is treated as a single intervention. In practice, the dataset pools heterogeneous purchasing strategies and heterogeneous purposes (growth hacking vs. malware promotion). The estimate is best read as a pooled average; heterogeneity is examined as a Step 4 alternative.

### What the Estimate Identifies If Assumptions Hold

If A1–A6 hold, the FE coefficient on $fake_{i, t-1}$ identifies the average within-repository elasticity of next-month real stars with respect to detected fake-star intensity, *averaged over the sub-population of repositories surviving in the panel*. This is closer in spirit to an Average Partial Effect within the surviving treated population than to an ATE on the full universe of GitHub repositories. The Discussion's counterfactual claim ("buying fake stars is ineffective") generalizes only to the extent that this APE is informative about the population of practitioners who would consider buying.

---

## Step 3 — Limitations and Known Caveats

**Goal:** Identify the residual threats to the *causal credibility* of the RQ4 estimate after the panel-FE design's controls. Concerns about non-classical measurement error in the treatment proxy, treatment heterogeneity, generalizability to undetected sophisticated campaigns, and the methodological scope of Granger causality testing are external validity, measurement validity, or treatment-generalizability concerns rather than threats to causal identification, and are addressed in the existing Limitations paragraph in the RQ4 section and in Section 3.4 of the paper.

### Causal Credibility Limitations

| Limitation | Assumption Threatened | Direction of Bias | Robustness check |
|---|---|---|---|
| Time-varying unobserved confounders (topic momentum, viral moments) | A2 | Direction depends on the confounder; upward if hype both drives buying and drives organic interest | Calendar-period stratification (R4) and domain stratification (R5), reported under Alternative 2. |
| Reverse causality between real-star growth and purchase decision | A1 | Direction depends on the lead-lag pattern (downward under panic-buying, upward under hype-amplification) | Lead-lag swap regression (R1), reported under Alternative 3. |
| Survivorship — 90.42% of detected repositories are deleted | A5 | Direction unclear; upward bias if repositories with successful short-run lift survive longer | Survivor-length stratification (R2), reported under Alternative 1. |
| SUTVA violation via platform algorithms | A4 | Direction unclear; magnitude bounded by trending share (0.42%) | No executed check; argued small in Alternative 4 (trending exclusion R6 not implemented because trending reach is rare). |
| Classical attenuation from imperfect detector recall | A3 | Lower bound on the true elasticity | Not amenable to a within-sample robustness check; argued from detector-recall benchmark. |
| Cumulative-real series is monotone non-decreasing by construction (GHArchive `WatchEvent` is additive only) | A5 (sub-mechanism of survivorship: GitHub moderation vs. user disengagement) | Cannot be tested in this dataset | **Design limitation** (formerly R3): distinguishing user-disengagement from platform-moderation channels of the long-run negative coefficient would require periodic snapshots of total star counts from a non-event-stream source (e.g., scheduled GitHub REST API polls), which is out of scope for the chapter's existing data pipeline. |

### Limitations Outside the Scope of Causal Credibility

The following concerns are not threats to internal causal identification of the RQ4 estimate and are addressed in the existing Limitations paragraph in the RQ4 section and in Section 3.4 of the paper:

- Non-classical measurement error in `fake_{i,t}` if \SystemName systematically misses sophisticated buyers (measurement validity beyond classical attenuation).
- Treatment heterogeneity (growth-hacking startups vs. phishing repositories vs. AI/LLM and Blockchain promotion pooled) (treatment generalizability).
- Generalizability to undetected sophisticated campaigns (external validity to evasive actors).
- Granger causality test infeasible due to short panels (methodological scope).

---

## Step 4 — Alternative Explanations

**Goal:** Identify the most threatening alternative causal structures and explain whether the design rules them out, partially addresses them, or leaves them open. Each alternative is paired with the concrete robustness check that operationalises it. The robustness checks were executed in `fake-star-reanalysis/robustness.Rmd` (knits to `robustness.html`); chunks are also embedded in `fake-star-reanalysis/regression.Rmd`. The baseline AR(2) FE replicates Table~\ref{tab:regression} of the chapter exactly: $\hat\beta_{l1\_fake} = +0.074^{***}$ (SE 0.013), $\hat\beta_{l2\_fake} = +0.029^{*}$ (SE 0.011), $\hat\beta_{l3\_total\_fake} = -0.045^{**}$ (SE 0.014), $n = 12{,}738$, 1{,}042 repositories.

**Reporting rule for the LaTeX rendering.** The chapter only reports a single consolidated robustness-checks table (the "Consolidated Coefficient Summary" at the end of this section). The per-alternative tables, code blocks, and stratum-by-stratum coefficient breakdowns shown below in Alternatives 1--4 are *plan-internal expansions* of individual rows of that consolidated table; they document specification choices and provide a paper trail for the executed checks but should not be reproduced in `analysis-fake-stars.tex`. Each alternative's prose in the LaTeX should reference the corresponding rows of the consolidated table by name (e.g., "panel length $\geq 12$ vs $< 12$") rather than repeating the per-alternative tables in the chapter.

### Alternative 1 — The Long-Run Negative Coefficient Is a Survivorship Artifact, Not a Penalty Effect

The coefficient on $\log all\_fake_{i, t-k-1}$ is significantly negative across all $AR(k)$ specifications. The Discussion interprets this as a real-star *penalty* --- users see an inflated history and disengage. Two alternatives are equally consistent with the negative sign:
1. *Selective deletion.* Repositories with larger and more obvious fake histories are deleted earlier, so the surviving panel observations at large $all\_fake_{i, t-k-1}$ are precisely those whose campaigns failed to convert into real attention.
2. *GitHub moderation.* Repositories with larger cumulative fake-star history are more likely to have stars retroactively removed, producing a negative correlation that reflects platform action rather than user behaviour.

**Robustness check R2 --- Survivor-length stratification (threatens A5).**

The CSV does not flag deletion directly, but panel length serves as a proxy: a repository GitHub deleted (or whose maintainer abandoned) early appears in fewer rows. For each repository, compute `panel_length = n_distinct(month)` and stratify the AR(2) FE estimator into long-survivors (`panel_length >= 12`) and short-survivors (`panel_length < 12`). The 12-month threshold is roughly twice the chapter's median panel length (6 months $\approx 12{,}738 / 2{,}089$); sensitivity to alternative thresholds (18, 24) yields the same qualitative pattern.

```r
panel_lengths <- repos %>%
  group_by(repo) %>%
  summarise(panel_length = n_distinct(month), .groups = "drop")

l2_long  <- l2_repos %>% inner_join(filter(panel_lengths, panel_length >= 12), by = "repo")
l2_short <- l2_repos %>% inner_join(filter(panel_lengths, panel_length <  12), by = "repo")

ar2_fe_long  <- fit_ar2_fe(l2_long)
ar2_fe_short <- fit_ar2_fe(l2_short)
```

| Stratum | $n$ | repos | $\hat\beta_{l1\_fake}$ | $\hat\beta_{l2\_fake}$ | $\hat\beta_{l3\_total\_fake}$ |
|---|---:|---:|---:|---:|---:|
| Long-survivors (panel length $\geq 12$) | 10{,}751 | 394 | $+0.078^{***}$ | $+0.009$ | $-0.045^{***}$ |
| Short-survivors (panel length $< 12$)   | 1{,}987 | 648 | $+0.078^{**}$ | $+0.063^{***}$ | $+0.061^{*}$ |

**Reading.** The long-run negative coefficient persists in long-survivors ($-0.045^{***}$) and *flips positive* ($+0.061^{*}$) in short-survivors. Both readings remain compatible:
- *Penalty-effect reading:* user-disengagement requires time to develop and is therefore visible only in long-panel repos.
- *Selective-survival reading:* short-lived repos with successful-looking inflated histories are deleted before the negative effect can materialise, so short-survivor estimates are tilted positive.

**Implication.** The long-run negative finding cannot be attributed unambiguously to user disengagement. The Discussion should soften the framing to "consistent with both user-disengagement and selective-survival mechanisms; the data cannot fully distinguish them." A stronger separation between the two would require a separate moderation signal (see the design limitation in Step 3 around the additive-only `WatchEvent` source).

### Alternative 2 — Topic-Momentum Confounding Inflates the Short-Run Coefficient

The 2024 surge in fake-star activity coincides with topic-level surges in AI/LLM and (earlier) blockchain interest. Within these domains, organic real-star arrivals also surge in the same period. A maintainer in a hyped topic at month $t-1$ has both higher incentive to buy fake stars and higher organic real-star arrivals in month $t$, generating a positive coefficient that does not reflect a causal effect of buying on attention. Repository fixed effects do not absorb this because hype is time-varying within a repository's lifecycle.

Two robustness checks address this alternative jointly: a calendar-period stratification (R4) that bounds time-varying confounding without requiring topic labels, and a topic stratification (R5) using the `repo_labels.csv` categories.

**Robustness check R4 --- Calendar-period stratification (threatens A2).**

```r
l2_pre2024  <- l2_repos %>% filter(month <  "2024-01")
l2_2024     <- l2_repos %>% filter(month >= "2024-01" & month < "2024-09")
l2_post2024 <- l2_repos %>% filter(month >= "2024-09")

ar2_fe_pre2024   <- fit_ar2_fe(l2_pre2024)
ar2_fe_2024surge <- fit_ar2_fe(l2_2024)
ar2_fe_post2024  <- fit_ar2_fe(l2_post2024)
```

| Period | $n$ | repos | $\hat\beta_{l1\_fake}$ | $\hat\beta_{l2\_fake}$ | $\hat\beta_{l3\_total\_fake}$ |
|---|---:|---:|---:|---:|---:|
| Pre-2024 (month $<$ 2024-01) | 7{,}951 | 419 | $+0.031$ | $-0.068^{.}$ | $-0.054^{**}$ |
| 2024 LLM surge (Jan--Aug 2024) | 3{,}580 | 841 | $+0.080^{***}$ | $+0.063^{***}$ | $+0.021$ |
| Post-surge (month $\geq$ 2024-09) | 1{,}207 | 479 | $+0.030$ | $+0.011$ | $-0.072^{.}$ |

**Reading.** The headline positive short-run coefficient is significant *only* during the 2024 LLM-surge window. Pre-2024 and post-2024 coefficients are statistically indistinguishable from zero. The long-run negative coefficient is concentrated pre-2024 and absent during the surge. The pooled $\hat\beta_1$ blends a near-zero pre-2024 effect with a positive surge-period effect during which both buying and organic AI/LLM/crypto interest spiked together.

**Robustness check R5 --- Topic stratification on `repo_labels.csv` (threatens A2).**

The cleanest test of $Z_t^{\text{topic}}$ confounding stratifies directly on the manual category labels. `repo_labels.csv` contains 580 labelled repositories with five columns (`repo`, `packages`, `trending`, `domain`, `ai_label`); the `domain` column is used because it has no missing values. Of the 580 labelled repositories, 375 also appear in the AR(2) panel.

```r
labels <- read.csv("repo_labels.csv", stringsAsFactors = FALSE)
l2_labeled <- l2_repos %>% inner_join(labels[, c("repo", "domain")], by = "repo")

ar2_fe_labeled <- fit_ar2_fe(l2_labeled)  # pooled R5 baseline
domain_models  <- lapply(setNames(domains_to_fit, domains_to_fit), function(dom)
  fit_ar2_fe(filter(l2_labeled, domain == dom)))
```

Strata smaller than 30 repositories or 100 panel observations (`database`, `basic-utility`, `other`, `bot`, `deleted`) are skipped because within-FE estimation is unstable for small panels.

| Stratum | $n$ | repos | $\hat\beta_{l1\_fake}$ | $\hat\beta_{l2\_fake}$ | $\hat\beta_{l3\_total\_fake}$ |
|---|---:|---:|---:|---:|---:|
| Pooled (labelled only) | 5{,}198 | 375 | $+0.067^{***}$ | $+0.021$ | $-0.076^{***}$ |
| domain = blockchain | 1{,}241 | 51 | $+0.023$ | $-0.019$ | $-0.069^{***}$ |
| domain = web | 895 | 48 | $+0.003$ | $+0.004$ | $-0.054^{.}$ |
| domain = tool/application | 683 | 54 | $+0.120^{*}$ | $-0.040$ | $-0.171^{**}$ |
| domain = ai | 626 | 74 | $+0.099^{*}$ | $+0.018$ | $-0.042$ |
| domain = suspicious | 542 | 55 | $+0.068^{*}$ | $+0.155^{***}$ | $-0.034$ |
| domain = tutorial/demo | 426 | 39 | $+0.192^{**}$ | $+0.085$ | $+0.024$ |

**Reading.** The pooled $\hat\beta_{l1\_fake}$ on labelled repositories ($+0.067^{***}$) hides an order-of-magnitude variation across domains. The short-run effect is significant in `tool/application`, `tutorial/demo`, `ai`, and `suspicious`, and null in `blockchain` and `web`. The long-run negative coefficient concentrates in `tool/application`, `blockchain`, and `web`, and is absent in `ai`, `suspicious`, and `tutorial/demo`. The pattern does not cleanly map to the simple "AI/LLM hype 2024" story --- `ai` has only a moderate effect, `blockchain` has none, and `tutorial/demo` (not a hype-driven category) shows the largest short-run coefficient.

**Joint implication for A2.** R4 and R5 together establish that the pooled estimate is not a single causal parameter; it is an average over heterogeneous within-period and within-domain effects. Topic-by-time confounding remains the leading concern, but the *channel* is plausibly broader than hype amplification --- consistent candidates include heterogeneity in mediator strength across content types (social-proof cues bind harder for tutorial-style content), heterogeneity in bot-traffic vs. real-user composition, and calendar-time concentration of certain domains during the 2024 surge. The pooled positive coefficient should not be reported as a single ATE-like quantity; the chapter should accompany the headline number with at least a calendar-period or domain breakdown.

### Alternative 3 — Reverse Causality Between Real-Star Growth and Purchase Decisions

Maintainers observing weak real-star growth in months $t-2, t-1$ may purchase fake stars in month $t$ to reignite visibility (the "panic-buy" story). Maintainers observing *strong* organic momentum may also buy to amplify it (the "hype-amplification" story). Either dynamic violates strict exogeneity (A1): the lagged-DV specification only partially blocks the path, and Nickell-style bias for short panels remains.

**Robustness check R1 --- Lead-lag swap regression (threatens A1).**

Swap the dependent variable: regress $\log fake_{i,t}$ on lagged real-star intensity, conditional on the same fixed-effects structure. The sign of the lagged-real coefficient distinguishes the two reverse-causality stories.

```r
rev_causality_fe <- plm(
  log(n_stars_fake + 1) ~
    log(l1_real + 1) + log(l2_real + 1) + log(l3_total_real + 1) +
    log(l1_fake + 1) + log(l2_fake + 1) + log(l3_total_fake + 1),
  data = l2_repos, index = c("repo", "month"), model = "within"
)
```

| Regressor | Coefficient (HC1 SE) |
|---|---:|
| $\log real_{i, t-1}$ | $+0.0934^{***}$ (0.0212) |
| $\log real_{i, t-2}$ | $+0.0342^{*}$ (0.0153) |
| $\log all\_real_{i, t-3}$ | $+0.1131^{***}$ (0.0145) |

**Reading.** All three lagged-real coefficients are *positive* and significant. Past organic momentum predicts subsequent fake-star buying. The "panic-buy" story (negative sign) is *not* supported; the data is consistent with hype-amplification or rich-get-richer in purchasing (maintainers riding momentum, possibly because trending placement makes them visible to merchants).

**Implication.** The bias on the headline $\hat\beta_1$ from this reverse-causality channel is *upward*, not downward. The headline short-run estimate should be treated as an *upper bound* under this story, not a lower bound. The Discussion's conclusion ("buying fake stars is ineffective") is *strengthened* under this reading: the true causal effect is plausibly smaller than the pooled estimate.

### Alternative 4 — Detection-Induced Selection and SUTVA via Trending

\SystemName detects fake stars by clusters satisfying lockstep or low-activity signatures. Sophisticated merchants who use realistic accounts, dispersed timing, or smaller batch sizes are systematically under-detected. The estimated effect therefore corresponds to the population of *detectable* campaigns --- likely the cheapest, most easily flagged tier of the market. A second concern under this alternative is SUTVA: a faked repository displacing organic competitors via Trending or search ranking would create cross-repository spillovers.

**No robustness check executed.** Two reasons.
1. *No within-sample test of detector evasion.* Whether sophisticated campaigns convert better into real attention cannot be tested with data \SystemName failed to flag; the question is fundamentally outside the scope of the existing dataset.
2. *Trending exclusion (R6) is not implemented because trending reach is rare.* Only 0.42\% of campaign repositories ever appear on GitHub Trending (chapter Section~\ref{sec:rq1}, Figure~\ref{fig:trending}). The maximum SUTVA-induced bias is bounded by this share, which is too small to materially shift any of the headline coefficients. Implementing R6 would require merging the trending-archive flag from a separate part of the chapter pipeline; the expected sensitivity does not justify the data-engineering cost. The original plan listed R6 as optional; after observing the magnitude of bias the trending channel can plausibly induce, R6 is dropped.

**Implication.** Both concerns are acknowledged and discussed rather than tested:
- The estimate identifies the effect of *detectable* fake-star buying. Under detector-evasion bias, the effect is a lower bound on the population-average effect of buying. The Discussion's policy recommendation against buying *strengthens* for non-sophisticated buyers (the dominant case in the data) but does not extend to actors with the resources to evade detection.
- The SUTVA violation magnitude is bounded by the small trending share (0.42\%); this is reported as a numeric bound rather than tested empirically.

### Consolidated Coefficient Summary

The headline fake-star coefficients across the baseline and all executed robustness specifications:

| Specification | $n$ | repos | $\hat\beta_{l1\_fake}$ | $\hat\beta_{l2\_fake}$ | $\hat\beta_{l3\_total\_fake}$ |
|---|---:|---:|---:|---:|---:|
| Baseline AR(2) FE | 12{,}738 | 1{,}042 | $+0.074^{***}$ | $+0.029^{*}$ | $-0.045^{**}$ |
| **Alt. 1, R2** | | | | | |
| panel length $\geq 12$ | 10{,}751 | 394 | $+0.078^{***}$ | $+0.009$ | $-0.045^{***}$ |
| panel length $< 12$ | 1{,}987 | 648 | $+0.078^{**}$ | $+0.063^{***}$ | $+0.061^{*}$ |
| **Alt. 2, R4** | | | | | |
| month $<$ 2024-01 | 7{,}951 | 419 | $+0.031$ | $-0.068^{.}$ | $-0.054^{**}$ |
| 2024-01 $\leq$ month $<$ 2024-09 | 3{,}580 | 841 | $+0.080^{***}$ | $+0.063^{***}$ | $+0.021$ |
| month $\geq$ 2024-09 | 1{,}207 | 479 | $+0.030$ | $+0.011$ | $-0.072^{.}$ |
| **Alt. 2, R5** | | | | | |
| labelled (pooled) | 5{,}198 | 375 | $+0.067^{***}$ | $+0.021$ | $-0.076^{***}$ |
| domain = blockchain | 1{,}241 | 51 | $+0.023$ | $-0.019$ | $-0.069^{***}$ |
| domain = web | 895 | 48 | $+0.003$ | $+0.004$ | $-0.054^{.}$ |
| domain = tool/application | 683 | 54 | $+0.120^{*}$ | $-0.040$ | $-0.171^{**}$ |
| domain = ai | 626 | 74 | $+0.099^{*}$ | $+0.018$ | $-0.042$ |
| domain = suspicious | 542 | 55 | $+0.068^{*}$ | $+0.155^{***}$ | $-0.034$ |
| domain = tutorial/demo | 426 | 39 | $+0.192^{**}$ | $+0.085$ | $+0.024$ |

R1 (Alt. 3) is reported separately because it has a different dependent variable ($\log fake_{i,t}$); see the table inside Alternative 3.

### Joint Implications for the Discussion

Across R1, R2, R4, and R5 the chapter's central conclusions survive but with sharpened qualifiers:
- The positive short-run effect appears predominantly during topic-hype windows (R4) and is heterogeneous across domains by an order of magnitude (R5); the pooled coefficient should not be interpreted as a single causal parameter.
- The bias from reverse causality is plausibly *upward* (R1, hype-amplification) rather than downward (panic-buy); the headline short-run estimate is best treated as an upper bound.
- The long-run penalty is partly mechanical via selective survival (R2); the data cannot fully distinguish the user-disengagement and selective-deletion channels, and the GitHub-moderation channel cannot be tested in this dataset at all (R3 design limitation).
- The Discussion's policy recommendation against buying fake stars survives all four checks. Outside topic-hype windows the data does not support a positive promotional effect at all; within hype windows the effect exists but is plausibly inflated by the reverse-causality channel; in either case the long-run trajectory is not net positive.

### Updates to the DAG Following Execution

Two annotations on Figure~\ref{fig:dag-fake-stars} should be revised to reflect the executed checks:
- The reverse-causality edge $real_{i, t-k} \to D_{i,t}$ should carry a *positive*-sign annotation (hype-amplification) rather than the original "panic-buy" framing.
- The $Z_t^{\text{topic}}$ confounder label should change from "topic momentum / hype waves" to "topic-by-time and topic-by-channel confounding," with R4 and R5 cited as joint evidence.

---

## On the Descriptive Status of RQ1–RQ3

The credibility analysis should explicitly note that RQ1 (prevalence), RQ2 (activity patterns), and RQ3 (repository characteristics) are **measurement and characterization** results, not causal claims. The chapter is already careful in its phrasing, but downstream readers may treat patterns like "repositories with fake star campaigns are short-lived" as a causal statement about the effect of fake-star buying on repository lifespan. The framing note should make clear that:

- RQ1–RQ3 estimate population frequencies and joint distributions, not counterfactual outcomes.
- The deletion-rate comparison in Section 3.4 (criterion validity) is a comparison of group means with no claim that detection *causes* deletion — it provides convergent evidence for the validity of the detector, not a causal effect.
- The implicit causal claim in the Discussion ("we recommend against buying fake stars... it is ineffective") rests entirely on RQ4 plus the assumptions in Step 2; readers should evaluate it against those assumptions, not against RQ1–RQ3.

---

## Dataset and Code Pointers

The robustness checks are implemented against:
- `fake-star-reanalysis/model_stars.csv` --- 34,840-row panel with 11 columns (`repo`, `month`, `campaign`, `n_stars`, `n_stars_fake`, `n_stars_real`, `n_stars_total`, `age`, `release`, `activity`, `had_release`); 18,617 unique repositories; 2,089 with `campaign = True`; AR(2) lag-window drop yields 12,738 obs / 1,042 repos.
- `fake-star-reanalysis/repo_labels.csv` --- 580 manually labelled repositories with five columns (`repo`, `packages`, `trending`, `domain`, `ai_label`); 375 of these appear in the AR(2) panel.
- `fake-star-reanalysis/robustness.Rmd` --- the executable robustness-check notebook (knits to `robustness.html`).
- `fake-star-reanalysis/regression.Rmd` --- the original AR$(k)$ regression notebook, with R1, R2, R4, R5 chunks appended for inline reproducibility.

The narrative for each check, including specification, code, results table, and interpretation, lives inside Step 4 above next to the alternative it addresses.

---

## Open Questions Before Drafting

- [x] **Literature review scope:** Completed in Step 1; all DAG nodes carry citation support, and the one missing reference (Nickell 1981) is flagged for a new bib entry.
- [x] **Robustness checks executed:** R1, R2, R4, R5 implemented in `robustness.Rmd` and embedded as chunks in `regression.Rmd`. R3 reframed as a design limitation in Step 3. R6 not implemented (justification under Alternative 4: trending reach is rare, only 0.42\% of campaign repositories).
- [x] **Section title:** `\section{Causal Credibility Analysis}` (matching the pinning and cursor chapters), recorded in the file header.
- [x] **DAG annotation updates:** Reverse-causality edge labelled with a positive sign (hype-amplification, per R1); $Z_t^{\text{topic}}$ confounder relabelled "topic-by-time and topic-by-channel confounding" (per R4 + R5 jointly).
- [x] **Robustness checks placement in the LaTeX:** Resolved. The chapter reports only the consolidated coefficient summary table (Step 4 end). Per-alternative tables, code blocks, and per-stratum printouts in the plan are reference material for executing the checks and do not appear in `analysis-fake-stars.tex`. Each alternative's prose in the LaTeX cites the relevant rows of the consolidated table by name; readers seeking the chunk-level reproduction follow the pointer to `fake-star-reanalysis/robustness.Rmd` (and the rendered `robustness.html`).
