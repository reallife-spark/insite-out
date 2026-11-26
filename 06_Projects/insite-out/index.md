---
title: insite-out — streaming EEG feedback for agents
status: active
updated: 2026-11-26
---

# insite-out project hub

The project turns a live stream of user EEG into model-interpretable **feedback events** that an
agent can consume as input to its next action.

## Scope

In scope:

- acquire Crown streams through the official Neurosity Python SDK (the programming standard);
- acquire live Watch5 Pro metrics through the Samsung Health Sensor SDK on a Wear OS companion app;
- one canonical acquisition adapter per source, with source payload shapes preserved at the boundary;
- interpret epochs, band powers, Focus, Calm, Kinesis and Watch metrics into typed feedback events;
- maintain an agent-facing contract with readiness, freshness and structured provenance.

Out of scope for now:

- Jetson / TensorRT-DLA / DeepStream deployment details from the originating answer — background reference only;
- replacing the SDK transport with LSL or OSC;
- training an EEG classifier.

## Owned documents

- `06_Projects/insite-out/physiological-feedback-spec.md` — spec for Crown and Watch5 Pro feedback.
- `06_Projects/insite-out/feedback-event-contract.md` — the agent-facing schema and failure modes.
- `06_Projects/insite-out/watch-metric-vocabulary.md` — first live Watch metric set, units and readiness.
- `06_Projects/insite-out/composed-physiological-state-design.md` — deferred, design-only correlation.
- `docs/adr/0001-neurosity-sdk-acquisition-boundary.md` — one canonical adapter per source.
- `docs/adr/0002-feedback-event-as-agent-boundary.md` — feedback event as the only agent-facing shape.
- `docs/adr/0003-watch-acquisition-adapter.md` — Wear OS adapter and local-only bridge.
- `docs/adr/0004-advisory-only-authority.md` — advisory-only rule and direct-trigger follow-up.
- `docs/adr/0005-composed-state-deferred.md` — parallel events stand; fusion stays design-only.
- `05_Knowledge/references/neurosity-python-sdk-contract.md` — distilled SDK contract.
- `05_Knowledge/references/web/streaming-eeg-feedback-sources.md` — depth-one source synthesis.
- `05_Knowledge/synthesis/stream-to-feedback-boundary.md` — cross-cutting design conclusion.

## Current state

The feedback-event envelope, Crown adapter and the complete Watch metric set (via a local-only
bridge) are implemented and tested at the agent-facing seam. Advisory-only authority is recorded and
composed physiological state has a reviewed design. No further implementation is planned; all seven
sub-issues await human review.
