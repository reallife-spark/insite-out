---
title: Feedback event contract
status: accepted
owner: insite-out
updated: 2026-11-26
---

# Feedback event contract

This is the only shape `insite-out` exposes to an agent. Raw epochs, PSD arrays, SDK metric
payloads and Watch sensor payloads do not cross this boundary. Physiological feedback is
**advisory-only**: it modulates agent decisions and never directly triggers an action.

## Required fields

| Field | Type | Meaning |
| --- | --- | --- |
| `kind` | string, enum | `focus`, `calm`, `kinesis`, `band-power`, `signal-quality`, `watch-metric` |
| `value` | number, object, or label string for `kinesis` | Interpreted value in the unit appropriate to `kind`; `null` only when `readiness` is `unavailable` |
| `confidence` | number 0.0–1.0 | Confidence in the interpretation, not the raw SDK probability; `0.0` for an unavailable feed |
| `readiness` | enum | `warming`, `ready`, `degraded`, `unavailable` |
| `source` | object | `{ device, model, metric }`; each field is a non-empty string |
| `source_timestamp` | integer | Device/source timestamp from the originating payload |
| `emitted_at` | integer | Time the feedback event was produced |
| `observed_at` | integer | Time the underlying observation was made |
| `expires_at` | integer | Time after which the event must not be consumed; not earlier than `observed_at` |
| `action_id` | string or null | Agent action this event responds to, when known |

A `watch-metric` event additionally requires top-level `metric` and `unit` non-empty strings. No
metric vocabulary is fixed by this contract; exact Watch metric names and units belong to a
dedicated ticket.

Additional fields for a specific `kind` are allowed only when defined here or in an ADR that
amends this contract. Consumers must ignore unknown fields rather than fail.

## Kind rules

- **focus / calm**: value is the SDK probability; `readiness` must be `warming` during the first
  ~16 seconds after stream start. A low probability with `readiness: warming` is not user state.
- **kinesis**: value is the command label; `confidence` is the detection probability. Emit only on
  a detection, not continuously.
- **band-power**: value is the SDK payload's `data` object keyed by band name; preserve the SDK's
  lowercase band labels and per-channel arrays. If the payload has no timestamp, use `emitted_at`
  as `observed_at` and `source_timestamp`.
- **signal-quality**: value is the per-sensor quality payload; `readiness` becomes `degraded` when
  quality falls below a threshold that is not yet fixed.
- **watch-metric**: value is the interpreted Watch metric in the stated `unit`; `metric` and `unit`
  are required and the metric name is not drawn from a fixed list in this contract.

## Freshness and unavailable feeds

- An event is expired when the current time is greater than or equal to `expires_at`.
- Consumers must not use an expired event as input to a decision.
- A disconnected, expired or lost feed emits an event with `readiness: unavailable`, `value: null`,
  `confidence: 0.0` and `expires_at` equal to `observed_at`. It never goes silent.
- Staleness is judged from `expires_at`, not from `source_timestamp` alone.

## Advisory-only authority

Feedback events inform the agent's next decision. They do not encode a command and must not be
mapped directly to an action trigger. Any later direct physiological-to-action policy requires its
own ADR before implementation.

## Lifecycle

1. One canonical acquisition adapter per source owns each subscription or tracker and its teardown
   path.
2. An adapter translates SDK or tracker payloads into feedback events without changing sample
   counts, channel order or band labels at the acquisition boundary.
3. Shutdown calls every teardown path before closing the agent-facing stream. The SDK's own
   `atexit` and signal handlers remain in force.
4. A subscription or tracker loss emits `readiness: unavailable` rather than silence.

## Failure modes

- **Warm-up**: awareness metrics are unreliable for ~16 s; carry `warming`, never zero-as-state.
- **Signal loss / poor contact**: emit `signal-quality` with `degraded`; downstream events carry
  the same readiness where possible.
- **Expired feed**: emit an `unavailable` event at the expiry boundary instead of leaving the agent
  with no signal.
- **Subscription leak**: prevented by owner-plus-teardown for every subscription or tracker.
- **Transport change**: LSL or OSC may replace a source transport later; because agents consume only
  feedback events, that change does not alter the agent-facing contract.
- **Actuation drift**: prevented by the advisory-only rule and the absence of direct triggers.

## Deliberately undecided

- The numeric signal-quality threshold for `degraded`.
- Whether `action_id` is required or optional in the first implementation.
- Aggregation window for raw epochs into a single event.
- The exact Galaxy Watch5 Pro metric names and units.
