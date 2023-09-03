from pathlib import Path
from typing import Optional

import typer

from ..encoders import DirectEncoder, LsbSteganographyEncoder
from ..image import Image

app = typer.Typer()


@app.command()
def direct(path: Path, text: str, encoding: str = "utf-8"):
    """Encode given text directly as a image"""
    image = Image.encode(DirectEncoder(data=bytes(text, encoding)))
    image.save(path)


@app.command()
def stegangography(
    path: Path, text: str, encoding: str = "utf-8", output: Optional[Path] = None
):
    """Encode the text to be hidden in the given image"""
    image = Image.read(path)
    image = image.encode(
        LsbSteganographyEncoder(data=bytes(text, encoding), img=image.img)
    )
    if not output:
        image.save(Path("output.png"))
    else:
        image.save(output)
