# Packaging and Publishing Workshop

There are three branches to this repo:

- `main` contains the slides and starting code, plus some details about how to work through the material.
- `basic` contains the basic starting code, and nothing else.
- `result` contains the final product, that you should hopefully put together yourself.

## Contents
1. [Setting up Codespaces](#codespaces)\
    1.1. [Create a new branch](#codespaces-branch)
2. [An overview of the project](#overview)
3. [Setting up Poetry](#poetry)\
    3.1. [File structure](#poetry-files)\
    3.2. [Licensing](#poetry-licensing)
4. [Packaging up our software](#packaging)

## 1. Setting up Codespaces <a id="codespaces"></a>
The first step is to create a new repository in your GitHub called `cancer-prediction`. Now head over to the `accelerate/packaging-publishing` repo, switch to the basic branch, and download a zip of the code.

Now head back over to your newly created repo and open Codespaces:

![](imgs/createcodespace.png)

You should now be in the browser version of VSCode. Unzip the folder you just downloaded, and drag it into the VSCode file explorer.

This is the absolute most basic version of code being submitted to GitHub. But we can do better...

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
 `/workspaces/cancer-prediction/venv/bin/python`

We install the dependencies using
```bash
python -m pip install -r requirements.txt
```

Notice that in the version control tab, we have over 1,000 unstaged changes!! If we have a look at these, they are mostly files from the virtual environment. We do NOT want to push these to our repo. So we create a `.gitignore`, and populate it with boiler plate text. If you have Copilot, it will do it for you, or you can copy the one [here](https://gist.github.com/rkdan/d082859a7479ba766f7dd32f3925c9ea).

Once you update, all the additional files should vanish from the staging area.

We will also create a `README.md`, and a `LICENSE` file. You can get the text here Once this is done, commit the changes, and sync the remote version with the local version.

Now create a new branch using the UI or using the git CLI.
```bash
git checkout -b dev
```
This will automatically create and move over to a new branch called `dev`. The environment and all the packages we installed should also be moved along with it.

In the source control tab, hit "Publish Branch".

## 2. An overview of the project <a id="overview"></a>
Deploying Jupyter notebooks either to production environments or for large scale simulations or machine learning optimization is impractical. Instead, it makes sense to convert all of our notebook code into python scripts. The end goal is to be able to run our code from the command line, or import the code into other python scripts or notebooks.

In general, when writing code in Notebooks, you should still stick to good programming habits: use appropriate variable names; write functions and classes where appropriate; document those classes and functions; add comments where appropriate. We should aim to have *self-documenting code* - i.e. it should be obvious what a particular function does, and comments are only added when absolutely needed to provide clarity.

The overall structure of this project initially should look like this:
```
cancer-prediction
├── data
│   ├── breast_cancer_test.csv
│   ├── breast_cancer_train.csv
│   └── breast_cancer.csv
├── models
│   └── cancer_model.pkl
├── scripts
│   ├── app.py
│   ├── cancer_model.py
│   └── streamlit_app.py
├── .gitignore
├── notebook.ipynb
├── README.md
└── requirements.txt
```

Have a look through the `notebook.ipynb` file. It is a basic starting point for a simple ML pipeline to perform cancer prediction.

Make a small change to one of the files (add a comment or remove a comment or something). Now head over to the version control tab, and add your file to the staging area, input a comment, and hit commit, and then publish branch. A dropdown box will appear - select *your* version, not the upstream version.

### 2.1. The transition from notebooks to python files

The goal is to package up this notebook into a form that can achieve two things:

1. It can be run from the command line with simple commands. If our software is quite complicated and we need to write slurm scripts to run them on the HPC, this can be handy.
2. It needs to be importable so others can build on top of it easily.

Let's look at the files:

`cancer_model.py`\
Here we have taken the most important parts of our notebook and constructed a `CancerModel` class. It will automatically perform hyperparameter optimization and fit the best model, as well as saving it. We also have the option to load a saved model, make predictions and get feature importances.

People who want to build on this model would be able to import this and this alone.

`streamlit_app.py`\
This is a basic user interface (UI) that builds a basic frontend for the model. I highly recommend streamlit as a way to quickly prototype applications.

`app.py`\
The part of the software that makes it possible to run the streamlit application from the command line. It is worth becoming familiar with Typer.

You can try out the app by running `streamlit run scripts/streamlit_app.py` in the command line.

This code is now at the level where we feel comfortable with having it public. But notice that our CLI won't work, people can't import it, there is no testing, and we don't know what version of python we are using! Let's start getting serious now.

## 3. Setting up Poetry <a id="Poetry"></a>
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

### 3.1. File structure <a id="poetry-files"></a>
Let's create the file directories according to the structure below. Don't worry if the order of the files and folders isn't the same. And don't worry about the additional files and folders that are just part of the course.
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

### 3.2. Licensing <a id="poetry-licensing"></a>
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

## 4. Testing
Now that the file structure is setup, try running the software with
```bash
streamlit run cancer_prediction/streamlit_app.py
```

When you reach a point that everything seems to be working, it's probably a good idea to commit your changes...

We'll now introduce some basic tests just to get an idea for how testing works. In the `cancer_model.py` file, there is a class method called `diagnosis_to_target()`, and another class method called `target_to_diagnosis()`. We will write a test for these.

Add a new file in the `test` directory called `test_CancerModel.py`. Import `unittest` and the relevant modules. We typically have a single test class for each actual class, and then test each method within the test class. This maintains cohesion on a class level. You can then have different test files for different actual files. So we start these tests like so:

```python
class TestCancerModel(unittest.TestCase):
```

Try writing test cases for these two methods. Think about how you would run this method in a Jupyter Notebook.

<details>
<summary>Click to reveal the answer</summary>

```python
import unittest

from cancer_prediction.cancer_model import CancerModel


class TestCancerModel(unittest.TestCase):

    def test_diagnosis_to_target(self):
        model = CancerModel()
        diagnosis = 'Malignant'
        target = model.diagnosis_to_target(diagnosis)
        self.assertEqual(target, 0)

        diagnosis = 'Benign'
        target = model.diagnosis_to_target(diagnosis)
        self.assertEqual(target, 1)

    def test_target_to_diagnosis(self):
        model = CancerModel()
        target = 0
        diagnosis = model.target_to_diagnosis(target)
        self.assertEqual(diagnosis, 'Malignant')

        target = 1
        diagnosis = model.target_to_diagnosis(target)
        self.assertEqual(diagnosis, 'Benign')

if __name__ == '__main__':
    unittest.main()

```
</details>

To run the tests, we click on the "Testing" tab on the sidebar, and then "Configure Python Tests". The order of clicks is as follows:

`unittest` -> `tests` -> `test_*.py`

This selects what type of testing framework to use, where the tests are located and what naming convention we have used for the files.

Now that the tests have run succesfully, it's time to commit and push the changes.

But it's annoying to have to run these tests everytime...surely we can automate it...

## Precommits
We can auto format all of our files using 4 packages:

- `black` - [Black](https://black.readthedocs.io/en/stable/) enforces code formatting compliant with [PEP 8](https://peps.python.org/pep-0008/) such as line lengths, indentation, blank lines, etc.
- `flake8` - [Flake8](https://flake8.pycqa.org/en/latest/index.html#) checks for style and syntax errors. Usually used in conjunction with `black`.
- `mypy` - [mypy](https://mypy.readthedocs.io/en/stable/) checks for typing errors, will help find potential problems with passing incorrect types, when type hints have been added in accordance with [PEP 484](https://peps.python.org/pep-0484/).
- `isort` - [isort](https://pycqa.github.io/isort/) sorts your imports appropriately.

In order to ensure code consistency, we will run these checks every time we make a commit. This can be annoying, but it is for our own good!

We first add pre-commit to the dev group:
```bash
poetry add --dev pre-commit
```

Add a file in the root directory called `.pre-commit-config.yaml` and add the following content:

```
repos:
- repo: https://github.com/psf/black
  rev: 24.3.0
  hooks:
  - id: black
- repo: https://github.com/PyCQA/flake8
  rev: 7.0.0
  hooks:
  - id: flake8
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.9.0
  hooks:
  - id: mypy
- repo: https://github.com/PyCQA/isort
  rev: 5.13.2
  hooks:
  - id: isort
```

We also add the following to the `pyproject.toml` file:
```
[tool.black]
line-length = 88
```

Create another file called `.flake8` and add
```
[flake8]
max-line-length = 88
```
I know...it's annoying that we can't do this in the toml file.

Now try and stage and commit your changes. You should get a pop up saying some stuff has failed. `black` will have altered some files, and `flake8` is probably complaining about something. Make the changes and restage and recommit. Hopefully you should see:

```
black....................................................................Passed
flake8...................................................................Passed
mypy.....................................................................Passed
isort....................................................................Passed
```

## Automated Testing

> [!NOTE]  
> Why don't we just include testing int he pre-commit hook? Pre-commit hooks are supposed to be fast and local. Automated tests and other automated workflows are more comprehensive, and can take longer to run. Separating them out allows you to separate interests and keep small changes fast.

Now we are making some progress, but we should try to automate testing everytime we push changes to the dev branch.

First create a new file in the root
```bash
touch .github/workflows/tests.yml
```

Now add the following text:
```
name: Run Tests
# Whenever code is pushed to dev and when a PR is merged from dev to main
# run all the jobs
on:
  push:
    branches: [dev]
  pull_request:
    branches: [main]
    types: [closed]

jobs:
  # Just have one job called "tests"
  tests:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pipx install poetry
        poetry install
    - name: Run tests
      run: |
        poetry run python -m unittest discover tests/
```

Let's break something, to make sure this works. In your `test_target_to_diagnosis()` method, swap the 1 and the 0 around...

```
Run poetry run python -m unittest discover tests/
.F
======================================================================
FAIL: test_target_to_diagnosis (test_CancerModel.TestCancerModel)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/cancer-prediction/cancer-prediction/tests/test_CancerModel.py", line 22, in test_target_to_diagnosis
    self.assertEqual(diagnosis, "Malignant")
AssertionError: 'Benign' != 'Malignant'
- Benign
+ Malignant


----------------------------------------------------------------------
Ran 2 tests in 0.000s

FAILED (failures=1)
Error: Process completed with exit code 1.
```

Great!, It's working! Since we have gone to the effort to use these tools, we should include them in the `README.md`. You can add the following:

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
![Test status](https://github.com/rkdan/cancer-prediction/actions/workflows/tests.yml/badge.svg?branch=dev)

While, we're at it, we will also run the pre-commit on a push action. We have three

<details>
<summary>Click to reveal the full workflow</summary>

```
name: Run Tests

on:
  push:
    branches: [dev]
  pull_request:
    branches: [main]
    types: [closed]

jobs:
  pre-commit:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - name: Install poetry
      run: pipx install poetry
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'poetry'
    - run: poetry install
    - name: Run pre-commit checks
      run: |
        poetry run pre-commit run --all-files

  tests:
    needs: pre-commit
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - name: Install poetry
      run: pipx install poetry
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'poetry'
    - run: poetry install
    - name: Run tests
      run: |
        poetry run python -m unittest discover tests/

```
</details>


## Publishing
We now essentially have a package ready to distribute.

### Pull Requests
First we will make a pull request to merge changes from dev to main. Head over to the repo and click on Pull requests. Submit a new PR. Make sure the base is main, and the compare is dev. Then create pull request

### Publish to PyPy
We will only publish to TestPyPi. First set up an account with [TestPyPi](https://test.pypi.org/). You will need to enable 2FA with an authenticator app.

Now run

```
poetry build
```

This will create two packages in thr `dist/` folder:

```
cancer_prediction-0.1.0-py3-none-any.whl
cancer_prediction-0.1.0.tar.gz
```

This are your distributable files. By default they will be included in the `.gitignore`, but you can remove them if you want people to be able to download development versions of your software.

Run
```
poetry config repositories.test-pypi https://test.pypi.org/legacy/
```

Create a new API Token in PyPi, and then run
```
poetry config pypi-token.test-pypi <your-token>
```

Finally, run
```
poetry publish -r test-pypi
```
You can now look at your TestPyPi projects and it should be there! To check it has all worked, we deactivate the current environment and create a new one:
```bash
python3.10 -m venv venvTest
. venvTest/bin/activate
```

You can verify the path of the python version you are using by running
```bash
which python
```
and this should return something like:\
 `/workspaces/cancer-prediction/venvTest/bin/python`

We install the dependencies in the new environment using
```bash
python -m pip install -r requirements.txt
```
We have to do this, because if you try to install a package from TestPyPi which has dendencies that are NOT hosted on TestPyPi, the installation will fail.

Now install your new package, and try out the `cancer-prediction run` command.

Boom. Done. The process for publishing to PyPi is pretty similar.

# Automate the publishing process

OK so we're not done yet. Now we will create a workflow that will publish a new version to TestPyPi when a PR is merged with `main`. This is a little more complicated. How can we provide maximum protection? We will have two workflows: one for `dev`, one for `main`. The breakdown might look like this:

__Workflow 1 - push to `dev`__:
```mermaid
graph LR;
    A[pre-commit checks]-->B[fast tests];
```

__Workflow 2 - Merge PR to `main`__:
```mermaid
graph LR;
    A[pre-commit checks]-->B[fast tests];
    B[fast tests]-->C[slow tests];
    C[slow tests]-->D[build];
    D[build]-->E[publish]
```

So you do the fast stuff on your push to `dev` and you do all of that, plus any additional testing before pushing to production. You can add an additional step for tests when a PR is submitted, but this will do for our cases. We don't have any additional slow tests either.

One handing thing you can do in GitHub is enforce "Rulesets". One Ruleset that we can create is protecting the main branch from idiocy - a PR is only allowed to be merged if all status checks are passed.

Now we will create a workflow that will build and publish only when a PR is merged. First we will make sure that our repo has access to the necessary permissions. To do this, go to Settings -> Actions -> General, and allow Read and write permissions. When a new package is published, we can now add a badge!
[![GitHub release](https://img.shields.io/github/v/release/rkdan/cancer-prediction?include_prereleases)](https://GitHub.com/rkdan/cancer-prediction/releases)

### 4.1. Adding a CLI
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

We can now try it out by running
```bash
cancer-prediction run
```

and the streamlit app should open! You should be able to play around with the app in the browser. In general, `streamlit` is a great way to prototype new applications. Try training a model using the training data - give it a name like `cancer_model_v2`. Then try running inference on this model with the testing data.
