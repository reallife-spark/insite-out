# Epoch

An **epoch** is one batched group of raw EEG samples. Crown emits 16 samples per epoch at 256 Hz, roughly every 62.5 ms, with a fixed channel order and an info object containing sampling rate, start time, channel names and notch frequency for filtered raw data.

The epoch is the smallest unit that preserves the spatial structure of the signal. Flattening it before interpretation loses the channel dimension.

Two variants exist: `raw` (device-filtered) and `rawUnfiltered` (ADC-level). Only the filtered variant carries `notchFrequency`.

Related: [[eeg-stream]], [[feedback-event]].
