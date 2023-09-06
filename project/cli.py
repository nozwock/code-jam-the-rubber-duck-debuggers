"""Args parsing for the CLI."""

import sys
from pathlib import Path
from typing import BinaryIO

import click
import cloup
from cloup.constraints import mutually_exclusive

from .encoders import DirectEncoder, LsbSteganographyEncoder
from .image import Image

# from cloup.constraints import AnySet, If, require_all


@cloup.group(
    context_settings=dict(help_option_names=["-h", "--help"], show_default=True)
)
def app():
    ...


# TODO: Add encryption options
# @app.command()
# @cloup.option_group(
#     "Encryption",
#     cloup.option("--encrypt", is_flag=True),
#     cloup.option(
#         "--cipher",
#         type=click.Choice(["chacha20", "aes-gcm"]),
#         default=None,
#         help="[default: aes-gcm]",
#     ),
#     cloup.option(
#         "--kdf",
#         type=click.Choice(["argon2", "pbkdf"]),
#         default=None,
#         help="[default: argon2]",
#     ),
# )
# @cloup.constraint(
#     If(AnySet("kdf", "cipher"), then=require_all),
#     ["encrypt"],
# )
# def test(**kwargs):
#     ...


@app.group()
def encode():
    """Encode text within an image."""
    ...


@app.group()
def decode():
    """Decode text from an image."""
    ...


@encode.command("direct")
@cloup.option_group(
    "Input",
    cloup.option("-t", "--text", type=str),
    cloup.option("-f", "--file", type=cloup.File("rb")),
    constraint=mutually_exclusive,
)
@cloup.option(
    "-o",
    "--output",
    type=cloup.Path(dir_okay=False),
    default=None,
)
@cloup.option("-w", "--width-limit", type=int, default=0)
@cloup.option("-c", "--channels", type=int, default=3)
def encode_direct(
    text: str | None,
    file: BinaryIO | None,
    output: Path | None,
    width_limit: int,
    channels: int,
):
    """Encodes data into an image by utilizing the pixel channels to store each byte of the data."""
    if text is not None:
        data = text.encode()
    else:
        assert file is not None
        try:
            data = file.read()
        except Exception as e:
            file.close()
            raise e

    image = Image.encode(
        DirectEncoder(data=data, width_limit=width_limit, channels=channels)
    )

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    click.echo("Image saved to: ", sys.stderr, nl=False)
    click.echo(save_to)


@decode.command("direct")
@cloup.argument("img", type=cloup.Path(exists=True, dir_okay=False))
@cloup.option(
    "-o",
    "--output",
    type=cloup.File("wb"),
    default=None,
)
def decode_direct(img: Path, output: BinaryIO | None):
    """Decodes data from an image."""
    data = Image.read(img).decode(DirectEncoder())

    if output is None:
        click.echo("Decoded data:", sys.stderr)
        sys.stdout.buffer.write(data)
    else:
        try:
            output.write(data)
        except Exception as e:
            output.close()
            raise e


@encode.command("steganography")
@cloup.argument("img", type=cloup.Path(exists=True, dir_okay=False))
@cloup.option_group(
    "Input",
    cloup.option("-t", "--text", type=str),
    cloup.option("-f", "--file", type=cloup.File("rb")),
    constraint=mutually_exclusive,
)
@cloup.option(
    "-o",
    "--output",
    type=cloup.Path(dir_okay=False),
    default=None,
)
def encode_steganography(
    text: str | None, file: BinaryIO | None, img: Path, output: Path | None
):
    """Encodes data into an image utilizing Steganography."""
    if text is not None:
        data = text.encode()
    else:
        assert file is not None
        try:
            data = file.read()
        except Exception as e:
            file.close()
            raise e

    image = Image.encode(
        LsbSteganographyEncoder(data=data, img=Image.read(img).as_array())
    )

    save_to = Path("output.png") if output is None else output
    image.save(save_to)

    click.echo("Image saved to: ", sys.stderr, nl=False)
    click.echo(save_to)


@decode.command("steganography")
@cloup.argument("img", type=cloup.Path(exists=True, dir_okay=False))
@cloup.option(
    "-o",
    "--output",
    type=cloup.File("wb"),
    default=None,
)
def decode_steganography(img: Path, output: BinaryIO | None):
    """Decodes data from an image utilizing Steganography."""
    data = Image.read(img).decode(LsbSteganographyEncoder())

    if output is None:
        click.echo("Decoded data:", sys.stderr)
        sys.stdout.buffer.write(data)
    else:
        try:
            output.write(data)
        except Exception as e:
            output.close()
            raise e
