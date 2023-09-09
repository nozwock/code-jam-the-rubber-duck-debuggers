import math

import cv2
import numpy as np
import pytesseract
from pytesseract import Output

from project.defines import EAST_TEXT_DETECTION_MODEL_PATH


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


def get_text_boxes(img: np.ndarray) -> list[tuple[int, 4]]:
    """Converts a given image into its text boxes"""
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    d = pytesseract.image_to_data(img_rgb, output_type=Output.DICT)
    n_boxes = len(d["text"])
    array_of_boxes = []
    for i in range(n_boxes):
        if int(d["conf"][i]) < 60:
            continue
        array_of_boxes.append(
            (
                d["top"][i],
                d["top"][i] + d["height"][i],  # y, y + h
                d["left"][i],
                d["left"][i] + d["width"][i],  # x, x + w
            )
        )
    return array_of_boxes


def get_text_color(img: np.ndarray, box: tuple[int, 4]) -> np.ndarray:
    (y1, y2, x1, x2) = box
    return np.array(cv2.mean(img[y1:y2, x1:x2]))


def inpaint_img(img: np.ndarray, boxes: list[tuple[int, 4]]) -> np.ndarray:
    """Inpaints the boxes of the given image"""
    for box in boxes:
        (y1, y2, x1, x2) = box
        mask = np.zeros(img.shape[:2], np.uint8)
        mask[y1:y2, x1:x2] = 255
        img = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
    return img


def add_text(img: np.ndarray, box: tuple[int, 4], text: str, color: np.ndarray):
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

    # img = cv2.imread("test.png")
    # bboxes = east_text_bbox(img, pp_width=480)
    # for pts in bboxes:
    #     cv2.polylines(img, [pts], True, (0, 255, 0), 2)
    # cv2.imwrite("output.png", img)

    ...
