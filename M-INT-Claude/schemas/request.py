from typing import Optional, List
from pydantic import BaseModel
from .base import Domain


class ImageItem(BaseModel):
    id: str
    url: Optional[str] = None
    b64: Optional[str] = None


class AnalyzeRequest(BaseModel):
    domain: Domain
    payload: dict  # plugin-specific payload, validated inside plugin
