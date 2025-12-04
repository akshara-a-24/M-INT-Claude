from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel


class ListingImage(BaseModel):
    id: str
    path: Optional[str] = None
    b64: Optional[str] = None


class RequestModel(BaseModel):
    listing_id: str
    seller_id: Optional[str] = None
    seller_notes: Optional[str] = None
    images: List[ListingImage]


class ResponseModel(BaseModel):
    listing_id: str
    authenticity_score: float
    ai_likelihood: float
    manipulation_likelihood: float
    fraud_score: float
    verdict: Literal["genuine", "suspicious", "likely_fraud", "unknown"]
    reasons: List[str]
    recommended_actions: List[str]
    vision_result: Dict[str, Any]
    supplemental: Dict[str, Any]
