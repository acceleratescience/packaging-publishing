In this course, we will only publish to Test PyPI, but the process is broadly the same for PyPI.

At this point, your `pyproject.toml` file should look like this:
```toml
[project]
name = "cancer-prediction-<your-CRSId>"
version = "0.1.0"
description = "A basic model to predict cancerous tumors based on certain properties."
authors = [{name = "You Name"}]
requires-python = ">=3.11"
dependencies = [
    "click>=8.3.0",
    "ipykernel>=7.1.0",
    "matplotlib>=3.10.7",
    "numpy>=2.3.4",
    "pandas>=2.3.3",
    "scikit-learn>=1.7.2",
    "streamlit>=1.50.0",
]

[dependency-groups]
dev = [
    "black>=25.9.0",
    "flake8>=7.3.0",
    "isort>=7.0.0",
]


[project.scripts]
cancer-prediction = "cancer_prediction.scripts.app:cli"

[build-system]
requires = ["uv_build>=0.9.5,<0.10.0"]
build-backend = "uv_build"

[tool.uv]
package = true
```

## Create PyPI Account
Head to [Test PyPI](https://test.pypi.org/). Register for a new account. You will probably need to set up Two Factor Authentication (2FA). This is easiest using an app such as Google or Microsoft Authenticator. Note that you will need to use this app when you log in to Test PyPI or PyPI in the future. And given that MFA is prevalent across the university, you should be familiar with this process.

Make sure you also save your recovery codes in a safe place. If you lose access to your 2FA app, you will need these codes to regain access to your account.

!!! note

    At this time, we recommend the use of Google Authenticator, as it allows the transfer of 2FA codes between different operating systems (e.g. Android to iOS). Microsoft Authenticator does not have this feature.

Go to 'Account settings', scroll down to Api Tokens, and click on 'Add API Token'. Leave this page open for now, because you will need this token shortly.

!!! tip

    Create a new file in the root of your project called `.env`, and add the following line to this file:
    ```
    TESTPYPI_API_TOKEN="your-token"
    ```
    Then add `.env` to your `.gitignore` file. This will ensure that your API token is not uploaded to GitHub.

## Build your package
Back in VSCode, run
```
uv build
```

This will create two packages in thr `dist/` folder:
```
cancer_prediction-0.1.0-py3-none-any.whl
cancer_prediction-0.1.0.tar.gz
```

These are your distributable files. By default they will be included in the `.gitignore`, but you can remove them if you want people to be able to download development versions of your software.


## Publish
Load your `.env` file into the shell (so your API token is available) using:
```bash
export $(grep -v '^#' .env | xargs)
```
Run the publish command:
```
uv publish --token "$TESTPYPI_API_TOKEN" --publish-url https://test.pypi.org/legacy/
```

You can now look in your Test PyPI projects and it should be there! To check it has all worked, we deactivate the current environment and create a new one:
```bash
python -m venv venvTest
. venvTest/bin/activate
```

You can verify the path of the python version you are using by running
```bash
which python
```
and this should return something like:
```
/workspaces/cancer-prediction/venvTest/bin/python
```

Just as a sanity check, trying running
```
cancer-prediction run
```

and hopefully zsh (or bash) should not recognize this command.

We install the dependencies in the new environment using (make sure to manually add `streamlit` and `typer` to requirements.txt before running this command)
```bash
python -m pip install -r requirements.txt
```
We have to do this, because if you try to install a package from Test PyPI which has dependencies that are NOT hosted on Test PyPI, the installation will fail.

Now install your new package using `pip`- copy the command from the Test PyPI page for your project, and try out the `cancer-prediction run` command.

It really is that simple.

<br>
![Dark Souls Bonfire](../imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }
<br>

!!! tip
    What happens when we try to publish to PyPI for a second time? We will need to increment the version number in the `pyproject.toml` file. This is because PyPI will not allow you to upload the same version of a package twice.

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Publishing resources__](../resources/references.md#publishing)

    ---
    Information on PyPI, Test PyPI, Python packaging and publishing with uv

</div>