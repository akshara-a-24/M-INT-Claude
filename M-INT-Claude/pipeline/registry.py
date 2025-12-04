from typing import Dict, Any
from .plugins import onlycars, drinkwise

# Each plugin module exposes a PLUGIN object with a well-defined interface.
PLUGIN_REGISTRY: Dict[str, Any] = {
    "onlycars": onlycars,
    "drinkwise": drinkwise,
}
