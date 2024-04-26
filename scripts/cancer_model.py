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
