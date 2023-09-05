import sys
from pathlib import Path
from typing import Annotated, Optional

import typer

from ..encoders import DirectEncoder, LsbSteganographyEncoder
from ..image import Image

app = typer.Typer()


@app.command()
def direct(
    text: str,
    output: Annotated[Optional[Path], typer.Option(dir_okay=False)] = None,
    width_limit: int = 0,
    channels: int = 3,
    encoding: str = "utf-8",
):
    """Encodes data into an image by utilizing the pixel channels to store each byte of the data."""
    image = Image.encode(
        DirectEncoder(
            data=bytes(text, encoding), width_limit=width_limit, channels=channels
        )
    )

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    typer.echo("Image saved as: ", sys.stderr, nl=False)
    typer.echo(save_to)


@app.command()
def steganography(
    text: str,
    img: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    output: Annotated[Optional[Path], typer.Option(dir_okay=False)] = None,
    encoding: str = "utf-8",
):
    """Encodes data into an image utilizing Steganography."""
    image = Image.encode(
        LsbSteganographyEncoder(
            data=bytes(text, encoding), img=Image.read(img).as_array()
        )
    )

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    typer.echo("Image saved as: ", sys.stderr, nl=False)
    typer.echo(save_to)
