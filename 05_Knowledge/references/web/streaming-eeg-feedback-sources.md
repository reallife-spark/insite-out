---
title: Streaming EEG feedback — depth-one source synthesis
status: distilled
root_source: https://share.google/aimode/mhgoDgYotEKcIHMGo
captures:
  - 03_Sources/web/ai-mode-eeg-jetson-answer.md
  - 03_Sources/web/neurosity-brainwaves-api.md
  - 03_Sources/web/neurosity-osc-api.md
  - 03_Sources/web/neurosity-neurosity-class.md
  - 03_Sources/web/neurosity-realtime-vs-offline-eeg.md
  - 03_Sources/web/neurosity-sdk-python-repo.md
  - 03_Sources/web/jetson-stats-repo.md
  - 03_Sources/web/nvidia-forums-hw-engines.md
  - 03_Sources/web/nvidia-forums-nvpmodel.md
  - 03_Sources/web/liblsl-repo.md
---

# Streaming EEG feedback — depth-one source synthesis

All citations below point at immutable captures under `03_Sources/web/`. The originating Google
AI Mode answer was CAPTCHA-blocked on direct fetch and was supplied by the user as rendered text;
the depth-one pages were fetched with defuddle 0.19.13 on 2026-11-26.

Each capture's `content_sha256` is SHA-256 of its Markdown body after the frontmatter, with leading
and trailing whitespace stripped. Two-space Markdown hard breaks inside the body are preserved as
part of the immutable capture; `.gitattributes` exempts those lines from `git diff --check`.

## What this project is, from the source

The AI answer's relevant part is the description of a live EEG stream from a Neurosity Crown:
8 channels at 256 Hz, band powers, on-device Focus and Calm probabilities, trained Kinesis
commands, and telemetry. The answer then proposes a particular Jetson/DeepStream deployment. The
deployment is **background context** for `insite-out`; the durable idea is the stream-to-feedback
boundary: raw neural data is interpreted into a small set of signals an agent can act on.

## Acquisition and payload facts

`neurosity-brainwaves-api.md` confirms four brainwave metrics — `raw`, `rawUnfiltered`, `psd`,
`powerByBand`; Crown epochs of 16 samples every ~62.5 ms; channel order
`CP3, C3, F5, PO3, PO4, F6, C4, CP4`; on-device notch (50/60 Hz) and 2–45 Hz Butterworth
bandpass. `neurosity-osc-api.md` describes the OSC path and raw-mode sample rate;
`neurosity-neurosity-class.md` documents the JavaScript class and its observable streams.
`neurosity-realtime-vs-offline-eeg.md` separates live streaming from recorded analysis and lists
the real-time streams available from the SDK.

`neurosity-sdk-python-repo.md` is the web view of the local authoritative checkout; the distilled
contract is `05_Knowledge/references/neurosity-python-sdk-contract.md`.

## Timing and feedback semantics

Focus and Calm are probabilities in 0.0–1.0 and take up to ~16 seconds to initialise. A feedback
layer must therefore distinguish an uninitialised metric from a low score, and should carry a
timestamp and a confidence or readiness signal rather than a bare number. Kinesis is a spike
detection over motor-imagery predictions, so it naturally maps to an event, not a continuous level.

## Local transport option

`neurosity-osc-api.md` and the AI answer both describe OSC and LSL as local-network alternatives
to the SDK's Firebase transport. `liblsl-repo.md` captures the LSL implementation used for local
low-latency streams. This repo records the option but does not adopt it as the acquisition
standard: the official Python SDK is the standard.

## Background: Jetson hardware engines

`jetson-stats-repo.md`, `nvidia-forums-hw-engines.md` and `nvidia-forums-nvpmodel.md` explain why
jtop shows DLA, NVENC, NVDEC, VIC and PVA as `[OFF]`: those engines are on demand and show an
active clock only when a workload uses them. The AI answer's TensorRT `--useDLACore` and
DeepStream `enable-dla=1` guidance is consistent with those threads. This material is retained as
background only and is not a committed dependency of `insite-out`.

## Source quality note

The AI answer contains a truncated clone URL (`https://github.com` for liblsl) and advises a
JetPack 5.1.x / DeepStream 6.3 stack that may be stale. Claims from that answer are not treated as
authoritative without a primary-source capture.
