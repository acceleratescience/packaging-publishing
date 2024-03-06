# Packaging and Publishing Workshop

There are two branches to this repo:

- `main` contains the starting code that you will fork over to your repo.
- `result` contains the final product, that you should hopefully put together yourself.

## Setting up Codespaces
The first step is to fork the main branch and open Codespaces!

> [!NOTE]  
> Even though we are using Codespaces, the general packaging process will still work with regular VSCode on your desktop.

![](imgs/fork.png)

This will create a version of the repo in your own GitHub page. Navigate to this repo and then open it in GitHub Codespaces

![](imgs/createcodespace.png)

Now you should be in the browser version of VSCode. It is good practice to do development work on a new branch, but first we should set up a virtual environment and install any dependencies.

```bash
python3.10 -m venv venv
. venv/bin/activate
```
We install the dependencies using
```bash
python -m pip install -r requirements.txt
```

Now create a new branch using the UI or using the git CLI.
```bash
git checkout -b dev
```
This will automatically create and move over to a new branch called `dev`. The environment and all the packages we installed should also be moved along with it.