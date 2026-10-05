import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


INPUT_FILE = Path("data/pemeriksaan_ralan_202610052113.csv")
OUTPUT_FILE = Path("output/candidates.csv")


STOPWORDS = {
    "yang",
    "dan",
    "atau",
    "dengan",
    "tidak",
    "ada",
    "dari",
    "untuk",
    "pada",
    "pasien",
    "sudah",
    "belum",
    "akan",
    "dalam",
    "karena",
    "sejak",
    "hari",
    "ini",
    "itu",
    "di",
    "ke",
    "dapat",
    "dengan",
}


UNITS = {
    "mm",
    "cm",
    "m",
    "kg",
    "g",
    "mg",
    "mcg",
    "ml",
    "l",
    "cc",
    "bpm",
    "x",
    "x/m",
}


KNOWN_CLINICAL_TERMS = {
    "demam",
    "batuk",
    "pilek",
    "sesak",
    "nyeri",
    "pusing",
    "mual",
    "muntah",
    "diare",
    "vaksin",
    "influenza",
    "wasir",
    "vagina",
    "perut",
    "mata",
    "wajah",
    "varises",
    "keluhan",
}


KNOWN_ABBREVIATIONS = {
    "usg",
    "pcv",
    "dpt",
    "mmr",
    "bab",
    "bak",
    "kpd",
    "smrs",
    "djj",
    "tfu",
    "hpl",
    "hpht",
    "ku",
    "tdk",
    "gak",
    "ga",
    "msk",
    "preskep",
    "puki",
}


def normalize_token(token: str) -> str:
    token = token.strip().lower()

    token = re.sub(
        r"^[^\w]+|[^\w]+$",
        "",
        token,
    )

    return token


def is_candidate(token: str) -> bool:

    if not token:
        return False

    if token in STOPWORDS:
        return False

    if token in UNITS:
        return True

    if len(token) < 2:
        return False

    if len(token) > 20:
        return False

    if not re.search(r"[a-z]", token):
        return False

    if token.isdigit():
        return False

    return True


def classify(token: str) -> str:

    if token in STOPWORDS:
        return "stopword"

    if token in UNITS:
        return "unit"

    if token in KNOWN_ABBREVIATIONS:
        return "abbreviation"

    if token in KNOWN_CLINICAL_TERMS:
        return "clinical_term"

    return "review"


def extract_tokens(text: str):

    raw_tokens = re.findall(
        r"\b[\w/.-]+\b",
        text.lower(),
    )

    tokens = []

    for raw_token in raw_tokens:

        token = normalize_token(raw_token)

        if is_candidate(token):
            tokens.append(token)

    return tokens


def get_context(
    text: str,
    token: str,
    max_examples: int = 3,
):

    sentences = re.split(
        r"[.!?\n]+",
        text,
    )

    examples = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if re.search(
            rf"\b{re.escape(token)}\b",
            sentence,
            re.IGNORECASE,
        ):

            if sentence not in examples:
                examples.append(sentence)

        if len(examples) >= max_examples:
            break

    return examples


def main():

    if not INPUT_FILE.exists():
        print(f"File tidak ditemukan: {INPUT_FILE}")
        return

    frequency = Counter()

    examples = defaultdict(list)

    total_records = 0

    with INPUT_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            print("CSV tidak memiliki header.")
            return

        if "keluhan" not in reader.fieldnames:
            print("CSV harus memiliki kolom 'keluhan'.")
            return

        for row in reader:

            text = (row.get("keluhan") or "").strip()

            if not text:
                continue

            total_records += 1

            tokens = extract_tokens(text)

            for token in set(tokens):

                frequency[token] += 1

                contexts = get_context(
                    text,
                    token,
                )

                for context in contexts:

                    if context not in examples[token]:
                        examples[token].append(context)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "term",
            "frequency",
            "classification",
            "example_1",
            "example_2",
            "example_3",
        ])

        for term, count in frequency.most_common():

            term_examples = examples[term]

            writer.writerow([
                term,
                count,
                classify(term),
                term_examples[0]
                if len(term_examples) > 0
                else "",
                term_examples[1]
                if len(term_examples) > 1
                else "",
                term_examples[2]
                if len(term_examples) > 2
                else "",
            ])

    print()
    print("=" * 50)
    print("Clinical NLP Candidate Discovery")
    print("=" * 50)
    print(f"Records    : {total_records}")
    print(f"Candidates : {len(frequency)}")
    print()
    print(f"Output     : {OUTPUT_FILE}")
    print()

    print("Top candidates:")

    for term, count in frequency.most_common(30):

        print(
            f"{term:<20} "
            f"{count:>6} "
            f"{classify(term)}"
        )


if __name__ == "__main__":
    main()