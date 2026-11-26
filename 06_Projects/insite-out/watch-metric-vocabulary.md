---
title: Galaxy Watch5 Pro watch metric vocabulary
status: accepted
owner: insite-out
updated: 2026-11-26
---

# Galaxy Watch5 Pro watch metric vocabulary

This record fixes the first live metric set for the Galaxy Watch5 Pro. It makes the generic
`watch-metric` kind in `06_Projects/insite-out/feedback-event-contract.md` directly implementable
without adding a new event kind or changing the schema. Watch measurements are **metrics**, not
channels; `channel` stays reserved for Crown EEG electrodes.

Samsung states that Samsung Health Sensor SDK data is for fitness and wellness information only,
not for the diagnosis or treatment of any medical condition. `insite-out` makes no medical claim
from these values.

## Primary sources

- Samsung Health Sensor SDK, Data Specifications —
  https://developer.samsung.com/health/sensor/guide/data-specifications.html
- Samsung Health Sensor SDK, Introduction —
  https://developer.samsung.com/health/sensor/guide/introduction.html
- `HealthTrackerType` enum —
  https://developer.samsung.com/health/sensor/api-reference/com/samsung/android/service/health/tracking/data/HealthTrackerType.html
- `ValueKey.HeartRateSet` —
  https://developer.samsung.com/health/sensor/api-reference/com/samsung/android/service/health/tracking/data/ValueKey.HeartRateSet.html
- `ValueKey.SkinTemperatureSet` —
  https://developer.samsung.com/health/sensor/api-reference/com/samsung/android/service/health/tracking/data/ValueKey.SkinTemperatureSet.html
- `ValueKey.SweatLossSet` —
  https://developer.samsung.com/health/sensor/api-reference/com/samsung/android/service/health/tracking/data/ValueKey.SweatLossSet.html
- Samsung Health Sensor SDK, Tracking data —
  https://developer.samsung.com/health/sensor/guide/tracking-data.html
- Samsung Health Sensor SDK, ECG Monitor sample —
  https://developer.samsung.com/health/sensor/sample/ecg-monitor.html

## Decision — first live metric set

`source.device` is `galaxy-watch5-pro` and `source.model` is `galaxy-watch5-pro` for every row.
`source.metric` and the top-level `metric` are the name in the first column. `kind` is
`watch-metric` for every row. `value` is the number or object described in the table.

| Metric name | Unit | Value | SDK tracker and value key | Cadence from source | Readiness behaviour |
| --- | --- | --- | --- | --- | --- |
| `heart-rate` | `bpm` | number | `HEART_RATE_CONTINUOUS` → `HeartRateSet.HEART_RATE` | Processed, 1 Hz; one `HeartRateSet` per measurement with the display on, batched with the display off | `warming` until the first valid sample after tracker start; `ready` after it; `degraded` when the SDK heart-rate status flags an error or the watch is off-body; `unavailable` on tracker error or disconnect |
| `inter-beat-interval` | `ms` | object keyed by beat index, values are integers | `HEART_RATE_CONTINUOUS` → `HeartRateSet.IBI_LIST` | Delivered with heart rate: 0–4 IBI values per data point; for batch data all IBI values arrive in the **first** data point and later points contain `null` | `warming` until the first IBI batch arrives; `ready` for that batch; `degraded` when `IBI_STATUS` flags an error; `unavailable` on tracker error or disconnect |
| `skin-temperature` | `celsius` | number | `SKIN_TEMPERATURE_CONTINUOUS` → `SkinTemperatureSet.OBJECT_TEMPERATURE` | Processed, event-driven; one `SkinTemperatureSet` per measurement with the display on, batched with the display off; Watch5 series and later, Android 13 / API 33 or higher | `warming` until the first normal-status measurement; `ready` after it; `degraded` when `STATUS` is other than `0` (normal); `unavailable` on tracker error or disconnect |
| `ambient-temperature` | `celsius` | number | `SKIN_TEMPERATURE_CONTINUOUS` → `SkinTemperatureSet.AMBIENT_TEMPERATURE` | Same measurement events as `skin-temperature` | Same as `skin-temperature`; contextual signal, not a user-state measure |

### Notes on the table

- Samsung's API calls the contacted-object value `OBJECT_TEMPERATURE`: "temperature of an object
  contacted with the Galaxy Watch", in Celsius. The SDK data type is `SKIN_TEMPERATURE_CONTINUOUS`.
  The metric name emitted by `insite-out` is `skin-temperature`, never "body temperature".
  Samsung explicitly states this value "is not the same as body temperature".
- Both temperature values are in Celsius and are emitted in two parallel events from one tracker
  callback; they are not merged into one object.
- `inter-beat-interval` is a snapshot batch, not a 1 Hz stream. Its `observed_at` is the timestamp
  of the data point that carried the batch, and its `expires_at` must reflect that time rather than
  implying a continuing series.
- The `value` of `inter-beat-interval` is an object because the contract accepts an object value;
  the keys are the beat indices within the delivered batch and preserve the SDK list order.

## Freshness budgets

The contract fixes the presence and ordering of `observed_at` and `expires_at`, not their numeric
offsets. These adapter-layer budgets are decisions for the Watch tracer ticket and may be revised
there without a contract change. They are small multiples of the source cadence.

| Metric | `expires_at - observed_at` | Basis |
| --- | --- | --- |
| `heart-rate` | 3000 ms | Three 1 Hz measurement intervals |
| `inter-beat-interval` | 3000 ms | Snapshot of recent beats, same budget as heart rate |
| `skin-temperature` | 60000 ms | Sparse, event-driven measurement; no fixed SDK cadence |
| `ambient-temperature` | 60000 ms | Same measurement event as skin temperature |

When the SDK delivers batched data with the watch display off, `observed_at` is the timestamp of
each data point in the batch, so each emitted event carries its own observation time.

## Decision — excluded from the first live set

| Tracker | Reason |
| --- | --- |
| `ECG_ON_DEMAND` | Raw, 500 Hz. On-demand trackers must run in a foreground app, only one at a time, for no longer than about 30 seconds; running a continuous tracker during an on-demand measurement can yield invalid values. Deferred. |
| `PPG_CONTINUOUS` | Raw PPG (green, IR, red) at 25 Hz. Raw waveform, not a processed metric; an on-demand PPG session is likewise foreground-only and short. Deferred. |
| `PPG_ON_DEMAND` | Raw PPG at 100 Hz, with the same foreground and 30-second session constraints. Deferred. |
| `ACCELEROMETER_CONTINUOUS` | Raw 25 Hz axis samples. Useful as context but not an interpreted physiological metric in the first set. Deferred. |
| `EDA_CONTINUOUS` | Raw electrodermal activity at 1 Hz and available only on Galaxy Watch8 series and later, so not available on Watch5 Pro. Excluded. |
| `SPO2_ON_DEMAND` | Processed but on-demand: foreground-only, short session, not a continuous live feed. Deferred to a dedicated decision. |
| `SKIN_TEMPERATURE_ON_DEMAND` | Processed but on-demand; the continuous tracker already covers the live path. Deferred. |
| `BIA_ON_DEMAND`, `MF_BIA_ON_DEMAND` | On-demand body-composition measurements, not a continuous feedback signal; MF-BIA requires Watch8 series or later. Deferred. |
| `SWEAT_LOSS` | Processed, but a single post-running prediction in millilitres, not a live continuous measurement. Deferred. |

The general rule is that the first set contains only **processed continuous** tracker values that
the Galaxy Watch5 Pro can supply. Raw waveforms and all on-demand trackers stay out until their
foreground, session-length and cross-tracker interference constraints have their own decision.

## Phone-side boundary

The phone's Samsung Health Data SDK can read stored Health records such as `HeartRateType` and
`SkinTemperatureType`, including daily or binned aggregates. Those are **slow stored aggregates**,
not the live feedback path. They may support later analysis or correlation, but they never produce
a `watch-metric` feedback event in this loop. Live events come only from the Wear OS companion app
using the Samsung Health Sensor SDK and bridged over the local network.

## Contract fit

- No new `kind` is required: every row is a `watch-metric` event.
- No new required field is required: `metric`, `unit` and `value` already exist at the top level.
- `source` already requires `device`, `model` and `metric`; the names above populate them.
- New metrics can be added later by adding a row here, with no schema change to the envelope.

## Verification checklist

1. Four metrics are named with explicit units: `heart-rate`, `inter-beat-interval`,
   `skin-temperature`, `ambient-temperature`.
2. Cadence and all four readiness states are recorded for each metric.
3. Source labels are fixed for `source.metric` and top-level `metric`.
4. Raw ECG and raw PPG are excluded with the foreground, one-at-a-time, ~30-second and
   interference reasons recorded.
5. Skin temperature is named as skin temperature and explicitly not body temperature.
6. The phone's Health Data SDK is limited to slow stored aggregates.
7. Every row fits `watch-metric` without a schema change.
