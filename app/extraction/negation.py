NEGATION_TERMS = (
    "tidak ada",
    "tidak",
    "tanpa",
    "disangkal",
    "belum ada",
    "(-)",
    "-",
)


def is_negated(
    text: str,
    entity_start: int,
) -> bool:

    context_start = max(
        0,
        entity_start - 40,
    )

    context = text[
        context_start:
        entity_start
    ].lower()

    return any(
        term in context
        for term in NEGATION_TERMS
    )