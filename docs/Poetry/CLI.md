# Implement the CLI entry point
Notice that the CLI will still not work in the way that we want it to. In order for the CLI to work, we have to make two alterations.

!!! tip

    There are a few different libraries that will help you handle CLI. In this project, we use `typer`, but `argparse` is also a very popular one.

## Additions to the code
At this point it is worth quickly going through the code for the `app.py` script. Click the arrows to find out what the code does.

``` python
import sys

import typer
from cancer_prediction import streamlit_app  # (1)!
from streamlit.web import cli as stcli     

app = typer.Typer()  # (2)!

@app.command()  # (3)!
def __version__():
    typer.echo("0.1.0")

@app.command()  # (4)!
def run():
    sys.argv = ["streamlit", "run", "cancer_prediction/streamlit_app.py"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    app()
```

1.  Since this depends on the `streamlit_app.py` script, we have to import it here
2.  Initialize the typer app
3.  A command that prints out the version of the app
4.  A command that essentially mimics the `streamlit run cancer_prediction/streamlit_app.py` command that we used earlier

We create a new folder inside `cancer_prediction` called `cli`. We also create a new `__init__.py` file and copy over the `app.py` file. The init file should contain only:
```python
from .app import app

__all__ = ["app"]
```

We also need to add the `typer` library. Since this is a main dependancy, we can add it using the regular `poetry add` command.

## Additions to the `.toml` file
We want someone to be able to do:
```bash
pip install cancer-prediction
```

and then
```
cancer-prediction run
```

We have defined our `run` command, but your bash terminal will not recognize the command `cancer-prediction`! To do this, we first need to define an entry point. We add the following line to `pyproject.toml` below the readme:
```toml
packages = [{include = "cancer_prediction"}]
```

Then we add the following lines
```
[tool.poetry.scripts]
cancer-prediction =  "cancer_prediction.cli:app"
```

This provides us with an entry point to the `cli/app.py` file. What is essentially says is: "When I type the command `cancer-prediction` into my command line, what I really mean is execute this app."

We then install a local copy of our package which mimics a pip installation:
```bash
poetry install
```

We can now try it out by running
```bash
cancer-prediction run
```

and the streamlit app should open! You should be able to play around with the app in the browser. In general, streamlit is a great way to prototype new applications. Try training a model using the training data - give it a name like `cancer_model_v2`. Then try running inference on this model with the testing data.

![Dark Souls Bonfire](../imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Poetry resources__](resources/references.md#poetry)

    ---
    Information on Poetry, toml files, and licensing

</div>