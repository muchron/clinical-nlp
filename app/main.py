from fastapi import FastAPI

from app.schemas import ClinicalTextRequest
from app.normalization.abbreviation import expand_abbreviations
from app.normalization.temporal_normalizer import normalize_temporal_expressions
from app.extraction.entity_extractor import extract_entities


app = FastAPI(
    title="Clinical NLP Service",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "service": "clinical-nlp",
        "status": "ok",
        "version": "0.1.0",
    }


@app.post("/nlp/extract")
def extract(request: ClinicalTextRequest):

    normalization = expand_abbreviations(request.text)

    normalized_text = normalize_temporal_expressions(
        normalization["normalized_text"]
    )

    entities = extract_entities(normalized_text)

    return {
        "original_text": request.text,
        "normalized_text": normalized_text,
        "abbreviations": normalization["replacements"],
        "entities": [
            entity.model_dump()
            for entity in entities
        ],
    }