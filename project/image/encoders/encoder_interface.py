from typing import Protocol


class EncoderInterface(Protocol):
    def encode(self) -> None: ...

    def decode(self) -> None: ...
