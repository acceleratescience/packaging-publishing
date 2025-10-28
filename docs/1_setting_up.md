## Setting up Codespaces
The first step is to fork this repository to your own GitHub account. This will allow you to make changes to the code without affecting the original repository.

Now head back over to your newly created repo. Everything in the `main` repo is not needed, so we do a few things:

**Change the default branch**

- Head to the Repo Settings
- There is a heading called "Default Branch"
- Click on the two arrow icon and change the default branch to `basic`

**Delete the `main` branch**

- Head back to the Code tab
- Locate the branch dropdown and click on the thing to the right of it (it should say `4 branches`)
- Find the `main` branch and delete it

**Rename the `basic` branch to `main`**

- In the same page for the `basic` branch, next to the trash can, click on the three dots
- Click on "Rename branch"
- Change the name to `main`

**Rename the repo**

- Head back over to the Settings tab
- At the top, you can change the name of the repo to whatever you want
- Rename it to `cancer-prediction-<your-crsid>`

Now open Codespaces on `main`:

![](imgs/createcodespace.png)

You should now be in the browser version of VSCode.

This is the absolute most basic version of code being submitted to GitHub. But we can do better...

!!! note

    Even though we are using Codespaces, the general packaging process will still work with regular VSCode on your desktop.

## Create a new branch
It is good practice to do development work on a new branch, but first we should set up a virtual environment and install any dependencies.

Set up the new virtual environment with,
```bash
python3.11 -m venv venv
. venv/bin/activate
```

!!! note

    If you are running this locally, you may not have python3.11. Just use whatever you have.

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

When you see this symbol:

<br>
![Dark Souls Bonfire](../imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }
<br>

it means that you should commit and push your changes to the repository. They indicate key checkpoints in the workshop.

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Set up resources__](resources/references.md#setting-up)

    ---
    Information on Git/GitHub, Codespaces, VSCode

</div>