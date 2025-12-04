from anthropic import Anthropic
from core.config import CLAUDE_API_KEY, CLAUDE_REASONER_MODEL

# One unified Claude client: primary key OR admin key
client = Anthropic(api_key=CLAUDE_API_KEY)


def reasoner_chat(messages, max_tokens=800):
    """
    Generic Claude reasoning call used by decision.fuse
    Supports system + user messages list.
    """
    response = client.messages.create(
        model=CLAUDE_REASONER_MODEL,
        max_tokens=max_tokens,
        messages=messages,
    )
    return response.content[0].text
