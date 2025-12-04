from typing import Any, Dict
from pydantic import BaseModel
from .base import Domain


class AnalyzeResponse(BaseModel):
    domain: Domain
    result: Dict[str, Any]
    processing_time: float
