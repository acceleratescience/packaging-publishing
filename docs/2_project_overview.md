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