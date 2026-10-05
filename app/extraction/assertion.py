import re


POSITIVE_PATTERNS = (
    r"\(\+\)",
    r"\+",
)

NEGATIVE_PATTERNS = (
    r"\(-\)",
    r"-",
)


def detect_assertion(
    text: str,
    entity_start: int,
    entity_end: int,
):
    """
    Mendeteksi status assertion entity.

    Contoh:

        mual (+)
        demam (-)

    Return:

        present
        absent
        None
    """

    # Ambil konteks setelah entity
    after = text[
        entity_end:
        entity_end + 20
    ]

    # Ambil konteks sebelum entity
    before = text[
        max(0, entity_start - 30):
        entity_start
    ]

    context = (
        before + " " + after
    ).lower()

    for pattern in NEGATIVE_PATTERNS:

        if re.search(
            pattern,
            after,
        ):
            return "absent"

    for pattern in POSITIVE_PATTERNS:

        if re.search(
            pattern,
            after,
        ):
            return "present"

    return None