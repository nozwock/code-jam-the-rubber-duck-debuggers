"""Args parsing for the CLI."""

import typer

from . import decode, encode

app = typer.Typer()

app.add_typer(encode.app, name="encode", help="encode given text to image")
app.add_typer(decode.app, name="decode", help="decode given image into text")


if __name__ == "__main__":
    app()
