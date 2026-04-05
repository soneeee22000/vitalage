import pytest

from src.agents.mistral_utils import AgentError, safe_json_parse


def test_safe_json_parse_valid() -> None:
    """Valid JSON dict parses correctly."""
    result = safe_json_parse('{"key": "value"}', agent_name="test")
    assert result == {"key": "value"}


def test_safe_json_parse_invalid_json() -> None:
    """Invalid JSON raises AgentError."""
    with pytest.raises(AgentError, match="Invalid JSON"):
        safe_json_parse("not json", agent_name="test")


def test_safe_json_parse_non_dict() -> None:
    """JSON array raises AgentError."""
    with pytest.raises(AgentError, match="Expected JSON object"):
        safe_json_parse("[1, 2, 3]", agent_name="test")
