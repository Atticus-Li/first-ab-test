# A/B Testing & CRO Coach — an AI Agent Skill

Give your existing AI a practical conversion rate optimization (CRO) workflow: turn an idea into an A/B test plan, check traffic and sample size, choose an appropriate statistical approach, and prepare implementation and readout checks.

For solo founders, startup teams, product managers and developers starting experimentation. One installable skill, no analytics integration or API key required. Start with an idea; the agent asks for the missing inputs that matter.

Think of it as an A/B testing coach inside your agent. It provides planning and method-selection guidance; you remain responsible for production changes and decisions. It does not install an autonomous CRO manager or execute every statistical method.

## What can I ask it?

| Your task | A useful request | What you get |
| --- | --- | --- |
| Solo founder: first landing-page test | “Will a shorter signup form help? I don't know our baseline.” | One testable question, missing measurements and a next step. |
| Startup with limited traffic | “We get 80 eligible people a week. Is an A/B test practical?” | A feasibility assessment when inputs permit, or a focused research/improvement task. |
| PM: plan a credible experiment | “Choose our primary metric, worthwhile effect, sample and stopping rule.” | A reviewable experiment brief with assumptions and guardrails. |
| Developer: implement the plan | “Specify stable assignment, exposure events and QA for this test.” | A provider-independent implementation checklist; code drafts when requested. |
| Team: choose analysis and read results | “Is this binary conversion, revenue or account-level data? Can we call it a win?” | A method recommendation and required inputs, with uncertainty and data-quality checks. |

This first skill focuses on running a trustworthy experiment. It can frame a copy or usability hypothesis, but it is not a full landing-page audit, pricing optimizer or heatmap service.

> “We want to shorten our signup form. Help me figure out whether and how to test it.”

See a [first conversation with no analytics connection](examples/first-conversation.md) and a
[synthetic planning example](examples/planning-example.md).

The skill helps define the question, choose a meaningful metric, check whether a useful effect can be measured in time, and prepare a launch checklist. If a test is not practical, it recommends one useful learning step instead. It does not promise conversion lift or launch experiments automatically.

## What you get

- A clear control and proposed treatment, with a reason for the change.
- One primary outcome, relevant guardrails and the intended audience.
- Sample and timing estimates with visible assumptions, or a clear measurement blocker.
- Assignment/tracking checks, a decision rule and one next action.

[Statistical method selection](skills/plan-first-ab-test/references/statistical-methods.md) covers conversion rates, revenue means, sparse data, account-level tests, repeated monitoring and multiple comparisons. [Developer handoff](skills/plan-first-ab-test/references/developer-handoff.md) turns the plan into assignment, tracking and launch checks.

An idea or description is enough to start. A URL or screenshot is optional. The agent asks a few useful questions rather than requiring a long onboarding form. Unknown numbers stay unknown. It does not automatically prescribe heatmaps or require you to install an analytics product.

## Install the skill

Use an AI application that supports Agent Skills. Open Terminal in your project folder, then run:

```bash
npx skills@1.9.1 add Atticus-Li/first-ab-test --skill plan-first-ab-test --copy
```

This uses the tested version of the open Skills installer to install the skill into the compatible agent you select. That installer requires Node.js 22.20 or newer; follow your client's skill installation instructions if you prefer manual installation. The skill itself has no JavaScript packages or analytics accounts to set up. See the [Skills installer documentation](https://www.skills.sh/docs) and [Agent Skills format](https://agentskills.io/specification).

The `--copy` option keeps the installed skill independent of the extracted download folder.

If you downloaded the release ZIP, you can instead open Terminal in its extracted folder and run:

```bash
npx skills@1.9.1 add . --skill plan-first-ab-test --copy
```

Then ask your agent:

> “Use plan-first-ab-test. We think clearer onboarding instructions could help more people finish setup. Help me plan a first test.”

The install name stays **`plan-first-ab-test`**. The display name is **A/B Testing & CRO Coach**; existing prompts and installations keep the same identifier. To receive an update, run the install command again and review the installer's replacement prompt.

In clients supporting `$` invocation, use `$plan-first-ab-test`. Client discovery and installation behavior vary; a skill is not installed in every AI application merely because its files are public.

## Calculation scope

The optional helper uses Python 3.8+ and its standard library. It needs no package install, network connection, key or account. The agent runs it when the inputs and design fit. Without Python, the agent can still draft a plan and leave numerical feasibility unresolved.

It estimates sample requirements for two equally allocated groups of independent people, a binary conversion increase, and a fixed-horizon, two-sided normal-approximation analysis. The helper does not calculate a winner, confidence interval or p-value. The skill explains which analysis fits the question and can use suitable tools already available to your agent; unsupported calculations remain unresolved. Clustered outcomes, revenue averages, multiple variants, unequal allocation, sparse outcomes and sequential designs need methods appropriate to those conditions.

The offline formula follows the existing GrowthLayer sample-size approximation. [Method and limits](skills/plan-first-ab-test/references/planning-method.md). The broader [GrowthLayer planner](https://growthlayer.app/calculator/ab-test-planner) and [free learning path](https://atticusli.com/learn/ab-testing/) are optional references, not prerequisites.

## Try the calculation directly

From this extracted folder in Terminal:

```bash
python3 skills/plan-first-ab-test/scripts/plan_binary_test.py --baseline 0.05 --weekly-eligible 2000 --weeks 4 --relative-mde 0.20 --followup-days 7
```

These synthetic inputs mean a 5% baseline, 2,000 new eligible people weekly, a four-week decision window and a 20% relative effect (5% to 6%). The estimate is 8,158 people per group, about 58 enrollment days plus seven follow-up days. That sample does not fit the four-week window under those assumptions. It is not a client result or a guarantee about a real experiment.

Omit `--relative-mde` to see labeled 10%, 20% and 30% scenarios. They are illustrations, not predicted effects or a choice of business target.

## Check and contribute

Run the helper tests from this folder:

```bash
python3 -m unittest discover -s tests -v
```

Maintainers can also install the development-only validator with `python3 -m pip install -r requirements-dev.txt`
and run `python3 tests/validate_skill.py`. This checks skill metadata and packaged links; it does not
evaluate an AI model's decisions. The calculator needs none of these development packages.

[Evaluation requests](evals/cases.json) exercise the skill's judgment. Run them in a compatible agent with the skill loaded; unit tests cannot establish that an AI follows the guidance. Use synthetic or approved redacted examples when sharing issues. Explain the request, observed behavior and why it was unhelpful. Do not include customer records or credentials.

[v0.2.0 QA findings](evals/results/v0.2.0-qa.md) document the executed tasks, calculation checks, installation test and coverage limits.

## Author and license

Created by [Atticus Li](https://atticusli.com/about/) for practical, evidence-led experimentation. Credit original researchers for their findings. The [MIT license](LICENSE) applies to original files in this release; it does not license the wider website, third-party sources or customer data. Source attribution is requested in generated plans, but cannot be guaranteed by an AI system.
