## Setting up Codespaces
The first step is to create a new repository in your GitHub called `cancer-prediction`. Now head over to the `accelerate/packaging-publishing` repo, switch to the basic branch, and download a zip of the code.

Now head back over to your newly created repo and open Codespaces:

![](imgs/createcodespace.png)

You should now be in the browser version of VSCode. Unzip the folder you just downloaded, and drag it into the VSCode file explorer.

This is the absolute most basic version of code being submitted to GitHub. But we can do better...

!!! note

    Even though we are using Codespaces, the general packaging process will still work with regular VSCode on your desktop.

## Create a new branch
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

Notice that in the version control tab, we have over 1,000 unstaged changes!! If we have a look at these, they are mostly files from the virtual environment. We do NOT want to push these to our repo. So we create the three core files we need: a `.gitignore`, a `LICENSE`, and a `README.md`, either using the UI or by typing in the terminal:

```bash
touch .gitignore LICENSE README.md
```

and populate it with boiler plate text. If you have Copilot, it will do it for you, or you can copy the one [here](https://gist.github.com/rkdan/d082859a7479ba766f7dd32f3925c9ea).

Once you update, all the additional files should vanish from the staging area. Once this is done, commit the changes, and sync the remote version with the local version.

Now create a new branch using the UI or using the git CLI.
```bash
git checkout -b dev
```

This will automatically create and move over to a new branch called `dev`. The environment and all the packages we installed should also be moved along with it.

In the source control tab, hit "Publish Branch".

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Set up resources__](resources/references.md#setting-up)

    ---
    Information on Git/GitHub, Codespaces, VSCode

</div>