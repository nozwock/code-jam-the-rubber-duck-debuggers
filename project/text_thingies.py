from imutils.object_detection import non_max_suppression
import cv2 as cv
import numpy as np

net = cv.dnn.readNet("./frozen_east_text_detection.pb")


def find_text(img: np.ndarray):
    original_image = img.copy()
    (H, W) = img.shape[:2]
    (newW, newH) = (320, 320)
    rW = W / float(newW)
    rH = H / float(newH)
    layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    blob = cv.dnn.blobFromImage(
        img, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False
    )
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    (rows, cols) = scores.shape[2:4]
    rects = []
    confidences = []
    for y in range(rows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
    for x in range(cols):
        if scoresData[x] < 0.5:
            continue
        (offsetX, offsetY) = (x * 4.0, y * 4.0)
        angle = anglesData[x]
        cos = np.cos(angle)
        sin = np.sin(angle)
        h = xData0[x] + xData2[x]
        w = xData1[x] + xData3[x]
        endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
        endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
        startX = int(endX - w)
        startY = int(endY - h)
        rects.append((startX, startY, endX, endY))
        confidences.append(scoresData[x])
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    for startX, startY, endX, endY in boxes:
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        cv.rectangle(original_image, (startX, startY), (endX, endY), (0, 255, 0), 2)
    cv.imshow("Text Detection", original_image)
    cv.waitkey(0)


if __name__ == "__main__":
    img = cv.imread("./project/wallmart.jpg", cv.IMREAD_UNCHANGED)
    find_text(img)
