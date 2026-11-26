# Feedback event

A **feedback event** is the agent-facing record produced when physiological observations from the Crown or the Watch5 Pro are interpreted. It is the only shape an agent sees; raw epochs and sensor payloads stay behind their acquisition boundaries.

A feedback event carries a typed meaning (`focus`, `calm`, `kinesis`, `band-power`, `signal-quality`, `watch-metric`), a confidence or readiness value, structured source identity, observation and expiry times, and provenance back to the stream that produced it. The authoritative enum and schema are owned by `06_Projects/insite-out/feedback-event-contract.md`.

Separating the event from the sample is what lets the transport change later — for example from SDK Firebase streams to local LSL/OSC — without changing what an agent consumes.

Related: [[eeg-stream]], [[agent-feedback-loop]], [[metric-readiness]].
