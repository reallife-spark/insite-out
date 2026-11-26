# Metric readiness

**Metric readiness** distinguishes "not yet meaningful" from "meaningful and low". Focus and Calm take about 16 seconds to initialise; before that, their numeric probability must not be read as user state.

A feedback event sourced from an unready metric always carries its `value` plus `readiness: warming`, so an agent cannot mistake a warm-up artefact for a low user-state score. A lost or expired feed instead carries `readiness: unavailable`, `value: null` and a zero confidence. The required fields are defined in `06_Projects/insite-out/feedback-event-contract.md`.

Related: [[feedback-event]], [[agent-feedback-loop]].
