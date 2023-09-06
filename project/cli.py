"""Args parsing for the CLI."""

import sys
from pathlib import Path

import click

from .encoders import DirectEncoder, LsbSteganographyEncoder
from .image import Image


@click.group(
    context_settings=dict(show_default=True, help_option_names=["-h", "--help"])
)
def app():
    ...


@app.group()
def encode():
    """Encode text within an image."""
    ...


@app.group()
def decode():
    """Decode text from an image."""
    ...


@encode.command("direct")
@click.argument("text", type=str)
@click.option(
    "--output",
    type=click.Path(dir_okay=False),
    default=None,
)
@click.option("--width-limit", type=int, default=0)
@click.option("--channels", type=int, default=3)
@click.option("--encoding", type=str, default="utf-8")
def encode_direct(
    text: str,
    output: Path | None,
    width_limit: int,
    channels: int,
    encoding: str,
):
    """Encodes data into an image by utilizing the pixel channels to store each byte of the data."""
    image = Image.encode(
        DirectEncoder(
            data=bytes(text, encoding), width_limit=width_limit, channels=channels
        )
    )

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    click.echo("Image saved to: ", sys.stderr, nl=False)
    click.echo(save_to)


@decode.command("direct")
@click.argument("img", type=click.Path(exists=True, dir_okay=False))
@click.option("--encoding", type=str, default="utf-8")
def decode_direct(img: Path, encoding: str):
    """Decodes data from an image."""
    text = Image.read(img).decode(DirectEncoder()).decode(encoding=encoding)

    click.echo("Decoded text:", sys.stderr)
    click.echo(text)


@encode.command("steganography")
@click.argument("text", type=str)
@click.argument("img", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--output",
    type=click.Path(dir_okay=False),
    default=None,
)
@click.option("--encoding", type=str, default="utf-8")
def encode_steganography(text: str, img: Path, output: Path | None, encoding: str):
    """Encodes data into an image utilizing Steganography."""
    image = Image.encode(
        LsbSteganographyEncoder(
            data=bytes(text, encoding), img=Image.read(img).as_array()
        )
    )

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    click.echo("Image saved to: ", sys.stderr, nl=False)
    click.echo(save_to)


@decode.command("steganography")
@click.argument("img", type=click.Path(exists=True, dir_okay=False))
@click.option("--encoding", type=str, default="utf-8")
def decode_steganography(img: Path, encoding: str):
    """Decodes data from an image utilizing Steganography."""
    text = Image.read(img).decode(LsbSteganographyEncoder()).decode(encoding=encoding)

    click.echo("Decoded text:", sys.stderr)
    click.echo(text)


if __name__ == "__main__":
    app()
