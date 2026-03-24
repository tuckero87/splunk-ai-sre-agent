# Runbook: Search Performance Degradation

## Typical symptoms

- Search latency is high
- Scheduler skips increase
- Saved searches miss schedule windows
- One app, role, or service account dominates search load

## Broad probes

- health_overview
- search_scheduler_pressure
- top_search_offenders
- resource_pressure
- recent_internal_errors

## Common fault domains

- scheduler pressure
- ad hoc concurrency bursts
- one expensive search family
- host resource contention
- recent app or knowledge-object change

## Escalate when

- multiple search heads are degraded with no obvious actor
- cluster-level behavior is unstable
- a remediation would require workload or config changes
