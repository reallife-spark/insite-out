SOURCE_IDENTITY_FIELDS = ("device", "model", "metric")
WATCH_METRIC_FIELDS = ("metric", "unit")
FRESHNESS_FIELDS = ("observed_at", "expires_at")
BASE_FIELDS = (
    "kind",
    "value",
    "confidence",
    "readiness",
    "source_timestamp",
    "emitted_at",
)
TIMESTAMP_FIELDS = ("source_timestamp", "emitted_at")
KINDS = frozenset(
    {"focus", "calm", "kinesis", "band-power", "signal-quality", "watch-metric"}
)
READINESS_STATES = frozenset({"warming", "ready", "degraded", "unavailable"})


def _is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_expired(event, now):
    return now >= event["expires_at"]


def unavailable_feedback_event(
    *,
    kind,
    device,
    model,
    metric,
    observed_at,
    emitted_at,
    action_id=None,
):
    return {
        "kind": kind,
        "value": None,
        "confidence": 0.0,
        "readiness": "unavailable",
        "source_timestamp": observed_at,
        "emitted_at": emitted_at,
        "observed_at": observed_at,
        "expires_at": observed_at,
        "source": {"device": device, "model": model, "metric": metric},
        "action_id": action_id,
    }


def validate_feedback_event(event):
    for field in BASE_FIELDS:
        if field not in event:
            raise ValueError(f"{field} is required")

    if event["kind"] not in KINDS:
        raise ValueError("kind is not a known feedback kind")
    if event["readiness"] not in READINESS_STATES:
        raise ValueError("readiness is not a known state")

    value = event["value"]
    if value is None:
        if event["readiness"] != "unavailable":
            raise ValueError("value may be null only when readiness is unavailable")
    elif isinstance(value, str):
        if event["kind"] != "kinesis":
            raise ValueError("string values are allowed only for kinesis labels")
    elif isinstance(value, bool) or not isinstance(value, (int, float, dict)):
        raise ValueError("value must be a number, object, or kinesis label")

    confidence = event["confidence"]
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not 0.0 <= confidence <= 1.0
    ):
        raise ValueError("confidence must be a number in 0.0–1.0")

    for field in TIMESTAMP_FIELDS:
        if not _is_integer(event[field]):
            raise ValueError(f"{field} must be an integer")

    source = event.get("source")
    if not isinstance(source, dict):
        raise ValueError("source must be an object")
    for field in SOURCE_IDENTITY_FIELDS:
        source_value = source.get(field)
        if not isinstance(source_value, str) or not source_value.strip():
            raise ValueError(f"source.{field} must be a non-empty string")

    if event["kind"] == "watch-metric":
        for field in WATCH_METRIC_FIELDS:
            watch_value = event.get(field)
            if not isinstance(watch_value, str) or not watch_value.strip():
                raise ValueError(f"{field} must be a non-empty string")

    for field in FRESHNESS_FIELDS:
        if field not in event:
            raise ValueError(f"{field} is required")
        if not _is_integer(event[field]):
            raise ValueError(f"{field} must be an integer")
    if event["expires_at"] < event["observed_at"]:
        raise ValueError("expires_at must not be earlier than observed_at")
    return event
