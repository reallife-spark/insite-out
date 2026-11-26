# ADR 0001 — One canonical acquisition adapter per source

- Status: accepted (amended 2026-11-26)
- Date: 2026-11-26

## Context

The originating AI answer describes several ways to get EEG off a headset: the Neurosity Python
and JavaScript SDKs, LSL, OSC, and a custom Jetson pipeline. The project now has two physiological
sources: the Neurosity Crown and the Samsung Galaxy Watch5 Pro. Each needs one authoritative way
for samples or metric events to enter the repo. The user supplied an authoritative local checkout
of the official Neurosity SDK at `/mnt/nvme/github/neurosity-sdk-python`, remote
`https://github.com/neurosity/neurosity-sdk-python.git`, MIT, version 2.2.0.

## Decision

There is **one canonical acquisition adapter per source**. The official Neurosity Python SDK is the
binding standard and acquisition adapter for Crown EEG. The Samsung Health Sensor SDK running on a
Wear OS companion app is the binding standard for live Galaxy Watch5 Pro metrics; that adapter is
specified in a later ticket and ADR. For either source, this repo does not fork the SDK, copy its
source into this repo, or redefine its payload shapes locally. The checkout stays external; this
repo records provenance, commit SHA and a distilled contract. Source lifecycle conventions — the
SDK's callback-plus-`unsubscribe` lifecycle for the Crown and tracker teardown for the Watch — are
binding at their respective boundaries.

LSL and OSC remain documented local-network options, but they are not the default acquisition path.
ADR 0002 continues to define the feedback event as the only agent-facing boundary.

## Consequences

- Adding a source requires naming its canonical adapter before building interpretation code.
- Payload shapes and stream lifecycle come from the recorded SDK version for that source; changing
  that assumption requires re-reading the source and amending its contract reference.
- Interpretation code sits after each acquisition boundary, never inside a replacement transport.
- The Jetson, TensorRT and DeepStream guidance in the source answer is background only and does not
  create a dependency for this repo.
- The phone's Samsung Health Data SDK is for slow stored aggregates, not the live feedback loop.

## Alternatives considered

- **One global SDK boundary**: rejected because a Watch adapter cannot satisfy a Crown-only SDK
  decision without contradiction.
- **LSL/OSC as primary**: lower latency and local-only, but not the official source SDK and would
  create a second acquisition standard.
- **Custom Jetson pipeline**: matches the source answer's deployment sketch but couples the project
  to specific hardware before the feedback contract is settled.
