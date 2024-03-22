## An overview of the project
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

Have a look through the [`notebook.ipynb` file](https://github.com/acceleratescience/packaging-publishing/blob/main/notebook.ipynb). It is a basic starting point for a simple ML pipeline to perform cancer prediction.

## The transition from notebooks to python files
The goal is to package up this notebook into a form that can achieve two things:

1. It can be run from the command line with simple commands. If our software is quite complicated and we need to write slurm scripts to run them on the HPC, this can be handy.
2. It needs to be importable so others can build on top of it easily.

Let's look at the files:

### `cancer_model.py`
Here we have taken the most important parts of our notebook and constructed a `CancerModel` class. It will automatically perform hyperparameter optimization and fit the best model, as well as saving it. We also have the option to load a saved model, make predictions and get feature importances.

<details>
<summary>Click to see the code</summary>

```python
import warnings

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

import pickle


class CancerModel:
    """A class to represent a cancer diagnosis prediction model.
    """
    def __init__(self):
        self.model = None
        self.pca = None
        self.scaler = None
        self.feature_names = None


    def __str__(self) -> str:
        return 'CancerModel'


    def fit(self, X : np.ndarray | pd.DataFrame, y : np.ndarray | pd.DataFrame) -> None:
        """Fit the model to the given data.

        Args:
            X (np.ndarray | pd.DataFrame): The features
            y (np.ndarray | pd.DataFrame): The diagnosis target
        """
        pipe = Pipeline([
            ('scaler', StandardScaler()),
            ('pca', PCA()),
            ('model', LogisticRegression())
        ])

        param_grid = {
            'pca__n_components': np.arange(1, 31),
            'model__C': np.logspace(-3, 1, 100)
        }

        grid = GridSearchCV(pipe, param_grid, cv=5, n_jobs=-1, scoring='accuracy', verbose=1)
        grid.fit(X, y)

        self.model = grid.best_estimator_
        self.model.fit(X, y)
        self.pca = self.model.named_steps['pca']
        self.scaler = self.model.named_steps['scaler']
        self.feature_names = self.model.feature_names_in_


    def save(self, path: str) -> None:
        """Save the model to the given path.

        Args:
            path (str): The path to save the model to.
        """
        # unsure that feature_names can be retrieved after loading the model
        with open(path, 'wb') as file:
            pickle.dump(self.model, file)


    def load(self, path: str) -> None:
        """Load the model from the given path.

        Args:
            path (str): The path to load the model from.
        """
        with open(path, 'rb') as file:
            self.model = pickle.load(file)
            self.pca = self.model.named_steps['pca']
            self.scaler = self.model.named_steps['scaler']
            self.feature_names = self.model.feature_names_in_


    def target_to_diagnosis(self, target: int) -> str:
        """Convert the target to a diagnosis.

        Args:
            target (int): The target value (0 or 1)

        Returns:
            str: The diagnosis (Malignant or Benign)
        """
        return 'Malignant' if target == 0 else 'Benign'
    

    def diagnosis_to_target(self, diagnosis: str) -> int:
        """Convert the diagnosis to a target.

        Args:
            diagnosis (str): The diagnosis (Malignant or Benign)

        Returns:
            int: The target value (0 or 1)
        """
        return 0 if diagnosis == 'Malignant' else 1


    def predict(self, X: np.ndarray | pd.DataFrame) -> list[tuple[str, float]]:
        """Make a prediction for the given features.

        Args:
            X (np.ndarray | pd.DataFrame): The features

        Returns:
            list[tuple[str, float]]: A list of tuples containing the diagnosis and the confidence
        """
        predictions = self.model.predict(X)
        diagnoses = [self.target_to_diagnosis(p) for p in predictions]
        probs = self.model.predict_proba(X)
        # get the corresponding probabilities
        diagnoses_confidence = []
        for i, pred in enumerate(predictions):
            diagnosis = diagnoses[i]
            prob = round(probs[i][pred], 2)
            diagnoses_confidence.append((diagnosis, prob))

        return diagnoses_confidence


    def predict_proba(self, X: np.ndarray | pd.DataFrame) -> np.ndarray:
        """Make a prediction for the given features.

        Args:
            X (np.ndarray | pd.DataFrame): The features

        Returns:
            np.ndarray: The probabilities of the predictions
        """
        return self.model.predict_proba(X)
    

    def accuracy(self, X: np.ndarray | pd.DataFrame, y: np.ndarray | pd.DataFrame) -> float:
        """Calculate the accuracy of the model on the given data.

        Args:
            X (np.ndarray | pd.DataFrame): The features
            y (np.ndarray | pd.DataFrame): The diagnosis target

        Returns:
            float: The accuracy of the model
        """
        return self.model.score(X, y)


    def get_feature_importance(self):
        return self.pca.components_


    def get_feature_variance(self):
        return self.pca.explained_variance_ratio_


    def get_feature_importance_df(self, X):
        feature_importance = self.get_feature_importance()
        feature_variance = self.get_feature_variance()

        feature_importance_df = pd.DataFrame(feature_importance, columns=self.feature_names)
        feature_importance_df['variance'] = feature_variance
        return feature_importance_df


    def get_feature_importance_df_sorted_by_variance_and_variance(self, X):
        feature_importance_df = self.get_feature_importance_df(X)
        return feature_importance_df['variance'].sort_values(ascending=False)

```
</details>

People who want to build on this model would be able to import this and this alone.

### `streamlit_app.py`
This is a basic user interface (UI) that builds a basic frontend for the model. I highly recommend streamlit as a way to quickly prototype applications.

<details>
<summary>Click to see the code</summary>

```python
import os
import pickle

import numpy as np
import pandas as pd
import streamlit as st

from cancer_model import CancerModel

st.set_page_config(page_title='Cancer Diagnosis Prediction', layout='wide')

MODELS_DIR = 'models'

def list_saved_models(directory):
    """List all '.pkl' files in the given directory."""
    return [file for file in os.listdir(directory) if file.endswith('.pkl')]

@st.cache_resource
def load_model(path='cancer_model.pkl') -> CancerModel:
    model = CancerModel()
    model.load(path)
    return model

def train_and_save_model(train_data, filename='cancer_model.pkl'):
    model = CancerModel()
    filename = os.path.join(MODELS_DIR, filename)
    X = train_data.drop('target', axis=1)
    y = train_data['target']
    model.fit(X, y)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    model.save(filename)
    return model

st.title('Cancer Diagnosis Prediction')

# Sidebar for navigation
app_mode = st.sidebar.selectbox("Choose an option", ["Home", "Train a new model", "Load model and predict", "Manual data entry for prediction"])

if app_mode == "Home":
    st.write("Welcome to the Cancer Diagnosis Prediction Application. Use the sidebar to navigate through the application.")

elif app_mode == "Train a new model":
    st.header("Train a new model")
    uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type="csv")
    model_name = st.text_input("Enter a name for your model (without extension)", value="cancer_model")

    if uploaded_file is not None and model_name:
        data = pd.read_csv(uploaded_file)
        if st.button('Train Model'):
            # Append .pkl extension if not provided
            if not model_name.endswith('.pkl'):
                model_name += '.pkl'
            train_and_save_model(data, model_name)
            st.success(f'Model "{model_name}" trained and saved successfully.')


if app_mode == "Load model and predict" or app_mode == "Manual data entry for prediction":
    st.header("Select a model for prediction")
    model_files = list_saved_models(MODELS_DIR)
    selected_model_file = st.selectbox("Select a model file", model_files)
    path = os.path.join(MODELS_DIR, selected_model_file)
    model = load_model(path)
    
    if app_mode == "Load model and predict":
        uploaded_file = st.file_uploader("Upload your dataset for prediction (CSV format)", type="csv")
        if uploaded_file is not None:
            test_data = pd.read_csv(uploaded_file)
            predictions, accuracy = model.predict(test_data.drop('target', axis=1)), model.accuracy(test_data.drop('target', axis=1), test_data['target'])
            st.write("Predictions:", predictions)
            st.write("Accuracy:", accuracy)
            
    elif app_mode == "Manual data entry for prediction":
        st.header("Manual data entry for prediction")
        
        # Define your features names here based on the model's training dataset
        feature_names = model.feature_names  # Replace these with actual feature names

        # Create a dictionary to store user inputs
        input_data = {}
        
        # Dynamically generate input fields for each feature
        for feature in feature_names:
            # You might want to customize the `step` parameter based on the feature's data type and expected range
            input_data[feature] = st.number_input(f"Enter {feature}:", step=0.01)

        if st.button('Predict'):
            # Prepare the data for prediction (ensure it matches the model's expected input format)
            input_df = pd.DataFrame([input_data])
            
            # Perform the prediction
            prediction = model.predict(input_df)
            
            # Display the prediction result
            st.write(f"Prediction: {prediction[0][0]} with confidence: {prediction[0][1]}")

```
</details>

### `app.py`
The part of the software that makes it possible to run the streamlit application from the command line. It is worth becoming familiar with Typer.

<details>
<summary>Click to see the code</summary>

```python
import sys

import typer
from cancer_prediction import streamlit_app
from streamlit.web import cli as stcli

app = typer.Typer()

@app.command()
def __version__():
    # Print the version of the app
    typer.echo("0.1.0")

@app.command()
def run():
    sys.argv = ["streamlit", "run", "cancer_prediction/streamlit_app.py"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    app()
```
</details>

You can try out the app by running `streamlit run scripts/streamlit_app.py` in the command line.

This code is now about as basic as you want to go. But notice that we have some problems:

- We can't run it from the command line (our CLI won't work).
- People can't import it.
- There is no testing.
- Although we have some dependencies, don't even know what version of python we are using!

Let's start getting serious.

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Project overview resources__](resources/references.md#overview)

    ---
    Information on Scikit Learn, Streamlit, and Typer

</div>