import base64
import logging
from typing import Any

from mistralai import Mistral
from mistralai.models import ResponseFormat
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.mistral_utils import safe_chat_complete, safe_json_parse
from src.services.audit_service import AuditService

AGENT_NAME = "meal_analyzer"
MODEL = "mistral-small-latest"

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Tu es un nutritionniste bienveillant qui analyse des photos de repas.
Tu dois identifier les aliments visibles et evaluer la qualite nutritionnelle.

IMPORTANT:
- Sois TOUJOURS positif. Commence par ce qui est bien dans le repas.
- Ne compte JAMAIS les calories. Evalue la qualite, pas la quantite.
- Donne UN conseil actionnable et bienveillant.
- Reponds en francais.

Reponds en JSON avec exactement ces cles:
{
  "foods_identified": ["liste des aliments identifies"],
  "nutritional_highlights": ["points forts nutritionnels, ex: riche en fibres"],
  "quality_score": 70,
  "micro_tip": "un conseil positif et actionnable",
  "summary": "description courte du repas en une phrase"
}

quality_score est un entier de 0 a 100 basé sur:
- Diversite des groupes alimentaires (proteines, legumes, feculents, fruits)
- Presence de fibres, vitamines, mineraux
- Equilibre general du repas
- Un repas avec legumes + proteines + feculents complets = 80+
- Un repas avec un seul groupe alimentaire = 40-50"""


class MealAnalyzer:
    """Analyzes meal photos for nutritional quality using Mistral vision."""

    def __init__(self, api_key: str, session: AsyncSession) -> None:
        self._client = Mistral(api_key=api_key)
        self._audit = AuditService(session)

    async def analyze_meal(
        self, image_base64: str, patient_ref: str
    ) -> dict[str, Any]:
        """Analyze a meal photo and return nutritional assessment."""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyse ce repas.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                ],
            },
        ]

        raw = await safe_chat_complete(
            self._client,
            model=MODEL,
            messages=messages,  # type: ignore[arg-type]
            response_format=ResponseFormat(type="json_object"),
            agent_name=AGENT_NAME,
            timeout_seconds=45.0,
        )

        parsed = safe_json_parse(raw, agent_name=AGENT_NAME)

        quality_score = parsed.get("quality_score", 50)
        if not isinstance(quality_score, int):
            try:
                quality_score = int(quality_score)
            except (ValueError, TypeError):
                quality_score = 50
        quality_score = max(0, min(100, quality_score))
        parsed["quality_score"] = quality_score

        await self._audit.log_ai_call(
            agent_name=AGENT_NAME,
            model_version=MODEL,
            patient_ref=patient_ref,
            input_text="[meal photo]",
            output_text=raw,
        )

        return parsed

    @staticmethod
    def validate_base64(image_base64: str) -> bool:
        """Check if the string is valid base64."""
        try:
            base64.b64decode(image_base64, validate=True)
            return True
        except Exception:
            return False
