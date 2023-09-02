"""Args parsing for the CLI."""

import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")
