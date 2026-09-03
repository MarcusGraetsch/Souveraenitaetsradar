from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class ApplicabilityStatus(str, Enum):
    APPLICABLE = "applicable"
    NOT_APPLICABLE = "not_applicable"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class ApplicabilityResult:
    status: ApplicabilityStatus
    reason: str
    matched_facts: tuple[str, ...] = ()


def _norm(value: str | None) -> str:
    text = (value or "").strip().lower()
    text = (
        text.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    text = re.sub(r"\s+", " ", text)
    return text


def _bool_fact(name: str, value: bool | None) -> tuple[str, bool | None]:
    return name, value


def _level_at_least(level: str | None, threshold: str) -> bool | None:
    order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    current = order.get(_norm(level))
    target = order.get(_norm(threshold))
    if current is None or target is None:
        return None
    return current >= target


def default_profile(assessment: dict[str, Any]) -> dict[str, Any]:
    workload = _norm(str(assessment.get("workload_type", "")))
    ai_used: bool | None
    agentic_ai: bool | None
    if workload == "ai-agent":
        ai_used, agentic_ai = True, True
    elif workload == "ai-system":
        ai_used, agentic_ai = True, False
    elif workload in {"application", "saas", "cloud-platform", "infrastructure"}:
        ai_used, agentic_ai = False, False
    else:
        ai_used, agentic_ai = None, None

    service_model = "saas" if workload == "saas" else "unknown"
    cloud_service = True if workload in {"saas", "cloud-platform"} else None

    return {
        "service_model": service_model,
        "cloud_service": cloud_service,
        "contract_in_scope": None,
        "data_processing": None,
        "persistent_data": None,
        "encryption_used": None,
        "key_model": "unknown",
        "ai_used": ai_used,
        "agentic_ai": agentic_ai,
        "exit_relevant": None,
        "backup_relevant": None,
        "multi_provider": None,
        "subcontractors_used": None,
        "c5_relevant": None,
        "c3a_relevant": None,
        "iam_relevant": None,
        "logging_relevant": None,
        "internet_exposed": None,
    }


def _predicate_candidates(
    applicability: str,
    assessment: dict[str, Any],
    profile: dict[str, Any],
) -> list[tuple[str, bool | None]]:
    text = _norm(applicability)
    candidates: list[tuple[str, bool | None]] = []

    def has(*parts: str) -> bool:
        return any(_norm(part) in text for part in parts)

    if has("generative ki", "agenten", "ki-agent", "ki agent", "agentisch"):
        candidates.append(_bool_fact("agentic_ai", profile.get("agentic_ai")))
    elif re.search(r"\bki\b", text):
        candidates.append(_bool_fact("ai_used", profile.get("ai_used")))

    if has("iaas/paas", "iaas oder paas", "iaas bzw. paas"):
        service = _norm(str(profile.get("service_model", "unknown")))
        candidates.append(("service_model in iaas/paas", None if service == "unknown" else service in {"iaas", "paas"}))
    elif re.search(r"\biaas\b", text):
        service = _norm(str(profile.get("service_model", "unknown")))
        candidates.append(("service_model=iaas", None if service == "unknown" else service == "iaas"))
    elif re.search(r"\bpaas\b", text):
        service = _norm(str(profile.get("service_model", "unknown")))
        candidates.append(("service_model=paas", None if service == "unknown" else service == "paas"))
    elif re.search(r"\bsaas\b", text):
        service = _norm(str(profile.get("service_model", "unknown")))
        candidates.append(("service_model=saas", None if service == "unknown" else service == "saas"))

    if has("cloud service", "cloud-service", "cloudservice"):
        candidates.append(_bool_fact("cloud_service", profile.get("cloud_service")))

    if has("vertrag", "contract"):
        candidates.append(_bool_fact("contract_in_scope", profile.get("contract_in_scope")))

    if has("daten verarbeitet", "datenverarbeitung", "daten verarbeitet werden"):
        candidates.append(_bool_fact("data_processing", profile.get("data_processing")))
    if has("daten gespeichert", "persistente daten", "persistenz"):
        if has("gespeichert/verarbeitet", "gespeichert oder verarbeitet"):
            a = profile.get("persistent_data")
            b = profile.get("data_processing")
            combined = True if a is True or b is True else False if a is False and b is False else None
            candidates.append(("persistent_data OR data_processing", combined))
        else:
            candidates.append(_bool_fact("persistent_data", profile.get("persistent_data")))

    if has("verschluessel"):
        candidates.append(_bool_fact("encryption_used", profile.get("encryption_used")))

    if has("schluessel providerbezogen", "providerbezogene schluessel", "provider-managed"):
        key_model = _norm(str(profile.get("key_model", "unknown")))
        candidates.append(("key_model provider/mixed", None if key_model == "unknown" else key_model in {"provider", "mixed"}))
    elif has("schluessel") and not has("schluesselwort"):
        key_model = _norm(str(profile.get("key_model", "unknown")))
        candidates.append(("key_model present", None if key_model == "unknown" else key_model not in {"none", ""}))

    if has("exit", "portabilitaet", "wechsel relevant"):
        candidates.append(_bool_fact("exit_relevant", profile.get("exit_relevant")))
    if has("backup", "wiederherstellung", "restore"):
        candidates.append(_bool_fact("backup_relevant", profile.get("backup_relevant")))
    if has("multi-provider", "mehrere provider", "mehrprovider"):
        candidates.append(_bool_fact("multi_provider", profile.get("multi_provider")))
    if has("unterauftragnehmer", "subprocessor", "subunternehmer"):
        candidates.append(_bool_fact("subcontractors_used", profile.get("subcontractors_used")))
    if re.search(r"\bc5\b", text):
        candidates.append(_bool_fact("c5_relevant", profile.get("c5_relevant")))
    if re.search(r"\bc3a\b", text):
        candidates.append(_bool_fact("c3a_relevant", profile.get("c3a_relevant")))
    if has("iam", "identitaets", "identity"):
        candidates.append(_bool_fact("iam_relevant", profile.get("iam_relevant")))
    if has("logging", "monitoring", "protokollierung"):
        candidates.append(_bool_fact("logging_relevant", profile.get("logging_relevant")))
    if has("internet-exponiert", "internet exponiert", "oeffentlich erreichbar"):
        candidates.append(_bool_fact("internet_exposed", profile.get("internet_exposed")))

    if has("kritischer workload", "kritisch", "hohe kritikalitaet"):
        candidates.append(("criticality>=high", _level_at_least(str(assessment.get("criticality", "")), "high")))
    if has("vertraulichkeit hoch", "hohe vertraulichkeit", "vertraulichkeit sehr hoch"):
        candidates.append(("confidentiality>=high", _level_at_least(str(assessment.get("confidentiality", "")), "high")))
    if has("verfuegbarkeit hoch", "hohe verfuegbarkeit", "verfuegbarkeit sehr hoch"):
        candidates.append(("availability>=high", _level_at_least(str(assessment.get("availability", "")), "high")))
    if has("integritaet hoch", "hohe integritaet", "integritaet sehr hoch"):
        candidates.append(("integrity>=high", _level_at_least(str(assessment.get("integrity", "")), "high")))

    seen: set[str] = set()
    result: list[tuple[str, bool | None]] = []
    for name, value in candidates:
        if name not in seen:
            seen.add(name)
            result.append((name, value))
    return result


def evaluate_applicability(
    applicability: str | None,
    assessment: dict[str, Any],
    profile: dict[str, Any] | None = None,
) -> ApplicabilityResult:
    raw = (applicability or "").strip()
    text = _norm(raw)
    merged = {**default_profile(assessment), **(profile or {})}

    if not text or text in {"immer", "always"}:
        return ApplicabilityResult(ApplicabilityStatus.APPLICABLE, "Frage ist laut Methodenbank immer anwendbar.")

    if not text.startswith("wenn") and "falls" not in text:
        return ApplicabilityResult(
            ApplicabilityStatus.NEEDS_REVIEW,
            f"Anwendbarkeitsregel '{raw}' ist noch nicht deterministisch operationalisiert.",
        )

    candidates = _predicate_candidates(text, assessment, merged)
    if not candidates:
        return ApplicabilityResult(
            ApplicabilityStatus.NEEDS_REVIEW,
            f"Anwendbarkeitsregel '{raw}' benötigt einen noch nicht modellierten Scope-Fakt.",
        )

    values = [value for _, value in candidates]
    names = tuple(name for name, _ in candidates)

    is_or = " oder " in text or "/" in text
    if is_or:
        if any(value is True for value in values):
            return ApplicabilityResult(
                ApplicabilityStatus.APPLICABLE,
                f"Mindestens eine Bedingung der Regel '{raw}' ist erfüllt.",
                names,
            )
        if all(value is False for value in values):
            return ApplicabilityResult(
                ApplicabilityStatus.NOT_APPLICABLE,
                f"Alle bekannten Alternativbedingungen der Regel '{raw}' sind ausgeschlossen.",
                names,
            )
    else:
        if any(value is False for value in values):
            return ApplicabilityResult(
                ApplicabilityStatus.NOT_APPLICABLE,
                f"Mindestens eine notwendige Bedingung der Regel '{raw}' ist nach aktuellem Scope ausgeschlossen.",
                names,
            )
        if all(value is True for value in values):
            return ApplicabilityResult(
                ApplicabilityStatus.APPLICABLE,
                f"Die bekannten Bedingungen der Regel '{raw}' sind erfüllt.",
                names,
            )

    return ApplicabilityResult(
        ApplicabilityStatus.NEEDS_REVIEW,
        f"Die Regel '{raw}' kann mit dem aktuellen Relevanzprofil nicht eindeutig entschieden werden.",
        names,
    )


def apply_to_questions(
    questions: Iterable[dict[str, Any]],
    assessment: dict[str, Any],
    profile: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for question in questions:
        decision = evaluate_applicability(question.get("applicability"), assessment, profile)
        result.append({
            **question,
            "applicability_status": decision.status.value,
            "applicability_reason": decision.reason,
            "applicability_facts": list(decision.matched_facts),
        })
    return result
