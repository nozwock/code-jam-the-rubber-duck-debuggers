import numpy
from encoder_interface import EncoderInterface
from encoder_impl import EncoderImpl


class Image:
    width = None
    height = None
    pixel_array = None
    encoder = None

    def __init__(self, pixel_array: numpy.ndarray,encoder: EncoderInterface):
        if len(pixel_array.shape) != 3:
            raise Exception(f"Unexpected pixel_arr shape: array has {len(pixel_array.shape)} dimensions, but expected 3")

        self.pixel_array = pixel_array
        self.height = self.pixel_array.shape[0]
        self.width = self.pixel_array.shape[1]
        self.encoder = encoder

        print("Created Instance")

    def encode(self) -> None:
        pass

    def decode(self) -> None:
        pass


def read_image(filepath: str) -> Image:
    if filepath == "":
        raise Exception(f"Invalid filepath provided: {filepath}")

    shape = (1, 1, 1)
    pixel_array = numpy.zeros(shape)
    encoder = EncoderImpl()

    return Image(pixel_array, encoder)

