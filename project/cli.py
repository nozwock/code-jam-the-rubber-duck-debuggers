"""Args parsing for the CLI."""

import typer
from image import Image
from encoders import (DirectEncoder, LsbSteganographyEncoder)

app = typer.Typer()

encode_app = typer.Typer()
app.add_typer(encode_app, name="encode", help="enocde given text to image")


@encode_app.command()
def direct(path: str, text: str, encoding: str = 'utf-8'):
    """Encode given text directly as a image"""
    image = Image.encode(DirectEncoder(data=bytes(text, encoding)))
    image.save(path)


@encode_app.command()
def stegangography(path: str, text: str, encoding: str = "utf-8", out_path: str = ""):
    """Encode the text to be hidden in the given image"""
    image = Image.read(path)
    image.encode(LsbSteganographyEncoder(text=text, img=image.img, encoding=encoding))
    if not out_path:
        image.save(path)
    else:
        image.save(out_path)


if __name__ == "__main__":
    app()
