# Real-Time Customer 360 Platform

A focused streaming example that parses customer events from Kafka with Spark
Structured Streaming, applies an event contract, writes valid events as
date-partitioned Parquet, and exposes a dbt customer-level aggregation.

## Implemented flow

- `src/stream_processor.py` builds a Kafka-to-Parquet streaming writer with a
  checkpoint and event-date partitions.
- `src/contracts.py` provides the Python-side event contract used by producers
  and fixture validation.
- `src/data_quality.py` validates offline/replay batches for blank identifiers,
  duplicates, missing event types, and invalid timestamps.
- `src/customer_360.py` provides an offline pandas aggregation.
- `dbt/` contains an executable project and the SQL customer aggregation.
- `infra/terraform/` provisions a versioned S3 bucket.
- Optional Bedrock summarization accepts aggregate operational metrics only.

## Run unit tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

CI intentionally tests contract, quality, and aggregation logic without
requiring Kafka, Spark, AWS, or a database. Install
`requirements-runtime.txt` to build the streaming graph.

## Current boundaries

- Invalid Spark records are filtered but are not yet persisted to a quarantine
  topic/path.
- The repository does not include a local Docker stack or a deployed serving
  database.
- The dbt model expects an external `silver.customer_events` source and a
  configured dbt profile.
- Terraform covers S3 only; Kafka and Spark infrastructure are external.
- Reconciliation/backfill orchestration is not implemented.
- Exactly-once guarantees depend on the configured source, checkpoint storage,
  and downstream sink.

These boundaries keep this project centered on streaming contracts and
customer aggregation rather than pretending to be a complete production
platform.
