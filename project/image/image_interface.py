from typing import Protocol
import numpy
from encoder_interface import EncoderInterface


class ImageInterface(Protocol):
    width: int
    height: int
    pixel_array: numpy.ndarray
    encoder: EncoderInterface

    def encode(self) -> None: ...

    def decode(self) -> None: ...