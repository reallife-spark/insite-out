# Domain glossary

**EEG stream**: a time-ordered sequence of electroencephalography samples arriving while a user is wearing the headset. In this repo the canonical source is the Neurosity Python SDK, which streams Firebase-backed metric events. _Avoid_: "brainwave feed" when naming the transport object.

**Epoch**: one batched group of raw EEG samples from a device. Crown emits 16 samples per epoch about every 62.5 ms at 256 Hz; Notion 1/2 emit 25 samples at 250 Hz. Epoch metadata carries channel names, sampling rate, start time and, for filtered raw, notch frequency. _Avoid_: "frame" (belongs to video) or "packet" (transport-level).

**Channel order**: the fixed Crown electrode order `CP3, C3, F5, PO3, PO4, F6, C4, CP4`. Downstream interpretation depends on this order, so it is preserved at the acquisition boundary. _Avoid_: reordered or alphabetised channel lists.

**Raw brainwaves**: filtered epochs emitted by `brainwaves_raw`; notch 50/60 Hz and a 2–45 Hz Butterworth bandpass are applied on-device. _Avoid_: treating raw as unfiltered.

**Unfiltered brainwaves**: ADC-level epochs emitted by `brainwaves_raw_unfiltered`, with no device-side filtering and no notch field in the info object. _Avoid_: using it by default; it is for advanced filter work.

**Band power**: power in a frequency band (Delta, Theta, Alpha, Beta, Gamma) emitted by `brainwaves_power_by_band`. _Avoid_: "frequency" alone; the unit is power, not a frequency value.

**Focus**: an awareness probability in 0.0–1.0 derived from gamma activity around 30–44 Hz; takes about 16 seconds to initialise. _Avoid_: a binary focused/unfocused flag.

**Calm**: an awareness probability in 0.0–1.0 from passive cognitive state; takes about 16 seconds to initialise. _Avoid_: a mood label.

**Kinesis**: a trained motor-imagery command detected as a spike over prediction probabilities. It is an event, not a level. _Avoid_: calling every awareness metric kinesis.

**Metric readiness**: the state of a stream whose value is not yet meaningful, such as Focus or Calm during the first ~16 seconds. Readiness is distinct from a low score. _Avoid_: encoding uninitialised as zero.

**Unsubscribe**: the callable returned by every SDK subscription method; it removes the remote subscription and closes the local stream. _Avoid_: abandoning a subscription without calling it.

**Feedback event**: the agent-facing record produced by interpreting observations from one or more acquisition sources. It carries a typed meaning, confidence or readiness, structured source identity, observation and expiry times, and provenance. _Avoid_: forwarding raw epochs or sensor payloads to a model as "feedback".

**Physiological feedback event**: a feedback event whose interpreted value comes from a body signal, whether Crown EEG or a Galaxy Watch5 Pro metric. It is advisory-only: it modulates agent decisions and never directly triggers an action. _Avoid_: "biofeedback", which is human-facing self-regulation.

**Watch metric**: a physiological measurement emitted by the Galaxy Watch5 Pro through the Samsung Health Sensor SDK, represented as a `watch-metric` feedback event with a metric name, unit and value. _Avoid_: calling it a channel; **channel** is reserved for Crown electrodes.

**Agent feedback loop**: the cycle in which an agent acts, the user's EEG is acquired and interpreted, and a feedback event is returned to the agent as input for the next action. _Avoid_: a one-way telemetry pipe.

**Acquisition boundary**: the interface where a source's samples or metric events enter this repo. There is one canonical adapter per source: the Neurosity Python SDK binds Crown EEG, and the Samsung Health Sensor SDK binds live Galaxy Watch5 Pro metrics. Source payload shapes and lifecycles are not redefined locally. _Avoid_: adding a second transport inside the feedback layer.

**Feedback-event contract**: the schema and lifecycle rules for feedback events, owned by `06_Projects/insite-out/feedback-event-contract.md`. _Avoid_: ad-hoc JSON shapes in consumers.
