import math

import numpy as np
from bitarray import bitarray

from .image import EncoderInterface, Image


class DirectEncoder(EncoderInterface):
    """
    An Encoder which utilizes the pixel channels to store each byte of the data.

    - When `width_limit` is set to `None`, it will generate an image with dimensions as close as possible to a square.
    """

    def __init__(
        self,
        data: bytes | None = None,
        *,
        width_limit: int | None = None,
        channels: int = 3,
    ):
        self.data = data
        self.width_limit = width_limit
        self.channels = channels

    def encode(self) -> Image:
        """Encodes data into an image by utilizing the pixel channels to store each byte of the data."""
        if self.data is None:
            raise Exception("There's no data to encode.")

        image = np.frombuffer(self.data, dtype=np.uint8)

        height = (
            math.ceil(abs(len(self.data) / (self.width_limit * self.channels)))
            if self.width_limit
            else math.ceil(abs(math.sqrt(len(self.data) / self.channels)))
            if self.width_limit is None
            else 1
        )
        width = math.ceil(abs(len(self.data) / (height * self.channels)))
        channels = abs(self.channels)

        pad_count = height * width * channels - len(self.data)
        if pad_count:
            padding = np.zeros((pad_count,), dtype=np.uint8)
            image = np.concatenate((image, padding))

        return Image(img=image.reshape(height, width, channels))

    def decode(self, img: np.ndarray) -> bytes:
        """Decodes data from an image."""
        return img.tobytes()


class LsbSteganographyEncoder(EncoderInterface):
    """An Encoder which utilizes LSB Steganography to encode data."""

    def __init__(
        self,
        data: bytes | None = None,
        img: np.ndarray | None = None,
    ):
        self.data = data
        self.img = img

    def encode(self) -> Image:
        """Encodes data into an image by storing each bit of the data in the lsb bit of each channel."""
        if self.data is None:
            raise Exception("There's no data to encode.")
        if self.img is None:
            raise Exception("There's no image to encode data to.")

        channels = self.img.flatten()
        bytes_for_data_bits = (len(channels).bit_length() + 7) // 8

        data = self.data
        data = len(data).to_bytes(bytes_for_data_bits, "big") + data
        data_bits = bitarray()
        data_bits.frombytes(data)

        if len(data_bits) > len(channels):  # Each channel can store 1 bit of the data
            raise Exception(
                "Can't fit the data within the image with the current implementation."
            )

        for i in range(channels.shape[0]):
            try:
                channels[i] = (channels[i] & ~1) | data_bits.pop(0)
            except IndexError:
                break

        return Image(img=channels.reshape(self.img.shape))

    def decode(self, img: np.ndarray) -> bytes:
        """Decodes data from an image by taking the lsb bits of the channels."""
        channels = img.flatten()
        bytes_for_data_bits = (len(channels).bit_length() + 7) // 8
        data_len_bits = bitarray()
        for lv in channels[: bytes_for_data_bits * 8]:
            data_len_bits.append(lv & 1)
        data_len = int.from_bytes(
            data_len_bits.tobytes(), "big"
        )  # number of bytes in data

        data = bitarray()
        for lv in channels[
            bytes_for_data_bits * 8 : bytes_for_data_bits * 8 + data_len * 8
        ]:
            data.append(lv & 1)

        return data.tobytes()


if __name__ == "__main__":
    # Example
    from pathlib import Path

    direct_encoder = DirectEncoder(b"Hello, World!", width_limit=2, channels=4)
    Image.encode(direct_encoder).save(Path("text_encoder_output.png"))
    print(Image.read(Path("text_encoder_output.png")).decode(direct_encoder).decode())

    # NOTE: `image.png` needs to be in the cwd for this to work!
    steganography_encoder = LsbSteganographyEncoder(
        b"Hello, World!", Image.read(Path("image.png")).as_array()
    )
    Image.encode(steganography_encoder).save(
        Path("lsb_stegnography_encoder_output.png")
    )
    print(
        Image.read(Path("lsb_stegnography_encoder_output.png"))
        .decode(steganography_encoder)
        .decode()
    )
