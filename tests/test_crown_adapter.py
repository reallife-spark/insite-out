from insite_out.crown_adapter import CrownAdapter


class FakeSDK:
    def __init__(self):
        self.callbacks = {}
        self.unsubscribed = []

    def focus(self, callback):
        self.callbacks["focus"] = callback
        return lambda: self.unsubscribed.append("focus")

    def calm(self, callback):
        self.callbacks["calm"] = callback
        return lambda: self.unsubscribed.append("calm")

    def brainwaves_power_by_band(self, callback):
        self.callbacks["band-power"] = callback
        return lambda: self.unsubscribed.append("band-power")

    def kinesis(self, label, callback):
        self.callbacks[f"kinesis:{label}"] = callback
        return lambda: self.unsubscribed.append(f"kinesis:{label}")


def test_focus_payload_becomes_a_valid_ready_event_after_warmup():
    sdk = FakeSDK()
    emitted = []
    clock = [17000]
    adapter = CrownAdapter(
        sdk,
        emit=emitted.append,
        now=lambda: clock[0],
        stream_started_at=0,
        kinesis_labels=("left",),
    )
    adapter.start()

    sdk.callbacks["focus"](
        {"probability": 0.82, "metric": "awareness", "label": "focus", "timestamp": 16000}
    )

    assert emitted == [
        {
            "kind": "focus",
            "value": 0.82,
            "confidence": 1.0,
            "readiness": "ready",
            "source": {
                "device": "neurosity-crown",
                "model": "crown",
                "metric": "focus",
            },
            "source_timestamp": 16000,
            "emitted_at": 17000,
            "observed_at": 16000,
            "expires_at": 18000,
            "action_id": None,
        }
    ]


def test_focus_payload_during_warmup_carries_warming_and_zero_confidence():
    sdk = FakeSDK()
    emitted = []
    clock = [15999]
    adapter = CrownAdapter(
        sdk,
        emit=emitted.append,
        now=lambda: clock[0],
        stream_started_at=0,
        kinesis_labels=("left",),
    )
    adapter.start()

    sdk.callbacks["focus"](
        {"probability": 0.02, "metric": "awareness", "label": "focus", "timestamp": 15000}
    )

    assert emitted[0]["readiness"] == "warming"
    assert emitted[0]["confidence"] == 0.0
    assert emitted[0]["value"] == 0.02


def test_calm_payload_becomes_a_valid_source_tagged_event():
    sdk = FakeSDK()
    emitted = []
    adapter = CrownAdapter(
        sdk,
        emit=emitted.append,
        now=lambda: 20000,
        stream_started_at=0,
        kinesis_labels=("left",),
    )
    adapter.start()

    sdk.callbacks["calm"](
        {"probability": 0.64, "metric": "awareness", "label": "calm", "timestamp": 19000}
    )

    assert emitted[0]["kind"] == "calm"
    assert emitted[0]["value"] == 0.64
    assert emitted[0]["source"] == {
        "device": "neurosity-crown",
        "model": "crown",
        "metric": "calm",
    }


def test_band_power_payload_preserves_band_labels():
    sdk = FakeSDK()
    emitted = []
    adapter = CrownAdapter(
        sdk,
        emit=emitted.append,
        now=lambda: 20000,
        stream_started_at=0,
        kinesis_labels=("left",),
    )
    adapter.start()

    sdk.callbacks["band-power"](
        {
            "label": "powerByBand",
            "data": {
                "alpha": [0.43, 0.70],
                "beta": [1.04, 0.65],
                "delta": [0.46, 1.00],
                "gamma": [0.22, 0.21],
                "theta": [0.64, 0.93],
            },
        }
    )

    assert emitted[0]["kind"] == "band-power"
    assert emitted[0]["value"] == {
        "alpha": [0.43, 0.70],
        "beta": [1.04, 0.65],
        "delta": [0.46, 1.00],
        "gamma": [0.22, 0.21],
        "theta": [0.64, 0.93],
    }
    assert emitted[0]["readiness"] == "ready"
    assert emitted[0]["source"]["metric"] == "band-power"
    assert emitted[0]["observed_at"] == 20000
    assert emitted[0]["source_timestamp"] == 20000


def test_kinesis_detection_becomes_an_event_with_the_command_label():
    sdk = FakeSDK()
    emitted = []
    adapter = CrownAdapter(
        sdk,
        emit=emitted.append,
        now=lambda: 20000,
        stream_started_at=0,
        kinesis_labels=("left",),
    )
    adapter.start()

    sdk.callbacks["kinesis:left"](
        {
            "probability": 0.93,
            "label": "left",
            "metric": "kinesis",
            "timestamp": 19000,
        }
    )

    assert emitted[0]["kind"] == "kinesis"
    assert emitted[0]["value"] == "left"
    assert emitted[0]["confidence"] == 0.93
    assert emitted[0]["source"]["metric"] == "left"


def test_subscription_loss_emits_unavailable_instead_of_silence():
    sdk = FakeSDK()
    emitted = []
    adapter = CrownAdapter(
        sdk,
        emit=emitted.append,
        now=lambda: 20000,
        stream_started_at=0,
        kinesis_labels=("left",),
    )
    adapter.start()

    sdk.callbacks["focus"](None)

    assert emitted == [
        {
            "kind": "focus",
            "value": None,
            "confidence": 0.0,
            "readiness": "unavailable",
            "source": {
                "device": "neurosity-crown",
                "model": "crown",
                "metric": "focus",
            },
            "source_timestamp": 20000,
            "emitted_at": 20000,
            "observed_at": 20000,
            "expires_at": 20000,
            "action_id": None,
        }
    ]


def test_close_calls_every_subscription_teardown_once():
    sdk = FakeSDK()
    adapter = CrownAdapter(
        sdk,
        emit=lambda event: None,
        now=lambda: 0,
        stream_started_at=0,
        kinesis_labels=("left",),
    )
    adapter.start()

    adapter.close()
    adapter.close()

    assert sdk.unsubscribed == ["focus", "calm", "band-power", "kinesis:left"]
