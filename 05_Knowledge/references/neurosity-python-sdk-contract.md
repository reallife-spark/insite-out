---
title: Neurosity Python SDK — canonical acquisition contract
status: distilled
source: "03_Sources/local/neurosity-sdk-python.md"
source_url: https://github.com/neurosity/neurosity-sdk-python
commit: 51e814fa4c4215376dcb781da3bf190b9ec3d2fc
---

# Neurosity Python SDK — canonical acquisition contract

This page states the acquisition rules `insite-out` follows. It is derived from the local
authoritative checkout; the SDK itself stays external.

## Package facts

- Distribution `neurosity`, version **2.2.0**, Python **>=3.8**, MIT licensed.
- Runtime dependency: `setup.py` declares `firebase-rest-api` without a pin; `requirements.txt`
  pins `firebase-rest-api~=1.10` for development installs.
- Transport in this SDK version is Firebase Realtime Database, not LSL or OSC. LSL/OSC are device
  console options described in the web sources and are a separate local-network path.

## Construction and authentication

```python
from neurosity import NeurositySDK

neurosity = NeurositySDK({"device_id": "<device id>"})
neurosity.login({"email": "<email>", "password": "<password>"})
```

- `device_id` is mandatory; the constructor raises `ValueError` without it.
- `environment` defaults to `production`; `staging` selects the staging Firebase config.
- Credentials belong in the environment or a secret store, never in this repo. This page names
  fields only.
- The SDK registers `atexit` and signal handlers that remove the client and every subscription.
  Code in this repo must let those handlers run and must call the returned unsubscribes itself on
  normal shutdown.

## Stream contract

Every subscription method takes a callback and returns an `unsubscribe` callable.

| Method | Metric / label | Atomic | Notes |
| --- | --- | --- | --- |
| `brainwaves_raw(cb)` | `brainwaves` / `raw` | no | Pre-filtered epochs |
| `brainwaves_raw_unfiltered(cb)` | `brainwaves` / `rawUnfiltered` | no | ADC data, no filters |
| `brainwaves_psd(cb)` | `brainwaves` / `psd` | no | Power spectral density |
| `brainwaves_power_by_band(cb)` | `brainwaves` / `powerByBand` | no | `{ label: "powerByBand", data: {...} }`; 4 events/s; no timestamp in the documented example |
| `signal_quality(cb)` | `signalQuality` | yes | Per-sensor quality |
| `accelerometer(cb)` | `accelerometer` | yes | Movement data |
| `calm(cb)` | `awareness` / `calm` | no | Probability 0.0–1.0; ~16 s to initialise |
| `focus(cb)` | `awareness` / `focus` | no | Probability 0.0–1.0; ~16 s to initialise |
| `kinesis(label, cb)` | `kinesis` / `<label>` | no | Trained motor-imagery trigger |
| `kinesis_predictions(label, cb)` | `predictions` / `<label>` | no | Raw command probabilities |
| `status(cb)` / `settings(cb)` | device path stream | — | Use `stream_from_path` |
| `status_once()` / `settings_once()` / `get_info()` | one-shot read | — | Return a snapshot value |

`add_marker(label)` writes a marker action; `add_action()` requires `command` and `action` and
supports `responseRequired` and `responseTimeout`.

## Data shapes to preserve

- Crown `raw` epochs: **16 samples**, roughly every **62.5 ms** at **256 Hz**; Notion 1/2 emit 25
  samples at 250 Hz.
- Channel order: `CP3, C3, F5, PO3, PO4, F6, C4, CP4`.
- `raw` info includes `channelNames`, `notchFrequency`, `samplingRate` and `startTime`.
  `rawUnfiltered` omits `notchFrequency`.
- Device-side filters on `raw`: notch 50/60 Hz with bandwidth 1, and a 2–45 Hz bandpass,
  Butterworth order 2.
- Awareness metrics emit `{ probability, metric, label, timestamp }`; kinesis emits
  `{ probability, label, timestamp, metric: "kinesis" }`.
- Band power emits `{ label: "powerByBand", data: { alpha, beta, delta, gamma, theta } }`, where
  each band maps to a per-channel array in the documented order; band labels are lowercase and the
  documented example has no timestamp field.

## Rules for this repo

1. Acquire through `NeurositySDK` methods; do not invent a parallel transport in the feedback path.
2. Treat the returned `unsubscribe()` as part of the stream lifecycle; every subscription has an
   owner and a teardown path.
3. Keep sample counts, channel order and metric shapes unchanged at the acquisition boundary.
   Interpretation happens downstream, in the feedback-event layer.
4. Pin the upstream version in provenance (currently v2.2.0) and re-read the checkout before
   changing any assumption about payload shape or lifecycle.
5. Never copy SDK source or embed its Firebase configuration into this repo.
