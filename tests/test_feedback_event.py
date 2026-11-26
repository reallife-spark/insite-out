import pytest

from insite_out.feedback_event import (
    is_expired,
    unavailable_feedback_event,
    validate_feedback_event,
)


def focus_event():
    return {
        "kind": "focus",
        "value": 0.82,
        "confidence": 0.91,
        "readiness": "ready",
        "source_timestamp": 1000,
        "emitted_at": 1001,
        "observed_at": 1000,
        "expires_at": 1600,
        "source": {
            "device": "neurosity-crown",
            "model": "crown",
            "metric": "focus",
        },
        "action_id": None,
    }


def watch_metric_event():
    return {
        "kind": "watch-metric",
        "value": 72,
        "confidence": 0.8,
        "readiness": "ready",
        "source_timestamp": 2000,
        "emitted_at": 2001,
        "observed_at": 2000,
        "expires_at": 2300,
        "source": {
            "device": "samsung-watch",
            "model": "galaxy-watch5-pro",
            "metric": "hypothetical-watch-metric",
        },
        "action_id": None,
        "metric": "hypothetical-watch-metric",
        "unit": "units",
    }


def test_valid_focus_event_is_accepted_at_agent_seam():
    event = focus_event()

    assert validate_feedback_event(event) == event


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [("device", ""), ("model", "   "), ("metric", "")],
)
def test_rejects_incomplete_source_identity(field, bad_value):
    event = focus_event()
    event["source"][field] = bad_value

    with pytest.raises(ValueError):
        validate_feedback_event(event)


def test_watch_metric_accepts_unlisted_metric_name():
    event = watch_metric_event()

    assert validate_feedback_event(event) == event


@pytest.mark.parametrize("field", ["metric", "unit"])
def test_watch_metric_requires_metric_and_unit(field):
    event = watch_metric_event()
    del event[field]

    with pytest.raises(ValueError):
        validate_feedback_event(event)


@pytest.mark.parametrize("field", ["observed_at", "expires_at"])
def test_requires_freshness_fields(field):
    event = focus_event()
    del event[field]

    with pytest.raises(ValueError):
        validate_feedback_event(event)


def test_rejects_expiry_before_observation():
    event = focus_event()
    event["expires_at"] = 999

    with pytest.raises(ValueError):
        validate_feedback_event(event)


@pytest.mark.parametrize(
    "field",
    ["kind", "value", "confidence", "readiness", "source_timestamp", "emitted_at"],
)
def test_requires_base_fields(field):
    event = focus_event()
    del event[field]

    with pytest.raises(ValueError):
        validate_feedback_event(event)


def test_rejects_unknown_kind():
    event = focus_event()
    event["kind"] = "not-a-feedback-kind"

    with pytest.raises(ValueError):
        validate_feedback_event(event)


def test_rejects_unknown_readiness():
    event = focus_event()
    event["readiness"] = "not-a-readiness-state"

    with pytest.raises(ValueError):
        validate_feedback_event(event)


def test_accepts_warming_readiness_for_focus():
    event = focus_event()
    event["readiness"] = "warming"
    event["value"] = 0.02

    assert validate_feedback_event(event) == event


def test_event_is_expired_at_and_after_expiry():
    event = focus_event()

    assert is_expired(event, 1599) is False
    assert is_expired(event, 1600) is True
    assert is_expired(event, 1601) is True


def test_unavailable_feed_event_is_valid_and_expired():
    event = unavailable_feedback_event(
        kind="focus",
        device="neurosity-crown",
        model="crown",
        metric="focus",
        observed_at=3000,
        emitted_at=3001,
    )

    assert event["readiness"] == "unavailable"
    assert event["expires_at"] == 3000
    assert validate_feedback_event(event) == event
    assert is_expired(event, 3000) is True


def test_null_value_is_rejected_when_readiness_is_ready():
    event = focus_event()
    event["value"] = None

    with pytest.raises(ValueError):
        validate_feedback_event(event)


def test_string_value_is_rejected():
    event = focus_event()
    event["value"] = "high"

    with pytest.raises(ValueError):
        validate_feedback_event(event)


def test_kinesis_accepts_a_command_label_value():
    event = focus_event()
    event["kind"] = "kinesis"
    event["value"] = "left"

    assert validate_feedback_event(event) == event


@pytest.mark.parametrize("bad_confidence", [-0.1, 1.1])
def test_rejects_confidence_outside_unit_interval(bad_confidence):
    event = focus_event()
    event["confidence"] = bad_confidence

    with pytest.raises(ValueError):
        validate_feedback_event(event)


@pytest.mark.parametrize("field", ["source_timestamp", "emitted_at"])
def test_rejects_non_integer_timestamps(field):
    event = focus_event()
    event[field] = "1000"

    with pytest.raises(ValueError):
        validate_feedback_event(event)
