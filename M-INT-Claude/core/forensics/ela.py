from typing import Dict, Any
import cv2
import numpy as np
from core.utils.image_loader import ImageInput, load_cv2_color


def compute_ela(img: ImageInput) -> Dict[str, Any]:
    original = load_cv2_color(img)
    if original is None:
        return {"ela_mean": None}

    ok, encoded = cv2.imencode(".jpg", original, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if not ok:
        return {"ela_mean": None}

    recompressed = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    ela = cv2.absdiff(original, recompressed)
    ela_mean = float(np.mean(ela))
    return {"ela_mean": ela_mean}
