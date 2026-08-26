import pandas as pd
import pytest

from src.data_quality import validate_event_batch


def test_quality_metrics_return_counts():
    df = pd.DataFrame(
        [
            {"event_id": "1", "customer_id": "c1", "event_type": "login", "event_ts": "2026-08-26T10:00:00Z"},
            {"event_id": "2", "customer_id": "c2", "event_type": "purchase", "event_ts": "2026-08-26T11:00:00Z"},
        ]
    )
    metrics = validate_event_batch(df)
    assert metrics["row_count"] == 2
    assert metrics["duplicate_event_ids"] == 0


def test_quality_gate_rejects_duplicates():
    df = pd.DataFrame(
        [
            {"event_id": "1", "customer_id": "c1", "event_type": "login", "event_ts": "2026-08-26T10:00:00Z"},
            {"event_id": "1", "customer_id": "c1", "event_type": "login", "event_ts": "2026-08-26T10:01:00Z"},
        ]
    )
    with pytest.raises(ValueError, match="quality gate"):
        validate_event_batch(df)
