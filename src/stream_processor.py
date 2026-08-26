from __future__ import annotations

from typing import Any


def build_streaming_job(spark: Any, kafka_bootstrap: str, topic: str, output_path: str, checkpoint_path: str) -> Any:
    """Build the Spark Structured Streaming query.

    The function constructs the production streaming graph without starting it,
    which keeps unit tests independent from Kafka/S3 credentials.
    """
    from pyspark.sql import functions as F
    from pyspark.sql.types import StringType, StructField, StructType, TimestampType

    event_schema = StructType(
        [
            StructField("event_id", StringType(), False),
            StructField("customer_id", StringType(), False),
            StructField("event_type", StringType(), False),
            StructField("event_ts", TimestampType(), False),
            StructField("payload", StringType(), True),
        ]
    )

    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap)
        .option("subscribe", topic)
        .option("startingOffsets", "latest")
        .load()
    )

    events = (
        raw.select(F.from_json(F.col("value").cast("string"), event_schema).alias("event"))
        .select("event.*")
        .withColumn("ingest_ts", F.current_timestamp())
        .withColumn("event_date", F.to_date("event_ts"))
    )

    valid = events.filter(
        F.col("event_id").isNotNull()
        & F.col("customer_id").isNotNull()
        & F.col("event_ts").isNotNull()
    )

    return (
        valid.writeStream.format("parquet")
        .option("path", output_path)
        .option("checkpointLocation", checkpoint_path)
        .partitionBy("event_date")
        .outputMode("append")
    )
