# Writing Patterns in AER/AEJ-Style Papers (Educational Guide)

This guide distills recurring writing patterns from two complete, narrative AEA-family papers found in this folder:
- AEJ: Policy proof — The effect of leaded gasoline on elderly mortality (Hollingsworth & Rudik, 2020)
- AER submission — Efficiency and Equity Impacts of Energy Subsidies (Hahn & Metcalfe, 2020, CARE program)

It is intended as a practical, teachable reference for reading, reviewing, and emulating this style.

## 1) Paper Arc (Macro Structure)
- Problem → Identification → Results → Policy: Lead with stakes, state the causal design crisply, report magnitudes, close with concrete policy implications.
- Standard sections: Abstract; Introduction; Physiological/Institutional context; Data; Methods & Results (often integrated); Heterogeneity/External Validity; Welfare/Policy; Conclusion; Appendices.
- Appendices do the heavy lifting: institutional details, construction, robustness, alternative specs, and additional checks.

## 2) Abstract Pattern (4–6 Sentences)
- Problem: State residual policy gap or exposure still present.
- Design: Name the natural experiment/regulatory change and method (DiD, event study, IV).
- Outcome chain: Link proximate (ambient/usage) → intermediate (biomarker/behavior) → final (mortality/welfare).
- Magnitudes: Include at least one interpretable number (elasticity, deaths per 100k, $/gram, % change).
- Identification strength: Briefly note what’s ruled out by design (co-pollutants, SES, selection).
- Policy relevance: Conclude with the main implication (efficient prices, welfare thresholds).

Example phrases:
- “Exploiting regulatory exemptions and a quasi‑experiment, we find …”
- “We provide the first causal estimates linking … to …”
- “Damages exceed $1,100 per gram of lead added.”

## 3) Introduction Pattern
- Hook with stakes: Acknowledge historical progress, then spotlight what remains (e.g., off‑road leaded fuel; $5T subsidies, 7% GDP).
- Gap → Contribution: Name what prior work lacks (clean causal estimates for the target population), then list contributions (numbered, concise).
- Identification teaser: One sentence on the clean variation and design labels (DiD/event study/IV) and what it lets you rule out.
- Policy link: Make welfare or policy levers explicit early (MSC/SCC, vouchers vs. price subsidies).
- Roadmap: 1–2 sentences, optionally with a compact appendix inventory for transparency.

Templates:
- “Despite [historic progress], [residual issue] persists and matters because [mechanism/evidence].”
- “We use [policy change/exemption] with [design] to causally identify [effect] on [outcomes].”
- “We estimate [elasticity/mortality effect], quantify [$X per unit], and assess [policy/welfare].”

## 4) Identification and Methods (Clarity over Novelty)
- State the estimand and design plainly; avoid inventing new labels.
- Define indices/variables once per equation; justify transforms (asinh vs. log) and clustering.
- Fixed effects: Specify levels (monitor‑by‑year; week‑by‑year; county; state‑by‑year) and why they matter.
- Identification source: Be explicit about within‑unit/time variation, and why it separates treatment from confounders.
- Placebos and gradients: Time gradients (pre‑trends) and distance gradients reinforce locality and timing; include placebo series where possible (e.g., IndyCar, baseball).

Useful phrasing:
- “Identification comes from within‑[unit] variation off common [time] effects.”
- “We estimate a precise zero for [placebo/unleaded].”
- “Results are similar if we [transform/specification].”

## 5) Results Reporting (Magnitude‑Forward)
- First‑stage/enrollment (if applicable) → Main effects → Heterogeneity → External validity.
- Text gives one-line takeaways with magnitudes; figures/tables carry detail; captions include a one‑line claim.
- Prefer concrete normalizations: per 100,000 population; % of mean; per 100,000 race miles.
- Heterogeneity: Pre‑declared subgroups (income, baseline usage, prior nudges); report both LATEs and elasticities when helpful.
- External validity: Compare experimental sample to population; report reweighted ranges; pick a transparent baseline.

Examples:
- “100,000 leaded miles in the prior week increase ambient lead by ≈14%; unleaded has a precise zero effect.”
- “Elderly mortality falls by 91 (race counties) and 38 (border) deaths per 100k after deleading.”
- “CARE elasticity is −0.35; very low‑income households respond more (−0.52 vs. −0.24).”

## 6) Welfare/Policy Sections (Transparent Assumptions)
- Translate outcomes to dollars via parameter chains (e.g., blood lead → IQ → earnings; deaths → life‑years → $/LY → $/gram).
- Make parameter choices explicit (year dollars, harvesting adjustments, SCC values, emissions totals), with appendix pointers.
- State thresholds/efficient prices: “Efficient price is orders of magnitude above current prices,” or “Benefits must be ≈6% higher to offset costs at SCC=$40/t.”
- Mechanism design framing: Vouchers vs. ad valorem taxes framed as moving prices toward MSC under second‑best constraints.

Examples:
- “Normalizing by ≈2 million grams emitted implies ≈$1,100 per gram.”
- “Cap‑and‑trade worsens welfare unless SCC exceeds ≈$79/t given current allowance prices.”

## 7) Conclusion (Brief, Conditional)
- Reaffirm causal contribution and main magnitudes; avoid re‑arguing methods.
- State conditionality (ambient levels, nonlinearity, marginal vs. average effects).
- Name data gaps that matter for policy (e.g., no public info on lead content/sales locations; ‘unleaded’ contamination).
- Extend implications (e.g., beyond children to elderly; pricing designs for utilities).

## 8) Mechanics and Style (Micro Patterns)
- Voice: Active for author actions (“we estimate/show/compute”); passive only for standards or facts.
- Sentences: 15–25 words typical; split multi‑clause sentences; lead with the claim, then qualify.
- Numbers/units: En dash for ranges (30–35%); consistent %; proper unit casing (µg/dL); minus sign (−0.35).
- Hyphenation: Compound modifiers before nouns (low‑income households; benefit–cost analysis; price‑subsidy change).
- Citations: End‑loaded; cluster rather than interject mid‑sentence; footnote for clarifications.
- Figures/Tables: Refer by number; captions contain a one‑line result (“Panel B shows a declining effect from 50–75 to 75–100 miles.”).

## 9) Phrases and Verbs to Reuse
- Estimate, identify, exploit, quantify, document, compute, lower‑bound, normalize, deflate.
- “No clear pre‑trends,” “precise zero,” “apparent in raw data,” “consistent with [mechanism/gradient].”
- “We rule out [confounders] via [design].”

## 10) Common Pitfalls (to Avoid)
- Overlong, conjunction‑heavy sentences in the Introduction with stacked parentheticals.
- Repeating the same exact magnitude across text, figure, and table — state once; summarize elsewhere.
- Inconsistent unit and percent formatting; mixed hyphenation (“benefit-cost” vs. “benefit–cost”).
- Under‑specifying ID source (what variation, at what level) and clustering.

## 11) Reverse‑Outline Checklist (Per Section)
- Abstract: Problem, design, magnitudes, ID strength, policy.
- Intro: Stakes; gap; one‑sentence ID; numbered contributions; roadmap.
- Data: Source, scope, why it matters for ID; placebos/comparisons.
- Methods: Spec with indices; FE and clustering; identification sentence.
- Results: One-line takeaway + key number; figure/table pointer; robustness pointer.
- Heterogeneity: Pre‑declared groups; economic interpretation.
- External validity: Sample→population comparison; reweighting; baseline choice.
- Policy/Welfare: Parameters explicit; thresholds; efficient price logic.
- Conclusion: Conditionality; data gaps; implication extensions.

## 12) Mini‑Templates (Fill‑in)
- Abstract sentence: “Exploiting [policy change/exemption] and [design], we show that [treatment] increases [proximate], which in turn raises [intermediate] and [final], implying [dollar/policy magnitude]. Our setting rules out [confounders].”
- ID sentence: “Identification comes from within‑[unit] variation off [time] fixed effects and the discrete switch from [leaded/subsidized] to [unleaded/market] in [year].”
- Result line: “Each [unit] increases [outcome] by [X% / Y per 100k]; effects are immediate and decay with [time/distance].”
- Welfare sentence: “Combining [effect] with [parameter chain] implies [$Z per unit] and an efficient price [relation] to current prices.”

## 13) Concrete Examples from These Papers
- Magnitude lead: “100,000 leaded miles in prior week → ≈14% ambient lead increase; unleaded → ≈0%.”
- Gradient: “Effect peaks in week 1 post‑race; declines to ≈0 by weeks 2–4; distance gradient 0–50 mi ≫ 75–100 mi.”
- Mortality: “Elderly all‑cause mortality falls by ~91 (race) and ~38 (border) per 100k after deleading; cardio and IHD drive results.”
- Elasticity: “CARE customers’ natural‑gas elasticity ≈ −0.35; very low‑income ≈ −0.52; high‑usage ≈ −0.41.”
- Welfare (CARE): “Introducing CARE likely reduces welfare unless prices move toward MSC; benefits must rise ≈6% to offset costs at SCC=$40/t.”

## 14) Practice Drills (Learning by Doing)
- Reverse outline two Introductions: write one sentence per paragraph; ensure each paragraph advances one idea.
- Abstract compression: rewrite to 150–175 words preserving method→magnitude→policy.
- Topic‑sentence audit: first sentences state the claim; details follow.
- Unit/number sweep: standardize ranges, units, percents; fix hyphenation.
- Figure captions: add one‑line takeaway; reference specific panels.

---

Appendix: Observed Section Headings (for familiarity)
- AEJPol paper: I. Physiology & Prior Work; II. Data; III. Methods & Results (Ambient, Blood lead, Elderly mortality); IV. Social cost; V. Conclusion; rich appendix with placebos, gradients, alternative specs, emissions calculation.
- CARE paper: 1. Introduction; 2. Background & Design; 3. Results (Enrollment; Price effect; Heterogeneity; External validity); 4. Welfare (baseline; cap‑and‑trade; vouchers; optimal subsidy; equity weights); 5. Conclusion; appendix with structural details and sensitivity.

## Per‑Paper Notes and Observed Patterns

1) AEJ: Policy — Leaded gasoline and elderly mortality (Hollingsworth & Rudik, 2020)
- Abstract: Problem→design→chain of outcomes→magnitudes→ID strength→policy.
- Intro: Historic success→residual off‑road use→gap→ID teaser (Clean Air Act exemption; 2007 deleading)→contributions (numbered)→roadmap.
- Methods & Results: Equation‑first clarity; FE/clustering specified; time/distance gradients; placebo series; precise zero for unleaded.
- Policy/Welfare: Transparent parameter chain; normalization to $/gram; efficient price logic; conditionality spelled out.
- Micro‑style: Active voice; end‑loaded citations; tight topic sentences; figures with one‑line takeaways.

2) AER submission — CARE natural field experiment (Hahn & Metcalfe, 2020)
- Abstract: Elasticity headline (−0.35), three welfare results, and MSC/SCC link; equity weight (≈6%).
- Intro: Global subsidies framing (≈$5T; 7% GDP)→gap (scarce causal elasticities)→NFE design→policy levers (cap‑and‑trade, vouchers)→contributions.
- Results: First‑stage enrollment effects (≈+9–11 pp), main elasticity, subgroup heterogeneity; external validity with reweighting.
- Welfare: Partial‑equilibrium structural model; clear assumptions; thresholds by SCC; optimal subsidy discussion; implicit equity weights.
- Micro‑style: Lists for clarity; standardizes parameters; avoids redundancy; places details in appendix.

3) AER‑style manuscript — Knowledge spillovers and corporate investment in research (Arora, Belenzon, Sheer)
- Abstract/Opening: Title page with authors; concise abstract stating dataset scale (~800K publications), private returns vs spillovers tension, and main comparative statics (“more internal use → more research; rival use → less research”).
- Intro: R vs D distinction; stakes with national R&D totals; historical quotes (Bush, 1945); motivation from theory of spillovers; numbered or clearly staged contributions.
- Style: AER tone and cadence; paragraph‑level topic sentences; end‑loaded citations; explanatory footnotes; uses “we focus on how private returns depend on the balance between…” structure.
- Identification/Empirics (inferred from abstract/body cues): Large‑scale bibliometrics; patent‑to‑paper citations as linkage; likely uses panel variation and rival exposure measures; emphasizes internal vs external use channels; careful about interpretation of “spillovers to rivals”.

4) Economics manuscript — Bankruptcy reform (BAPCPA) and credit outcomes
- Abstract/Intro pattern: Policy debate setup (Posner vs critics); model→calibration→pass‑through benchmark in bps per pp change in filings; empirical design exploiting the BAPCPA notch and event timing; “excess mass/missing mass” language; long‑run ~50% decline in filings net of rush‑to‑file.
- Methods: Event studies and DiD across credit‑score segments; key assumption (common trends) explicitly tested; uses proprietary rate offers + filing risk changes.
- Results reporting: Clear numeric benchmarks (80–113 bps per 1 pp change in filings); null on income distribution shift; modest Chapter 13 share changes.
- Style: AER empirical cadence; claims lead sentences; figures implied to carry timing; robustness called out.
- 5) AER — Colonial medical campaigns and present‑day health trust (AER‑2018‑0284, proof)
- Abstract: Historical policy intervention (1921–1956 forced medical exams/injections) digitized at granular geography across five African countries; long‑run effects on vaccination and trust (blood‑test consent); spillover to WB health project success.
- Style: Archival digitization + modern outcomes; emphasizes “granular geographic level,” “document,” and “present‑day relevance.”
- Likely sections: Historical context; Data construction from archives; Identification (campaign exposure intensity); Present‑day outcomes (vaccination/refusal/trust); Mechanisms/robustness; External validity to development projects.
- Pattern: Bridges historical shocks to contemporary behaviors; strong emphasis on data construction and validation; policy salience via project performance.

- 6) AER: Insights — Optimal spatial lockdowns (AERI‑2020‑0401, proof)
- Sections: Introduction; Model; Data and Parametrization; Optimal Spatial Lockdowns; Conclusion.
- Style: Theory‑first with calibrated parameters; policy counterfactuals; concise insights format with a sharp “optimal policy” headline.
- Pattern: Clear separation of model and calibration; welfare or objective function explicit; results framed as implementable rules (spatial targeting).

- 7) AER — Experimental/conceptual design paper (AER‑2020‑0304, proof)
- Sections: Introduction; A Conceptual Framework; Design and Procedures; Results; Conclusion.
- Style: Conceptual scaffold precedes experimental design; methods described under “Procedures”; results reported with pre‑registered or pre‑declared outcomes; concise conclusion.
- Pattern: Clean arc from framework → design → results; prioritizes internal validity language; likely includes manipulation checks and protocol details in appendix.

- 8) International trade — Swiss trade policy to EU (Bühler et al., 2011)
- Sections: Introduction; Swiss Trade Policy towards the EU; Data; Econometrics; Results; Conclusion.
- Style: Policy setting chapter; standard empirical pipeline; econometric specification section named as such; discipline‑typical separation of data and methods.
- Pattern: Clear, modular layout suitable for readers to jump to Econometrics/Results; policy context upfront; tables carry identification details.

- 9) Historical economics — Abramitzky (Final 6‑9‑2020)
- Abstract present; manuscript likely book‑style or overview with extensive data linkage (US federal census panels across years).
- Style: Historical demographic/economic analysis; likely narrative plus measurement sections; extensive figures and bands noted.
- Note: While not a journal proof, the prose still follows AEA clarity norms: topic sentences, end‑loaded citations, explicit data sources.

- Note on non‑journal reports: The NHTS “Summary of Travel Trends” is a statistical report; it does not follow AER narrative conventions and is excluded from style synthesis.

## Exemplar Snippets (Abstract/Intro/Results Lines)

These short quotes illustrate phrasing to emulate. Use them as concrete models alongside the templates.

- AEJ: Policy — Leaded gasoline and elderly mortality
  - Abstract: “Exploiting regulatory exemptions and a novel quasi‑experiment, we find that leaded gasoline use in racing increases ambient lead, elevated blood lead rates, and elderly mortality… each gram of lead added to gasoline exceeds $1,100 in damages.”
  - Intro hook: “Despite these advances, the phaseout of lead from gasoline remains incomplete… there is no safe level of exposure.”
  - Results: “Every 100,000 leaded miles driven in the past week increases ambient asinh(Pb) by 0.13 (≈14%). We estimate a precise zero effect of unleaded miles.”
  - Mortality: “We estimate a decline in elderly mortality rates of 91 deaths per 100,000 in race counties and 38 per 100,000 in border counties.”

- AER submission — CARE natural field experiment
  - Abstract: “Using a natural field experiment, we estimate the price elasticity of demand for natural gas to be about −0.35 for CARE customers… benefits to CARE customers need to increase by 6% to offset the costs of the program.”
  - Enrollment: “Letters raise enrollment by around 9.0–11.1 percentage points (p < 0.01) with little difference across behavioral variants.”
  - Heterogeneity: “Elasticities are −0.52 for very low‑income vs −0.24 for others; −0.41 for high‑usage vs −0.13 for low‑usage households.”
  - External validity: “Reweighted elasticities range from −0.31 to −0.43 (weighted) and −0.29 to −0.35 (unweighted). We use −0.35 as baseline.”

- AER manuscript — Knowledge spillovers in corporate research
  - Abstract: “Using data on 800,000 corporate publications and patent citations… private returns to corporate research depend on the balance between two opposing forces: the benefits from the use of science in own downstream inventions, and the costs of spillovers to rivals.”
  - Intro framing: “Although economists often speak of R&D as a single construct, it is useful to distinguish between research (‘R’) and development (‘D’).”
  - Contribution line: “Firms produce more research when it is used internally, but less research when it is used by rivals.”

- Bankruptcy reform (BAPCPA) manuscript
  - Model calibration: “We find an interest‑rate pass‑through of 80–113 basis points for each one‑percentage‑point change in the bankruptcy‑filing rate.”
  - Design: “We estimate the ‘excess mass’ and ‘missing mass’ of bankruptcy filings around the effective date of BAPCPA to recover a net effect of the reform.”
  - Results: “Over time… the reform reduced the bankruptcy rate by roughly 50 percent. Net of the rush‑to‑file period, ~1 million fewer filings in two years.”

- AER — Colonial medical campaigns and present‑day trust
  - Abstract: “We digitized thirty years of archival records… greater campaign exposure reduces vaccination rates and trust in medicine — as measured by willingness to consent to a blood test… World Bank projects in the health sector are less successful in areas with greater exposure.”

- AER: Insights — Optimal spatial lockdowns
  - Section flow: “Model → Data and Parametrization → Optimal Spatial Lockdowns → Conclusion”
  - Style exemplar: concise claims tied directly to the model’s objective function and calibrated parameters; headline results framed as implementable rules.

- AER proof — Conceptual framework → design → results arc
  - Sections: “Introduction; A Conceptual Framework; Design and Procedures; Results; Conclusion.”
  - Style exemplar: framework‑led exposition with procedures labeled; results tied to pre‑specified outcomes and manipulation checks.

## Auto‑Generated Per‑Paper Analyses

The following summaries were generated by the automation pass (see `paper_analysis/`).
- AEJ: Policy — leaded gasoline and elderly mortality: `paper_analysis/AEAREP-103-ssh_aea_packages_complete_aearep-1143_AEJPol-2019-0654.R2_Proof_hi.md`
- CARE — energy subsidy natural field experiment: `paper_analysis/AEAREP-103-ssh_aea_packages_complete_aearep-1556_127824_CARE_Paper_Dec2.md`
- AER: Insights — optimal spatial lockdowns: `paper_analysis/AEAREP-103-ssh_aea_packages_complete_AEAREP-1601_AERI-2020-0401.R3_Proof_hi.md`
- AER — colonial medical campaigns and trust: `paper_analysis/AEAREP-103-ssh_aea_packages_complete_aearep-1299_AER-2018-0284.R4_Proof_hi.md`
- AER — conceptual framework → design → results arc: `paper_analysis/AEAREP-103-ssh_aea_packages_complete_aearep-1793_AER-2020-0304.R2_Proof_hi.md`

To re‑run automation on all papers: `bash scripts/auto_analyze_papers.sh` (skips non‑narrative PDFs; writes Markdown per paper).
