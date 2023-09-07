import numpy as np
import cv2

height, width = 500, 1000
b, g, r = 255, 255, 255
image = np.zeros((height, width, 3), np.uint8)
image[:, :, 0] = b
image[:, :, 1] = g
image[:, :, 2] = r

# font
font = cv2.FONT_HERSHEY_SIMPLEX
# origin
origin = (0, 200)
# fontScale
fontScale = 1
# Blue color in BGR
color = (255, 0, 0)
# Line thickness of 2 px
thickness = 2
# Using cv2.putText() method
image = cv2.putText(image, 'OpenCV', origin, font,
                    fontScale, color, thickness, cv2.LINE_AA)
cv2.imshow("A New Image", image)
cv2.waitKey(0)