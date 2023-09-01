import numpy
from project.image.encoders.encoder_interface import EncoderInterface


class Image:
    width = None
    height = None
    pixel_array = None

    def __init__(self, pixel_array: numpy.ndarray):
        if len(pixel_array.shape) != 3:
            raise Exception(f"Unexpected pixel_arr shape: array has {len(pixel_array.shape)} dimensions, but expected 3")

        self.pixel_array = pixel_array
        self.height = self.pixel_array.shape[0]
        self.width = self.pixel_array.shape[1]
        print("Created Instance")

    def encode(self, encoder: EncoderInterface) -> None:
        pass

    def decode(self, encoder: EncoderInterface) -> None:
        pass


def read_image(filepath: str) -> Image:
    if filepath == "":
        raise Exception(f"Invalid filepath provided: {filepath}")

    shape = (1, 1, 1)
    pixel_array = numpy.zeros(shape)

    return Image(pixel_array)