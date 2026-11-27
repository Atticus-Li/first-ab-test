# Plan My First A/B Test

Give your AI an idea. Get a practical first experiment plan—and understand the choices behind it.

For founders, new product managers and teams starting experimentation. One skill, no analytics integration or API key required.

> “We want to shorten our signup form. Help me figure out whether and how to test it.”

See a [first conversation with no analytics connection](examples/first-conversation.md) and a
[synthetic planning example](examples/planning-example.md).

The skill helps define the question, choose a meaningful metric, check whether a useful effect can be measured in time, and prepare a launch checklist. If a test is not practical, it recommends one useful learning step instead. It does not promise conversion lift or launch experiments automatically.

## What you get

- A clear control and proposed treatment, with a reason for the change.
- One primary outcome, relevant guardrails and the intended audience.
- Sample and timing estimates with visible assumptions, or a clear measurement blocker.
- Assignment/tracking checks, a decision rule and one next action.

An idea or description is enough to start. A URL or screenshot is optional. The agent asks a few useful questions rather than requiring a long onboarding form. Unknown numbers stay unknown. It does not automatically prescribe heatmaps or require you to install an analytics product.

## Install the skill

Use an AI application that supports Agent Skills. Open Terminal in your project folder, then run:

```bash
npx skills add Atticus-Li/first-ab-test --skill plan-first-ab-test --copy
```

This uses the open Skills installer to install the skill into the compatible agent you select. The installer requires Node.js 22.20 or newer; follow your client's skill installation instructions if you prefer manual installation. The skill itself has no JavaScript packages or analytics accounts to set up. See the [Skills installer documentation](https://www.skills.sh/docs) and [Agent Skills format](https://agentskills.io/specification).

The `--copy` option keeps the installed skill independent of the extracted download folder.

If you downloaded the release ZIP, you can instead open Terminal in its extracted folder and run:

```bash
npx skills add . --skill plan-first-ab-test --copy
```

Then ask your agent:

> “Use plan-first-ab-test. We think clearer onboarding instructions could help more people finish setup. Help me plan a first test.”

In clients supporting `$` invocation, use `$plan-first-ab-test`. Client discovery and installation behavior vary; a skill is not installed in every AI application merely because its files are public.

## Calculation scope

The optional helper uses Python 3.8+ and its standard library. It needs no package install, network connection, key or account. The agent runs it when the inputs and design fit. Without Python, the agent can still draft a plan and leave numerical feasibility unresolved.

It estimates sample requirements for two equally allocated groups of independent people, a binary conversion increase, and a fixed-horizon, two-sided normal-approximation analysis. It is not a results analyzer or a complete statistics engine. Clustered outcomes, revenue averages, multiple variants, unequal allocation, sparse outcomes and sequential designs need methods appropriate to those conditions.

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

## Author and license

Created by [Atticus Li](https://atticusli.com/about/) for practical, evidence-led experimentation. Credit original researchers for their findings. The [MIT license](LICENSE) applies to original files in this release; it does not license the wider website, third-party sources or customer data. Source attribution is requested in generated plans, but cannot be guaranteed by an AI system.
