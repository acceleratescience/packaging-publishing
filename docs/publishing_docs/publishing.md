In this course, we will only publish to Test PyPI, but the process is broadly the same for PyPI.

## Create PyPI Account
Head to [Test PyPI](https://test.pypi.org/). Register for a new account. You will probably need to set up Two Factor Authentication (2FA). This is easiest using an app such as Google Authenticator.

Go to 'Account settings', scroll down to Api Tokens, and click on 'Add API Token'. Leave this page open for now, because you will need this token shortly.

## Build your package
Back in VSCode, run
```
poetry build
```

This will create two packages in thr `dist/` folder:
```
cancer_prediction-0.1.0-py3-none-any.whl
cancer_prediction-0.1.0.tar.gz
```

These are your distributable files. By default they will be included in the `.gitignore`, but you can remove them if you want people to be able to download development versions of your software.


## Publish
Copy the API Token you created in Test PyPI, and then run
```
poetry config pypi-token.test-pypi <your-token>
```

Finally, run
```
poetry publish -r test-pypi
```

You can now look in your Test PyPI projects and it should be there! To check it has all worked, we deactivate the current environment and create a new one:
```bash
python3.10 -m venv venvTest
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

We install the dependencies in the new environment using
```bash
python -m pip install -r requirements.txt
```
We have to do this, because if you try to install a package from Test PyPI which has dendencies that are NOT hosted on Test PyPI, the installation will fail.

Now install your new package using `pip`- copy the command from the Test PyPI page for your project, and try out the `cancer-prediction run` command.

It really is that simple. Like Poetry.

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Publishing resources__](../resources/references.md#publishing)

    ---
    Information on PyPI, Test PyPI, Python packaging and publishing with Poetry

</div>