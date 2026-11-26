# Repository agent instructions

Start here for work in `insite-out`. The numbered spine is canonical:

- `00_System/`: steering, purpose, navigation and log.
- `01_Inbox/`: unprocessed inputs; `01_Inbox/web/` holds captured web sources.
- `02_Daily/`: session records, `PLAN.md` (`current:` names the active step) and `hot.md`.
- `03_Sources/`: immutable accepted sources, including the local SDK manifest.
- `04_Evergreen/`: durable notes.
- `05_Knowledge/`: `MEMORY.md`, full domain model and distilled references.
- `06_Projects/`: projects owned by this repo.
- `07_Archives/`: superseded material.

Canonical copies live in their numbered directories; the matching names at the repo root are relative symlinks. Keep the symlinks resolving.

## Agent skills

### Issue tracker

GitHub Issues on `reallife-spark/insite-out`. See `docs/agents/issue-tracker.md`.

### Triage labels

Home standard set: `needs-triage`, `ready-for-human`, `priority: critical`. See
`docs/agents/triage-labels.md` for the mapping from the five canonical roles.

### Domain docs

Single-context repo with a full domain model: root `GLOSSARY.md`,
`05_Knowledge/concepts/`, `05_Knowledge/synthesis/`, `05_Knowledge/references/` and
`docs/adr/`. See `docs/agents/domain.md`.

## Project invariants

- The official Neurosity Python SDK is the acquisition standard and programming boundary. Its
  checkout stays external; read `05_Knowledge/references/neurosity-python-sdk-contract.md` before
  touching stream assumptions.
- Agents consume only feedback events defined by
  `06_Projects/insite-out/feedback-event-contract.md`; raw epochs and SDK metric payloads do not
  cross that boundary.
- Jetson, TensorRT-DLA, DeepStream and dual-Xavier material is background context only, not
  committed architecture.
- Credentials stay in the environment or a secret store. Never write them into this repo.
- Repo-scoped docs, ADRs, plans and instructions stay here; cross-repo pointers stay in Home.

## Working rules

- Write session detail to `02_Daily/YYYY-MM-DD.md`; append to `00_System/log.md` when a step advances.
- Use the glossary vocabulary in issues, specs and code comments.
- Do not commit unless explicitly requested.
