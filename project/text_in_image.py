import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from project.defines import FONT_ANDALEMO_PATH


def create_colored_image(
    width: int, height: int, color: tuple[int, int, int] = (0, 0, 0)
) -> np.ndarray:
    """Creates a image with a bgr space color."""
    b, g, r = color
    image = np.zeros((height, width, 3), np.uint8)
    image[:, :, 0] = b
    image[:, :, 1] = g
    image[:, :, 2] = r
    return image


# TODO:
# - add padding_x
# - secret word must not be longer than the repeat word
# - pad out the secret word if shorted than the repeat word
def hide_with_repeatation(
    img: np.ndarray,
    secret: str,
    repeat: str,
    color: tuple[int, int, int] = (255, 255, 255),
    font_size: int = 10,
    padding_y: int = 2,
) -> np.ndarray:
    """Add the repeated text and the secret text in the image"""
    img_height, img_width = img.shape[:2]

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
    image = hide_with_repeatation(image, "12345", "World")
    cv2.imwrite("output.png", image)
    # cv2.imshow("A New Image", image)
    # cv2.waitKey(0)
