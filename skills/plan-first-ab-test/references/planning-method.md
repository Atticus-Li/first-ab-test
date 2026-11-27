# Planning method and boundaries

## The practical question

Start with a decision, population and outcome. Statistical planning estimates the information needed for a specified effect; it does not establish that the treatment is worthwhile, that tracking works or that the effect will exist.

The helper covers a narrow common first case: two groups, 50/50 assignment, independent people, a binary conversion outcome, fixed-horizon analysis, and an increase from baseline p0 to p1. Alpha defaults to 0.05, two-sided; power defaults to 0.80. These are disclosed defaults, not a universal recommendation. No continuity correction is applied.

For delta = p1 − p0 and pbar = (p0 + p1) / 2, the normal-approximation sample per group is rounded up from:

```text
n = [z(1 − alpha/2) × sqrt(2 × pbar × (1 − pbar))
     + z(power) × sqrt(p0 × (1 − p0) + p1 × (1 − p1))]² / delta²
```

This is the same approximation used by GrowthLayer's `calculateSampleSize` function, ported into a dependency-free offline helper. GrowthLayer remains the full planner; this skill does not reproduce its broader statistics engine, integrations or results analysis. Python's standard-library normal quantiles avoid introducing a new math package. A 50% to 75% example at 90% power needs approximately 76.7 people per group before rounding, consistent with the published R example.

References:

- [R: power calculations for two-sample proportions](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/power.prop.test.html). Methods and conventions can differ; calculators need not return identical samples if they use different corrections or tests.
- [GrowthLayer planner](https://growthlayer.app/calculator/ab-test-planner). Review the selected design and assumptions when using the full planner.
- [Atticus Li's A/B testing learning path](https://atticusli.com/learn/ab-testing/). Practical planning, implementation and decision lessons.

## Traffic, time and uncertainty

Use new eligible independent people per week, not repeat visits or all-site sessions. At 50/50 allocation, enrollment days are approximately ceil(2 × n × 7 / weekly eligible people). Add the outcome follow-up after the last entrant. Weekly/calendar patterns, delays, ramp-up, exclusions and implementation constraints can lengthen the real schedule. The helper does not impose a universal minimum number of weeks.

Separate a worthwhile business effect from the design MDE. If no target effect is chosen, the helper returns 10%, 20% and 30% relative scenarios as illustrations; it does not choose among them or declare the experiment launch-ready. At a 5% baseline, a 20% relative increase is 6%, or +1 percentage point.

The helper plans a difference against zero under its stated method. Detecting a nonzero effect is a different claim from establishing that the effect exceeds a business margin. For example, an interval entirely above zero but spanning +1 percentage point can support a positive effect while leaving a +1-point minimum business requirement unresolved. Do not use an MDE as a guaranteed lower bound or quietly turn significance into proof of commercial value.

Baseline and traffic estimates can be wrong. Label rough inputs and examine sensitivity when plausible ranges materially change the recommendation. Do not silently turn a point estimate into a precise promise. If there are zero observed conversions, a missing denominator, an unstable outcome definition or only session counts, resolve measurement or get appropriate methods help.

Sparse expected successes/failures can make a normal approximation unsuitable. The helper flags an expected cell count below ten at the planned sample and withholds its numeric-window verdict. That is a heuristic review flag, not an exact-test implementation. Account-level randomization, correlated people, multiple arms, continuous outcomes, decrease-only questions or sequential designs require a matching planning method.

## Setup and decision checks

Assignment and exposure are different events. Balanced assignment does not prove correct exposure logging or an unbiased analysis population. Treatment-dependent filtering can change who enters the analysis. Investigate sample-ratio mismatch and other data-quality problems before interpreting an effect.

- [Fabijan and colleagues: diagnosing sample-ratio mismatch](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/).
- [Johari, Pekelis and Walsh: Always Valid Inference](https://arxiv.org/abs/1512.04922). Monitoring and stopping must match the inferential method; a live-updating dashboard alone does not establish sequential validity.

For the first plan, define the outcome window, analysis/stopping method, guardrails, useful business effect, rollback owner and the action if uncertainty remains. The offline script calculates no p-value, confidence interval or winner. A non-significant result is not evidence that two variants are equivalent.

These references support established methods. The skill's instructional structure is Atticus Li's synthesis; research findings remain attributed to their original authors. Examples in this package are synthetic, not client results.
