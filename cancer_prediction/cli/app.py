import sys

import typer
from streamlit.web import cli as stcli

app = typer.Typer()


@app.command()
def version() -> None:
    """Prints the version of the app."""
    typer.echo("0.1.0")


@app.command()
def run() -> None:
    """Runs the Streamlit app."""
    sys.argv = ["streamlit", "run", "cancer_prediction/streamlit_app.py"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    app()
