import logging
from typing import Any

from mistralai import Mistral
from mistralai.models import ResponseFormat
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.mistral_utils import safe_chat_complete, safe_json_parse
from src.services.audit_service import AuditService

AGENT_NAME = "insight_engine"
MODEL = "mistral-small-latest"

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Tu es un analyste sante bienveillant. A partir des donnees de
bilans quotidiens d'un patient, tu detectes des correlations personnelles
entre ses habitudes et son bien-etre.

Genere des insights en francais, personnels et actionnables.
Chaque insight doit etre une observation basee sur les DONNEES du patient,
pas un conseil generique.

Bon exemple: "Quand vous dormez plus de 4/5, votre energie
le lendemain est 35% plus elevee"
Mauvais exemple: "Dormez bien pour avoir de l'energie"

Reponds en JSON:
{
  "insights": [
    {
      "text": "l'insight en francais",
      "type": "correlation",
      "data": {
        "dimension_a": "sleep",
        "dimension_b": "energy",
        "direction": "positive",
        "strength": "strong"
      }
    }
  ]
}

Types possibles: "correlation", "trend", "recommendation"
Directions: "positive", "negative"
Strength: "strong", "moderate", "weak"
Genere entre 3 et 5 insights."""


class InsightEngine:
    """Detects personal health correlations from check-in data."""

    def __init__(self, api_key: str, session: AsyncSession) -> None:
        self._client = Mistral(api_key=api_key)
        self._audit = AuditService(session)

    async def generate_insights(
        self, patient_data_summary: str, patient_ref: str
    ) -> list[dict[str, Any]]:
        """Generate personal health insights from patient data."""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Voici les donnees des bilans quotidiens du patient:\n\n"
                    f"{patient_data_summary}\n\n"
                    "Analyse ces donnees et genere des insights personnels."
                ),
            },
        ]

        raw = await safe_chat_complete(
            self._client,
            model=MODEL,
            messages=messages,
            response_format=ResponseFormat(type="json_object"),
            agent_name=AGENT_NAME,
            timeout_seconds=30.0,
        )

        parsed = safe_json_parse(raw, agent_name=AGENT_NAME)
        insights = parsed.get("insights", [])

        await self._audit.log_ai_call(
            agent_name=AGENT_NAME,
            model_version=MODEL,
            patient_ref=patient_ref,
            input_text=patient_data_summary[:500],
            output_text=raw,
        )

        if not isinstance(insights, list):
            return []
        return insights
