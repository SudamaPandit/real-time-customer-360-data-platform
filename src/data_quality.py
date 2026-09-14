from __future__ import annotations

import pandas as pd


def validate_event_batch(df: pd.DataFrame) -> dict[str, int]:
    required = {"event_id", "customer_id", "event_type", "event_ts"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    event_ids = df["event_id"].astype("string").str.strip()
    customer_ids = df["customer_id"].astype("string").str.strip()
    event_types = df["event_type"].astype("string").str.strip()
    metrics = {
        "row_count": int(len(df)),
        "blank_event_ids": int((event_ids.isna() | event_ids.eq("")).sum()),
        "duplicate_event_ids": int(event_ids.duplicated().sum()),
        "blank_customer_ids": int((customer_ids.isna() | customer_ids.eq("")).sum()),
        "blank_event_types": int((event_types.isna() | event_types.eq("")).sum()),
        "invalid_timestamps": int(
            pd.to_datetime(df["event_ts"], utc=True, errors="coerce").isna().sum()
        ),
    }
    failing = {name: value for name, value in metrics.items() if name != "row_count" and value}
    if not metrics["row_count"] or failing:
        raise ValueError(f"Event quality gate failed: {metrics}")
    return metrics
