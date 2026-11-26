# ADR 0004 — Advisory-only authority for physiological feedback

- Status: accepted
- Date: 2026-11-26

## Context

The agent-facing stream now carries interpreted physiology from two devices: Crown EEG (Focus,
Calm, Kinesis, band power, signal quality) and Galaxy Watch5 Pro metrics (heart rate, IBI, skin
temperature, ambient temperature). ADR 0002 makes the feedback event the only shape an agent sees,
but a shape alone does not say what an event is allowed to do. Without an explicit authority rule,
a `confidence` of 0.9 or a "kinesis" label can be mistaken for a command, and a noisy sensor can
become an actuator.

Both sources are probabilistic and context-dependent. Crown Focus and Calm need roughly 16 seconds
to initialise and can emit warm-up artefacts; Kinesis is a sparse detection with a probability, not
an instruction. Watch heart rate and temperature are wellness signals that vary with movement,
contact and environment; Samsung states the SDK data is for fitness and wellness information only,
not for diagnosis or treatment. Neither source establishes intent to act. Mapping either directly
to an action would give a false positive the power to change the environment and would make consent
scope and accountability unclear.

## Decision

Physiological feedback events **inform agent decisions and never directly trigger actions** in the
first iteration. An event is advisory input: it can change how an agent deliberates, what it asks,
or which option it prefers, but no event is an instruction and no event field grants actuation
authority. The event schema is unchanged by this decision; it adds no action, command or trigger
field. There are zero code paths in this iteration that map a physiological event to an action
trigger.

### Consumer guidance

Consumers modulate behaviour proportionally rather than treating a value as a switch:

- `confidence` weights how strongly an interpretation should influence a decision. A low-confidence
  signal is a weak preference, not a veto or a command.
- `readiness` gates interpretation. `warming` values are not user state, `degraded` values are
  suspect, and `unavailable` means the feed is lost rather than unchanged.
- `observed_at` tells the consumer when the underlying observation was made, so it can align
  feedback with the agent action that may have prompted it.
- `expires_at` bounds use. A consumer must not act on an event at or after expiry and should prefer
  the freshest valid event when several exist.

A consumer may combine these fields into a policy such as "lower the certainty of an answer when
Focus is warming" or "ask before proceeding when signal quality is degraded". It may not bind any
of them to a direct tool call or environment mutation.

## Consequences

- Agent behaviour can be shaped by physiology without giving a noisy or ambiguous signal control
  over the environment.
- Fewer categories of user consent are implied: reading a wellness signal does not become
  permission to act on the user's behalf.
- Tests verify this rule by review of the agent-facing seam and by the absence of direct-trigger
  paths; no actuation test is introduced in the first iteration.
- The advisory rule applies equally to Crown and Watch events, so adding a metric does not silently
  change authority.
- **Follow-up — direct-trigger policy**: any future design that lets a physiological event invoke
  an action requires its own visible ticket and its own ADR before implementation. That decision
  must define the trigger policy, thresholds, consent, failure handling and audit trail. It is not
  authorised by this ADR and is deliberately not created here.

## Alternatives considered

- **Direct event-to-action triggers**: lower latency, but turns warm-up artefacts, sensor noise and
  wellness signals into commands with no intent or consent basis.
- **Schema-level authority field**: would let an event claim actuation rights, which is exactly the
  coupling this decision avoids; authority belongs to a policy decision, not to a payload.
- **Crown-only advisory rule**: rejected because Watch metrics carry the same uncertainty and
  would otherwise acquire authority by omission.
