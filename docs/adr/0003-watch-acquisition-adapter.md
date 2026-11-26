# ADR 0003 — Watch acquisition adapter and local bridge

- Status: accepted
- Date: 2026-11-26

## Context

ADR 0001 now requires one canonical acquisition adapter per source. The Crown has the official
Neurosity Python SDK. The Galaxy Watch5 Pro exposes live sensor data through the Samsung Health
Sensor SDK, which runs on a Wear OS app; the phone's Samsung Health Data SDK only reads stored
aggregate records and cannot drive a live feedback loop. The agent service runs elsewhere and must
not depend on a direct Watch-to-cloud path. The first Watch slice is one tracer metric, `heart-rate`,
before the remaining approved vocabulary is added.

## Decision

The canonical Watch acquisition adapter is the **Samsung Health Sensor SDK on a Wear OS companion
app**. That app registers a tracker listener, translates each `TrackerEventListener.onDataReceived`
batch into a small JSON record of the form `{ "tracker": ..., "timestamp": ..., "values": ... }`
using Samsung's own value keys, and publishes it through `LocalWatchBridge` to a **loopback or
private-network endpoint** only. A public endpoint is rejected at bridge construction. The agent
side receives that record and `WatchAdapter.translate` emits a `watch-metric` feedback event at the
single feedback-event seam.

`WatchAdapter` holds a metric-spec registry (`METRIC_SPECS`). Issue #6 implemented `heart-rate`
(`HEART_RATE_CONTINUOUS` → `HEART_RATE`, `bpm`, 3000 ms freshness); issue #7 completed the approved
vocabulary with `inter-beat-interval` (packed `IBI_LIST`, `ms`, 3000 ms), `skin-temperature`
(`OBJECT_TEMPERATURE`, celsius, 60000 ms) and `ambient-temperature` (`AMBIENT_TEMPERATURE`, celsius,
60000 ms). New metrics are registry rows; no new event kind, contract field or translation branch is
needed. One tracker payload can emit several parallel events: heart rate plus IBI, or skin plus
ambient temperature. A status other than `0` produces `readiness: warming` with confidence `0.0`
until the first valid sample for that metric, then `degraded` with confidence `0.5`. A disconnect or
expiry produces an `unavailable` event with `metric`, `unit`, null `value` and zero confidence.

Only allowlisted processed continuous trackers translate. Raw ECG and raw PPG are excluded: Samsung
requires on-demand trackers to run in the foreground, one at a time, for no longer than about 30
seconds, and warns that continuous tracking during an on-demand measurement can yield invalid values.
On-demand and stored-aggregate sources need their own decisions before entering this path.

`LocalWatchBridge.start` owns the tracker subscription and `close` calls its unsubscribe exactly
once. Watch events remain parallel source-tagged events; no fused physiological state is emitted,
and ADR 0004's advisory-only rule applies to them unchanged.

## Consequences

- The Watch path is verifiable with recorded JSON payloads and no watch, credentials or Samsung SDK
  code in this repo.
- The local endpoint guard makes a direct Watch-to-cloud agent path a construction error rather
  than a deployment convention.
- Adding a metric is a registry change plus a recorded payload test; issue #7 used that path for
  all three remaining vocabulary rows.
- Expiry is represented by `is_expired(event, now)` and an explicit `mark_unavailable` call; there
  is no background timer in this slice, so consumers must check freshness before use.
- The Wear OS companion app itself lives outside this Python repo; this ADR fixes its wire contract
  and lifecycle, not its Android implementation.

## Alternatives considered

- **Direct Watch-to-cloud agent path**: simpler wiring but adds a cloud dependency, wider consent
  scope and a failure mode this project does not need.
- **Phone Health Data SDK as the live source**: provides stored aggregates, not live tracker events,
  so it cannot support the feedback loop.
- **One adapter per metric**: would duplicate the bridge and teardown logic; a spec registry keeps
  one canonical adapter per source.
- **Including raw ECG/PPG now**: rejected because foreground-only sessions and cross-tracker
  interference make them unsuitable for a continuous advisory feed.
