from sklearn.base import BaseEstimator, ClassifierMixin
from dtaidistance import dtw
import numpy as np

class DTWClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, axiswise=True):
        self.axiswise = axiswise
        self.templates_ = []

    def fit(self, X, y):
        """
        X: list of np.ndarrays, each shape (T, D)
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


    def predict_proba(self, X):
            probas = []
            for x in X:
                # Berechne die "Ähnlichkeit" für jedes Template
                distances = []
                for template, label in self.templates_:
                    dist = 0
                    if self.axiswise:
                        for i in range(x.shape[1]):
                            dist += dtw.distance(x[:, i], template[:, i])
                    else:
                        dist = dtw.distance(x.flatten(), template.flatten())
                    distances.append(dist)

                # Inverse der Distanz, um Ähnlichkeit zu bekommen (kleinere Distanz -> höhere Ähnlichkeit)
                eps = 1e-6  # Kleine Zahl, um eine Division durch Null zu vermeiden
                similarities = 1 / (np.array(distances) + eps)

                # Berechne Wahrscheinlichkeiten für jede Klasse
                class_scores = {}
                for i, (_, label) in enumerate(self.templates_):
                    if label not in class_scores:
                        class_scores[label] = 0
                    class_scores[label] += similarities[i]

                # Normalisiere die Scores auf Wahrscheinlichkeiten
                total_score = sum(class_scores.values())
                probas.append([class_scores.get(label, 0) / total_score for label in sorted(class_scores.keys())])

            return np.array(probas)
