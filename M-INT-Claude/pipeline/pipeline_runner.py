from typing import Dict, Any
from schemas.base import Domain
from .loader import load_plugin


def run_pipeline(domain: Domain, payload: dict) -> Dict[str, Any]:
    """
    Domain-agnostic orchestrator.

    Each plugin must implement:
    - schema: RequestModel, ResponseModel
    - visual.analyze(payload)
    - supplemental.run(payload, vision_result)
    - decision.fuse(payload, vision_result, supplemental_result)
    """
    plugin = load_plugin(domain.value)

    # 1. validate / normalize plugin-specific payload
    RequestModel = plugin.schema.RequestModel
    ResponseModel = plugin.schema.ResponseModel
    parsed_payload = RequestModel(**payload)

    # 2. visual (LLM Vision / core understanding)
    vision_result = plugin.visual.analyze(parsed_payload)

    # 3. supplemental (forensics, metadata, etc.)
    supplemental_result = plugin.supplemental.run(parsed_payload, vision_result)

    # 4. decision (final LLM fusion + scoring)
    decision = plugin.decision.fuse(parsed_payload, vision_result, supplemental_result)

    # 5. validate structured response
    return ResponseModel(**decision).dict()
