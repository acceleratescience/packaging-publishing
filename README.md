# Packaging and Publishing Workshop

There are two branches to this repo:

- `main` contains the starting code that you will fork over to your repo.
- `result` contains the final product, that you should hopefully put together yourself.

The first step is to fork the main branch and open Codespaces!

## Setting up Poetry
A fresh poetry project can be initialized from a blank directory, or from a directory with pre-existing code and an environment. First we will make sure we have the correct dependencies. In the terminal create a new environment:

```bash
python3.10 -m venv venv
. venv/bin/activate
```
We install the dependencies using
```bash
python -m pip install -r requirements.txt
```

Now we create a Poetry project within our current folder