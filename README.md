# Real-Time Customer 360 Data Platform

A production-oriented streaming data platform that builds a unified customer view from real-time behavioral events and batch customer data.

## Architecture

```text
Web / Mobile / Business Events
            |
            v
      Apache Kafka
            |
            v
   Spark Structured Streaming
            |
      +-----+------+
      |            |
      v            v
 S3 Bronze     Data Quality
      |            |
      +-----+------+
            v
       S3 Silver
   (partitioned Parquet)
            |
            v
 PostgreSQL / Warehouse
       Customer 360
            |
        +---+---+
        |       |
        v       v
      dbt    Analytics APIs

Airflow --> batch backfills / reconciliation / SLA monitoring
Terraform --> AWS infrastructure
GitHub Actions --> CI / tests / validation
Bedrock --> AI-assisted event/customer insight summarization
```
<img width="1536" height="1024" alt="Real-Time Customer 360 Data Platform" src="https://github.com/user-attachments/assets/49d1de4f-a54b-4c07-8177-a103039578cb" />


## What this demonstrates

- Event-driven ingestion with Kafka
- PySpark Structured Streaming for scalable event processing
- Lakehouse-style Bronze/Silver layers on Amazon S3
- Customer 360 dimensional modeling and SQL analytics
- PostgreSQL locally with a warehouse-compatible serving pattern
- dbt-style transformation and data tests
- Airflow for batch backfills, reconciliation, and operational workflows
- Terraform for repeatable cloud infrastructure
- AI-assisted operational intelligence using Amazon Bedrock as an optional runtime integration
- Automated unit/integration checks through GitHub Actions

## Streaming flow

1. Customer events are published to Kafka.
2. Spark Structured Streaming reads events and validates the event contract.
3. Invalid records are routed to a quarantine path instead of silently dropped.
4. Valid events are written to S3 Bronze and transformed into partitioned Silver Parquet.
5. Customer-level aggregates are upserted into the analytics serving layer.
6. dbt models expose business-ready customer metrics.
7. Airflow manages backfills, reconciliation, and scheduled maintenance.
8. Aggregate quality metrics can be sent to an approved LLM endpoint for incident/insight summarization.

## Repository structure

```text
├── .github/workflows/        # CI
├── airflow/dags/             # Airflow orchestration
├── dbt/                      # Analytics models and tests
├── docker/                   # Local Kafka/Postgres services
├── infra/terraform/          # AWS infrastructure
├── src/
│   ├── contracts.py          # Event contract validation
│   ├── stream_processor.py   # Spark streaming transformations
│   ├── customer_360.py       # Customer-level aggregation logic
│   ├── data_quality.py       # Deterministic quality checks
│   └── ai_insights.py        # Optional Bedrock integration
├── tests/                    # Fast local tests
├── requirements-dev.txt      # Lightweight CI/test dependencies
├── requirements-runtime.txt  # Production runtime dependencies
└── README.md
```

## Local validation

```bash
python -m venv .venv
# activate the environment
pip install -r requirements-dev.txt
python -m pytest -q
```

The CI workflow intentionally does not require AWS credentials, Kafka, Spark, or a live database. Cloud/runtime integration code is validated through unit tests and static checks, while infrastructure and streaming services are exercised through their deployment/runtime environments.

## Security

No credentials, connection strings, tokens, or cloud account identifiers belong in source control. Runtime values are supplied through environment variables, AWS IAM/Secrets Manager, or the deployment environment.
