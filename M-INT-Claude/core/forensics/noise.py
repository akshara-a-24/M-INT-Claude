from typing import Dict, Any
import numpy as np
from core.utils.image_loader import ImageInput, load_cv2_gray


def analyze_noise(img: ImageInput) -> Dict[str, Any]:
    gray = load_cv2_gray(img)
    if gray is None:
        return {"var_dark": None, "var_mid": None, "var_bright": None}

    dark = gray[gray < 85]
    mid = gray[(gray >= 85) & (gray < 170)]
    bright = gray[gray >= 170]

    var_dark = float(np.var(dark)) if dark.size else None
    var_mid = float(np.var(mid)) if mid.size else None
    var_bright = float(np.var(bright)) if bright.size else None

    return {
        "var_dark": var_dark,
        "var_mid": var_mid,
        "var_bright": var_bright,
    }
