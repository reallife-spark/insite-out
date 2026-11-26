# ADR 0002 — Feedback event as the only agent-facing boundary

- Status: accepted
- Date: 2026-11-26

## Context

EEG sources are heterogeneous: 16-sample epochs roughly every 62.5 ms, band powers, slow awareness
probabilities with a ~16 s warm-up, and sparse Kinesis detections. Agents need typed meaning,
confidence, readiness and timestamps; they cannot act directly on electrode arrays or raw
probabilities. ADR 0001 fixes the acquisition boundary but not the consumer boundary.

## Decision

Agents consume only **feedback events** as defined in
`06_Projects/insite-out/feedback-event-contract.md`. Raw epochs, PSD arrays and SDK metric payloads
never cross into the agent-facing interface. Every event carries kind, value, confidence,
readiness, source timestamp, emission time and provenance; warm-up is represented explicitly and
never as zero-valued user state.

## Consequences

- The agent-facing contract is stable even if the transport later changes from SDK Firebase streams
  to LSL or OSC.
- Interpretation must translate, not forward; this is where readiness and confidence are assigned.
- Consumers ignore unknown fields, so the contract can grow without breaking them.

## Alternatives considered

- **Forward raw streams to the model**: simpler but forces the model to understand electrode order,
  filtering and device-specific cadence, and makes warm-up indistinguishable from low scores.
- **Expose metrics directly**: loses provenance and readiness, and ties the agent to SDK naming.
