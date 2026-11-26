# Physiological feedback for agents — specification

## Problem Statement

`insite-out` currently models feedback from one device: the Neurosity Crown. An agent can receive Crown EEG interpretations such as Focus, Calm, Kinesis and band power as feedback events, but it cannot see physiological state from the Samsung Galaxy Watch5 Pro, cannot reliably tell which device produced an event, cannot tell whether a value is still fresh, and has no explicit rule preventing a physiological signal from being treated as a direct command.

The user's goal is for an agent to receive physiological feedback composed from both the Crown and the Watch5 Pro and to act accordingly. Turning that goal into safe, testable work requires decisions about terminology, source identity, Watch metric representation, freshness, authority and acquisition boundaries. The exact Watch metric set and raw ECG/PPG capture are deliberately deferred, so the contract must accommodate them without hard-coding a premature list.

## Solution

Extend the existing agent-facing feedback-event boundary to carry physiological feedback from both devices. Keep the Crown's official Neurosity Python SDK as its binding acquisition adapter. Add a Samsung Health Sensor SDK adapter running on a Wear OS companion app as the Watch acquisition path, bridged to the agent service over the local network.

Represent every device's output as a parallel, source-tagged feedback event. Make `source` structured so the device, model and metric are explicit. Add a generic `watch-metric` kind with required metric name, unit and value, leaving the exact metric vocabulary to a later ticket. Add `observed_at` and `expires_at` so consumers can reject stale feedback. Make the first loop advisory-only: physiological feedback modulates agent decisions but never directly triggers an action.

Generalise the acquisition-boundary decision from one SDK to one canonical adapter per source, amend ADR 0001 accordingly, and add ADR 0003 for the Watch adapter. Add the glossary terms `physiological feedback event` and `watch metric`.

## User Stories

1. As an agent developer, I want one feedback-event stream covering both the Crown and the Watch5 Pro, so that I do not have to build two unrelated consumers.
2. As an agent developer, I want every event to identify its source device, so that I can reason about Crown EEG and Watch metrics separately.
3. As an agent developer, I want `source` to be structured with device, model and metric, so that source identity is machine-readable rather than encoded in a free-text string.
4. As an agent developer, I want Watch measurements represented with a generic `watch-metric` kind, so that new metrics can be added without changing the event contract.
5. As an agent developer, I want each Watch event to carry metric name, unit and value, so that I can interpret the number correctly.
6. As an agent developer, I want the exact Watch metric set deferred to a ticket, so that we do not freeze an uninformed list before the specs are implemented.
7. As an agent developer, I want every event to carry `observed_at`, so that I know when the underlying physiological observation was made.
8. As an agent developer, I want every event to carry `expires_at`, so that I can reject feedback that is too old to act on.
9. As an agent developer, I want expired feeds to emit `readiness: unavailable` rather than silence, so that absence of data is distinguishable from no change.
10. As an agent developer, I want Crown Focus and Calm warm-up represented as `warming`, so that I do not read a warm-up artefact as a low user-state score.
11. As an agent developer, I want devices to emit parallel events rather than a single fused state, so that provenance remains clear in the first iteration.
12. As an agent developer, I want a composed physiological state to be a later capability, so that fusion rules are designed after both feeds exist.
13. As an agent developer, I want the first loop to be advisory-only, so that physiological signals inform decisions without becoming commands.
14. As an agent developer, I want no code path that maps a physiological event directly to an action trigger in the first iteration, so that feedback cannot accidentally actuate the environment.
15. As an agent operator, I want to correlate feedback with the agent action that prompted it, so that I can tell which behaviour changed the user's state.
16. As an agent operator, I want confidence and readiness preserved alongside values, so that I can modulate behaviour proportionally rather than binaryly.
17. As an agent operator, I want unknown event fields to be ignored, so that adding a new metric does not break existing consumers.
18. As a wearable user, I want explicit permissions required for Watch sensor access, so that physiological data is collected only with consent.
19. As a wearable user, I want no credentials or sensor configuration values stored in the repo, so that my accounts and device settings stay private.
20. As a wearable user, I want skin temperature described as skin temperature rather than body temperature, so that the metric is not over-interpreted.
21. As a wearable user, I want on-demand Watch sensors treated as short foreground sessions, so that the system does not imply continuous availability where the SDK does not provide it.
22. As a system operator, I want a Wear OS companion app using the Samsung Health Sensor SDK, so that continuous Watch metrics can reach the feedback path.
23. As a system operator, I want the Watch companion app to bridge events over the local network, so that the agent service does not need a direct Watch-to-cloud path.
24. As a system operator, I want the phone's Samsung Health Data SDK used only for slow stored aggregates, so that the live loop is not confused with historical health data.
25. As a system operator, I want the Crown adapter unchanged in shape and lifecycle, so that the existing acquisition standard remains authoritative for EEG.
26. As a system operator, I want one canonical acquisition adapter per source, so that each device has an explicit owner and no transport is improvised inside the feedback layer.
27. As a system operator, I want every subscription and tracker to have a teardown path, so that shutdown does not leak device sessions.
28. As a system operator, I want a disconnected device to emit `readiness: unavailable`, so that the agent can degrade gracefully.
29. As a tester, I want one primary test seam at the agent-facing feedback-event stream, so that tests assert external behaviour rather than SDK internals.
30. As a tester, I want to replay recorded Crown SDK payloads into the Crown adapter, so that translation can be verified without live hardware.
31. As a tester, I want to replay recorded Samsung Health Sensor SDK tracker payloads into the Watch adapter, so that Watch translation can be verified without a watch.
32. As a tester, I want every emitted event validated against the contract, so that schema drift is caught at the seam.
33. As a tester, I want freshness assertions on `observed_at` and `expires_at`, so that stale feedback is proven to be rejected.
34. As a tester, I want to add a hypothetical new Watch metric in a test without changing the contract, so that the generic kind is proven extensible.
35. As a tester, I want raw ECG and PPG excluded from the first test set, so that deferred capabilities are not accidentally implemented.
36. As a maintainer, I want `physiological feedback event` added to the glossary, so that the new subtype is unambiguous.
37. As a maintainer, I want `watch metric` added to the glossary, so that Watch measurements are not called channels.
38. As a maintainer, I want ADR 0001 amended to per-source adapters, so that the architecture matches the two-device reality.
39. As a maintainer, I want ADR 0003 to record the Watch adapter decision, so that the choice of Samsung Health Sensor SDK is explainable later.
40. As a maintainer, I want follow-up tickets for metric specificity, advisory policy and adapter implementation, so that deferred work is visible rather than lost.
41. As a researcher, I want raw ECG and PPG deferred until after the specs are implemented, so that on-demand and foreground constraints are handled deliberately.
42. As a researcher, I want the exact first-wave metric set decided in a dedicated ticket, so that the decision has its own evidence and acceptance criteria.
43. As a privacy owner, I want the boundary between live sensor access and stored health data documented, so that consent scope is clear.
44. As a policy owner, I want a separate ADR and ticket before any direct physiological-to-action trigger, so that actuation authority is never implied by an event schema.
45. As a product owner, I want measurable acceptance criteria, so that completion can be verified rather than asserted.

## Implementation Decisions

- The canonical subtype is `physiological feedback event`; `feedback event` remains the umbrella term. “Biofeedback” remains reserved for human-facing self-regulation.
- Watch measurements are called **metrics**. `channel` remains reserved for Crown EEG electrode positions.
- The acquisition boundary is generalised: one canonical acquisition adapter per source. The Neurosity Python SDK remains binding for Crown EEG; the Samsung Health Sensor SDK running on a Wear OS companion app becomes canonical for live Watch metrics.
- The phone's Samsung Health Data SDK is not part of the live feedback loop. It remains available for slow stored aggregates only.
- Every emitted event has a structured `source` object containing `device`, `model` and `metric`. The device vocabulary begins with the Crown and the Galaxy Watch5 Pro; the metric vocabulary is deferred to a ticket.
- Watch events use a generic `kind` of `watch-metric`, with required `metric`, `unit` and `value` fields. Specific metric names and units are not fixed in this spec.
- Every event has `observed_at` and `expires_at`. Consumers must not use an event after `expires_at`; an expired or lost feed emits `readiness: unavailable` rather than silence.
- Crown warm-up semantics are unchanged: Focus and Calm carry `readiness: warming` for approximately the first sixteen seconds after stream start.
- Devices emit parallel events. No fused physiological state object is produced in the first iteration.
- The first loop is advisory-only. A physiological event informs agent decisions but does not directly trigger an action. Direct triggers require a separate policy ticket and ADR.
- The glossary gains `physiological feedback event` and `watch metric`. ADR 0001 is amended to per-source adapters, and ADR 0003 records the Watch adapter decision.
- Raw ECG, raw PPG, exact Watch metric enumeration and composed state are deferred to follow-up tickets.
- Measurable acceptance criteria:
  1. 100% of emitted events validate against the feedback-event contract.
  2. 100% of emitted events have non-empty `device`, `model` and `metric` in `source`.
  3. 100% of Watch events use `kind: watch-metric` and include `metric`, `unit` and `value`.
  4. 100% of emitted events include `observed_at` and `expires_at`, with `expires_at` not earlier than `observed_at`.
  5. 0 events are consumed after `expires_at` in the test suite.
  6. 100% of disconnected or expired feeds emit `readiness: unavailable`.
  7. 0 fused physiological state objects are emitted in the first iteration.
  8. 0 code paths in the first iteration map a physiological event directly to an action trigger.
  9. Crown Focus and Calm events carry `readiness: warming` for approximately the first sixteen seconds after stream start.
  10. 100% of Crown subscriptions and Watch trackers have an explicit teardown path.
  11. There is exactly one primary test seam: the agent-facing feedback-event stream.
  12. Implementation work is split into exactly three follow-up tickets.

## Testing Decisions

- A good test asserts externally observable emitted feedback events only: kind, value, source identity, unit, readiness, confidence, observed time and expiry. It does not assert SDK internals, Firebase paths, Wear OS service wiring or private helper state.
- The primary seam is the agent-facing feedback-event stream. Recorded Crown SDK payloads and recorded Samsung Health Sensor SDK tracker payloads are replayed into their respective adapters, and assertions are made on emitted events at that seam.
- Modules to be tested: the Crown acquisition adapter, the Watch acquisition adapter, the feedback-event translation layer, and contract validation at the agent-facing seam.
- Prior art is conceptual rather than executable: the existing feedback-event contract, the recorded SDK/source captures, ADR 0001 and ADR 0002. No runtime test suite exists yet, so the first tests establish the seam.
- Tests cover structured source identity, generic Watch metric representation, freshness and expiry, warm-up readiness, parallel-event emission, teardown, and the advisory-only contract assertion.
- Tests deliberately exclude raw ECG/PPG, exact metric enumeration, fused state and direct action triggers.

## Out of Scope

- Raw ECG and raw PPG capture from the Watch5 Pro.
- The exact first-wave Watch metric set and units; these belong to a dedicated ticket.
- A fused or composed physiological state object.
- Direct physiological-to-action triggers and any actuation authority.
- Using the phone's Samsung Health Data SDK as the live feedback path.
- Replacing the Crown SDK transport with LSL or OSC.
- Jetson, TensorRT-DLA, DeepStream and dual-Xavier deployment details from the originating answer; they remain background only.
- Training an EEG classifier or making medical claims from either device.

## Further Notes

- Samsung Health Sensor SDK on-demand trackers are foreground-only, intended for roughly thirty-second sessions, and continuous and on-demand trackers can interfere. This is why raw ECG and PPG are deferred.
- Skin temperature is available on Watch5 series devices with the required watch software level and is not equivalent to body temperature.
- The advisory-only rule is a consumer policy. It is specified here and enforced by the absence of direct-trigger code paths in the first iteration; a future ADR is required before that changes.
- Planned follow-up tickets in `reallife-spark/insite-out`:
  1. Define the exact Galaxy Watch5 Pro metric set and units for physiological feedback.
  2. Define advisory-only policy and a separate direct-trigger follow-up with its own ADR.
  3. Implement the Samsung Health Sensor SDK bridge and Watch acquisition adapter.
- The triage role `ready-for-agent` maps to this repo's `ready-for-human` label.
