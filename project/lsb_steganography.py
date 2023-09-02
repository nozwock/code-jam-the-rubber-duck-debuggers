import numpy as np


def encrypt(text: str, img: np.ndarray):
    text += "#####"
    text = "".join([f"{ord(i):08b}" for i in text])
    total_pixels_required = (len(text) // 3)
    bits_and_bobs = img.flatten()
    for i in range(total_pixels_required):
        if not bits_and_bobs[i] & int(text[i]):
            bits_and_bobs |= int(text[i])
    ret_img = bits_and_bobs.reshape(img.shape)
    return ret_img

    # for index, value in enumerate(img.flatten()):
    #    print(something)
    #    if index >= len(text):
    #        something += (bytes(format(value, "08b"), "ascii"))
    #        continue
    #    something += bytes(format(value, "08b")[:-1] + text[index], "ascii")
    # ret_img = np.frombuffer(something, dtype=img.dtype)
    # ret_img = ret_img.reshape(img.shape)
    # return ret_img


def decrypt(img):
    binary_values = list(map(lambda x: format(x, "08b")[-1], img.flatten()))
    binary_values = ["".join(binary_values[i: i + 8]) for i in range(0, len(binary_values), 8)]
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
