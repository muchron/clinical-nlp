import re


TEMPORAL_REPLACEMENTS = [
    (
        re.compile(
            r"\b(\d+)\s*hr\s+yll\b",
            re.IGNORECASE,
        ),
        r"\1 hari yang lalu",
    ),
    (
        re.compile(
            r"\b(\d+)\s*hr\b",
            re.IGNORECASE,
        ),
        r"\1 hari",
    ),
    (
        re.compile(
            r"\b(\d+)\s*mgg\b",
            re.IGNORECASE,
        ),
        r"\1 minggu",
    ),
    (
        re.compile(
            r"\b(\d+)\s*bln\b",
            re.IGNORECASE,
        ),
        r"\1 bulan",
    ),
]


def normalize_temporal_expressions(text: str):
    result = text

    for pattern, replacement in TEMPORAL_REPLACEMENTS:
        result = pattern.sub(replacement, result)

    return result