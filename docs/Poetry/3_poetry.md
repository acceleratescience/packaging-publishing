## Setting up Poetry
We first need to install Poetry. The easiest way to do this is with `pipx`:
```bash
pipx install poetry
```
Your experience doing this with other operating systems may vary. Further details about installation can be found [here](https://python-poetry.org/docs/#installing-with-pipx).

Don't do this now, but you can initialize a new project with poetry from scratch:
```bash
poetry new my-project-name
```
Typically you would do this from the start of your work.

Or you might have some existing work and an environment that you might want to continue developing using poetry:
```bash
poetry init
```
Since we already have some code, we use the later option for this project. Running `poetry init` will involve having to run through some basic setup steps to define out config file.

```
Package name [packaging-publishing]:  cancer-prediction-crsid
Version [0.1.0]:  
Description []:  A basic model to predict cancerous tumors based on certain properties.
Author [Ryan Daniels <31715811+rkdan@users.noreply.github.com>, n to skip]:  
License []:  GPL-3.0-or-later
Compatible Python versions [^3.10]:  

Would you like to define your main dependencies interactively? (yes/no) [yes] yes
```
We can then open the requirements file and just read them off. Do this for everything except `streamlit`. When we are asked to define development dependencies, we will add `black`, `isort`, and `flake8`. Confirm the generation, and that should create our `pyproject.toml`. We'll discuss this in more detail in the notes

## File structure <a id="poetry-files"></a>
Let's create the file directories according to the structure below. Don't worry if the order of the files and folders isn't the same.
```
cancer-prediction-crsid
├── venv
├── models
│   └── cancer_model.pkl
├── data
│   ├── breast_cancer_test.csv
│   ├── breast_cancer_train.csv
│   └── breast_cancer.csv
├── cancer_prediction
│   ├── __init__.py
│   ├── app.py
│   ├── cancer_model.py
│   └── streamlit_app.py
├── tests
│   └── __init__.py
├── pyproject.toml
├── README.md
├── LICENSE.md
├── .gitignore
├── requirements.txt
└── notebook.ipynb
```

## Licensing <a id="poetry-licensing"></a>
We also need to populate the `LICENSE.md` file. You can find out the details of licensing [here](https://choosealicense.com/)

!!! warning

    If you do not include a license, nobody else can copy, distribute, or modify your work without being at risk of take-downs, shake-downs, or litigation. If the work has other contributors, this includes **YOU**. The GitHub Terms of Service allow people to view or fork your code. 

!!! warning

    If software does not have a license, this generally means that you do not have permission to use, modify, or share the code. Forking and viewing code **does not imply that you are permitted to use, modify or share it**. Your best option is to nicely ask the authors to add a license, by either sending them an email, or opening an Issue on the repo.

## Adding packages to your Poetry environment
Now let's add `streamlit` to our project. If you open the `pyproject.toml` file, you'll notice that there is a list of dependencies:

```
[tool.poetry.dependencies]
python = "^3.10"
pandas = "2.2.1"
scikit-learn = "1.4.1.post1"
matplotlib = "3.8.3"
numpy = "1.26.4"
```

If we want to add another package to our project, such as `streamlit`, we can just say,
```
poetry add streamlit
```

Notice that now `streamlit` has appeared in `pyproject.toml`! Poetry has also created a file called `poetry.lock`. This file essentially locks in all of your dependencies so someone external can recreate your environment. It is somewhat analogous to the conda `environment.yml` file. Generally, we never alter this file manually.

When you see this symbol:

![Dark Souls Bonfire](../imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }

it means that you should commit and push your changes to the repository. They indicate key checkpoints in the workshop.

## Implement the CLI entry point
Notice that the CLI will still not work in the way that we want it to. In order for the CLI to work, we have to make two alterations.

!!! tip

    There are a few different libraries that will help you handle CLI. In this project, we use `typer`, but `argparse` is also a very popular one.

### Additions to the code
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

### Additions to the `.toml` file
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

![Dark Souls Bonfire](imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Poetry resources__](resources/references.md#poetry)

    ---
    Information on Poetry, toml files, and licensing

</div>