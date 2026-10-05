import re


FREQUENCY_PATTERN = re.compile(
    r"\b(\d+)\s*(x|kali)\b",
    re.IGNORECASE,
)


def extract_frequency(
    text: str,
    entity_end: int,
):
    """
    Mendeteksi frekuensi setelah entity.

    Contoh:

        muntah 1x
        BAB cair 5x
        muntah 3 kali

    Return:

        {
            "value": 5,
            "unit": "times"
        }

    atau None.
    """

    context = text[
        entity_end:
        entity_end + 30
    ]

    match = FREQUENCY_PATTERN.search(
        context
    )

    if not match:
        return None

    value = int(
        match.group(1)
    )

    return {
        "value": value,
        "unit": "times",
    }