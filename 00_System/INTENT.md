# Intent

Invariants that must hold for this repo:

- The numbered spine `00_` through `07_` stays in place and root identity names stay symlinked to it.
- Repo-scoped material stays in this repo; cross-repo material stays in Home.
- The official Neurosity Python SDK remains the acquisition boundary; no parallel EEG transport is
  added inside the feedback layer.
- Raw epochs, PSD arrays and SDK metric payloads never cross into the agent-facing interface;
  agents consume only feedback events.
- SDK payload shapes, channel order, epoch cadence and unsubscribe lifecycle are not redefined
  locally without re-reading the authoritative checkout.
- Jetson, TensorRT-DLA, DeepStream and dual-Xavier guidance remains background reference only.
- Credentials and SDK configuration values are never stored in this repo.
- The engineering-skill setup is recorded in `docs/agents/`; do not re-run it unless the tracker,
  label vocabulary or domain layout changes.
