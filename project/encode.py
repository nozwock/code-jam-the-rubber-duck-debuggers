"""Encode text to image."""

import math

import cv2
import numpy as np

Image = np.ndarray


def encode_text_to_image(
    text: str,
    encoding: str = "utf-8",
    width_limit: int = 0,
    channels: int = 3,
) -> Image:
    data = bytes(text, encoding)
    height = (
        1 if not width_limit else math.ceil(len(data) / (abs(width_limit) * channels))
    )
    width = math.ceil(len(data) / (height * channels))

    image = np.array(list(data), dtype=np.uint8)

    pad_count = height * width * channels - len(data)
    print(f"{height, width, channels, pad_count=}")
    if pad_count:
        padding = np.zeros((pad_count,), dtype=np.uint8)
        image = np.concatenate((image, padding))
        print(f"{image, image.size, padding, padding.size=}")
    image = image.reshape(height, width, channels)

    print(f"{image, image.size=}")
    print(f"{data, image.tobytes()=}")

    return image


if __name__ == "__main__":
    cv2.imwrite(
        "output.png", img=encode_text_to_image("hello world", channels=4, width_limit=4)
    )
