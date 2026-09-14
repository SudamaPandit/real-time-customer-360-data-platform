from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CustomerEvent:
    event_id: str
    customer_id: str
    event_type: str
    event_ts: datetime
    payload: dict[str, Any]


def validate_event(event: dict[str, Any]) -> CustomerEvent:
    required = {"event_id", "customer_id", "event_type", "event_ts", "payload"}
    missing = required.difference(event)
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")

    if not str(event["event_id"]).strip() or not str(event["customer_id"]).strip():
        raise ValueError("event_id and customer_id are required")
    if not str(event["event_type"]).strip():
        raise ValueError("event_type is required")
    if not isinstance(event["payload"], dict):
        raise ValueError("payload must be an object")

    event_ts = event["event_ts"]
    if isinstance(event_ts, str):
        try:
            event_ts = datetime.fromisoformat(event_ts.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("event_ts must be a valid ISO timestamp") from exc
    if not isinstance(event_ts, datetime):
        raise ValueError("event_ts must be an ISO timestamp or datetime")

    return CustomerEvent(
        event_id=str(event["event_id"]).strip(),
        customer_id=str(event["customer_id"]).strip(),
        event_type=str(event["event_type"]).strip().lower(),
        event_ts=event_ts,
        payload=event["payload"],
    )
