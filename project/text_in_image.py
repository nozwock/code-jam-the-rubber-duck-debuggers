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


def hide_with_repeatation(
    image: np.ndarray,
    secret: str,
    repeat: str,
    color: tuple[int, int, int] = (255, 255, 255),
):
    """Add the repeated text and the secret text in the image"""
    height, width, _ = image.shape
    cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    font = ImageFont.truetype(str(FONT_ANDALEMO_PATH), 10)
    x, y = 0, 0
    text_width = font.getbbox(repeat)[2]
    text_height = font.getbbox(repeat)[3]
    text_width_secret = font.getbbox(secret)[2]
    max = ((height // text_height) - 1) * ((width // text_width) - 1)
    secret_num = random.randint(0, max)
    flag_secret_counter = True
    for count_y, y in enumerate(range(0, height, text_height + 2)):
        # Plus 2 is added to give a small gap between the text lines
        count_x = 0
        x = 0
        while x < width:
            origin = (x, y)
            # if x + text_width > width:
            #     break
            if (count_y * (width // text_width)) + count_x != secret_num:
                draw.text(origin, repeat, color, font)
                x += text_width
            elif flag_secret_counter:
                # print((count_x, count_y))
                draw.text(origin, secret, color, font=font)
                flag_secret_counter = False
                x += text_width_secret
            else:
                draw.text(origin, repeat, color, font)
            count_x += 1
    cv_image = np.array(pil_im)

    # Convert RGB to BGR
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    return cv_image


if __name__ == "__main__":
    image = create_colored_image(720, 480)
    image = hide_with_repeatation(image, "Hello", "World")
    cv2.imwrite("output.png", image)
    # cv2.imshow("A New Image", image)
    # cv2.waitKey(0)
