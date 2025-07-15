import joblib
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
# import pandas as pd

class ModelManager:
    def __init__(self, model_type='rf_reg', degree = 1,  **kwargs):
        """
        Initialisiert das Modell. Unterstützte Typen: 'mlp', 'rf', 'svm'
        kwargs: Zusätzliche Parameter für das Modell
        """
    #     AVAILABLE_MODELS = {
    #     "mlp": MLPClassifier,
    #     "rf": RandomForestClassifier,
    #     "knn": KNeighborsClassifier,
    #     "svm": SVC,
    #     "logreg": LogisticRegression,
    #     # Regressoren:
    #     "lin_reg": LinearRegression,
    #     "mlp_reg": MLPRegressor,
    #     "rf_reg": RandomForestRegressor,
    #     "knn_reg": KNeighborsRegressor,
    #     "svr": SVR,
    # }
        self.is_trained = False
        self.is_running = False
        self.model_type = model_type
        self.degree = degree
        self.model = self._create_model(**kwargs)

    def _create_model(self, **kwargs):
        """
        Erstellt ein Pipeline-Modell mit optionalem Preprocessing.
        """
        if self.model_type == 'mlp':
            model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, **kwargs)
        elif self.model_type == 'rf':
            model = RandomForestClassifier(n_estimators=100, **kwargs)
        elif self.model_type == 'svm':
            model = SVC(probability=True, **kwargs)

            # === Regressors ====
        elif self.model_type == 'rf_reg':
            model = RandomForestRegressor(n_estimators=100, max_depth=None, random_state=42)
        elif self.model_type == 'lin_poly_reg':
            model = LinearRegression(degree = 2, **kwargs)
        elif self.model_type == 'mlp_reg':        
            model = MLPRegressor(
            hidden_layer_sizes=(20,),     # kleineres Netz (z. B. 20 Neuronen)
            activation='tanh',            # glattere Aktivierung bei wenig Daten
            solver='lbfgs',               # besser bei kleinen, dichten Datensätzen
            alpha=0.001,                  # etwas stärkere Regularisierung
            max_iter=1000,                # mehr Iterationen zur Sicherheit
            random_state=42
        )
        elif self.model_type == 'svr':
            model = SVR(
            kernel='rbf',       # oder 'linear', 'poly', 'sigmoid'
            C=1.0,              # Regularisierung (höher = weniger Fehler erlaubt)
            epsilon=0.1,        # Toleranzzone, in der Fehler nicht bestraft werden
            gamma='scale'       # Wie stark sich einzelne Punkte auf die Form auswirken
        )
        else:
            raise ValueError(f"Unbekannter Modelltyp: {self.model_type}")
        
        # Pipeline mit StandardScaler
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('poly', PolynomialFeatures(degree=self.degree)),
            ('model', model)
        ])
        return pipeline

    def train(self, X, y):
        """
        Trainiert das Modell mit Trainingsdaten.
        :param X: Feature-Matrix (z. B. numpy.ndarray)
        :param y: Zielwerte
        """
        self.model.fit(X, y)
        self.is_trained = True
        print("Training completed")

    def predict(self, X):
        """
        Gibt Vorhersagen für neue Eingabedaten zurück.
        :param X: Eingabedaten (z. B. ein einzelner Vektor oder Batch)
        :return: Vorhergesagte Klassenlabels
        """
        return self.model.predict(X)

    # def predict_proba(self, X):
    #     """
    #     Gibt Wahrscheinlichkeiten der Klassen zurück (falls unterstützt).
    #     """
    #     if hasattr(self.model.named_steps['model'], 'predict_proba'):
    #         return self.model.predict_proba(X)
    #     else:
    #         raise NotImplementedError("Dieses Modell unterstützt keine Wahrscheinlichkeiten.")

    # def save_model(self, filepath):
    #     """
    #     Speichert das Modell als .joblib-Datei.
    #     """
    #     joblib.dump(self.model, filepath)

    # def load_model(self, filepath):
    #     """
    #     Lädt ein Modell aus einer .joblib-Datei.
    #     """
    #     self.model = joblib.load(filepath)
