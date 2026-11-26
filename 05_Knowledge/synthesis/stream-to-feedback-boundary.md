# Synthesis — the stream-to-feedback boundary

The source material and the domain concepts converge on one design conclusion: **the durable responsibility of `insite-out` is the boundary between a live EEG stream and an agent-facing feedback event**.

Three facts force that boundary:

1. The SDK owns acquisition. Its epoch sizes, channel order, filters, metric shapes and unsubscribe lifecycle are external facts recorded in `05_Knowledge/references/neurosity-python-sdk-contract.md`. Reimplementing them locally would create a second, drifting standard.
2. The streams are heterogeneous. Raw epochs are high-rate arrays; Focus and Calm are slow probabilities with a ~16 s warm-up; Kinesis is a sparse event. A single undifferentiated stream of numbers would make all three unusable.
3. The consumer is an agent, not a human dashboard. An agent needs typed meaning, confidence or readiness, a timestamp and provenance — not an electrode array.

Therefore the repo's architecture has one hard seam: everything before the boundary preserves SDK shapes, and everything after it emits feedback events defined by `06_Projects/insite-out/feedback-event-contract.md`. The Jetson / TensorRT / DeepStream material in the originating answer sits outside this seam as background; it is one possible deployment of the feedback layer, not its definition.

Consequences recorded as ADRs: `docs/adr/0001-neurosity-sdk-acquisition-boundary.md` and `docs/adr/0002-feedback-event-as-agent-boundary.md`.
