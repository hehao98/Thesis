# Causal Credibility Analysis — Fake Stars Chapter

**Status:** Draft plan, pending author review
**Target file:** `analysis-fake-stars.tex`
**Placement:** Between RQ4 results (Section 4.4) and Discussion (Section 5)
**Scope:** RQ4 (Promotional Effect) is the only research question that makes a quantitative causal claim, so the formal apparatus targets RQ4. RQ1–RQ3 are descriptive / measurement results and only require a brief framing note clarifying that they are *not* causal claims (and should not be read as such downstream). The criterion-validity argument in Section 3.4 (deletion-rate comparison) is a secondary application of the toolkit.

---

## Tasks

- [ ] Literature review to justify each DAG node (cite sources for each confounder and mediator; pinning-chapter review identified ~10 sources, similar effort expected here)
- [ ] Draw DAG figure (`figs-fake-stars/dag-fake-stars.pdf`) for Step 1, covering RQ4
- [ ] Draft a one-paragraph framing note clarifying the descriptive scope of RQ1–RQ3
- [ ] Write Step 1 — Causal Theory
- [ ] Write Step 2 — Causal Estimand and Identifying Assumptions
- [ ] Write Step 3 — Limitations and Known Caveats (causal credibility threats only)
- [ ] Write Step 4 — Alternative Explanations
- [ ] Specify and implement two robustness extensions (heterogeneity split + survivor-only re-estimation) to operationalize Step 4
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

**Literature review pending.** Each entry below lists what published evidence is required to support the node's inclusion. Bibliographic entries should be added during the literature review pass before drawing the DAG. Where the existing chapter already discusses a node empirically, that discussion can stand in for the literature support.

#### Treatment and Observed Proxy

**$D_{i,t}$ — Maintainer's decision to purchase fake stars (unobserved)**
- Need: existing studies documenting the fake-star marketplace and its actors.

**$\widehat{D}_{i,t} = fake_{i,t}$ — Detected fake stars from \SystemName**
- Need: the chapter's own measurement-validity discussion (Section 3) and any prior detector benchmarks (Stargazer Ghost Network ground truth).

#### Outcomes

**$real_{i, t+k}$ — Non-fake stars gained in subsequent months**
- Need: literature establishing GitHub stars as a popularity / discovery signal.

#### Mediators

**Visibility channel** (inflated star count $\to$ trending placement, search ranking, perceived popularity $\to$ real users discover and star)
- Need: GitHub trending/discovery studies, search ranking literature, social-proof effects in OSS adoption.

**Penalty channel** (inflated star count $\to$ user inspection of activity signals $\to$ skeptical users decline to star)
- Need: literature on credibility cues in OSS adoption, signal incongruence effects, prior fake-star detection studies on user reactions.

#### Confounders

**$U_i$ — Maintainer competence / strategy (time-invariant)** — absorbed by repository fixed effects to the extent the trait is stable
- Need: literature on growth-hacking practices in OSS, maintainer-quality typologies.

**$Z_t^{\text{topic}}$ — Topic momentum (time-varying)** — hype waves in LLMs (2023–2024), blockchain (2021–2022)
- Need: literature documenting technology hype cycles on GitHub, sectoral attention studies.

**$T$ — Calendar time** — the 2024 surge in both fake stars and real-star activity in trending domains
- Need: any longitudinal GitHub-activity studies covering the 2019–2024 window.

**Project quality / release activity** — controlled in the RE specification via $release_{i,t}$ and $activity_{i,t}$
- Need: literature linking release activity and quality signals to repository popularity.

#### Reverse-Causality Edge

**$real_{i, t-1} \to D_{i,t}$** — declining real-star growth may itself trigger a purchase decision
- Need: behavioral literature on developer responses to declining attention. This edge is the most threatening identification problem for the FE estimator and is what motivates the lagged-DV specification.

### Critical Argument

Unlike the pinning chapter, the fake-stars analysis does *not* have a counterfactual simulation that imposes treatment by construction. Treatment is observational and the maintainer chooses it endogenously. The panel-FE estimator's causal interpretation therefore rests on a strict exogeneity assumption: conditional on repository fixed effects and the included time-varying controls, the treatment is uncorrelated with the unobserved error at all leads and lags. This is a strong assumption. The DAG is designed to surface paths that would violate strict exogeneity, namely the reverse-causality edge and time-varying topic confounding.

### Deliverable

A single DAG figure (`figs-fake-stars/dag-fake-stars.pdf`) showing:
1. The unobserved treatment $D_{i,t}$ with a measurement-error link to its observed proxy $fake_{i,t}$.
2. Both mediators (visibility, penalty) on the path from treatment to $real_{i, t+k}$.
3. The time-invariant confounder $U_i$ absorbed by fixed effects (drawn with a dashed box).
4. The time-varying confounder $Z_t^{\text{topic}}$ that is *not* fully absorbed (drawn solid as a remaining threat).
5. The reverse-causality edge from $real_{i, t-1}$ to $D_{i,t}$.

TikZ recommended for consistency with the pinning DAG style.

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

| Limitation | Assumption Threatened | Direction of Bias | Analysis |
|---|---|---|---|
| Time-varying unobserved confounders (topic momentum, viral moments) | A2 | Likely upward bias on short-run $\beta_1$ if topic hype both drives buying *and* drives organic interest | FE absorbs only time-invariant traits. Time FE not in the reported FE specification. Including $release_{i,t}$ and $activity_{i,t}$ in the RE specification yields qualitatively similar coefficients, suggesting the bias is bounded but not eliminated. |
| Reverse causality from declining real-star growth to purchase decision | A1 | Likely downward bias on $\beta_1$ (panic-buying clusters in periods of weak organic momentum) | The lagged-DV structure absorbs *some* of this, but the Nickell bias for short panels remains. Robustness check: regress $fake_{i,t}$ on lagged $real_{i, t-k}$ to test whether stagnation precedes purchasing. |
| Survivorship — 90.42% of detected repositories are deleted | A5 | Direction unclear; likely upward bias on $\beta_1$ if repositories with successful short-run lift survive longer | The FE panel runs on 12,738 observations from the surviving repositories; the deleted majority is not in the regression at all. Robustness: stratify by eventual deletion status and re-estimate within survivors only. |
| SUTVA violation via platform algorithms | A4 | Direction unclear; magnitude plausibly small | Only 0.42% of fake-star repositories reach trending; the violation magnitude is bounded by this share. Robustness: re-estimate with trending-affected repositories excluded. |
| Classical attenuation from imperfect detector recall | A3 | Lower bound on the true elasticity | Recall $\sim$81%, precision uncertain. Estimated short-run effect is a lower bound on the true elasticity under classical errors. |

### Limitations Outside the Scope of Causal Credibility

The following concerns are not threats to internal causal identification of the RQ4 estimate and are addressed in the existing Limitations paragraph in the RQ4 section and in Section 3.4 of the paper:

- Non-classical measurement error in `fake_{i,t}` if \SystemName systematically misses sophisticated buyers (measurement validity beyond classical attenuation).
- Treatment heterogeneity (growth-hacking startups vs. phishing repositories vs. AI/LLM and Blockchain promotion pooled) (treatment generalizability).
- Generalizability to undetected sophisticated campaigns (external validity to evasive actors).
- Granger causality test infeasible due to short panels (methodological scope).

---

## Step 4 — Alternative Explanations

**Goal:** Identify the most threatening alternative causal structures and explain whether the design rules them out, partially addresses them, or leaves them open. Each alternative is paired with a concrete robustness check that operationalizes the response.

### Alternative 1 — The Long-Run Negative Coefficient Is a Survivorship Artifact, Not a Penalty Effect

The coefficient on $all\_fake_{i, t-k-1}$ is significantly negative across all $AR(k)$ specifications. The Discussion interprets this as a real-star *penalty* — users see an inflated history and disengage. An alternative explanation is mechanical: repositories with larger cumulative fake-star history are more likely to have stars retroactively removed by GitHub's moderation, producing a negative correlation that reflects platform action rather than user behavior. A second alternative is selective deletion: repositories with bigger, more obvious fake histories are deleted earlier, so the surviving panel observations at large $all\_fake_{i, t-k-1}$ are precisely those whose campaigns failed to convert into real attention.

**How to address:**
- Re-estimate the model after excluding repositories that lost stars (i.e., where total star count was non-monotone) to isolate the user-disengagement channel from the GitHub-removal channel.
- Stratify the FE estimator by eventual deletion status and report whether the long-run negative coefficient is concentrated in repositories that GitHub eventually deleted.
- If both diagnostic checks attenuate or eliminate the negative coefficient, the long-run penalty interpretation in the Discussion should be softened to "consistent with either user-disengagement or platform-moderation mechanisms; the data cannot distinguish between them."

### Alternative 2 — Topic-Momentum Confounding Inflates the Short-Run Coefficient

The 2024 surge in fake-star activity coincides with topic-level surges in AI/LLM and blockchain interest. Within these domains, organic real-star arrivals also surge for the same period. A maintainer in a hyped topic at month $t-1$ has both higher incentive to buy fake stars and higher organic real-star arrival in month $t$, generating a positive coefficient that does not reflect a causal effect of buying on attention. Repository fixed effects do not absorb this because hype is time-varying within a repository's life cycle.

**How to address:**
- Add explicit topic-by-time fixed effects using the RQ3 categorical labels as a treatment for confounding by domain hype.
- For the subset of categorized repositories (Trending + Packages + sampled Other = 580 repos with labels), estimate a stratified model and report whether the short-run coefficient survives within each topic category.
- If the coefficient drops sharply in the AI/LLM and Blockchain strata, the pooled estimate is partly driven by topic confounding; the Discussion claim should be qualified accordingly.

### Alternative 3 — Reverse Causality from Stagnation to Purchase

Maintainers observing weak real-star growth in months $t-2, t-1$ may purchase fake stars in month $t$ to reignite visibility. Under this story, $fake_{i, t}$ is caused by past $real_{i, \cdot}$, and the lagged-DV specification only partially blocks the path. If reverse causality is operative, the estimated $\beta_1$ understates the true effect, so the H$_2$ partial-support finding may itself be conservative.

**How to address:**
- Estimate a lead-lag specification: regress $fake_{i,t}$ on lagged $real_{i, t-k}$ to test whether stagnation precedes purchasing. A significant negative coefficient would substantiate the reverse-causality concern.
- If supported, present the elasticity as a *lower bound* on the true short-run promotional effect rather than a point estimate, and note that the Discussion's "ineffective for growth hacking" claim is then partially defended by reverse-causality alone.

### Alternative 4 — Detection-Induced Selection Biases the Estimate Toward "Ineffective"

\SystemName detects fake stars by clusters that satisfy lockstep or low-activity signatures. Sophisticated merchants who use realistic accounts, dispersed timing, or smaller batch sizes are systematically under-detected. The estimated effect therefore corresponds to the population of *clumsy* campaigns that triggered detection — likely the cheapest, most easily flagged tier of the market. If sophisticated campaigns convert better into real attention, the estimated effect understates the true population-average effect of buying fake stars.

**How to address:**
- Acknowledge openly that the estimate identifies the effect of *detectable* fake-star buying.
- Discuss the asymmetry in the Discussion: the policy recommendation against buying fake stars *strengthens* under this caveat for non-sophisticated buyers (the dominant case in our data) but does not extend to actors with the resources to evade detection.
- This is a *feature* of the design from a public-policy perspective — practitioners considering a casual buy from a typical merchant face the estimated effect, not the sophisticated-evasion effect.

---

## On the Descriptive Status of RQ1–RQ3

The credibility analysis should explicitly note that RQ1 (prevalence), RQ2 (activity patterns), and RQ3 (repository characteristics) are **measurement and characterization** results, not causal claims. The chapter is already careful in its phrasing, but downstream readers may treat patterns like "repositories with fake star campaigns are short-lived" as a causal statement about the effect of fake-star buying on repository lifespan. The framing note should make clear that:

- RQ1–RQ3 estimate population frequencies and joint distributions, not counterfactual outcomes.
- The deletion-rate comparison in Section 3.4 (criterion validity) is a comparison of group means with no claim that detection *causes* deletion — it provides convergent evidence for the validity of the detector, not a causal effect.
- The implicit causal claim in the Discussion ("we recommend against buying fake stars... it is ineffective") rests entirely on RQ4 plus the assumptions in Step 2; readers should evaluate it against those assumptions, not against RQ1–RQ3.

---

## Open Questions Before Drafting

- [ ] **Literature review scope:** Conduct a literature review pass before drawing the DAG to populate the citations flagged in Step 1.
- [ ] **Robustness checks:** Should the two recommended robustness extensions (heterogeneity by topic, survivor-only re-estimation) go in the new analysis section, or as additional appendix tables alongside the existing $AR(k)$ results?
- [ ] **Section title:** "Causal Credibility of the Promotional-Effect Analysis" or a shorter "Identification and Threats to Validity" matching econometric convention?
