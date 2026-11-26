---
title: Composed physiological state — deferred design
status: deferred design, not implemented in the first iteration
owner: insite-out
updated: 2026-11-26
---

# Composed physiological state — deferred design

**This is a design only. It is not implemented in the first iteration.** No runtime seam, event kind
or code path exists for it. Devices continue to emit parallel source-tagged feedback events, as
required by `06_Projects/insite-out/physiological-feedback-spec.md`. This document exists for
visibility and design review, following the completion of both feedback feeds and ADR 0004's
advisory-only authority rule.

## Why a design, and why deferred

Crown and Watch feedback now arrive as parallel events at the single agent-facing seam. An agent
that wants a correlated view of user state must currently combine them itself. A composed state
could make that easier, but fusion decisions — which signals may be combined, how stale inputs are
handled, and what a combined value means — need a documented rule set before any code exists.
Deferring the implementation keeps provenance clear while both feeds are still being validated.

## Inputs

The only inputs are existing feedback events from `06_Projects/insite-out/feedback-event-contract.md`:

- Crown: `focus`, `calm`, `kinesis`, `band-power`, `signal-quality`.
- Watch5 Pro: `watch-metric` events for `heart-rate`, `inter-beat-interval`, `skin-temperature` and
  `ambient-temperature`.

Raw epochs, PSD arrays, SDK metric payloads and Watch tracker records never enter composition. No
new transport, event kind or field is introduced by this design.

## Composition model

A composed state is a **consumer-side derived projection** over a bounded set of feedback events. It
is computed on demand from events already delivered at the seam; it is not a new stream, does not
replace the parallel events and is not persisted as canonical state.

The projection is keyed by a correlation window:

1. Normalise all inputs to their `observed_at` value in epoch milliseconds. `source_timestamp` is
   retained for provenance but is not used to reorder events across devices.
2. Select events whose `observed_at` falls inside the window and that are not expired according to
   `is_expired(event, now)`.
3. Preserve each contributor as a separate entry. Grouping is by window, never by replacing two
   sources with one averaged number.
4. When `action_id` is present, group contributors by `action_id` so a state can be read as feedback
   on a particular agent action. Events with different `action_id` values are not fused.

The correlation window length is deliberately undecided; a starting proposal is 5000 ms, chosen to
cover several 1 Hz heart-rate samples and at least one Crown interpretation. It is a design input to
be validated, not a committed constant.

## Preserving the four properties

### Provenance

Each contributor keeps `kind`, `source.device`, `source.model`, `source.metric`, top-level `metric`
and `unit` where applicable, `source_timestamp` and `observed_at`. The composed state holds a
list of these contributors; it does not flatten them into anonymous values. A consumer can always
trace a claim in the state back to the exact source event that produced it.

### Freshness

The composed state's validity window is bounded by the **earliest** `expires_at` among its
contributors. When that boundary is reached, the whole state is stale and must not be consumed. An
expired contributor is dropped from a newly computed state, and if no contributor remains the state
is `unavailable` rather than silently empty. Freshness is judged from `expires_at`, never from
`source_timestamp` alone.

### Readiness

The composed state takes the worst readiness of its contributors, ordered
`unavailable` > `degraded` > `warming` > `ready`:

- any `unavailable` contributor makes the state `unavailable`;
- otherwise any `degraded` contributor makes it `degraded`;
- otherwise any `warming` contributor makes it `warming`;
- otherwise the state is `ready`.

This prevents a single confident source from masking an unready or lost feed.

### Confidence

Confidence stays **per contributor**. The state may expose a conservative summary equal to the
minimum contributor confidence, but it must not average away a low-confidence source. Each
contributor's original `confidence` is retained alongside its identity.

## Fusion rules (documented, not implemented)

1. Only `ready` and `degraded` contributors carry interpretive weight. `warming` contributors are
   attached as context with zero weight; `unavailable` contributors are recorded as explicit
   absence, not as a zero value.
2. Correlation is temporal and provenance-based. Events are grouped by `observed_at` window and
   `action_id`; no signal is inferred from device identity alone.
3. A composed statement may describe co-occurrence, such as "Crown focus and Watch heart rate were
   both observed in this window". It must not infer emotion, intent, medical condition or an
   engagement score that neither feed measures.
4. A state is advisory input only. It informs deliberation in the same way as its contributors and
   never becomes a command or direct action trigger.
5. Unknown event fields are ignored; adding a future `watch-metric` does not require changing this
   design.
6. The parallel events remain available. A consumer may ignore the composed state entirely and read
   the source-tagged events directly.

## Explicit non-goals

- No actuation authority and no physiological-to-action trigger (ADR 0004).
- No medical claim, diagnosis or treatment use; Samsung's data is wellness information only.
- No replacement of parallel source-tagged events with a single fused event.
- No new agent-facing event kind, schema field, transport or runtime seam.
- No persistence of composed state as canonical history; it is derived on demand.
- No raw ECG, raw PPG or on-demand Watch tracker input.

## Advisory-only authority

ADR 0004 applies unchanged. A composed state inherits the same limits as its contributors: it can
modulate how an agent decides, but it cannot invoke a tool, mutate the environment or be bound to a
trigger. Any future direct-trigger policy needs its own visible ticket and ADR, whether it operates
on raw feedback events or on a composed state.

## Design review map

| Criterion | Where addressed |
| --- | --- |
| Correlated state composed from Crown and Watch events | Composition model, Inputs |
| Provenance preserved | Provenance |
| Freshness preserved | Freshness |
| Readiness preserved | Readiness |
| Confidence preserved | Confidence |
| Explicitly not implemented in first iteration | Status banner, Why deferred |
| Fusion rules after both feeds and advisory authority exist | Why deferred, Fusion rules |
| Advisory-only, no actuation authority | Advisory-only authority, Non-goals |
| Design review only, no runtime seam | Non-goals and this map; no source or test files added |

## Open questions for a future implementation ticket

- Correlation window length and whether it differs per source cadence.
- Clock tolerance between device-local `observed_at` values.
- Representation of explicit absence from an `unavailable` contributor.
- Whether the conservative confidence summary is useful or should be omitted.
- Whether composition belongs in each consumer or in one optional shared helper.
