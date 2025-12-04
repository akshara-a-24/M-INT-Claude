import os
from dotenv import load_dotenv

load_dotenv()

# Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_ADMIN_API_KEY = os.getenv("ANTHROPIC_ADMIN_API_KEY")

# Effective key (primary → fallback)
CLAUDE_API_KEY = ANTHROPIC_API_KEY or ANTHROPIC_ADMIN_API_KEY

if not CLAUDE_API_KEY:
    raise RuntimeError("ERROR: Missing ANTHROPIC_API_KEY or ANTHROPIC_ADMIN_API_KEY")

# Models
CLAUDE_VISION_MODEL = os.getenv("CLAUDE_VISION_MODEL", "claude-3-opus-20240229")
CLAUDE_REASONER_MODEL = os.getenv("CLAUDE_REASONER_MODEL", "claude-3-sonnet-20240229")
