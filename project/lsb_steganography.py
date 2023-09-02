import numpy as np
from bitarray import bitarray


def encode(
    text: str, img: np.ndarray, encoding: str = "utf-8", message_end: bytes = b"\0"
):
    text += message_end.decode()
    data = bitarray()
    data.frombytes(bytes(text, encoding=encoding))

    channels = img.flatten()
    if len(data) > len(channels) * 8:
        raise Exception(
            "Can't fit the text within the image with the current implementation."
        )

    for i in range(channels.shape[0]):
        try:
            channels[i] = (channels[i] & ~1) | data.pop(0)
        except IndexError:
            break

    return channels.reshape(img.shape)


def decode(img: np.ndarray, encoding: str = "utf-8", message_end: bytes = b"\0") -> str:
    channels = img.flatten()
    data = bitarray()
    for lv in channels:
        data.append(lv & 1)

        if (
            len(data) % 8 == 0
            and data[-len(message_end) * 8 :].tobytes() == message_end
        ):
            del data[-len(message_end) * 8 :]
            break

    return data.tobytes().decode(encoding=encoding)


if __name__ == "__main__":
    # Example
    import cv2 as cv

    img = cv.imread("image.png")
    secret_img = encode("hello world", img)
    cv.imwrite("output.png", secret_img)
    print(decode(secret_img))
