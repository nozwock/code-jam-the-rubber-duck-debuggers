import pytesseract
import cv2 as cv
import numpy as np
from pathlib import Path
import os

img = cv.imread("./project/test.png", cv.IMREAD_UNCHANGED)
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_cpy = img.copy()
height, width, channels = img.shape

boxes = pytesseract.image_to_boxes(img_rgb).splitlines()
for box in boxes:
    x1, y1, x2, y2 = map(int, box.split(" ")[1:-1])
    img_cpy = cv.rectangle(img, (x1, height - y1), (x2, height - y2), (0, 255, 0), 2)
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[y1:y2, x1:x2] = 255
    masked_img = cv.bitwise_and(img, img, mask=mask)
    cv.imshow("", masked_img)
    cv.waitKey(0)
    img = cv.inpaint(img, mask, 3, cv.INPAINT_NS)

cv.imshow("", img_cpy)
cv.waitKey(0)
cv.imshow("", img)
cv.waitKey(0)
cv.imshow("output", img)
cv.waitKey(0)
