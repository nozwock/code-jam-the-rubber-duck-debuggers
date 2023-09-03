"""Args parsing for the CLI."""

import typer
from pathlib import Path
from typing import Optional
from image import Image
from encoders import (DirectEncoder, LsbSteganographyEncoder)

app = typer.Typer()

encode_app = typer.Typer()
decode_app = typer.Typer()
app.add_typer(encode_app, name="encode", help="encode given text to image")
app.add_typer(decode_app, name="decode", help="decode given image into text")


@encode_app.command()
def direct(path: str, text: str, encoding: str = 'utf-8'):
    """Encode given text directly as a image"""
    image = Image.encode(DirectEncoder(data=bytes(text, encoding)))
    image.save(path)


@encode_app.command()
def stegangography(path: str, text: str, encoding: str = "utf-8", output: Optional[Path] = None):
    """Encode the text to be hidden in the given image"""
    image = Image.read(path)
    image = image.encode(LsbSteganographyEncoder(data=bytes(text, encoding), img=image.img))
    if not output:
        image.save("output.png")
    else:
        image.save(output)


@decode_app.command()
def direct(path: Path, encoding='utf-8'):
    image = Image.read(path)
    print(image.decode(DirectEncoder()).decode(encoding=encoding))


@decode_app.command()
def stegangography(path: Path, encoding='utf-8'):
    image = Image.read(path)
    print(image.decode(LsbSteganographyEncoder(img=image.as_array())).decode(encoding=encoding))


if __name__ == "__main__":
    app()
