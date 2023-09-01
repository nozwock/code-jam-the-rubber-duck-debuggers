"""Text Encoder."""
import math

import numpy as np

Image = np.ndarray


def encode_text_to_image(
    text: str,
    encoding: str = "utf-8",
    width_limit: int = 0,
    channels: int = 3,
) -> Image:
    """Encodes text into an image by utilizing the pixel channels to store \
each byte of the text using the specified encoding method."""
    data = text.encode(encoding)
    image = np.array(list(data), dtype=np.uint8)

    height = math.ceil(abs(len(data) / (width_limit * channels))) if width_limit else 1
    width = math.ceil(abs(len(data) / (height * channels)))
    channels = abs(channels)

    pad_count = height * width * channels - len(data)
    if pad_count:
        padding = np.zeros((pad_count,), dtype=np.uint8)
        image = np.concatenate((image, padding))

    return image.reshape(height, width, channels)


if __name__ == "__main__":
    # Example
    import cv2

    cv2.imwrite(
        "output.png", img=encode_text_to_image("hello world", channels=4, width_limit=3)
    )
