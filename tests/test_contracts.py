import pytest

from src.contracts import validate_event


def event(**overrides):
    value = {
        "event_id": "e1",
        "customer_id": "c1",
        "event_type": "Purchase",
        "event_ts": "2026-08-26T10:00:00Z",
        "payload": {"amount": 25.5},
    }
    value.update(overrides)
    return value


def test_validate_event_normalizes_values():
    result = validate_event(event(event_id=" e1 "))
    assert result.event_id == "e1"
    assert result.event_type == "purchase"


def test_validate_event_rejects_missing_fields():
    with pytest.raises(ValueError, match="Missing required fields"):
        validate_event({"event_id": "e1"})


@pytest.mark.parametrize("change,message", [
    ({"payload": "bad"}, "payload"),
    ({"event_ts": "not-a-date"}, "valid ISO"),
    ({"customer_id": " "}, "required"),
])
def test_validate_event_rejects_invalid_values(change, message):
    with pytest.raises(ValueError, match=message):
        validate_event(event(**change))
