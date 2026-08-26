from __future__ import annotations

import pandas as pd


def validate_event_batch(df: pd.DataFrame) -> dict[str, int]:
    required = {"event_id", "customer_id", "event_type", "event_ts"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    metrics = {
        "row_count": int(len(df)),
        "null_event_ids": int(df["event_id"].isna().sum()),
        "duplicate_event_ids": int(df["event_id"].duplicated().sum()),
        "null_customer_ids": int(df["customer_id"].isna().sum()),
        "invalid_timestamps": int(pd.to_datetime(df["event_ts"], utc=True, errors="coerce").isna().sum()),
    }
    if metrics["null_event_ids"] or metrics["duplicate_event_ids"] or metrics["null_customer_ids"]:
        raise ValueError(f"Event quality gate failed: {metrics}")
    return metrics
