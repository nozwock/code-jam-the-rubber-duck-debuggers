import numpy as np


def encrypt(text: str, img: np.ndarray):
    text += "#####"  # Delimiter for text change to your favorite character
    text = "".join([f"{ord(i):08b}" for i in text])

    flattened_img = img.flatten()
    for i in range(len(text)):
        flattened_img[i] = (flattened_img[i] & ~1) | int(text[i])

    return flattened_img.reshape(img.shape)


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
