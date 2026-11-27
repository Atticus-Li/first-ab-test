# Which statistical calculation fits this A/B test?

Choose the method from the question and design, before inspecting which method gives the most favorable answer. This is routing guidance, not an implementation of every method below. Use suitable tested tools or request methodological review when needed.

## First identify the claim

What decision matters: any difference, a useful increase, avoiding unacceptable harm, or equivalence within a margin? Identify the outcome and window, independent randomization unit, analysis population, allocation and stopping rule. Clarify which comparisons are confirmatory. A design MDE is not a guaranteed minimum benefit.

## Route by metric and design

| Situation | Suitable starting approach | Inputs and boundaries |
| --- | --- | --- |
| Binary conversion, two independent groups, fixed endpoint | Two-proportion inference with an effect estimate and a suitable confidence interval; a large-sample two-sided z test is a common test of equal proportions. | Successes and eligible units per arm, identical follow-up and valid assignment. Report absolute percentage-point change as well as relative lift when the control rate is nonzero. A p-value is not an effect size or the probability the treatment is better. |
| Planning that binary test, 50/50 allocation and an increase | Bundled approximate sample-size helper. | Baseline, planning effect, eligible independent people, deadline, follow-up, alpha and power. It does not compute the readout. See [planning-method.md](planning-method.md). |
| Sparse binary outcomes or zero events | Consider Fisher's exact test for an independent 2×2 table and an appropriate interval for the chosen effect measure; seek matching sample-planning support. | An exact test does not create power or precision. Do not add fake successes, use a zero observed rate as a known population rate, or turn a sparse-data flag into a launch recommendation. |
| Mean revenue, time or another numerical outcome per independent unit | For independent groups, consider Welch's two-sample t method for a mean difference, after checking whether its assumptions and sample behavior are adequate. | Need unit-level data or sample size, mean and variance per arm. Include eligible nonpayers as zero when estimating revenue per eligible person; revenue per purchaser is a different metric and may condition on treatment outcomes. Heavy tails or small samples can need tailored robust/resampling methods and review. No universal sample follows from a baseline conversion rate. |
| Several observations per person or teammates sharing an account | Respect the randomized unit and dependence. Define an account-level outcome or use design-appropriate cluster-aware estimation. | Need independent account counts, sizes, outcome definition and within-account dependence for planning. Do not count events, teammates or sessions as independent sample size. Account aggregation can change the estimand; state whether accounts or people receive equal weight. |
| Ratios such as revenue per session | Define the ratio estimand and use inference that accounts for numerator/denominator covariance and the randomized unit, such as an appropriate delta-method estimator. | A ratio of totals differs from a mean of individual ratios. Repeated sessions are correlated; neither a binary calculator nor an ordinary t test on sessions automatically fits. |
| Continuous efficacy monitoring or stopping as soon as results look good | Use a specified sequential design with its matching analysis, such as always-valid inference, or retain the precommitted fixed endpoint. | A dashboard updating daily does not establish validity. Do not attach an ordinary fixed-horizon p-value or interval to optional stopping as if the plan were unchanged. |
| Several variants, endpoints or searched subgroups | Specify the comparison family and error-control goal in advance. Holm is one option for family-wise error control; false-discovery-rate methods address a different goal. | Sample planning and intervals must also fit the design. Do not test every segment and present only a favorable unadjusted finding. Exploratory findings should be labeled and independently checked. |
| Noninferiority, equivalence or a minimum business margin | Use an explicit margin-based design and corresponding test/interval. | Choose the margin and direction before results. Failure to reject equality does not establish equivalence. An interval above zero but crossing a required +1-point benefit leaves that commercial claim unresolved. |

These rows can combine: a clustered, multi-arm revenue test needs all relevant design conditions addressed. Paired observations, unequal allocation, time-to-event outcomes and interference across units require their own design choices rather than being forced into a row that only partly fits.

## Give a useful readout

Before a numerical verdict, verify the original plan, exposure/outcome logging, allocation and follow-up. Check sample-ratio mismatch at the correct assignment unit. Do not remove unfavorable users or condition the analysis on an action the treatment can change. Identify missing outcomes and exclusions.

Report the method, denominators, effect estimate and uncertainty against the business threshold and guardrails. If the interval permits materially different decisions, call the evidence inconclusive. If the original team stopped opportunistically, record that limitation; do not retroactively claim sequential validity. Recommend a suitable reanalysis if possible or a new preplanned experiment. Do not invent a correction without the required monitoring history and method.

Without an appropriate calculation tool, return the method and required data, not a fabricated p-value or winner. Explain the next calculation in plain language. Respect privacy: aggregate counts can suffice for some binary analyses; never ask users to publish customer records.

## Primary references

- [NIST: comparing two proportions, including small samples](https://www.itl.nist.gov/div898/handbook/prc/section3/prc33.htm).
- [NIST: two-sample t methods, including unequal variance and nonzero differences](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm).
- [Microsoft Research: challenges of tenant-randomized tests](https://www.microsoft.com/en-us/research/articles/why-tenant-randomized-a-b-test-is-challenging-and-tenant-pairing-may-not-work/).
- [Deng, Knoblich and Lu: Applying the Delta Method in Metric Analytics](https://www.microsoft.com/en-us/research/publication/applying-the-delta-method-in-metric-analytics-a-practical-guide-with-novel-ideas/).
- [Johari, Pekelis and Walsh: Always Valid Inference](https://arxiv.org/abs/1512.04922).
- [R documentation: multiple-comparison adjustments and their error-control goals](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html).

The routing and teaching structure are Atticus Li's synthesis. Statistical findings remain credited to the original sources.
