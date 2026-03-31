# Splunk AI SRE Agent v0.1 Starter

A local, minimal, **agentic** proof-of-concept for Splunk incident triage using **GitHub Copilot CLI** as the reasoning harness.

This starter is intentionally shaped around:

- **alert intake**
- **hypothesis-driven investigation**
- **bounded probe tools**
- **case memory**
- **operator-grade triage output**

It is **not** a workflow runner that assumes a fixed investigation path.

## Philosophy

The repo separates responsibilities cleanly:

- **Copilot CLI custom agent** does the reasoning.
- **Python tools** provide bounded probe capabilities.
- **Case files** persist investigation state outside the model context window.
- **Runbooks** provide guardrails and escalation guidance.
- **MCP server** is the upgrade path for structured tool access.

## Current scope

v0.1 focuses on three incident families:

1. Search performance degradation
2. Indexing / ingestion degradation
3. Forwarding / data gap detection

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev,mcp]
```

If you do not want MCP yet:

```bash
pip install -e .[dev]
```

### 2. Configure your environment

Copy the example env file:

```bash
cp config/env.example .env
```

Edit `config/splunk_targets.yaml` and populate your target details.

### 3. Create a case from an alert

```bash
python -m tools.triage_case   --alert "Search latency high on prod search heads"   --target default
```

This creates a case file in `cases/open/` and seeds:
- candidate fault domains
- initial hypotheses
- suggested next probes

### 4. Render a markdown summary

```bash
python -m reports.render_case_report cases/open/<case-file>.json
```

### 5. Use with Copilot CLI

Start Copilot CLI in this repository and select the custom agent:

```text
/agent splunk-sre-agent
```

Good starter prompts:

```text
Triage the latest case in cases/open. Use the case file, prompts, and runbooks to decide the next best probe. Do not assume a fixed workflow.
```

```text
Review the alert in the newest case file, update the hypotheses, choose the highest-value next probe, and explain why.
```

## Suggested dev loop

1. Generate or paste an alert.
2. Create a case with `tools.triage_case`.
3. Let Copilot CLI reason over the case file.
4. Run bounded probes through Python modules or the MCP server.
5. Append findings to the case.
6. Render a clean markdown triage note.

## Notes

- The SPL in the probe modules is intentionally conservative starter content. Tune it for your estate.
- The MCP server is optional in v0.1, but the repo is laid out so you can switch from file/tool usage to structured MCP tool calling later.
- The code defaults to **read-only** investigation. It does not perform production changes.

## Development

Run tests:

```bash
python -m unittest discover -s tests -v
```
