from __future__ import annotations

import pandas as pd


def build_customer_360(events: pd.DataFrame) -> pd.DataFrame:
    required = {"event_id", "customer_id", "event_type", "event_ts"}
    missing = required.difference(events.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df = events.copy()
    df["event_ts"] = pd.to_datetime(df["event_ts"], utc=True, errors="coerce")
    df = df.dropna(subset=["customer_id", "event_ts"])
    df = df.drop_duplicates(subset=["event_id"])

    summary = (
        df.groupby("customer_id", as_index=False)
        .agg(
            event_count=("event_id", "count"),
            last_event_ts=("event_ts", "max"),
            purchase_count=("event_type", lambda s: (s == "purchase").sum()),
            login_count=("event_type", lambda s: (s == "login").sum()),
        )
    )
    summary["customer_status"] = summary["purchase_count"].map(
        lambda n: "active_buyer" if n > 0 else "engaged"
    )
    return summary
