The final stage is to publish the documentation.

Here is the workflow for this:
```yaml
name: documentation
on:
  push:
    branches:
    - main

jobs:
  build-docs:
    needs: tests
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      # Set up dependencies
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'
      - run: python3 -m pip install mkdocs==1.4.2 mkdocstrings==0.21.2 "mkdocstrings[python]>=0.18"

      # Deploy docs
      - name: Deploy documentation
        run: mkdocs gh-deploy --force
```

This simply says: when a push is made to main, publish the documentation.

In addition, since we are using some tools, we should let everyone know! So we can add the following to our `README.md` file:
```html
<div align="center">

  <a href="">[![GitHub release](https://img.shields.io/github/v/release/rkdan/cancer-prediction?include_prereleases)](https://GitHub.com/rkdan/cancer-prediction/releases)</a>
  <a href="">![Test status](https://github.com/rkdan/cancer-prediction/actions/workflows/tests.yml/badge.svg?branch=dev)</a>

</div>

<div align="center">

  <a href="">[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)</a>
  <a href="">[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)</a>
  <a href="">[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)</a>
</div>
```

which should display as the following:
![](../imgs/badges.png)

Before we push these changes, we will configure GitHub Pages so that our documentation will create a url for people to visit. Go to the repo Settings -> Pages, and pick a branch to deploy from, in this case 'gh-pages'. So now when we push these changes and merge them to `main`, the documentation will be published and the badges will be displayed on the README!

!!! tip

    You can in principle delete the 'dev' branch whenever you build your package. But if for whatever reason you decide to keep it, be sure to do the following
    ```bash
    git checkout dev
    git fetch origin
    git merge origin/main
    ```

    This will ensure that the 'dev' branch is up to date with the 'main' branch. Do this BEFORE you make any changes to the 'dev' branch, otherwise you have to merge the changes manually.