import numpy as np


def encrypt(text: str, img: np.ndarray):
    text += "#####"
    text = "".join([format(ord(i), "08b") for i in text])
    something = []
    for index, value in enumerate(img.flatten()):
        if index >= len(text):
            something.append(bytes(format(value, "08b"), "ascii"))
            continue
        something.append(bytes(format(value, "08b")[:-1] + text[index], "ascii"))
    ret_img = np.array(something, dtype=img.dtype)
    ret_img = ret_img.reshape(img.shape)
    return ret_img


def decrypt(img):
    binary_values = list(map(lambda x: format(x, "08b")[-1], img.flatten()))
    binary_values = [
        "".join(binary_values[i : i + 8]) for i in range(0, len(binary_values), 8)
    ]
    decoded_data = ""
    for byte in binary_values:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":
            break
    print(decoded_data[:-5])
    return decoded_data[:-5]


if __name__ == "__main__":
    import cv2 as cv

    img = cv.imread("Untitled.png")
    img_2 = encrypt("hello world", img)
    cv.imwrite("output.png", encrypt("hello world", img))
    decrypt(img_2)
