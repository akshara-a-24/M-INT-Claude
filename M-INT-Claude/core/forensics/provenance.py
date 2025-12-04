from typing import Dict, Any
import imagehash
from core.utils.image_loader import ImageInput, load_pil


def compute_provenance(img: ImageInput) -> Dict[str, Any]:
    pil_img = load_pil(img)
    if pil_img is None:
        return {"phash": None, "seen_before": False, "matches": []}

    phash = str(imagehash.phash(pil_img))

    # stub – plug DB or reverse search here
    return {
        "phash": phash,
        "seen_before": False,
        "matches": [],
    }
