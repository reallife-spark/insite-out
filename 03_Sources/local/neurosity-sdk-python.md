---
title: Neurosity Python SDK — local authoritative checkout
source_path: /mnt/nvme/github/neurosity-sdk-python
source_url: https://github.com/neurosity/neurosity-sdk-python.git
commit: 51e814fa4c4215376dcb781da3bf190b9ec3d2fc
local_state: "README.md modified locally at capture time; left untouched"
license: MIT
version: 2.2.0
python_requires: ">=3.8"
status: accepted
fetch_date: 2026-11-26
---

# Neurosity Python SDK — source manifest

This is the canonical acquisition source for `insite-out`. The checkout stays external; no SDK
code is copied into this repo.

## Files read for the contract

- `README.md` — public API walkthrough, payload shapes and stream lifecycle (locally modified; read as-is).
- `setup.py` — package metadata: `neurosity` 2.2.0, `python_requires >=3.8`, install requires `firebase-rest-api`, MIT.
- `requirements.txt` — `firebase-rest-api~=1.10`.
- `neurosity/__init__.py`, `neurosity/config.py`, `neurosity/neurosity.py` — implementation.
- `examples/example.py`, `examples/brain_terminal.py` — usage examples.

Note: `neurosity/config.py` carries the public Firebase client configuration used by the SDK. It is
not copied here and must not be treated as a secret store or pasted into project docs.

## Implementation facts

`NeurositySDK(options)` requires `device_id`, defaults `environment` to `production`, initialises
Firebase auth/database, tracks subscription ids and registers `atexit` plus `SIGTERM`/`SIGINT`/
`SIGHUP` handlers that call `exit_handler()` to remove the client and all subscriptions.

`login(credentials)` signs in with `email` and `password`, stores `idToken`, and registers a client
under `devices/<device_id>/clients`.

`stream_metric(callback, metric, label, atomic)` creates a subscription under
`devices/<device_id>/subscriptions`, streams `devices/<device_id>/metrics/<metric>[/<label>]`,
merges incremental child updates into a full payload, and returns an `unsubscribe()` callable that
removes the subscription and closes the stream.

`stream_from_path(callback, path_name, ...)` backs `status()` and `settings()`; `get_from_path()`
backs the `*_once()` reads and `get_info()`.
