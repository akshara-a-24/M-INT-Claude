from anthropic import Anthropic
from core.config import CLAUDE_API_KEY, CLAUDE_VISION_MODEL


# Unified client → primary key OR admin key
client = Anthropic(api_key=CLAUDE_API_KEY)


def vision_chat(image_b64: str, prompt: str = "Analyze this image"):
    """
    Sends a single image + text prompt to Claude Vision.
    Returns the text output only.
    """
    response = client.messages.create(
        model=CLAUDE_VISION_MODEL,
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return response.content[0].text
