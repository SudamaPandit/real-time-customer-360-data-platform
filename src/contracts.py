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

    if not event["event_id"] or not event["customer_id"]:
        raise ValueError("event_id and customer_id are required")
    if not isinstance(event["payload"], dict):
        raise ValueError("payload must be an object")

    event_ts = event["event_ts"]
    if isinstance(event_ts, str):
        event_ts = datetime.fromisoformat(event_ts.replace("Z", "+00:00"))
    if not isinstance(event_ts, datetime):
        raise ValueError("event_ts must be an ISO timestamp or datetime")

    return CustomerEvent(
        event_id=str(event["event_id"]),
        customer_id=str(event["customer_id"]),
        event_type=str(event["event_type"]),
        event_ts=event_ts,
        payload=event["payload"],
    )
