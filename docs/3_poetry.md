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

!!! warning

    If you do not include a license, nobody else can copy, distribute, or modify your work without being at risk of take-downs, shake-downs, or litigation. If the work has other contributors, this includes **YOU**. The GitHub Terms of Service allow people to view or fork your code. 

!!! warning

    If software does not have a license, this generally means that you do not have permission to use, modify, or share the code. Forking and viewing code **does not imply that you are permitted to use, modify or share it**. Your best option is to nicely ask the authors to add a license, by either sending them an email, or opening an Issue on the repo.

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