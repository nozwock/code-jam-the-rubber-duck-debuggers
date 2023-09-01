import numpy as np


def image_to_text(img: np.ndarray) -> str:
    """Converts a given image into the data associated with its pixel values"""
    return img.tobytes().decode()
