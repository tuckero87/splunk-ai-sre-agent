# Splunk AI SRE Agent

Proof-of-concept repo starter for a **Splunk AI SRE assistant** that runs locally and uses **GitHub Copilot CLI** as the operator-facing harness.

The repo is intentionally small:

- **Collectors** gather a few Splunk operational signals.
- **Detectors** convert those signals into incident candidates.
- **Reports** render machine- and human-friendly incident outputs.
- **Runbooks** give the agent and operator a safe next-step path.
- **State** stores snapshots and incident artifacts locally.

This starter is designed for a read-only, low-risk first pass. It focuses on three incident families:

1. Search performance degradation
2. Indexing / ingestion degradation
3. Forwarding / data gap detection

## Repo layout

```text
.github/
  agents/
collectors/
config/
detectors/
prompts/
reports/
runbooks/
shared/
state/
tests/
tools/
```

## Quick start

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2. Create local environment variables

```bash
cp config/env.example .env
set -a
source .env
set +a
```

### 3. Edit target and rule config

Start with:

- `config/splunk_targets.yaml`
- `config/rules.yaml`

The sample SPL is intentionally conservative and may need tuning for your Splunk version and logging patterns.

### 4. Collect signals and detect incidents

```bash
./tools/collect_all.sh
./tools/detect_all.sh
./tools/triage_latest.sh
```

## Running with GitHub Copilot CLI

This repo includes:

- repository-wide instructions in `.github/copilot-instructions.md`
- a project-scoped custom agent profile in `.github/agents/splunk-sre-agent.agent.md`

Example usage:

```bash
copilot
```

Then in the interactive session:

```text
/agent splunk-sre-agent
Collect current Splunk signals, run all detectors, and summarize any active incidents.
```

Or programmatically:

```bash
copilot --agent splunk-sre-agent \
  --allow-tool='shell(python:*)' \
  --allow-tool='shell(bash:*)' \
  --allow-tool='write(state/*)' \
  --prompt "Collect current Splunk signals, run all detectors, and summarize any active incidents."
```

## Security model for v0.1

Use a **read-only Splunk service account** where possible.

This starter assumes:

- read-only REST access to health/search endpoints
- read-only SPL against operational indexes used by the collectors
- no write-back into Splunk
- all mutable outputs stay inside `state/`

## Default flow

1. Collectors write raw normalized snapshots into `state/snapshots/`
2. Detectors read the latest snapshots and create JSON incidents in `state/incidents/`
3. Reports render markdown summaries for the latest incidents
4. Copilot CLI reads those artifacts and helps with triage and next steps

## Notes

- The detector logic is intentionally simple and deterministic.
- The sample SPL is a starting point, not a final production content pack.
- The repo is structured so you can later add MCP, GitHub issue creation, richer baselines, or approval-gated actions without redesigning the whole thing.

## Roadmap

v0.1

Local repo, local scripts, Copilot CLI harness, three detectors, markdown incident output.

v0.2

Add:

baseline comparison
GitHub issue output
richer runbooks
more structured confidence scoring
v0.3

Add:

MCP wrapper around collectors and detectors
approval-gated write actions
separate specialist agents:
search-sre
indexing-sre
forwarding-sre
v1 candidate

Package it as a controlled internal tool with policy, RBAC, logging, and approved integrations.
