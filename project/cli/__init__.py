"""Args parsing for the CLI."""

import typer

from . import decode, encode

app = typer.Typer()

app.add_typer(encode.app, name="encode", help="Encode text within an image.")
app.add_typer(decode.app, name="decode", help="Decode text from an image.")


if __name__ == "__main__":
    app()
