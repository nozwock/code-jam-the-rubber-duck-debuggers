import pytesseract
from pytesseract import Output
import cv2 as cv
import numpy as np


def get_text_boxes(img: np.ndarray) -> list[tuple[int, 4]]:
    """Converts a given image into its text boxes"""
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_cpy = img.copy()
height, width, channels = img.shape

d = pytesseract.image_to_data(img_rgb, output_type=Output.DICT)
n_boxes = len(d["text"])
for i in range(n_boxes):
    if int(d["conf"][i]) < 60:
        continue

    (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[y : y + h, x : x + w] = 255
    masked_img = cv.bitwise_and(img, img, mask=mask)
    cv.imshow("", mask)
    cv.waitKey(0)
    img = cv.inpaint(img, mask, 3, cv.INPAINT_NS)

cv.waitKey(0)
cv.imshow("", img)
cv.waitKey(0)
cv.imshow("output", img)
cv.waitKey(0)
