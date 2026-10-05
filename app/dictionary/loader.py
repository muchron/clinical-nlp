import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DICTIONARY_DIR = (
    BASE_DIR
    / "data"
    / "dictionaries"
)


def load_json(filename: str):

    path = DICTIONARY_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Dictionary tidak ditemukan: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def load_abbreviations():

    return load_json(
        "abbreviations.json"
    )


def load_clinical_terms():

    return load_json(
        "clinical_terms.json"
    )


def load_units():

    return load_json(
        "units.json"
    )


def load_stopwords():

    return load_json(
        "stopwords.json"
    )