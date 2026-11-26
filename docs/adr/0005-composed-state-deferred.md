# ADR 0005 — Composed physiological state stays deferred

- Status: accepted (design only)
- Date: 2026-11-26

## Context

The Crown and Watch5 Pro now emit parallel, source-tagged feedback events at the single agent-facing
seam. ADR 0002 makes that event the only shape an agent sees, ADR 0003 fixes the Watch adapter and
local bridge, ADR 0004 makes all physiological feedback advisory-only, and the approved Watch metric
vocabulary is implemented. Issue #8 asks for a composed physiological state that correlates Crown
and Watch feedback, while stating that it is intentionally deferred and out of the first iteration.

Fusion is a semantic decision, not a transport problem. Combining a 16-second Crown warm-up with a
1 Hz heart-rate stream and sparse skin-temperature measurements can hide provenance, freshness or
readiness if done carelessly. The design is useful now; the runtime behaviour is not.

## Decision

A composed physiological state is **documented but not implemented** in the first iteration. Its
design lives in `06_Projects/insite-out/composed-physiological-state-design.md`. Devices continue to
emit parallel source-tagged events; no new event kind, contract field, runtime seam or fused state
object is introduced.

If a future ticket implements the design, the projection must be consumer-side and derived on
demand from existing feedback events. It must preserve per-contributor source identity and
observation time, take its validity window from the earliest contributor expiry, degrade readiness
to the worst contributor, keep confidence per contributor, and remain advisory-only under ADR 0004.
Any actuation policy still needs its own visible ticket and ADR.

## Consequences

- Provenance and freshness stay unambiguous while both feeds are being validated.
- Agents that want correlation must combine parallel events themselves until a future helper exists.
- The design is reviewable now without a second agent-facing seam to maintain or test.
- Implementing the design later is a deliberate reversal of the parallel-events rule and requires
  an explicit ticket; it is not authorised by this ADR.

## Alternatives considered

- **Implement fusion now**: would hide which device produced a claim and risk treating warm-up values
  as state before both feeds are validated.
- **Add a fused event kind**: would create a second agent-facing shape and conflict with ADR 0002.
- **Leave no design at all**: would lose the fusion constraints just established and make a future
  implementation easier to get wrong.
