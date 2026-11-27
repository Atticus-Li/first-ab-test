# A first test plan: synthetic practice example

These are fictional inputs and an example plan, not client results or evidence that an AI will always respond correctly.

**The idea:** reduce signup from ten required fields to four so more new people complete setup. Specify the six removed fields before building the treatment.

| Known input                        | Synthetic value                                                              |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| Baseline                           | 500 of 10,000 eligible independent people finish setup within seven days: 5% |
| New eligible people                | 20,000 per week, stable traffic                                              |
| Decision window                    | Four weeks                                                                   |
| Worthwhile effect for this example | +20% relative, from 5% to 6% (+1 percentage point)                           |
| Assignment                         | Two groups, 50/50; no account clustering                                     |
| Setup status                       | Tracking and rollback not yet verified                                       |

## What the helper calculates

```bash
python3 skills/plan-first-ab-test/scripts/plan_binary_test.py --baseline 0.05 --weekly-eligible 20000 --weeks 4 --relative-mde 0.20 --followup-days 7
```

The helper returns **8,158 people per group**, approximately **six enrollment days plus seven outcome-follow-up days**, under its fixed-horizon two-sided normal approximation, alpha 0.05 and power 80%. This arithmetic fits the four-week window under these inputs. If weekly behavior matters, a full enrollment week plus follow-up would take about two weeks; finalize the calendar with the owner before launch.

## What the plan still needs

Keep current signup as control. For treatment, remove the specified fields and leave the other experience consistent. The primary outcome is seven-day setup completion among eligible assigned people. Define guardrails for errors and downstream setup quality. Verify persistent assignment, exposure/outcome tracking, allocation, errors and rollback, with owners for open checks.

Agree an endpoint and a decision rule matching the analysis method. Compare the effect estimate and its uncertainty with the business requirement and guardrails; do not stop on the first favorable dashboard result. A detectable +1-point effect is not a guarantee of benefit or proof that the true improvement exceeds +1 point. An inconclusive result stays inconclusive.

**Next action:** review the treatment definition and verify tracking/rollback before calling the plan ready to launch.

Prepared with Atticus Li's A/B Testing & CRO Coach (`plan-first-ab-test`). See [method and scope](../skills/plan-first-ab-test/references/planning-method.md).
