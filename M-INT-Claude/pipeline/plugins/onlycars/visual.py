import json
import mimetypes
from typing import Any, Dict
from anthropic import Anthropic

from core.utils.image_loader import ImageInput, to_base64
from .schema import RequestModel
from core.config import CLAUDE_API_KEY, CLAUDE_VISION_MODEL

# Claude client (primary or admin key automatically chosen)
client = Anthropic(api_key=CLAUDE_API_KEY)


VISION_SYSTEM_PROMPT = """
You are an automotive image forensics and fraud expert.

You receive:
- multiple photos of a car listing
- optional seller notes

Goals:
- Decide if images look real vs AI-generated.
- Detect manipulation (fake plates, weird reflections, inconsistent shadows, missing details).
- Spot cross-image inconsistencies (different cars, colors, environments).

Return STRICT JSON:
{
  "raw_summary": "<short description>",
  "ai_likelihood": 0.0-1.0,
  "manipulation_likelihood": 0.0-1.0,
  "fraud_risk": 0.0-1.0,
  "inconsistencies": ["<issue>", "..."],
  "per_image_notes": {
    "<image_id>": ["<note>", "..."]
  }
}
"""


def analyze(request: RequestModel) -> Dict[str, Any]:
    """
    Claude-based implementation of your listing image analysis.
    Replaces OpenAI + vision_chat.
    """

    # Initial textual content
    content = [
        {
            "type": "text",
            "text": (
                f"Listing ID: {request.listing_id}\n"
                f"Seller Notes: {request.seller_notes}"
            ),
        }
    ]

    # Add images (converted to base64)
    for img in request.images:

        wrapper = ImageInput(id=img.id, path=img.path, b64=img.b64)
        b64 = to_base64(wrapper)

        # Try to guess mime
        mime = "jpeg"
        if img.path:
            guess = mimetypes.guess_type(img.path)[0]
            if guess:
                mime = guess.split("/")[-1]

        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": f"image/{mime}",
                    "data": b64,
                },
            }
        )

    # Claude Vision Request
    response = client.messages.create(
        model=CLAUDE_VISION_MODEL,
        max_tokens=900,
        system=VISION_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    raw = response.content[0].text.strip()

    # Remove accidental ```json blocks
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:-1]).strip()

    # Try strict JSON parse
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {
            "raw_summary": "vision parsing failed",
            "ai_likelihood": 0.5,
            "manipulation_likelihood": 0.5,
            "fraud_risk": 0.5,
            "inconsistencies": [],
            "per_image_notes": {img.id: [] for img in request.images},
        }

    # Add usage metadata
    parsed["_usage"] = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        "model": CLAUDE_VISION_MODEL,
    }

    return parsed
