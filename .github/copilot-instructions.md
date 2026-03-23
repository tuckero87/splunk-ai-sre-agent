## Project purpose
- This repository implements a local proof-of-concept Splunk AI SRE assistant.
- Prefer minimal, safe, incremental changes.
- Keep the design easy to run on a laptop.

## Safety boundaries
- Default to read-only behavior against Splunk.
- Never introduce autonomous production-changing behavior unless explicitly requested.
- Do not add actions that restart services, disable searches, change Splunk configs, or modify production routing unless a human asks for that specifically.

## Engineering rules
- Prefer deterministic Python scripts over one-off shell pipelines.
- Reuse existing helpers in `shared/` before adding new utility modules.
- Keep file formats stable and machine-readable.
- Write structured JSON for snapshots and incidents.
- Keep markdown incident reports concise and operator-friendly.

## Code style
- Use Python 3.12+.
- Add docstrings to public functions.
- Use type hints.
- Fail with clear error messages.
- Avoid unnecessary dependencies.

## Workflow
- Plan changes before editing.
- Make iterative changes in small chunks.
- After code changes, run focused tests or linters when practical.
- Preserve the current repo layout unless there is a strong reason to change it.

## Incident logic expectations
- Separate collection, detection, and reporting concerns.
- Keep detectors explainable.
- Prefer explicit thresholds and evidence lists over opaque scoring.
- Always include recommended next steps in incident outputs.
