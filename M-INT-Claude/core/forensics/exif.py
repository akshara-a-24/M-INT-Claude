from typing import Dict, Any
import piexif
from . import __init__  # keep package
from core.utils.image_loader import ImageInput, load_pil


def extract_exif(img: ImageInput) -> Dict[str, Any]:
    pil_img = load_pil(img)
    if pil_img is None:
        return {"exif_present": False}

    try:
        exif_bytes = pil_img.info.get("exif", b"")
        if not exif_bytes:
            return {"exif_present": False}
        ex = piexif.load(exif_bytes)
        return {
            "exif_present": True,
            "camera_make": ex["0th"].get(piexif.ImageIFD.Make),
            "camera_model": ex["0th"].get(piexif.ImageIFD.Model),
            "timestamp": ex["Exif"].get(piexif.ExifIFD.DateTimeOriginal),
            "software": ex["0th"].get(piexif.ImageIFD.Software),
        }
    except Exception:
        return {"exif_present": False}
