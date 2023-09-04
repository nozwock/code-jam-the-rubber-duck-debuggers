from pathlib import Path

import typer

from ..encoders import DirectEncoder, LsbSteganographyEncoder
from ..image import Image

app = typer.Typer()


@app.command()
def direct(img: Path, encoding: str = "utf-8"):
    """Decodes data from an image."""
    text = Image.read(img).decode(DirectEncoder()).decode(encoding=encoding)

    print(f"Decoded text:\n{text}")


@app.command()
def steganography(img: Path, encoding: str = "utf-8"):
    """Decodes data from an image utilizing Steganography."""
    text = Image.read(img).decode(LsbSteganographyEncoder()).decode(encoding=encoding)

    print(f"Decoded text:\n{text}")
