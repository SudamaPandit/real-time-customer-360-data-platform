import pandas as pd
import pytest

from src.data_quality import validate_event_batch


def valid_batch():
    return pd.DataFrame([
        {"event_id": "1", "customer_id": "c1", "event_type": "login", "event_ts": "2026-08-26T10:00:00Z"},
        {"event_id": "2", "customer_id": "c2", "event_type": "purchase", "event_ts": "2026-08-26T11:00:00Z"},
    ])


def test_quality_metrics_return_counts():
    metrics = validate_event_batch(valid_batch())
    assert metrics["row_count"] == 2
    assert metrics["duplicate_event_ids"] == 0


@pytest.mark.parametrize("column,value,metric", [
    ("event_id", "1", "duplicate_event_ids"),
    ("customer_id", " ", "blank_customer_ids"),
    ("event_type", "", "blank_event_types"),
    ("event_ts", "bad", "invalid_timestamps"),
])
def test_quality_gate_rejects_bad_events(column, value, metric):
    df = valid_batch()
    df.loc[1, column] = value
    with pytest.raises(ValueError, match=metric):
        validate_event_batch(df)


def test_quality_gate_rejects_empty_batch():
    with pytest.raises(ValueError, match="quality gate"):
        validate_event_batch(valid_batch().iloc[:0])
