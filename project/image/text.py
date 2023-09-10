import math
import random

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from project.defines import EAST_TEXT_DETECTION_MODEL_PATH, FONT_ANDALEMO_PATH


def east_text_bbox(
    img: np.ndarray,
    pp_width: int = 320,
    pp_height: int = 320,
    score_threshold: float = 0.5,
    nms_threshold: float = 0.3,
) -> np.ndarray:
    """
    Returns an array of arrays, where each inner array contains points defining a bounding box.

    `pp_width` and `pp_height` represent pre-processed dimensions and should always be multiples of 32.

    ```py
    img = cv2.imread("img.png")
    bboxes = east_text_bbox(img)
    for pts in bboxes:
        cv2.polylines(img, [pts], True, (0, 255, 0), 2)
    ```
    """
    layers = ("feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3")
    detector = cv2.dnn.readNet(str(EAST_TEXT_DETECTION_MODEL_PATH))

    height, width = img.shape[:2]
    ratio_height = height / pp_height
    ratio_width = width / pp_width

    img = cv2.resize(img, (pp_width, pp_height))
    height, width = img.shape[:2]

    blob = cv2.dnn.blobFromImage(
        img, 1.0, (width, height), (123.68, 116.78, 103.94), swapRB=True, crop=False
    )

    detector.setInput(blob)
    scores, geometry = detector.forward(layers)

    rows, cols = scores.shape[2:4]
    detections, confidences = [], []

    for y in range(rows):
        score = scores[0, 0, y]
        *dimensions, angles = tuple(geometry[0, i, y] for i in range(5))

        for x in range(cols):
            if score[x] < score_threshold:
                continue

            angle = angles[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            height = dimensions[0][x] + dimensions[2][x]
            width = dimensions[1][x] + dimensions[3][x]

            offset_x, offset_y = (
                x * 4.0 + cos * dimensions[1][x] + sin * dimensions[2][x],
                y * 4.0 - sin * dimensions[1][x] + cos * dimensions[2][x],
            )

            p1 = (-sin * height + offset_x, -cos * height + offset_y)
            p2 = (-cos * width + offset_x, sin * width + offset_y)
            center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

            detections.append((center, (width, height), -1 * angle * 180.0 / math.pi))
            confidences.append(score[x])

    indices = cv2.dnn.NMSBoxesRotated(
        detections, confidences, score_threshold, nms_threshold
    )

    bboxes = []
    for i in indices:
        pts = cv2.boxPoints(detections[i])

        for j in range(4):
            pts[j][0] *= ratio_width
            pts[j][1] *= ratio_height

        bboxes.append(pts)

    return np.array(bboxes, dtype=np.int32)


def inpaint_bbox(img: np.ndarray, bboxes: np.ndarray) -> np.ndarray:
    """Inpaints the bboxes for an image."""
    for pts in bboxes:
        mask = np.zeros(img.shape[:2], np.uint8)
        cv2.fillPoly(mask, [pts], 255)
        img = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
    return img


def get_contour_color(img: np.ndarray) -> tuple[float, ...]:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(
        gray, 150, 255, cv2.THRESH_BINARY
    )  # doesn't work for dark text, require cv2.THRESH_BINARY_INV

    contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(mask, contours, -1, 255, -1)
    return cv2.mean(img, mask)


# TODO: Need to put text according to the bbox, it could be rotated
def add_text(
    img: np.ndarray, box: tuple[int, int, int, int], text: str, color: np.ndarray
):
    return cv2.putText(
        img,
        text,
        (box[2], box[1]),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        tuple(color),
        1,
        cv2.LINE_AA,
    )


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
    """
    Hide `secret` string in an image by putting it in between repeations of some word.

    - `color` is in RGB.
    """
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
    # img = cv2.imread("./project/test.png", cv2.IMREAD_UNCHANGED)
    # boxes = get_text_boxes(img)
    # inpainted_img = inpaint_img(img, boxes)
    # color = get_text_color(img, boxes[2])
    # print("Average color (BGR)", color)
    # inpainted_img = add_text(inpainted_img, boxes[2], "hello", color)
    # inpainted_img = add_text(inpainted_img, boxes[0], "world", color)
    # inpainted_img = add_text(inpainted_img, boxes[1], "2?", color)
    # cv2.imshow("", inpainted_img)
    # cv2.waitKey(0)

    img = cv2.imread("test.png")
    bboxes = east_text_bbox(img, pp_width=480)
    cv2.imwrite("output.png", inpaint_bbox(img, bboxes))
    for pts in bboxes:
        # x, y, w, h = cv2.boundingRect(pts)
        # cropped = img[y : y + h, x : x + w].copy()
        # print(get_contour_color(cropped))

        cv2.polylines(img, [pts], True, (0, 255, 0), 2)

        ...

    # cv2.imwrite("output.png", img)

    ...
