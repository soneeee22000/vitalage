from datetime import datetime, timezone
from uuid import uuid4

from fhir.resources.auditevent import AuditEvent
from fhir.resources.consent import Consent
from fhir.resources.patient import Patient

from src.models.fhir_constants import (
    AUDIT_CODE_AI_QUERY,
    AUDIT_CODE_AI_QUERY_DISPLAY,
    AUDIT_SYSTEM_DCM,
    CONSENT_CATEGORY_CODE,
    SYSTEM_VITALAGE,
)


def create_patient(
    given_name: str, family_name: str, identifier: str
) -> Patient:
    """Create a FHIR Patient resource."""
    return Patient(
        id=str(uuid4()),
        identifier=[
            {  # type: ignore[list-item]
                "system": SYSTEM_VITALAGE,
                "value": identifier,
            }
        ],
        name=[{"given": [given_name], "family": family_name}],  # type: ignore[list-item]
    )


def create_consent(
    patient_ref: str, scope: str
) -> Consent:
    """Create a FHIR Consent resource."""
    return Consent(
        id=str(uuid4()),
        status="active",
        category=[
            {  # type: ignore[list-item]
                "coding": [
                    {
                        "system": SYSTEM_VITALAGE,
                        "code": CONSENT_CATEGORY_CODE,
                    }
                ]
            }
        ],
        subject={"reference": patient_ref},  # type: ignore[arg-type]
        date=datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),  # type: ignore[arg-type]
        provision=[
            {  # type: ignore[list-item]
                "purpose": [
                    {
                        "system": SYSTEM_VITALAGE,
                        "code": scope,
                        "display": f"Consent for {scope}",
                    }
                ],
            }
        ],
    )


def create_audit_event(
    agent_name: str,
    patient_ref: str | None = None,
) -> AuditEvent:
    """Create a FHIR AuditEvent for tracking AI agent calls."""
    entity_list = []
    if patient_ref:
        entity_list.append({"what": {"reference": patient_ref}})
    return AuditEvent(
        id=str(uuid4()),
        code={  # type: ignore[arg-type]
            "coding": [
                {
                    "system": AUDIT_SYSTEM_DCM,
                    "code": AUDIT_CODE_AI_QUERY,
                    "display": AUDIT_CODE_AI_QUERY_DISPLAY,
                }
            ]
        },
        agent=[
            {  # type: ignore[list-item]
                "who": {"display": agent_name},
                "requestor": False,
            }
        ],
        source={"observer": {"display": "vitalage-api"}},  # type: ignore[arg-type]
        recorded=datetime.now(tz=timezone.utc).isoformat(),  # type: ignore[arg-type]
        entity=entity_list if entity_list else None,  # type: ignore[arg-type]
    )
