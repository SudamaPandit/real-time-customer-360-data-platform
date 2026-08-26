import pandas as pd

from src.customer_360 import build_customer_360


def test_build_customer_360_deduplicates_and_aggregates():
    df = pd.DataFrame(
        [
            {"event_id": "1", "customer_id": "c1", "event_type": "login", "event_ts": "2026-08-26T10:00:00Z"},
            {"event_id": "2", "customer_id": "c1", "event_type": "purchase", "event_ts": "2026-08-26T11:00:00Z"},
            {"event_id": "2", "customer_id": "c1", "event_type": "purchase", "event_ts": "2026-08-26T11:00:00Z"},
            {"event_id": "3", "customer_id": "c2", "event_type": "login", "event_ts": "2026-08-26T12:00:00Z"},
        ]
    )

    result = build_customer_360(df)
    c1 = result[result["customer_id"] == "c1"].iloc[0]
    assert c1["event_count"] == 2
    assert c1["purchase_count"] == 1
    assert c1["customer_status"] == "active_buyer"
