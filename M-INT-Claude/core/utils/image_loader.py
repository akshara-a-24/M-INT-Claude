import base64
from typing import Optional
from PIL import Image
import io
import numpy as np
import cv2
import os


class ImageInput:
    def __init__(self, id: str, path: Optional[str] = None, b64: Optional[str] = None):
        self.id = id
        self.path = path
        self.b64 = b64


def load_bytes(img: ImageInput) -> Optional[bytes]:
    try:
        if img.b64:
            return base64.b64decode(img.b64)
        if img.path:
            with open(img.path, "rb") as f:
                return f.read()
        return None
    except Exception:
        return None


def load_pil(img: ImageInput):
    data = load_bytes(img)
    if not data:
        return None
    return Image.open(io.BytesIO(data))


def load_cv2_color(img: ImageInput):
    data = load_bytes(img)
    if not data:
        return None
    arr = np.frombuffer(data, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def load_cv2_gray(img: ImageInput):
    data = load_bytes(img)
    if not data:
        return None
    arr = np.frombuffer(data, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)


def to_base64(img: ImageInput) -> Optional[str]:
    data = load_bytes(img)
    if not data:
        return None
    return base64.b64encode(data).decode("utf-8")
