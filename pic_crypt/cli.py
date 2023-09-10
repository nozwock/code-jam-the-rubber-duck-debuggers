"""Args parsing for the CLI."""

import sys
from pathlib import Path
from typing import BinaryIO, cast

import click
import cloup
from cloup.constraints import AnySet, If, require_all, require_one
from PIL import ImageColor

from .ciphers import KDF, Cipher
from .encoders import DirectEncoder, LsbSteganographyEncoder
from .image import Image
from .image.text import create_colored_image, hide_with_repeatation


@cloup.group(
    context_settings=dict(help_option_names=["-h", "--help"], show_default=True)
)
def app():
    ...


@app.command("hide-text")
@cloup.argument("secret", type=str)
@cloup.argument("repeat", type=str)
@cloup.option_group(
    "Image",
    cloup.option("-w", "--width", type=int, default=720),
    cloup.option("-h", "--height", type=int, default=480),
    cloup.option("--img-color", type=str, default="#000000"),
)
@cloup.option("-c", "--color", type=str, default="#ffffff")
@cloup.option("--font-size", type=int, default=10)
@cloup.option("-p", "--padding", type=str, default="0, 2")
@cloup.option("--trim-extra", type=bool, default=True)
@cloup.option(
    "-o",
    "--output",
    type=cloup.Path(dir_okay=False),
    default=None,
)
def hide_text(
    secret: str,
    repeat: str,
    width: int,
    height: int,
    img_color: str,
    color: str,
    font_size: int,
    padding: str,
    trim_extra: bool,
    output: Path | None,
):
    """Generates an image with a hidden secret string by putting it in between repeations of some string."""
    rgb_color = ImageColor.getrgb(color)
    rgb_img_color = ImageColor.getrgb(img_color)

    save_to = Path("output.png") if output is None else output
    Image(
        hide_with_repeatation(
            create_colored_image(width, height, rgb_img_color),
            secret,
            repeat,
            color=rgb_color,
            font_size=font_size,
            padding=cast(tuple[int, int], tuple(map(int, padding.split(",")[:2]))),
            trim_extra=trim_extra,
        )
    ).save(save_to)

    click.echo("Image saved to: ", sys.stderr, nl=False)
    click.echo(save_to)


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
    constraint=require_one,
)
@cloup.option(
    "-o",
    "--output",
    type=cloup.Path(dir_okay=False),
    default=None,
)
@cloup.option("-w", "--width-limit", type=int, default=None)
@cloup.option("-c", "--channels", type=int, default=3)
@cloup.option_group(
    "Encryption",
    cloup.option("-e", "--encrypt", is_flag=True),
    cloup.option("-k", "--key", type=str, default=None),
    cloup.option(
        "--cipher",
        type=click.Choice(Cipher._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: Cipher._member_map_[v] if v else None,
    ),
    cloup.option(
        "--kdf",
        type=click.Choice(KDF._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: KDF._member_map_[v] if v else None,
    ),
)
@cloup.constraint(
    If(
        AnySet("key", "cipher", "kdf"),
        then=require_all,
    ),
    ["encrypt"],
)
def encode_direct(
    text: str | None,
    file: BinaryIO | None,
    output: Path | None,
    width_limit: int | None,
    channels: int,
    encrypt: bool,
    key: str | None,
    cipher: Cipher | None,
    kdf: KDF | None,
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

    if encrypt:
        cipher = Cipher.ChaCha20 if cipher is None else cipher
        kdf = KDF.Argon2 if kdf is None else kdf
        key = (
            click.prompt("Password Key", hide_input=True, confirmation_prompt=True)
            if key is None and encrypt
            else key
        )

        data = cipher.value().encrypt(data, secret=key.encode(), kdf=kdf.value())

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
@cloup.option_group(
    "Encryption",
    cloup.option("-d", "--decrypt", is_flag=True),
    cloup.option("-k", "--key", type=str, default=None),
    cloup.option(
        "--cipher",
        type=click.Choice(Cipher._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: Cipher._member_map_[v] if v else None,
    ),
    cloup.option(
        "--kdf",
        type=click.Choice(KDF._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: KDF._member_map_[v] if v else None,
    ),
)
@cloup.constraint(
    If(
        AnySet("key", "cipher", "kdf"),
        then=require_all,
    ),
    ["decrypt"],
)
def decode_direct(
    img: Path,
    output: BinaryIO | None,
    decrypt: bool,
    key: str | None,
    cipher: Cipher | None,
    kdf: KDF | None,
):
    """Decodes data from an image."""
    data = Image.read(img).decode(DirectEncoder())

    if decrypt:
        cipher = Cipher.ChaCha20 if cipher is None else cipher
        kdf = KDF.Argon2 if kdf is None else kdf
        key = (
            click.prompt("Password Key", hide_input=True)
            if key is None and decrypt
            else key
        )

        try:
            data = cipher.value().decrypt(data, secret=key.encode(), kdf=kdf.value())
        except Exception as e:
            click.echo(f"Error: {repr(e)}", sys.stderr)
            sys.exit(1)

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
    constraint=require_one,
)
@cloup.option(
    "-o",
    "--output",
    type=cloup.Path(dir_okay=False),
    default=None,
)
@cloup.option_group(
    "Encryption",
    cloup.option("-e", "--encrypt", is_flag=True),
    cloup.option("-k", "--key", type=str, default=None),
    cloup.option(
        "--cipher",
        type=click.Choice(Cipher._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: Cipher._member_map_[v] if v else None,
    ),
    cloup.option(
        "--kdf",
        type=click.Choice(KDF._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: KDF._member_map_[v] if v else None,
    ),
)
@cloup.constraint(
    If(
        AnySet("key", "cipher", "kdf"),
        then=require_all,
    ),
    ["encrypt"],
)
def encode_steganography(
    text: str | None,
    file: BinaryIO | None,
    img: Path,
    output: Path | None,
    encrypt: bool,
    key: str | None,
    cipher: Cipher | None,
    kdf: KDF | None,
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

    if encrypt:
        cipher = Cipher.ChaCha20 if cipher is None else cipher
        kdf = KDF.Argon2 if kdf is None else kdf
        key = (
            click.prompt("Password Key", hide_input=True, confirmation_prompt=True)
            if key is None and encrypt
            else key
        )

        data = cipher.value().encrypt(data, secret=key.encode(), kdf=kdf.value())

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
@cloup.option_group(
    "Encryption",
    cloup.option("-d", "--decrypt", is_flag=True),
    cloup.option("-k", "--key", type=str, default=None),
    cloup.option(
        "--cipher",
        type=click.Choice(Cipher._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: Cipher._member_map_[v] if v else None,
    ),
    cloup.option(
        "--kdf",
        type=click.Choice(KDF._member_names_, case_sensitive=False),
        default=None,
        callback=lambda ctx, param, v: KDF._member_map_[v] if v else None,
    ),
)
@cloup.constraint(
    If(
        AnySet("key", "cipher", "kdf"),
        then=require_all,
    ),
    ["decrypt"],
)
def decode_steganography(
    img: Path,
    output: BinaryIO | None,
    decrypt: bool,
    key: str | None,
    cipher: Cipher | None,
    kdf: KDF | None,
):
    """Decodes data from an image utilizing Steganography."""
    data = Image.read(img).decode(LsbSteganographyEncoder())

    if decrypt:
        cipher = Cipher.ChaCha20 if cipher is None else cipher
        kdf = KDF.Argon2 if kdf is None else kdf
        key = (
            click.prompt("Password Key", hide_input=True)
            if key is None and decrypt
            else key
        )

        try:
            data = cipher.value().decrypt(data, secret=key.encode(), kdf=kdf.value())
        except Exception as e:
            click.echo(f"Error: {repr(e)}", sys.stderr)
            sys.exit(1)

    if output is None:
        click.echo("Decoded data:", sys.stderr)
        sys.stdout.buffer.write(data)
    else:
        try:
            output.write(data)
        except Exception as e:
            output.close()
            raise e
