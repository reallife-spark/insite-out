import json
from pathlib import Path

import pytest

from insite_out.feedback_event import is_expired
from insite_out.watch_adapter import LocalWatchBridge, WatchAdapter

FIXTURES = Path(__file__).parent / "fixtures"
FIXTURE = FIXTURES / "heart_rate_payload.json"
IBI_FIXTURE = FIXTURES / "heart_rate_ibi_payload.json"
TEMPERATURE_FIXTURE = FIXTURES / "skin_temperature_payload.json"


class FakeTracker:
    def __init__(self):
        self.callback = None
        self.unsubscribed = 0

    def subscribe(self, callback):
        self.callback = callback
        return self.unsubscribe

    def unsubscribe(self):
        self.unsubscribed += 1


class FakeTransport:
    def __init__(self, receiver):
        self.receiver = receiver
        self.endpoints = []

    def send(self, endpoint, payload):
        self.endpoints.append(endpoint)
        self.receiver(payload)


def test_recorded_heart_rate_payload_becomes_one_valid_watch_metric_event():
    payload = json.loads(FIXTURE.read_text())
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)

    adapter.translate(payload)

    assert emitted == [
        {
            "kind": "watch-metric",
            "value": 72,
            "confidence": 1.0,
            "readiness": "ready",
            "source": {
                "device": "galaxy-watch5-pro",
                "model": "galaxy-watch5-pro",
                "metric": "heart-rate",
            },
            "source_timestamp": 17000,
            "emitted_at": 17005,
            "observed_at": 17000,
            "expires_at": 20000,
            "metric": "heart-rate",
            "unit": "bpm",
            "action_id": None,
        }
    ]


def test_error_status_marks_the_metric_degraded():
    payload = {
        "tracker": "HEART_RATE_CONTINUOUS",
        "timestamp": 17000,
        "values": {"HEART_RATE": 72, "HEART_RATE_STATUS": 1},
    }
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)

    payload["values"]["HEART_RATE_STATUS"] = 0
    adapter.translate(payload)
    payload["values"]["HEART_RATE_STATUS"] = 1
    adapter.translate(payload)

    assert emitted[-1]["readiness"] == "degraded"
    assert emitted[-1]["confidence"] == 0.5


def test_expired_heart_rate_is_rejected_at_its_expiry_boundary():
    payload = json.loads(FIXTURE.read_text())
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)
    adapter.translate(payload)

    assert is_expired(emitted[0], 19999) is False
    assert is_expired(emitted[0], 20000) is True


def test_disconnect_emits_an_unavailable_watch_metric_event():
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 20000)

    adapter.mark_unavailable("heart-rate", 20000)

    assert emitted == [
        {
            "kind": "watch-metric",
            "value": None,
            "confidence": 0.0,
            "readiness": "unavailable",
            "source": {
                "device": "galaxy-watch5-pro",
                "model": "galaxy-watch5-pro",
                "metric": "heart-rate",
            },
            "source_timestamp": 20000,
            "emitted_at": 20000,
            "observed_at": 20000,
            "expires_at": 20000,
            "metric": "heart-rate",
            "unit": "bpm",
            "action_id": None,
        }
    ]


def test_raw_ecg_and_ppg_payloads_are_ignored():
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)

    adapter.translate({"tracker": "ECG_ON_DEMAND", "timestamp": 17000, "values": {"ECG": [1, 2]}})
    adapter.translate({"tracker": "PPG_CONTINUOUS", "timestamp": 17000, "values": {"PPG_GREEN": [3]}})
    adapter.translate({"tracker": "PPG_ON_DEMAND", "timestamp": 17000, "values": {"PPG_GREEN": [3]}})

    assert emitted == []


def test_bridge_delivers_tracker_data_to_the_agent_seam_over_a_local_endpoint():
    payload = json.loads(FIXTURE.read_text())
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)
    transport = FakeTransport(adapter.translate)
    tracker = FakeTracker()
    bridge = LocalWatchBridge(
        tracker,
        transport=transport,
        host="127.0.0.1",
        port=8765,
    )

    bridge.start()
    tracker.callback(payload)

    assert len(emitted) == 1
    assert emitted[0]["kind"] == "watch-metric"
    assert emitted[0]["source"]["metric"] == "heart-rate"
    assert transport.endpoints == [("127.0.0.1", 8765)]


def test_heart_rate_payload_with_ibi_emits_two_parallel_events():
    payload = json.loads(IBI_FIXTURE.read_text())
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)

    adapter.translate(payload)

    assert [event["metric"] for event in emitted] == ["heart-rate", "inter-beat-interval"]
    assert emitted[1] == {
        "kind": "watch-metric",
        "value": {0: 812, 1: 803, 2: 798},
        "confidence": 1.0,
        "readiness": "ready",
        "source": {
            "device": "galaxy-watch5-pro",
            "model": "galaxy-watch5-pro",
            "metric": "inter-beat-interval",
        },
        "source_timestamp": 17000,
        "emitted_at": 17005,
        "observed_at": 17000,
        "expires_at": 20000,
        "metric": "inter-beat-interval",
        "unit": "ms",
        "action_id": None,
    }


def test_temperature_payload_emits_skin_and_ambient_as_parallel_events():
    payload = json.loads(TEMPERATURE_FIXTURE.read_text())
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17510)

    adapter.translate(payload)

    assert [event["metric"] for event in emitted] == ["skin-temperature", "ambient-temperature"]
    assert [event["unit"] for event in emitted] == ["celsius", "celsius"]
    assert [event["expires_at"] - event["observed_at"] for event in emitted] == [60000, 60000]
    assert [event["readiness"] for event in emitted] == ["ready", "ready"]
    assert [event["value"] for event in emitted] == [33.6, 22.4]
    assert all(event["source"]["model"] == "galaxy-watch5-pro" for event in emitted)
    assert all(event["kind"] == "watch-metric" for event in emitted)


def test_temperature_error_status_marks_both_metrics_degraded():
    payload = json.loads(TEMPERATURE_FIXTURE.read_text())
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17510)

    adapter.translate(payload)
    payload["values"]["STATUS"] = -1
    adapter.translate(payload)

    assert [event["readiness"] for event in emitted[-2:]] == ["degraded", "degraded"]
    assert [event["confidence"] for event in emitted[-2:]] == [0.5, 0.5]


def test_ibi_error_status_marks_only_the_interval_degraded():
    payload = json.loads(IBI_FIXTURE.read_text())
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)

    adapter.translate(payload)
    payload["values"]["IBI_STATUS_LIST"] = [0, 1, 0]
    adapter.translate(payload)

    assert [event["metric"] for event in emitted[-2:]] == ["heart-rate", "inter-beat-interval"]
    assert [event["readiness"] for event in emitted[-2:]] == ["ready", "degraded"]


def test_first_invalid_sample_is_warming_then_later_invalid_samples_are_degraded():
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 17005)
    payload = json.loads(FIXTURE.read_text())

    payload["values"]["HEART_RATE_STATUS"] = 1
    adapter.translate(payload)
    payload["values"]["HEART_RATE_STATUS"] = 0
    adapter.translate(payload)
    payload["values"]["HEART_RATE_STATUS"] = 1
    adapter.translate(payload)

    assert [event["readiness"] for event in emitted] == ["warming", "ready", "degraded"]
    assert [event["confidence"] for event in emitted] == [0.0, 1.0, 0.5]
    assert emitted[0]["value"] == 72


@pytest.mark.parametrize(
    "metric,ttl_ms",
    [
        ("heart-rate", 3000),
        ("inter-beat-interval", 3000),
        ("skin-temperature", 60000),
        ("ambient-temperature", 60000),
    ],
)
def test_each_metric_uses_its_approved_freshness_budget(metric, ttl_ms):
    from insite_out.watch_adapter import METRIC_SPECS

    assert METRIC_SPECS[metric]["ttl_ms"] == ttl_ms


def test_registry_covers_every_approved_watch_metric():
    from insite_out.watch_adapter import METRIC_SPECS

    assert set(METRIC_SPECS) == {
        "heart-rate",
        "inter-beat-interval",
        "skin-temperature",
        "ambient-temperature",
    }


@pytest.mark.parametrize(
    "metric,unit",
    [
        ("heart-rate", "bpm"),
        ("inter-beat-interval", "ms"),
        ("skin-temperature", "celsius"),
        ("ambient-temperature", "celsius"),
    ],
)
def test_every_metric_can_emit_an_unavailable_event(metric, unit):
    emitted = []
    adapter = WatchAdapter(emit=emitted.append, now=lambda: 30000)

    adapter.mark_unavailable(metric, 30000)

    assert emitted[0]["metric"] == metric
    assert emitted[0]["unit"] == unit
    assert emitted[0]["readiness"] == "unavailable"
    assert emitted[0]["value"] is None
    assert emitted[0]["expires_at"] == 30000
    assert emitted[0]["source"]["metric"] == metric


def test_bridge_rejects_a_public_endpoint():
    adapter = WatchAdapter(emit=lambda event: None, now=lambda: 0)
    transport = FakeTransport(adapter.translate)

    with pytest.raises(ValueError):
        LocalWatchBridge(
            FakeTracker(),
            transport=transport,
            host="8.8.8.8",
            port=8765,
        )


def test_bridge_close_unregisters_the_tracker_once():
    adapter = WatchAdapter(emit=lambda event: None, now=lambda: 0)
    transport = FakeTransport(adapter.translate)
    tracker = FakeTracker()
    bridge = LocalWatchBridge(
        tracker,
        transport=transport,
        host="127.0.0.1",
        port=8765,
    )
    bridge.start()

    bridge.close()
    bridge.close()

    assert tracker.unsubscribed == 1
