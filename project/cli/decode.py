from pathlib import Path

import typer

from ..encoders import DirectEncoder, LsbSteganographyEncoder
from ..image import Image

app = typer.Typer()


@app.command()
def direct(img: Path, encoding="utf-8"):
    text = Image.read(img).decode(DirectEncoder()).decode(encoding=encoding)

    print(f"Decoded text:\n{text}")


@app.command()
def stegangography(img: Path, encoding="utf-8"):
    text = (
        Image.read(img)
        .decode(LsbSteganographyEncoder(img=Image.read(img).as_array()))
        .decode(encoding=encoding)
    )

    print(f"Decoded text:\n{text}")
