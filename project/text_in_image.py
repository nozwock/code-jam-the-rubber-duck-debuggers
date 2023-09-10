import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from project.defines import FONT_ANDALEMO_PATH


def create_colored_image(
    width: int, height: int, color: tuple[int, int, int] = (0, 0, 0)
) -> np.ndarray:
    """Creates a image with a BGR color space."""
    b, g, r = color
    image = np.zeros((height, width, 3), np.uint8)
    image[:, :, 0] = b
    image[:, :, 1] = g
    image[:, :, 2] = r
    return image


# TODO:
# - add padding_x
def hide_with_repeatation(
    img: np.ndarray,
    secret: str,
    repeat: str,
    color: tuple[int, int, int] = (255, 255, 255),
    font_size: int = 10,
    padding_y: int = 2,
    trim_extra: bool = True,
) -> np.ndarray:
    """Hide `secret` string in an image by putting it in between repeations of some word."""
    img_height, img_width = img.shape[:2]

    if len(secret) > len(repeat):
        if trim_extra:
            secret = secret[: len(repeat)]
        else:
            raise ValueError("Expected length of `secret` string to be <= `repeat`.")
    elif len(secret) < len(repeat):
        secret += repeat[len(secret) :]

    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype(str(FONT_ANDALEMO_PATH), font_size)

    repeat_width, text_height = font.getbbox(repeat)[2:4]
    secret_width = font.getbbox(secret)[2]

    max_texts = ((img_height // text_height) - 1) * ((img_width // repeat_width) - 1)
    secret_pos = random.randint(0, max_texts)

    put_secret = True
    for i, y in enumerate(range(0, img_height, text_height + padding_y)):
        j = x = 0

        while x < img_width:
            org = (x, y)

            if (i * (img_width // repeat_width)) + j != secret_pos:
                draw.text(org, repeat, color, font)
                x += repeat_width
            elif put_secret:
                draw.text(org, secret, color, font)
                put_secret = False
                x += secret_width
            else:
                draw.text(org, repeat, color, font)

            j += 1

    return np.array(pil_img)


if __name__ == "__main__":
    image = create_colored_image(720, 480)
    image = hide_with_repeatation(image, "Supreme", "World")
    cv2.imwrite("output.png", image)
    # cv2.imshow("A New Image", image)
    # cv2.waitKey(0)
