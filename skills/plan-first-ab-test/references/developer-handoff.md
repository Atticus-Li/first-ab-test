# Turn an agreed A/B test plan into implementation checks

Start from the approved question, metric and design. Reuse the existing stack. If those choices are missing, resolve only the inputs that change implementation. A code draft is not proof that production tracking or randomization works.

## Specify the contract

- **Identity and assignment:** experiment ID/version, eligibility, independent randomization unit, allocation and stable assignment. Define persistence across refreshes, devices and anonymous-to-signed-in transitions. Keep the same account in one variant when teammates share the experience. Do not randomize afresh on every request.
- **Exposure:** define when a unit enters the analysis and when the assigned experience is actually rendered. Log assignment and exposure distinctly where applicable. An exposure filter affected by treatment can bias the comparison; document the analysis population before launch.
- **Outcomes:** define the primary outcome window and deduplication unit. Specify whether events represent attempts or successful completion; reconcile successful payment/setup with the authoritative backend when relevant. Record timestamps, experiment version, variant and pseudonymous unit keys using existing data controls. Do not log secrets or unnecessary personal information.
- **Operations:** owner, errors/harm checks, allocation investigation, rollout/ramp behavior and rollback. Changing allocation or treatment mid-test can change interpretation; version and document material changes rather than silently pooling them.

## Reviewable staging QA

1. Verify repeat visits retain assignment and ineligible units receive the intended default. Test authentication transitions and shared-account consistency where relevant.
2. Force each variant in staging and confirm the experience, mobile interaction and accessibility. Separate forced QA traffic from the experiment population.
3. Reconcile assignment, rendered exposure and backend outcomes on synthetic journeys. Check duplicate events, missing IDs, delayed outcomes and timestamp/window handling.
4. Check expected allocation over a suitable sample at the assignment unit. Investigate sample-ratio mismatch rather than silently balancing or deleting records. A tiny random sample need not be exactly 50/50.
5. Exercise rollback and verify what happens to ongoing participants and outcome collection. Label unexecuted checks as pending.

For a shared workspace dashboard, for example, assign by a stable workspace key so teammates see one variant; renewal is an account outcome. Session totals do not supply the independent workspace count. Do not use the bundled person-level calculator for that design.

Return the proposed contract, a small implementation/code change if requested, checks actually run and remaining launch blockers. Deployment still requires the user's applicable authorization. This skill does not require PostHog, an MCP server, a feature-flag SDK or a new account.

Method references: [statistical selection](statistical-methods.md) and [sample-ratio mismatch research](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/).
