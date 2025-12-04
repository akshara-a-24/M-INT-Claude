from typing import Dict, Any
from core.utils.image_loader import ImageInput
from core.forensics.exif import extract_exif
from core.forensics.ela import compute_ela
from core.forensics.noise import analyze_noise
from core.forensics.provenance import compute_provenance
from .schema import RequestModel


def run(request: RequestModel, vision_result: Dict[str, Any]) -> Dict[str, Any]:
    results = []

    for img in request.images:
        wrapper = ImageInput(id=img.id, path=img.path, b64=img.b64)

        results.append(
            {
                "image_id": img.id,
                "exif": extract_exif(wrapper),
                "ela": compute_ela(wrapper),
                "noise": analyze_noise(wrapper),
                "provenance": compute_provenance(wrapper),
            }
        )

    return {"per_image": results}
