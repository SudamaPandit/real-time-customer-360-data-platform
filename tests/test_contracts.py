import pytest

from src.contracts import validate_event


def test_validate_event_accepts_iso_timestamp():
    event = validate_event(
        {
            "event_id": "e1",
            "customer_id": "c1",
            "event_type": "purchase",
            "event_ts": "2026-08-26T10:00:00Z",
            "payload": {"amount": 25.5},
        }
    )
    assert event.customer_id == "c1"
    assert event.event_type == "purchase"


def test_validate_event_rejects_missing_fields():
    with pytest.raises(ValueError, match="Missing required fields"):
        validate_event({"event_id": "e1"})


def test_validate_event_rejects_non_object_payload():
    with pytest.raises(ValueError, match="payload"):
        validate_event(
            {
                "event_id": "e1",
                "customer_id": "c1",
                "event_type": "login",
                "event_ts": "2026-08-26T10:00:00Z",
                "payload": "bad",
            }
        )
