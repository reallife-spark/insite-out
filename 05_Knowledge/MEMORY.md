# Memory

Standing state only; never session history.

## Repo

- Public repo: `reallife-spark/insite-out` at `/mnt/knowledge/insite-out`.
- Issue tracker: GitHub Issues; labels `needs-triage`, `ready-for-human`, `priority: critical`.
- Domain layout: single-context full model under `05_Knowledge/` plus root `GLOSSARY.md`.

## Canonical source

- Acquisition standard: official Neurosity Python SDK, v2.2.0, MIT, Python >=3.8.
- Local checkout: `/mnt/nvme/github/neurosity-sdk-python`.
- Recorded commit: `51e814fa4c4215376dcb781da3bf190b9ec3d2fc`.
- The local checkout had a modified `README.md` at capture time; that user work was left untouched.

## Boundaries

- Acquisition: `05_Knowledge/references/neurosity-python-sdk-contract.md`.
- Agent-facing: `06_Projects/insite-out/feedback-event-contract.md`.
- Background only: Jetson, TensorRT-DLA, DeepStream and dual-Xavier material under
  `05_Knowledge/references/web/streaming-eeg-feedback-sources.md`.

## Current implementation state

Documentation and source capture only. No runtime code exists yet.
