import re

from app.dictionary.loader import load_clinical_terms
from app.extraction.negation import is_negated
from app.extraction.temporal import extract_onset
from app.extraction.assertion import detect_assertion
from app.extraction.frequency import extract_frequency

from app.models import ClinicalEntity


def find_candidates(text: str):
    """
    Mencari seluruh clinical term yang terdapat
    di dalam text berdasarkan clinical_terms.json.

    Output candidate berisi:
    - term
    - start
    - end
    - metadata
    """

    dictionary = load_clinical_terms()

    candidates = []

    for term, metadata in dictionary.items():

        # Hanya gunakan dictionary yang sudah diverifikasi
        if metadata.get("status") != "verified":
            continue

        term = term.strip()

        if not term:
            continue

        escaped_term = re.escape(term)

        # Memastikan term merupakan kata/frasa utuh.
        pattern = rf"(?<!\w){escaped_term}(?!\w)"

        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):

            candidates.append({
                "term": match.group(0),
                "dictionary_term": term,
                "start": match.start(),
                "end": match.end(),
                "metadata": metadata,
            })

    return candidates


def remove_overlaps(candidates):
    """
    Menghilangkan candidate yang saling overlap.

    Prioritas:
    1. Frasa paling panjang
    2. Posisi paling awal

    Contoh:

        nyeri
        nyeri dada

    Jika keduanya ditemukan pada posisi yang sama,
    maka yang dipilih adalah "nyeri dada".
    """

    candidates = sorted(
        candidates,
        key=lambda item: (
            -(item["end"] - item["start"]),
            item["start"],
        ),
    )

    selected = []

    for candidate in candidates:

        overlap = False

        for existing in selected:

            if (
                candidate["start"] < existing["end"]
                and candidate["end"] > existing["start"]
            ):
                overlap = True
                break

        if not overlap:
            selected.append(candidate)

    # Kembalikan sesuai urutan kemunculan dalam teks
    selected.sort(
        key=lambda item: item["start"]
    )

    return selected


def extract_entities(text: str):
    """
    Pipeline entity extraction:

        text
          ↓
        find candidates
          ↓
        remove overlaps
          ↓
        negation detection
          ↓
        temporal detection
          ↓
        ClinicalEntity
    """

    candidates = find_candidates(text)

    selected = remove_overlaps(candidates)

    entities = []

    for candidate in selected:
        metadata = candidate["metadata"]

        start = candidate["start"]
        end = candidate["end"]

        entity_text = candidate["term"]

        normalized = metadata.get(
            "normalized",
            candidate["dictionary_term"],
            )

        entity_type = metadata.get(
            "type",
            "clinical_entity",
        )

        onset = extract_onset(text, end)
        negated = is_negated(text, start)
        assertion = detect_assertion(text, start, end)
        frequency = extract_frequency(text, end)

        entity = ClinicalEntity(
            text=entity_text,
            type=entity_type,
            normalized=normalized,
            negated=negated,
            assertion=assertion,
            temporality=None,
            onset=onset,
            value=frequency["value"] if frequency else None,
            unit=frequency["unit"] if frequency else None,
        )

        entities.append(entity)
    return entities