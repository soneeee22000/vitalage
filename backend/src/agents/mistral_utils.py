import asyncio
import json
import logging
from typing import Any

from mistralai import Mistral
from mistralai.models import ResponseFormat

logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Raised when an AI agent call fails."""

    def __init__(self, agent_name: str, detail: str) -> None:
        self.agent_name = agent_name
        self.detail = detail
        super().__init__(f"[{agent_name}] {detail}")


class AgentTimeoutError(AgentError):
    """Raised when an AI agent call times out."""

    def __init__(self, agent_name: str) -> None:
        super().__init__(agent_name, "Request timed out")


async def safe_chat_complete(
    client: Mistral,
    *,
    model: str,
    messages: list[dict[str, str]],
    response_format: ResponseFormat | None = None,
    temperature: float = 0.3,
    timeout_seconds: float = 30.0,
    agent_name: str = "unknown",
    max_retries: int = 3,
) -> str:
    """Call Mistral chat API with timeout, retry on 429, and error handling."""
    last_exc: Exception | None = None

    for attempt in range(max_retries):
        try:
            response = await asyncio.wait_for(
                client.chat.complete_async(
                    model=model,
                    messages=messages,  # type: ignore[arg-type]
                    response_format=response_format,
                    temperature=temperature,
                ),
                timeout=timeout_seconds,
            )
        except TimeoutError as exc:
            logger.error(
                "[%s] Mistral API timed out after %ss",
                agent_name,
                timeout_seconds,
            )
            raise AgentTimeoutError(agent_name) from exc
        except Exception as exc:
            last_exc = exc
            if "429" in str(exc) and attempt < max_retries - 1:
                wait = 2 ** attempt + 1
                logger.warning(
                    "[%s] Rate limited (429), retrying in %ss (attempt %d/%d)",
                    agent_name,
                    wait,
                    attempt + 1,
                    max_retries,
                )
                await asyncio.sleep(wait)
                continue
            logger.error("[%s] Mistral API error: %s", agent_name, exc)
            raise AgentError(agent_name, f"API call failed: {exc}") from exc
        else:
            if not response.choices:
                raise AgentError(agent_name, "Empty choices in Mistral response")

            content = response.choices[0].message.content
            if content is None:
                raise AgentError(agent_name, "Null content in Mistral response")

            return str(content)

    raise AgentError(
        agent_name, f"API call failed after {max_retries} retries: {last_exc}"
    )


def safe_json_parse(raw: str, *, agent_name: str) -> dict[str, Any]:
    """Parse a JSON string with a clear error on failure."""
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("[%s] Invalid JSON from Mistral: %s", agent_name, raw[:200])
        raise AgentError(agent_name, f"Invalid JSON response: {exc}") from exc

    if not isinstance(parsed, dict):
        kind = type(parsed).__name__
        raise AgentError(agent_name, f"Expected JSON object, got {kind}")

    return parsed
