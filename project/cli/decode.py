from pathlib import Path

import typer

from ..encoders import DirectEncoder, LsbSteganographyEncoder
from ..image import Image

app = typer.Typer()


@app.command()
def direct(path: Path, encoding="utf-8"):
    image = Image.read(path)
    print(image.decode(DirectEncoder()).decode(encoding=encoding))


@app.command()
def stegangography(path: Path, encoding="utf-8"):
    image = Image.read(path)
    print(
        image.decode(LsbSteganographyEncoder(img=image.as_array())).decode(
            encoding=encoding
        )
    )
