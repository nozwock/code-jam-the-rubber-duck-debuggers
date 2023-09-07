import pytesseract
from pytesseract import Output
import cv2 as cv
import numpy as np


def get_text_boxes(img: np.ndarray) -> list[tuple[int, 4]]:
    """Converts a given image into its text boxes"""
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
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
    return np.array(cv.mean(img[y1:y2, x1:x2]))


def inpaint_img(img: np.ndarray, boxes: list[tuple[int, 4]]) -> np.ndarray:
    """Inpaints the boxes of the given image"""
    for box in boxes:
        (y1, y2, x1, x2) = box
        mask = np.zeros(img.shape[:2], np.uint8)
        mask[y1:y2, x1:x2] = 255
        img = cv.inpaint(img, mask, 3, cv.INPAINT_NS)
    return img


def add_text(img: np.ndarray, box: tuple[int, 4], text: str, color: np.ndarray):
    return cv.putText(
        img,
        text,
        (box[2], box[1]),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        tuple(color),
        1,
        cv.LINE_AA,
    )


if __name__ == "__main__":
    img = cv.imread("./project/test.png", cv.IMREAD_UNCHANGED)
    boxes = get_text_boxes(img)
    inpainted_img = inpaint_img(img, boxes)
    cv.imshow("", inpainted_img)
    cv.waitKey(0)
