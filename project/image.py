from __future__ import annotations

import typing

import numpy
import cv2

# from project.image.encoders.iface import EncoderInterface
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

    @staticmethod
    def read_image(filepath: str) -> Image:
        pathlib_path = Path(filepath)
        if not(pathlib_path.exists()) or not(pathlib_path.is_file()):
            raise Exception(f"Invalid filepath provided: {filepath}")

        data = cv2.imread(str(pathlib_path))

        return Image(data)

    def save(self) -> None:
        pass


if __name__ == "__main__":
    image = Image.read_image("./image.jpg")
