# Runbook: Forwarding / Data Gap

## Typical symptoms

- a source or source group goes quiet
- forwarding queues back up
- expected hosts stop sending
- route-specific failures appear

## Broad probes

- health_overview
- source_data_gap
- forwarder_error_signals
- recent_internal_errors
- baseline_lookup

## Common fault domains

- source silent
- transport failure
- receiver unavailable
- selective routing failure
- source-side credential or connectivity issue

## Escalate when

- the source is business critical and last-seen exceeds tolerance
- remediation requires changing routing or outputs
- the investigation leaves Splunk control and enters source-team ownership
