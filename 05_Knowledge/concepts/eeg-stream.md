# EEG stream

An **EEG stream** is the live sequence of samples or metric events emitted by a headset. In this repo the canonical stream is delivered by the official Neurosity Python SDK through `NeurositySDK` subscriptions.

Streams differ in cadence and meaning: raw epochs arrive about every 62.5 ms, band powers and PSD arrive as epochs are processed, and awareness metrics arrive as slowly changing probabilities. A consumer must not assume all streams share a rate.

Every SDK subscription returns an **unsubscribe** callable. A stream without an owner and a teardown path is a leak; see `05_Knowledge/references/neurosity-python-sdk-contract.md`.

Related: [[epoch]], [[feedback-event]], [[agent-feedback-loop]].
