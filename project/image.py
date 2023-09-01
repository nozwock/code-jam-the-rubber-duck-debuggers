from __future__ import annotations

import typing

import numpy
import cv2

from pathlib import Path


class EncoderInterface(typing.Protocol):
    def encode(self) -> Image: ...

    def decode(self, img: numpy.ndarray) -> str: ...


class Image:
    width = None
    height = None
    img = None

    def __init__(self, img: numpy.ndarray):
        # if len(pixel_array.shape) != 3:
        #     raise Exception(f"Unexpected pixel_arr shape: array has {len(pixel_array.shape)} dimensions, but expected 3")

        self.img = img
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]

    @staticmethod
    def encode(encoder: EncoderInterface) -> Image:
        return encoder.encode()

    def decode(self, encoder: EncoderInterface) -> str:
        return encoder.decode(self.img)

    @classmethod
    def read(cls, path: Path) -> Image:
        data = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        return cls(data)

    def save(self, filename: str) -> None:
        cv2.imwrite(filename, self.img)


if __name__ == "__main__":
    image = Image.read(Path("./image.jpg"))
    image.save("image1.jpg")
    