import re


TEMPORAL_PATTERN = re.compile(
    r"\b"
    r"(?:sejak|selama)"
    r"\s+"
    r"(\d+)"
    r"\s+"
    r"(detik|menit|jam|hari|minggu|bulan|tahun)"
    r"\b",
    re.IGNORECASE,
)


def extract_onset(
    text: str,
    entity_end: int,
):

    context = text[
        entity_end:
        entity_end + 80
    ]

    match = TEMPORAL_PATTERN.search(context)

    if not match:
        return None

    value = match.group(1)
    unit = match.group(2).lower()

    return f"{value} {unit}"