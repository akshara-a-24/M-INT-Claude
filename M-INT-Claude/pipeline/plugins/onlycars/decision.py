import json
from typing import Dict, Any
from core.reasoner_client import reasoner_chat
from .schema import RequestModel
import traceback
import os
from datetime import datetime


FUSION_SYSTEM_PROMPT = """
You are an automotive fraud decision engine.

You receive:
- listing metadata (listing_id, seller_notes)
- vision_result: a JSON from a multimodal model that saw all car photos
- supplemental: per-image EXIF, ELA, noise, and provenance

Your job:
- Combine them into ONE verdict about authenticity and fraud risk.
- Be conservative: if uncertain, use 'suspicious'.

Return STRICT JSON:
{
  "listing_id": "<string>",
  "authenticity_score": 0.0-1.0,
  "ai_likelihood": 0.0-1.0,
  "manipulation_likelihood": 0.0-1.0,
  "fraud_score": 0.0-1.0,
  "verdict": "genuine" | "suspicious" | "likely_fraud" | "unknown",
  "reasons": ["<short>", "..."],
  "recommended_actions": ["<slug>", "..."],
  "vision_result": {...},
  "supplemental": {...}
}
"""


def fuse(
    request: RequestModel,
    vision_result: Dict[str, Any],
    supplemental_result: Dict[str, Any],
) -> Dict[str, Any]:

    payload = {
        "listing_id": request.listing_id,
        "seller_notes": request.seller_notes,
        "vision_result": vision_result,
        "supplemental": supplemental_result,
    }

    raw = reasoner_chat(
        messages=[
            {"role": "system", "content": FUSION_SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload)},
        ]
    )

    txt = raw.strip()

    # Remove ```json fences if present
    if txt.startswith("```"):
        lines = txt.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        txt = "\n".join(lines).strip()

    # ----------------------------------------------------------------------
    # NEW: WRITE RAW TXT OUTPUT TO FILE
    # ----------------------------------------------------------------------
    os.makedirs("debug_outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    debug_path = f"debug_outputs/fusion_raw_{request.listing_id}_{timestamp}.json"

    with open(debug_path, "w", encoding="utf-8") as f:
        f.write(txt)

    print(f"[Fusion Debug] Raw output written to: {debug_path}")
    # ----------------------------------------------------------------------

    try:
        result = json.loads(txt)

    except Exception as e:
        print(traceback.format_exc())
        result = {
            "listing_id": request.listing_id,
            "authenticity_score": 0.5,
            "ai_likelihood": vision_result.get("ai_likelihood", 0.5),
            "manipulation_likelihood": vision_result.get(
                "manipulation_likelihood", 0.5
            ),
            "fraud_score": vision_result.get("fraud_risk", 0.5),
            "verdict": "unknown",
            "reasons": [
                f"Fusion JSON parse error: {e}",
                f"See debug file: {debug_path}",
            ],
            "recommended_actions": ["manual_review"],
            "vision_result": vision_result,
            "supplemental": supplemental_result,
        }

    return result
