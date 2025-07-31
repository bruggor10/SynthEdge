from sklearn.base import BaseEstimator, ClassifierMixin
from dtaidistance import dtw
import numpy as np

class DTWClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, axiswise=True):
        self.axiswise = axiswise
        self.templates_ = []

    def fit(self, X, y):
        """
        X: list of np.ndarrays, each shape (T, D) where D = 3 for 3D accel
        y: list of labels (same length as X)
        """
        self.templates_ = list(zip(X, y))
        return self

    def predict(self, X):
        return [self._predict_one(x) for x in X]

    def _predict_one(self, x):
        best_label = None
        best_dist = float('inf')

        for template, label in self.templates_:
            dist = 0
            if self.axiswise:
                for i in range(x.shape[1]):
                    dist += dtw.distance(x[:, i], template[:, i])
            else:
                # Flatten (e.g. T×3 → T*3) if axiswise=False
                dist = dtw.distance(x.flatten(), template.flatten())

            if dist < best_dist:
                best_label = label
                best_dist = dist

        return best_label
