from pathlib import Path
from typing import Optional

import typer

from ..encoders import DirectEncoder, LsbSteganographyEncoder
from ..image import Image

app = typer.Typer()


@app.command()
def direct(text: str, output: Optional[Path] = None, encoding: str = "utf-8"):
    """Encode given text directly as a image"""
    image = Image.encode(DirectEncoder(data=bytes(text, encoding)))

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    print(f"Image saved as: {save_to}")


@app.command()
def stegangography(
    text: str, img: Path, output: Optional[Path] = None, encoding: str = "utf-8"
):
    """Encode the text to be hidden in the given image"""
    image = Image.encode(
        LsbSteganographyEncoder(
            data=bytes(text, encoding), img=Image.read(img).as_array()
        )
    )

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    print(f"Image saved as: {save_to}")
