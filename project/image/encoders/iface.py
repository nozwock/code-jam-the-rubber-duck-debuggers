from typing import Protocol
from project.image import Image


class EncoderInterface(Protocol):
    def encode(self) -> Image: ...

    def decode(self) -> None: ...
