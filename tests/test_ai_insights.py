import os

from src.ai_insights import build_insight_prompt, summarize_with_bedrock


def test_prompt_contains_only_aggregate_metrics():
    prompt = build_insight_prompt({"row_count": 1000, "duplicate_rate": 0.02})
    assert "row_count" in prompt
    assert "duplicate_rate" in prompt


def test_ai_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("AI_ENABLED", raising=False)
    assert summarize_with_bedrock({"row_count": 10}) == "AI insights disabled"


def test_ai_enabled_without_model_id_fails_clearly(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.delenv("BEDROCK_MODEL_ID", raising=False)
    try:
        summarize_with_bedrock({"row_count": 10})
    except Exception as exc:
        assert isinstance(exc, (KeyError, ModuleNotFoundError))
