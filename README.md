# Real-Time Customer 360 Platform

Streaming pipeline that merges real-time behavioral events (Kafka) with
batch customer data into a single, continuously-updated customer view.
This is the project I built to go deeper than "read from Kafka, write to
S3" - the interesting part is what happens at the boundary between
streaming and batch, and how invalid events get handled instead of
quietly dropped.

## The part I actually cared about here

Two things break streaming pipelines in practice, so I built around them:

**Bad events shouldn't disappear.** `contracts.py` validates every event
against an explicit schema before it's processed. Anything that fails
validation goes to a quarantine path - it's inspectable and
replayable later - instead of being silently discarded, which is what
happens by default in a lot of streaming code I've seen.

**Batch and streaming have to agree eventually.** Real-time aggregates
drift from ground truth over time (late-arriving events, brief consumer
lag, retries). Airflow-driven backfill/reconciliation jobs periodically
recompute the customer aggregates from the full event history and
reconcile them against what streaming produced - so "real-time" doesn't
quietly become "permanently approximate."

## Architecture

```
Events (web/mobile/business)
        │
        ▼
     Kafka
        │
        ▼
Spark Structured Streaming ── validates event contract
        │
   ┌────┴────┐
   ▼         ▼
Quarantine   S3 Bronze
(invalid)      │
               ▼
         Data quality
               │
               ▼
         S3 Silver (partitioned Parquet)
               │
               ▼
      Postgres - Customer 360 serving layer
               │
               ▼
            dbt models ── business-ready metrics

Airflow: backfill / reconciliation / SLA monitoring
Terraform: AWS infra
```
<img width="1536" height="1024" alt="Real-Time Customer 360 Data Platform" src="https://github.com/user-attachments/assets/49d1de4f-a54b-4c07-8177-a103039578cb" />

## Repository structure

```
airflow/dags/            orchestration - backfills, reconciliation, SLA checks
dbt/                      transformation models + data tests
docker/                   local Kafka + Postgres for development
infra/terraform/          AWS infra
src/
  contracts.py            event schema validation
  stream_processor.py     Spark Structured Streaming logic
  customer_360.py         aggregation into the unified customer view
  data_quality.py          deterministic checks on the batch side
  ai_insights.py           optional Bedrock-based summarization
tests/
requirements-dev.txt       for CI/local test runs
requirements-runtime.txt   what actually runs in production
```

## Running it locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
```

Tests don't need a live Kafka broker, Spark cluster, or database - the
streaming logic is tested against recorded event fixtures, and I kept the
CI dependency list (`requirements-dev.txt`) deliberately lighter than
the runtime one, since Spark/Kafka client libraries are large and CI
doesn't need them to validate the transformation logic.

## How I actually developed and tested this

I don't run a live Kafka cluster or Spark streaming job continuously -
there's no traffic to justify it, and MSK/EMR-class services aren't
free-tier.

- Local development used Kafka and Postgres via `docker/` (Docker
  Compose) - this is genuinely how most of the iteration happened, and
  it's a normal way to develop against Kafka even in real jobs.
- I ran Spark Structured Streaming against the local Kafka container to
  validate the actual streaming logic (windowing, watermarking, the
  quarantine path) end-to-end, not just against unit-test fixtures.
- S3 was used directly for a handful of validation runs (free tier
  covers this).
- Bedrock calls for the optional insight-summarization step are pay-per
  token and cheap enough to actually run for real - a handful of test
  calls, not a recurring cost.

If asked in an interview "is this running live," the honest answer is
no - it's a local-first build that was validated end-to-end, not a
permanently deployed service, because keeping Kafka/Spark infrastructure
running 24/7 for a portfolio project doesn't make financial sense.

## What I'd change at real scale

- Exactly-once semantics aren't fully guaranteed end-to-end yet - Spark
  Structured Streaming gives strong guarantees within itself, but the
  handoff into Postgres would need idempotent upserts hardened further
  for true exactly-once behavior under retry.
- Schema evolution for the event contract is manual right now; I'd want
  a schema registry (Confluent/Glue Schema Registry) so producers and
  consumers can evolve independently.
- Reconciliation currently runs on a fixed schedule; SLA-driven
  triggering would be better once there's a real freshness requirement
  to hit.
