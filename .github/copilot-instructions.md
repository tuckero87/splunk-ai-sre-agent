# Splunk AI SRE Agent Repository Instructions

This repository is a local proof-of-concept for an **agentic Splunk SRE investigator**.

## Primary goal

Use alert context plus gathered evidence to reason about the next best probe. Do **not** assume a fixed search chain unless the user explicitly asks for one.

## Working model

- Treat the incoming alert or anomaly as a starting point, not a conclusion.
- Build and refine hypotheses as evidence arrives.
- Prefer broad and cheap probes before narrow and expensive probes.
- Avoid repeating equivalent probes unless the case state shows a real reason to re-run them.
- Update the case file after each meaningful step.
- Separate facts, hypotheses, and recommended actions clearly.

## Tooling expectations

- Prefer the existing Python tool modules or MCP tools over inventing ad hoc shell pipelines.
- Keep Splunk access read-only unless a future policy file explicitly permits an action.
- Keep probe logic reusable. A probe is an investigation primitive, not a case-specific workflow.

## Case handling

- Case files under `cases/open/` and `cases/closed/` are the source of operational memory.
- Append concise investigation steps to the case file rather than relying on chat history.
- Never write chain-of-thought into case files. Write operational summaries only.

## Safety constraints

- Do not modify Splunk configs, restart services, disable searches, or change routing.
- Do not add hidden side effects to probe functions.
- Escalate when confidence is low, blast radius is unclear, or a runbook crosses into L3 / platform engineering territory.

## Coding expectations

- Keep changes iterative and focused.
- Maintain type hints and docstrings.
- Prefer plain Python and explicit data structures over clever abstractions.
- Preserve the local-first design.
