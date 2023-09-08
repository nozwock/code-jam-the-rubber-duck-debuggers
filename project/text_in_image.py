import numpy as np
import cv2
import random


width, height = 720, 480
b, g, r = 255, 255, 255
image = np.zeros((height, width, 3), np.uint8)
image[:, :, 0] = b
image[:, :, 1] = g
image[:, :, 2] = r

font = cv2.FONT_HERSHEY_SIMPLEX
x, y = 0, 0
word_filler = "Hello"
word_secret = "World"
fontScale = 1
color = (0, 0, 0)  # BGR Format
thickness = 2  # Line Thickness
(text_width, text_height), baseline = cv2.getTextSize(word_filler, font, fontScale, thickness)
(text_width_secret, text_height_secret), baseline_secret = cv2.getTextSize(word_secret, font, fontScale, thickness)

print(text_width, text_height)
max = (((height//text_height) - 1) * ((width//text_width) - 1))
secret_num = random.randint(0, max)
print(max)
print(text_height, text_width)
print(secret_num)
flag_secret_counter = True

for count_y, y in enumerate(range(text_height, height, text_height+2)):
    # Plus 2 is added to give a small gap between the text lines
    count_x = 0
    x = 0
    while x < width:
        origin = (x, y)
        # if x + text_width > width:
        #     break
        if (count_y*(width//text_width))+count_x != secret_num:
            image = cv2.putText(image, word_filler, origin, font,
                                fontScale, color, thickness, cv2.LINE_AA)
            x += text_width
        elif flag_secret_counter:
            print("reached")
            print((count_x, count_y))
            image = cv2.putText(image, word_secret, origin, font,
                                fontScale, color, thickness, cv2.LINE_AA)
            flag_secret_counter = False
            x += text_width_secret
        else:
            image = cv2.putText(image, word_filler, origin, font,
                                fontScale, color, thickness, cv2.LINE_AA)
        count_x += 1

cv2.imshow("A New Image", image)
cv2.waitKey(0)
