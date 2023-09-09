import numpy as np
import cv2
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def create_blank_image(width: int, height: int, colour_bgr: tuple | None):
    """Creates a blank image on bgr space"""
    if colour_bgr is None:
        colour_bgr = (0, 0, 0)
    b, g, r = colour_bgr
    image = np.zeros((height, width, 3), np.uint8)
    image[:, :, 0] = b
    image[:, :, 1] = g
    image[:, :, 2] = r
    return image


def add_text(image: np.uint8, word_filler: str, word_secret: str, text_colour_rgb: tuple | None = (255, 255, 255)):
    """Add the repeated text and the secret text in the image"""
    height, width, _ = image.shape
    cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    font = ImageFont.truetype("andalemo.ttf", 10)
    x, y = 0, 0
    text_width = font.getbbox(word_filler)[2]
    text_height = font.getbbox(word_filler)[3]
    text_width_secret = font.getbbox(word_secret)[2]
    max = (((height//text_height) - 1) * ((width//text_width) - 1))
    secret_num = random.randint(0, max)
    flag_secret_counter = True
    for count_y, y in enumerate(range(0, height, text_height+2)):
        # Plus 2 is added to give a small gap between the text lines
        count_x = 0
        x = 0
        while x < width:
            origin = (x, y)
            # if x + text_width > width:
            #     break
            if (count_y*(width//text_width))+count_x != secret_num:
                draw.text(origin, word_filler, text_colour_rgb, font)
                x += text_width
            elif flag_secret_counter:
                # print((count_x, count_y))
                draw.text(origin, word_secret, text_colour_rgb, font=font)
                flag_secret_counter = False
                x += text_width_secret
            else:
                draw.text(origin, word_filler, text_colour_rgb, font)
            count_x += 1
    cv_image = np.array(pil_im)

    # Convert RGB to BGR
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    return cv_image


if __name__ == "__main__":
    image = create_blank_image(720, 480, None)
    image = add_text(image, "Hello", "World", (255, 255, 255))
    cv2.imshow("A New Image", image)
    cv2.waitKey(0)
