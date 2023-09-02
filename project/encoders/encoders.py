import math

import numpy as np

from project.image import EncoderInterface, Image


class TextEncoder(EncoderInterface):
    """A Text Encoder which utilizes the pixel channels to store each byte of the text."""

    def __init__(
        self,
        *,
        text: str | None = None,
        encoding: str = "utf-8",
        width_limit: int = 0,
        channels: int = 3,
    ):
        self.text = text
        self.encoding = encoding
        self.width_limit = width_limit
        self.channels = channels

    def encode(self) -> Image:
        """Encodes text into an image by utilizing the pixel channels to store \
each byte of the text using the specified encoding method."""
        if self.text is None:
            raise Exception("There's no text to encode.")

        data = self.text.encode(self.encoding)
        image = np.array(list(data), dtype=np.uint8)

        height = (
            math.ceil(abs(len(data) / (self.width_limit * self.channels)))
            if self.width_limit
            else 1
        )
        width = math.ceil(abs(len(data) / (height * self.channels)))
        channels = abs(self.channels)

        pad_count = height * width * channels - len(data)
        if pad_count:
            padding = np.zeros((pad_count,), dtype=np.uint8)
            image = np.concatenate((image, padding))

        return Image(img=image.reshape(height, width, channels))

    def decode(self, img: np.ndarray) -> str:
        """Converts a given image into the data associated with its pixel values."""
        return img.tobytes().decode(encoding=self.encoding)


if __name__ == "__main__":
    # Example
    from pathlib import Path

    Image.encode(TextEncoder(text="Hello, World!", width_limit=2, channels=4)).save(
        Path("output.png")
    )
