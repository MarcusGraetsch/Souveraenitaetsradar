from __future__ import annotations

from typing import Any


BOOLEAN_OPTIONS = [
    {"value": "yes", "label": "Ja"},
    {"value": "no", "label": "Nein"},
    {"value": "unknown", "label": "Noch unklar"},
]

BOOLEAN_PARTIAL_OPTIONS = [
    {"value": "yes", "label": "Ja"},
    {"value": "partial", "label": "Teilweise"},
    {"value": "no", "label": "Nein"},
    {"value": "unknown", "label": "Noch unklar"},
]

SCALE_1_5_OPTIONS = [
    *[{"value": str(value), "label": f"Stufe {value}"} for value in range(1, 6)],
    {"value": "unknown", "label": "Noch unklar"},
]


def _control(
    source_type: str,
    kind: str,
    *,
    options: list[dict[str, str]] | None = None,
    placeholder: str = "",
    help_text: str = "",
    mapping_status: str = "mapped",
) -> dict[str, Any]:
    return {
        "source_type": source_type,
        "kind": kind,
        "options": options or [],
        "placeholder": placeholder,
        "help_text": help_text,
        "mapping_status": mapping_status,
    }


def _explicit_enum_options(raw: str) -> list[dict[str, str]] | None:
    if not raw.startswith("Enum "):
        return None
    values = raw.removeprefix("Enum ").strip()
    if not values or values == "1-5":
        return None
    parts = [part.strip() for part in values.split("/") if part.strip()]
    if len(parts) < 2:
        return None
    return [
        *[{"value": part, "label": part} for part in parts],
        {"value": "unknown", "label": "Noch unklar"},
    ]


def answer_control_for(answer_type: str) -> dict[str, Any]:
    """Map method-level `Antworttyp` values to a small, deterministic UI vocabulary.

    The question bank remains the source for the semantic answer type. This mapping only
    chooses a suitable input control; it does not change scoring, applicability or gates.
    Unknown method types are surfaced as `needs_review` instead of silently falling back
    to the old compliance-status dropdown.
    """

    raw = (answer_type or "").strip()
    lowered = raw.casefold()

    if raw == "Boolean":
        return _control(raw, "single_select", options=BOOLEAN_OPTIONS)
    if raw == "Boolean/Teilweise":
        return _control(raw, "single_select", options=BOOLEAN_PARTIAL_OPTIONS)
    if raw == "Enum 1-5":
        return _control(
            raw,
            "single_select",
            options=SCALE_1_5_OPTIONS,
            help_text="Interne 1–5-Einstufung gemäß der konkreten Methodenfrage.",
        )

    explicit_options = _explicit_enum_options(raw)
    if explicit_options:
        return _control(raw, "single_select", options=explicit_options)

    if raw in {"Text/ID", "Text", "Freitext", "Rolle/Person", "Land"}:
        return _control(raw, "text", placeholder="Antwort eingeben")

    if raw in {"Liste", "Referenzliste", "Länderliste"}:
        return _control(
            raw,
            "list",
            placeholder="Mehrere Werte – je Zeile ein Eintrag",
            help_text="Mehrere Werte können zeilenweise erfasst werden.",
        )

    if raw == "Dauer":
        return _control(
            raw,
            "text",
            placeholder="z. B. 4 Stunden oder 30 Tage",
            help_text="Wert und Zeiteinheit gemeinsam angeben.",
        )

    if raw == "Größe":
        return _control(
            raw,
            "text",
            placeholder="z. B. 500 GB oder 2,5 TB",
            help_text="Wert und Einheit gemeinsam angeben.",
        )

    if raw in {"Datum", "Zeitpunkt"}:
        return _control(raw, "date")

    if raw in {"Prozent", "Percentage"}:
        return _control(raw, "text", placeholder="z. B. 80 %")

    # Complex answer types already present in the method bank combine several facts.
    # Until dedicated structured schemas exist, collect them explicitly as structured
    # text rather than pretending that fulfilled/partial/not-fulfilled is meaningful.
    complex_markers = (
        "matrix",
        "multi-select",
        "3x enum",
        "boolean+",
        "dauer+",
        "enum/",
        "sla/",
        "fristen",
        "kosten",
        "betrag",
        "version",
        "score",
        "gewicht",
        "ratio",
        "bandbreite",
        "anzahl",
        "datum+",
        "+datum",
        "sov1-8",
        "graph/",
        "dokument+",
        "prozent/",
    )
    if any(marker in lowered for marker in complex_markers):
        return _control(
            raw,
            "structured_text",
            placeholder=f"Strukturierte Antwort ({raw})",
            help_text=(
                "Dieser Methoden-Antworttyp enthält mehrere Teilwerte. "
                "Bis ein eigenes Feldschema vorliegt, werden diese gemeinsam als strukturierte Textantwort erfasst."
            ),
        )

    # Generic Enum without encoded options must not invent an option set.
    if raw == "Enum":
        return _control(
            raw,
            "structured_text",
            placeholder="Auswahl/Einordnung beschreiben",
            help_text=(
                "Die Methodenbank kennzeichnet diese Frage als Enum, enthält aber noch keine maschinenlesbare Optionsliste. "
                "Die Auswahl wird deshalb vorerst als strukturierte Antwort erfasst."
            ),
        )

    # A few method types are descriptive but use domain-specific labels. Treat these
    # only when they clearly describe a textual/list/numeric value.
    if any(token in lowered for token in ("liste", "rolle", "person", "land", "staat", "jurisdiktion")):
        return _control(raw, "list", placeholder="Werte eingeben – je Zeile ein Eintrag")
    if any(token in lowered for token in ("dauer", "frist", "zeit", "rto", "rpo")):
        return _control(raw, "text", placeholder="Wert mit Zeiteinheit eingeben")
    if any(token in lowered for token in ("größe", "volumen", "menge")):
        return _control(raw, "text", placeholder="Wert mit Einheit eingeben")
    if any(token in lowered for token in ("text", "id", "name", "referenz")):
        return _control(raw, "text", placeholder="Antwort eingeben")

    return _control(
        raw,
        "structured_text",
        placeholder=f"Antwort zum Methodentyp {raw or 'unbekannt'} eingeben",
        help_text="Für diesen Methoden-Antworttyp ist noch kein explizites UI-Control-Mapping definiert.",
        mapping_status="needs_review",
    )
