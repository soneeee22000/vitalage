from typing import Any

from mistralai import Mistral
from mistralai.models import ResponseFormat
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.mistral_utils import safe_chat_complete, safe_json_parse
from src.services.audit_service import AuditService

AGENT_NAME = "check_in_analyzer"
MODEL = "mistral-small-latest"


class CheckInAnalyzer:
    """Structures free-text symptoms from daily check-ins."""

    def __init__(self, api_key: str, session: AsyncSession) -> None:
        self._client = Mistral(api_key=api_key)
        self._audit = AuditService(session)

    async def analyze_symptoms(
        self, symptoms_text: str, patient_ref: str
    ) -> dict[str, Any]:
        """Parse free-text symptoms into structured categories."""
        messages = [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant sante qui structure les symptomes "
                    "rapportes par un patient. Reponds en JSON avec les cles: "
                    '"categories" (liste de categories de symptomes), '
                    '"severity" (leger/modere/important), '
                    '"recommendation" (conseil bienveillant en francais). '
                    "Sois positif et rassurant. Ne fais jamais de diagnostic."
                ),
            },
            {
                "role": "user",
                "content": f"Symptomes rapportes: {symptoms_text}",
            },
        ]

        raw = await safe_chat_complete(
            self._client,
            model=MODEL,
            messages=messages,
            response_format=ResponseFormat(type="json_object"),
            agent_name=AGENT_NAME,
        )

        parsed = safe_json_parse(raw, agent_name=AGENT_NAME)

        await self._audit.log_ai_call(
            agent_name=AGENT_NAME,
            model_version=MODEL,
            patient_ref=patient_ref,
            input_text=symptoms_text,
            output_text=raw,
        )

        return parsed
