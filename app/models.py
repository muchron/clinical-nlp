from typing import Optional

from pydantic import BaseModel


class ClinicalEntity(BaseModel):

    text: str

    type: str

    normalized: Optional[str] = None

    negated: bool = False

    assertion: Optional[str] = None

    temporality: Optional[str] = None

    onset: Optional[str] = None

    value: Optional[float] = None

    unit: Optional[str] = None