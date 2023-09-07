import numpy as np
import cv2

height, width = 500, 1000
b, g, r = 255, 255, 255
image = np.zeros((height, width, 3), np.uint8)
image[:, :, 0] = b
image[:, :, 1] = g
image[:, :, 2] = r

cv2.imshow("A New Image", image)
cv2.waitKey(0)
