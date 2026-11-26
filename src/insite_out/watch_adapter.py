from ipaddress import ip_address

from .feedback_event import unavailable_feedback_event, validate_feedback_event

DEVICE = "galaxy-watch5-pro"
MODEL = "galaxy-watch5-pro"

METRIC_SPECS = {
    "heart-rate": {
        "tracker": "HEART_RATE_CONTINUOUS",
        "value_key": "HEART_RATE",
        "status_key": "HEART_RATE_STATUS",
        "unit": "bpm",
        "ttl_ms": 3000,
    },
    "inter-beat-interval": {
        "tracker": "HEART_RATE_CONTINUOUS",
        "value_key": "IBI_LIST",
        "status_key": "IBI_STATUS_LIST",
        "unit": "ms",
        "ttl_ms": 3000,
        "pack_values": True,
    },
    "skin-temperature": {
        "tracker": "SKIN_TEMPERATURE_CONTINUOUS",
        "value_key": "OBJECT_TEMPERATURE",
        "status_key": "STATUS",
        "unit": "celsius",
        "ttl_ms": 60000,
    },
    "ambient-temperature": {
        "tracker": "SKIN_TEMPERATURE_CONTINUOUS",
        "value_key": "AMBIENT_TEMPERATURE",
        "status_key": "STATUS",
        "unit": "celsius",
        "ttl_ms": 60000,
    },
}


def _status_is_ok(status):
    if isinstance(status, list):
        return all(value == 0 for value in status)
    return status == 0


class WatchAdapter:
    def __init__(self, *, emit, now):
        self.emit = emit
        self.now = now
        self._valid_metrics = set()

    def translate(self, payload):
        values = payload["values"]
        observed_at = payload["timestamp"]
        emitted_at = self.now()
        for metric, spec in METRIC_SPECS.items():
            if payload.get("tracker") != spec["tracker"]:
                continue
            if spec["value_key"] not in values:
                continue
            status = values.get(spec["status_key"])
            if _status_is_ok(status):
                readiness = "ready"
                self._valid_metrics.add(metric)
            elif metric in self._valid_metrics:
                readiness = "degraded"
            else:
                readiness = "warming"
            confidence = {"ready": 1.0, "degraded": 0.5, "warming": 0.0}[readiness]
            value = values[spec["value_key"]]
            if spec.get("pack_values"):
                value = dict(enumerate(value))
            event = {
                "kind": "watch-metric",
                "value": value,
                "confidence": confidence,
                "readiness": readiness,
                "source": {
                    "device": DEVICE,
                    "model": MODEL,
                    "metric": metric,
                },
                "source_timestamp": observed_at,
                "emitted_at": emitted_at,
                "observed_at": observed_at,
                "expires_at": observed_at + spec["ttl_ms"],
                "metric": metric,
                "unit": spec["unit"],
                "action_id": None,
            }
            self.emit(validate_feedback_event(event))

    def mark_unavailable(self, metric, now):
        spec = METRIC_SPECS[metric]
        event = unavailable_feedback_event(
            kind="watch-metric",
            device=DEVICE,
            model=MODEL,
            metric=metric,
            observed_at=now,
            emitted_at=now,
        )
        event["metric"] = metric
        event["unit"] = spec["unit"]
        self.emit(validate_feedback_event(event))


class LocalWatchBridge:
    """Publishes tracker records to a local-only endpoint for the agent-side adapter."""

    def __init__(self, tracker, *, transport, host="127.0.0.1", port=8765):
        address = ip_address(host)
        if not (address.is_loopback or address.is_private):
            raise ValueError("Watch bridge endpoint must be loopback or private")
        self.endpoint = (host, port)
        self.tracker = tracker
        self.transport = transport
        self._unsubscribe = None

    def start(self):
        if self._unsubscribe is None:
            self._unsubscribe = self.tracker.subscribe(self._on_data)

    def _on_data(self, payload):
        self.transport.send(self.endpoint, payload)

    def close(self):
        if self._unsubscribe is not None:
            self._unsubscribe()
            self._unsubscribe = None
