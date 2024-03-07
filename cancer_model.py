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
    def __init__(self):
        self.model = None
        self.pca = None
        self.scaler = None
        self.feature_names = None

    def __str__(self):
        return 'CancerModel'

    def fit(self, X, y):
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

    def save(self, path):
        # unsure that feature_names can be retrieved after loading the model
        with open(path, 'wb') as file:
            pickle.dump(self.model, file)

    def load(self, path):
        with open(path, 'rb') as file:
            self.model = pickle.load(file)
            self.pca = self.model.named_steps['pca']
            self.scaler = self.model.named_steps['scaler']
            self.feature_names = self.model.feature_names_in_

    def target_to_diagnosis(self, target):
        return 'Malignant' if target == 0 else 'Benign'
    
    def diagnosis_to_target(self, diagnosis):
        return 0 if diagnosis == 'Malignant' else 1

    def predict(self, X):
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

    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def accuracy(self, X, y):
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

def main():

    # Load the data
    train_data = pd.read_csv('data/breast_cancer_train.csv')
    test_data = pd.read_csv('data/breast_cancer_test.csv')
    X = train_data.drop('target', axis=1)
    y = train_data['target']

    # Train the model
    model = CancerModel()
    model.fit(X, y)

    feature_names = model.feature_names

    # print(model.accuracy(X, y))

    # Save the model
    model.save('models/cancer_model.pkl')

    # Load the model
    loaded_model = CancerModel()
    loaded_model.load('models/cancer_model.pkl')

    X = test_data.drop('target', axis=1)
    y = test_data['target']

    # Make predictions
    predictions = loaded_model.predict(X)
    print(predictions)
    print(loaded_model.accuracy(X, y))

    # run a single prediction
    single_prediction = X.iloc[[1]]
    print(loaded_model.predict(single_prediction))

if __name__ == '__main__':
    main()