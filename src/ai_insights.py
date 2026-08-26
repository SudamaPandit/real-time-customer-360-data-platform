from __future__ import annotations

import json
import os
from typing import Any


def build_insight_prompt(metrics: dict[str, Any]) -> str:
    safe_metrics = json.dumps(metrics, sort_keys=True)
    return (
        "Analyze these aggregate Customer 360 pipeline metrics. "
        "Identify anomalies, likely engineering causes, and three useful "
        "investigation actions. Do not infer or request personal data.\n"
        f"Metrics: {safe_metrics}"
    )


def summarize_with_bedrock(metrics: dict[str, Any]) -> str:
    """Optional Bedrock integration; deterministic pipeline remains authoritative."""
    if os.getenv("AI_ENABLED", "false").lower() != "true":
        return "AI insights disabled"

    import boto3

    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
    response = client.converse(
        modelId=os.environ["BEDROCK_MODEL_ID"],
        messages=[{"role": "user", "content": [{"text": build_insight_prompt(metrics)}]}],
        inferenceConfig={"maxTokens": 400, "temperature": 0.1},
    )
    return response["output"]["message"]["content"][0]["text"]
