import re

from app.dictionary.loader import load_abbreviations


# Abbreviation yang tetap dipertahankan
# di normalized_text karena akan dipakai
# oleh clinical entity extractor.
PRESERVE_ABBREVIATIONS = {
    "bab",
    "bak",
}


def expand_abbreviations(text: str):
    abbreviations = load_abbreviations()

    result = text
    replacements = []

    for abbreviation, metadata in abbreviations.items():

        if metadata.get("status") != "verified":
            continue

        expansion = metadata["expansion"]

        pattern = rf"\b{re.escape(abbreviation)}\b"

        matches = list(
            re.finditer(
                pattern,
                result,
                flags=re.IGNORECASE,
            )
        )

        for match in matches:
            replacements.append({
                "original": match.group(0),
                "normalized": expansion,
                "start": match.start(),
                "end": match.end(),
            })

        # BAB dan BAK dicatat sebagai abbreviation,
        # tetapi tidak diubah pada normalized_text.
        if abbreviation.lower() in PRESERVE_ABBREVIATIONS:
            continue

        result = re.sub(
            pattern,
            expansion,
            result,
            flags=re.IGNORECASE,
        )

    return {
        "original_text": text,
        "normalized_text": result,
        "replacements": replacements,
    }