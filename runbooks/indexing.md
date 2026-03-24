# Runbook: Indexing / Ingestion Degradation

## Typical symptoms

- ingest rate drops
- indexing delay rises
- queues appear stressed
- some peers look abnormal
- HEC or parsing paths look unhealthy

## Broad probes

- health_overview
- indexing_pipeline_stress
- resource_pressure
- recent_internal_errors
- baseline_lookup

## Common fault domains

- pipeline contention
- parsing bottleneck
- receiver-side pressure
- source-side burst or data shape change
- node-specific resource stress

## Escalate when

- multiple peers degrade together
- changes to indexing or pipeline settings are required
- symptoms point to cluster-level capacity issues
