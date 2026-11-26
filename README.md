# insite-out

Streaming EEG interpreted as model-interpretable feedback for agents.

`insite-out` acquires live EEG through the official Neurosity Python SDK and translates the SDK's
streams into typed feedback events an agent can consume. The SDK is the programming standard; its
checkout stays external at `/mnt/nvme/github/neurosity-sdk-python`. Jetson, TensorRT-DLA,
DeepStream and dual-Xavier material is background reference only.

## Current state

The agent-facing feedback-event envelope, the Crown acquisition adapter and all four approved Watch
metrics are implemented and tested through a local-only bridge. Advisory-only authority is recorded
and composed physiological state has a deferred, design-only specification. The repo uses the full
numbered vault spine; root identity names are symlinks into it.

## Read first

1. `AGENTS.md` — operating rules and boundaries.
2. `00_System/MISSION.md` and `00_System/INTENT.md` — purpose and invariants.
3. `05_Knowledge/MEMORY.md` and `02_Daily/PLAN.md` — standing state and active work.
4. `06_Projects/insite-out/index.md` — project hub.
5. `05_Knowledge/references/neurosity-python-sdk-contract.md` — acquisition contract.
6. `06_Projects/insite-out/feedback-event-contract.md` — agent-facing contract.
7. `docs/adr/` — decisions.

## Sources

- Captured web sources: `03_Sources/web/`.
- Local authoritative SDK manifest: `03_Sources/local/neurosity-sdk-python.md`.
- Depth-one synthesis: `05_Knowledge/references/web/streaming-eeg-feedback-sources.md`.

## Development

Run the test suite from the repo root:

```sh
python3 -m pytest
```

The tests exercise the agent-facing feedback-event stream only; no SDK internals are imported.

## Conventions

- GitHub Issues on `reallife-spark/insite-out`; see `docs/agents/issue-tracker.md`.
- Triage labels: `needs-triage`, `ready-for-human`, `priority: critical`.
- Do not commit unless explicitly requested.
