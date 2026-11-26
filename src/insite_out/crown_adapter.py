from .feedback_event import unavailable_feedback_event, validate_feedback_event

CROWN_TTL_MS = 1000
WARMUP_MS = 16000
DEVICE = "neurosity-crown"
MODEL = "crown"


class CrownAdapter:
    def __init__(
        self,
        sdk,
        *,
        emit,
        now,
        stream_started_at,
        kinesis_labels=(),
    ):
        self.sdk = sdk
        self.emit = emit
        self.now = now
        self.stream_started_at = stream_started_at
        self.kinesis_labels = tuple(kinesis_labels)
        self.unsubscribes = []

    def start(self):
        self.unsubscribes.append(self.sdk.focus(lambda payload: self._on_awareness("focus", payload)))
        self.unsubscribes.append(self.sdk.calm(lambda payload: self._on_awareness("calm", payload)))
        self.unsubscribes.append(
            self.sdk.brainwaves_power_by_band(self._on_band_power)
        )
        for label in self.kinesis_labels:
            self.unsubscribes.append(
                self.sdk.kinesis(label, lambda payload, label=label: self._on_kinesis(label, payload))
            )

    def close(self):
        for unsubscribe in self.unsubscribes:
            unsubscribe()
        self.unsubscribes.clear()

    def _handle_loss(self, payload, kind, metric):
        if payload is not None:
            return False
        now = self.now()
        event = unavailable_feedback_event(
            kind=kind,
            device=DEVICE,
            model=MODEL,
            metric=metric,
            observed_at=now,
            emitted_at=now,
        )
        self.emit(validate_feedback_event(event))
        return True

    def _on_awareness(self, kind, payload):
        if self._handle_loss(payload, kind, kind):
            return
        now = self.now()
        observed_at = payload["timestamp"]
        readiness = self._readiness(now)
        event = {
            "kind": kind,
            "value": payload["probability"],
            "confidence": 0.0 if readiness == "warming" else 1.0,
            "readiness": readiness,
            "source": {
                "device": DEVICE,
                "model": MODEL,
                "metric": kind,
            },
            "source_timestamp": observed_at,
            "emitted_at": now,
            "observed_at": observed_at,
            "expires_at": now + CROWN_TTL_MS,
            "action_id": None,
        }
        self.emit(validate_feedback_event(event))

    def _on_band_power(self, payload):
        if self._handle_loss(payload, "band-power", "band-power"):
            return
        now = self.now()
        observed_at = payload.get("timestamp", now)
        event = {
            "kind": "band-power",
            "value": payload["data"],
            "confidence": 1.0,
            "readiness": "ready",
            "source": {
                "device": DEVICE,
                "model": MODEL,
                "metric": "band-power",
            },
            "source_timestamp": observed_at,
            "emitted_at": now,
            "observed_at": observed_at,
            "expires_at": now + CROWN_TTL_MS,
            "action_id": None,
        }
        self.emit(validate_feedback_event(event))

    def _on_kinesis(self, label, payload):
        if self._handle_loss(payload, "kinesis", label):
            return
        now = self.now()
        observed_at = payload["timestamp"]
        event = {
            "kind": "kinesis",
            "value": payload["label"],
            "confidence": payload["probability"],
            "readiness": "ready",
            "source": {
                "device": DEVICE,
                "model": MODEL,
                "metric": label,
            },
            "source_timestamp": observed_at,
            "emitted_at": now,
            "observed_at": observed_at,
            "expires_at": now + CROWN_TTL_MS,
            "action_id": None,
        }
        self.emit(validate_feedback_event(event))

    def _readiness(self, now):
        if now - self.stream_started_at < WARMUP_MS:
            return "warming"
        return "ready"
