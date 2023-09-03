from __future__ import annotations

from pathlib import Path
from typing import Protocol

import cv2
import numpy as np


class EncoderInterface(Protocol):
    """A standardized interface for encoding data within images."""

    def encode(self) -> Image:
        """An interface method for encoding data into an image."""
        ...

    def decode(self, img: np.ndarray) -> bytes:
        """An interface method for decoding data from an image."""
        ...


class Image:
    """A basic image class that implements fundamental methods."""

    def __init__(self, img: np.ndarray):
        dimensions = len(img.shape)
        if dimensions != 3:
            raise Exception(f"{dimensions=}, Image must have 3 dimensions.")

        self.img = img

    @staticmethod
    def encode(encoder: EncoderInterface) -> Image:
        """A method for text encoding within an image using the provided encoder."""
        return encoder.encode()

    def decode(self, encoder: EncoderInterface) -> bytes:
        """A method for decoding data from an image using the provided encoder."""
        return encoder.decode(self.img)

    @classmethod
    def read(cls, path: Path) -> Image:
        """A method to read an image from disk and create an Image object."""
        # NOTE: Don't prefer writing docs for self explanatory methods like these,
        # should probably disbale lints for these?
        return cls(img=cv2.imread(str(path), cv2.IMREAD_UNCHANGED))

    def save(self, path: Path) -> None:
        """A method for saving an image to disk."""
        cv2.imwrite(str(path), self.img)

    def as_array(self) -> np.ndarray:
        return self.img


if __name__ == "__main__":
    image = Image.read(Path("image.jpg"))
    image.save(Path("image1.jpg"))
