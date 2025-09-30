## Setting up `uv` package manager
We first need to install `uv`. The easiest way to do this is with `pipx`:
```bash
pipx install uv
```
Your experience doing this with other operating systems may vary. Further details about installation can be found [here](https://docs.astral.sh/uv/getting-started/installation/).

_**Don't do this**_, but you can initialize a new project with `uv` from scratch:
```bash
uv init my-project-name
```
This creates a fresh project scaffold (including some folders we will not make use of in this workshop) and is typically what you'd do at the very start of a project.

Since we already have some code, we don't want the scaffold. Instead, we use the bare option:
```bash
uv init --bare
```
This creates only a minimal pyproject.toml in the current directory (no extra files or folders), which is what we need to neatly manage our dependencies.

Once the minimal config is in place, we can migrate out dependencies automatically from the existing `requirements.txt`.
```bash
uv add -r requirements.txt
```
And for development dependencies, let's add `black`, `isort` and `flake8`.
```bash
uv add --dev black isort flake8
```
If you navigate to the `pyproject.toml`, you can also add a description and author of the project.
```
description: "A basic model to predict cancerous tumors based on certain properties."
authors: [{name: Ryan Daniels}]
```
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

## Adding packages to your uv environment
Now let's add `streamlit` to our project. If you open the `pyproject.toml` file, you'll notice that there is a list of dependencies:

```toml
dependencies = [
    "scikit-learn>=1.5.2",
    "numpy>=2.1.3",
    "ipykernel>=6.30.1",
    "pandas>=2.3.2",
    "matplotlib>=3.10.6",
]
```

If we want to add another package to our project, such as `streamlit`, we can just say,
```
uv add streamlit
```

Notice that now `streamlit` has appeared in `pyproject.toml`! `uv` has also created a file called `uv.lock`. This file essentially locks in all of your dependencies so someone external can recreate your environment. It is somewhat analogous to the conda `environment.yml` file. Generally, we never alter this file manually.

<br>
![Dark Souls Bonfire](../imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }
<br>

Now let's implement the command line interface (CLI).