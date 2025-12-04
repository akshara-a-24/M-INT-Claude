from typing import Any
from .registry import PLUGIN_REGISTRY


def load_plugin(domain: str) -> Any:
    if domain not in PLUGIN_REGISTRY:
        raise ValueError(f"Unknown domain: {domain}")
    return PLUGIN_REGISTRY[domain]
