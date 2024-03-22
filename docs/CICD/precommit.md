We start with the pre-commit. This is our first line of defence against simple to correct errors in our code.

## Packages

### `black`
[Black](https://black.readthedocs.io/en/stable/) enforces code formatting compliant with [PEP 8](https://peps.python.org/pep-0008/) enforces code formatting compliant with PEP 8 such as line lengths, indentations, blank lines, etc. It is customizable, so if you don't like certain line length restrictions, you can always change them. You can also tell `black` not to look in certain files, or ignore certain features.

### `flake8`
[Flake8](https://flake8.pycqa.org/en/latest/index.html#) checks for style and syntax errors. Usually used in conjunction with `black`, and you can also tell it to ignore things.

### `mypy`
[Mypy](https://mypy.readthedocs.io/en/stable/) checks for typing errors, will help find potential problems with passing incorrect types, when type hints have been added in accordance with [PEP 484](https://peps.python.org/pep-0484/).

### `isort`
[Isort](https://pycqa.github.io/isort/) sorts your imports appropriately.

In order to ensure code consistency, we will run these checks every time we make a commit. This can be annoying, but it is for our own good!

## Setting up pre-commit
First, we need to make sure we add the required files to our project:
```
poetry add --dev pre-commit black isort flake8 mypy
```

We must now make some changes to our `pyproject.toml` file:

```
[tool.black]
line-length = 88
exclude = '''
/(
      .eggs         
    | .git          
    | .hg
    | .mypy_cache
    | .tox
    | venv
    | _build
    | buck-out
    | build
    | dist
  )/
'''
```

Take it from me, we __DO NOT__ want our tools to try and alter the files in our virtual environment or distributions folders!

Similarly, for `isort`:
```
[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
virtual_env = "venv"
```

Unfortunately, `flake8` can't be configured inside the `pyproject.toml` file, so we have to create a separate file in our root directory called `.flake8`. In it, we add:

```
[flake8]
max-line-length = 88
```

### The pre-commit hook
Now we create a file in the root directory called `.pre-commit-config.yaml`, and add the following:
```yaml
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

## Trying it out
In the command line, we can run
```
poetry run pre-commit run --all-files
```

and we should get the following:
```
black....................................................................Passed
flake8...................................................................Passed
mypy.....................................................................Passed
isort....................................................................Passed
```

If there are any issues, work through them to fix the issues. Similarly when you use the VSCode UI to make a commit, any issues will be picked up.

Now in the `cancer_model.py` file, add the following import statement
```python
import matplotlib.pyplot as plt
```

You should get the following output when you run the pre-commit
```
black....................................................................Passed
flake8...................................................................Failed
- hook id: flake8
- exit code: 1

cancer_prediction/cancer_model.py:4:1: F401 'matplotlib.pyplot as plt' imported but unused

mypy.....................................................................Passed
isort....................................................................Passed
```

Now head into the `streamlit_app.py` file and in the `train_and_save_model() function, for the `filename` argument, change the type to `int`, so it reads:
```python
def train_and_save_model(train_data, filename: int = "cancer_model.pkl"):
```

This is nonsensical, since you are trying to pass a string as argument that should be an `int`! And sure enough, when you run the pre-commit, you get this complaint from `mymp`
```
black....................................................................Passed
flake8...................................................................Passed
mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

cancer_prediction/streamlit_app.py:25: error: Incompatible default for argument "filename" (default has type "str", argument has type "int")  [assignment]
cancer_prediction/streamlit_app.py:27: error: No overload variant of "join" matches argument types "str", "int"  [call-overload]
cancer_prediction/streamlit_app.py:27: note: Possible overload variants:
cancer_prediction/streamlit_app.py:27: note:     def join(str, /, *paths: str) -> str
cancer_prediction/streamlit_app.py:27: note:     def join(str | PathLike[str], /, *paths: str | PathLike[str]) -> str
cancer_prediction/streamlit_app.py:27: note:     def join(bytes | PathLike[bytes], /, *paths: bytes | PathLike[bytes]) -> bytes
cancer_prediction/streamlit_app.py:32: error: No overload variant of "dirname" matches argument type "int"  [call-overload]
cancer_prediction/streamlit_app.py:32: note: Possible overload variants:
cancer_prediction/streamlit_app.py:32: note:     def [AnyStr in (str, bytes)] dirname(p: PathLike[AnyStr]) -> AnyStr
cancer_prediction/streamlit_app.py:32: note:     def [AnyOrLiteralStr in (str, bytes, str)] dirname(p: AnyOrLiteralStr) -> AnyOrLiteralStr
cancer_prediction/streamlit_app.py:33: error: Argument 1 to "save" of "CancerModel" has incompatible type "int"; expected "str"  [arg-type]
Found 4 errors in 1 file (checked 7 source files)

isort....................................................................Passed
```

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__CI/CD - Pre-commit resources__](../resources/references.md#pre-commit)

    ---
    Information on GitHub Actions, Black, Flake8, Mypy, Isort, and Git Hooks

</div>