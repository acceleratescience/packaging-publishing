# Packaging and Publishing Workshop

There are two branches to this repo:

- `main` contains the starting code that you will fork over to your repo.
- `result` contains the final product, that you should hopefully put together yourself.

## Contents
1. [Setting up Codespaces](#codespaces)\
    1.1. [Create a new branch](#codespaces-branch)
2. [Setting up Poetry](#poetry)\
    2.1. [File structure](#poetry-files)\
    2.2. [Licensing](#poetry-licensing)
3. [Packaging up our software](#packaging)
4. [Finetuning for classification](#bert)
5. [No-code](#no-code)
6. [Stable Diffusion](#stable-diffusion)

## 1. Setting up Codespaces <a id="codespaces"></a>
The first step is to fork the main branch and open Codespaces!

![](imgs/fork.png)

This will create a version of the repo in your own GitHub page. Navigate to this repo and then open it in GitHub Codespaces

![](imgs/createcodespace.png)

Now you should be in the browser version of VSCode.

> [!NOTE]  
> Even though we are using Codespaces, the general packaging process will still work with regular VSCode on your desktop.

### 1.1. Create a new branch <a id="codespaces-branch"></a>
It is good practice to do development work on a new branch, but first we should set up a virtual environment and install any dependencies.

Set up the new virtual environment with,
```bash
python3.10 -m venv venv
. venv/bin/activate
```

You can verify the path of the python version you are using by running
```bash
which python
```
and this should return something like:\
 `/workspaces/packaging-publishing/venv/bin/python`

We install the dependencies using
```bash
python -m pip install -r requirements.txt
```

Now create a new branch using the UI or using the git CLI.
```bash
git checkout -b dev
```
This will automatically create and move over to a new branch called `dev`. The environment and all the packages we installed should also be moved along with it.

## 2. Setting up Poetry <a id="Poetry"></a>
We first need to install Poetry. The easiest way to do this is with `pipx`:
```bash
pipx install poetry
```
Your experience doing this with other operating systems may vary. Further details about installation can be found [here](https://python-poetry.org/docs/#installing-with-pipx).

You can initialize a new project with poetry from scratch:
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
Package name [packaging-publishing]:  cancer-prediction
Version [0.1.0]:  
Description []:  A basic model to predict cancerous tumors based on certain properties.
Author [Ryan Daniels <31715811+rkdan@users.noreply.github.com>, n to skip]:  
License []:  GPL-3.0-or-later
Compatible Python versions [^3.10]:  

Would you like to define your main dependencies interactively? (yes/no) [yes] yes
```
We can then open the requirements file and just read them off. Do this for everything except `streamlit`. When we are asked to define development dependencies, we will add `black`, `isort`, and `flake8`. Confirm the generation, and that should create our `pyproject.toml`. We'll discuss this in more detail in the notes

### 2.1. File structure <a id="poetry-files"></a>
Let's create the file directories according to the structure below. You should also create two additional files: `.gitignore`, and `LICENSE.md`. Don't worry if the order of the files and folders isn't the same.
```
packing-publishing
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
│   └── cancer_model.py
├── tests
│   └── __init__.py
├── pyproject.toml
├── README.md
├── LICENSE.md
├── .gitignore
├── requirements.txt
└── notebook.ipynb
```

### 2.2. Licensing <a id="poetry-licensing"></a>
We also need to create a `LICENSE.md` file, and populate it. You can find out the details of licensing [here](https://choosealicense.com/)

> [!WARNING]  
> If you do not include a license, nobody else can copy, distribute, or modify your work without being at risk of take-downs, shake-downs, or litigation. If the work has other contributors, this includes **YOU**. The GitHub Terms of Service allow people to view or fork your code. 

> [!CAUTION]
> If software does not have a license, this generally means that you do not have permission to use, modify, or share the code. Forking and viewing code **does not imply that you are permitted to use, modify or share it**. Your best option is to nicely ask the authors to add a license, by either sending them an email, or opening an Issue on the repo.

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

Notice that now `streamlit` has appeared in `pyproject.toml`! Poetry has also created a file called `poetry.lock`. This file essentially locks in all of your dependencies so someone external can recreate your environment. It is somewhat analogous to the conda `environment.yml` file.

## 3. Packaging up our software <a id="packaging"></a>
Now that the file structure is setup, try running the software with
```bash
streamlit run cancer_prediction/streamlit_app.py
```

You should be able to play around with the app in the browser. In general, `streamlit` is a great way to prototype new applications. Try training a model using the training data - give it a name like `cancer_model_v2`. Then try running inference on this model with the testing data.

### 3.1. Building a CLI
We want to be as versatile as possible with our software package. We want it to be relatively easy to use, but also flexible enough so that people can develop on top of it, or modify it. We want people to be able to just run it easily from the command line. We create a new folder inside `cancer_prediction` called `cli`. We also create a new `__init__.py` file and copy over the `app.py` file. The init file should contain only:
```python
from .app import app

__all__ = ["app"]
```

We also have to add the `typer` library. We want someone to be able to do:
```bash
pip install cancer-prediction
```

and then
```
cancer-prediction run
```

To do this, we first need to define this entry point `run`. Your terminal won't just magically recognize these commands! First we add the following line to `pyproject.toml` below the readme:
```toml
packages = [{include = "cancer_prediction"}]
```

Then we add the following lines
```
[tool.poetry.scripts]
cancer-prediction =  "cancer_prediction.cli:app"
```

This provides us with an entry point to the `cli/app.py` file.

Now we can install a local copy of our package which mimics a pip installation:

```bash
poetry install
```