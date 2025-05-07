import sys

import typer
from streamlit.web import cli as stcli

from cancer_prediction import streamlit_app

app = typer.Typer()


@app.command()
def __version__():
    # Print the version of the app
    typer.echo("0.1.0")


@app.command()
def run():
    sys.argv = ["streamlit", "run", "cancer_prediction/streamlit_app.py"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    app()
