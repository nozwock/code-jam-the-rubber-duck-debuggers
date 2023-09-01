import numpy as np


def decode_image_to_text(img: np.ndarray, encoding: str = "utf-8") -> str:
    """Converts a given image into the data associated with its pixel values"""
    return img.tobytes().decode(encoding=encoding)


if __name__ == "__main__":
    # Example
    import cv2

    print(decode_image_to_text(cv2.imread("output.png", cv2.IMREAD_UNCHANGED)))
