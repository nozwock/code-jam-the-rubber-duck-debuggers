from __future__ import annotations

import typing

import numpy
import cv2

# from project.image.encoders.iface import EncoderInterface
from pathlib import Path


class EncoderInterface(typing.Protocol):
    def encode(self) -> Image: ...

    def decode(self) -> None: ...


class Image:
    width = None
    height = None
    data = None

    def __init__(self, data: numpy.ndarray):
        # if len(pixel_array.shape) != 3:
        #     raise Exception(f"Unexpected pixel_arr shape: array has {len(pixel_array.shape)} dimensions, but expected 3")

        self.data = data
        self.height = self.data.shape[0]
        self.width = self.data.shape[1]
        print("Created Instance")

    @staticmethod
    def encode(self, encoder: EncoderInterface) -> Image:
        pass

    def decode(self, encoder: EncoderInterface, data: numpy.ndarray) -> None:
        pass


def read_image(filepath: str) -> Image:
    pathlib_path = Path(filepath)
    if not(pathlib_path.exists()) or not(pathlib_path.is_file()):
        raise Exception(f"Invalid filepath provided: {filepath}")

    data = cv2.imread(str(pathlib_path))

    return Image(data)


if __name__ == "__main__":
    image = read_image("image/")
