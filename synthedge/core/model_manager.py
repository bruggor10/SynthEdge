import joblib
# Klassifikatoren
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# Regressoren
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

# Preprocessing & Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline


class ModelManager:
    def __init__(self, **kwargs):
        """
        Initialisiert das Modell. Unterstützte Typen: Classifiers: 'mlp', 'rf', 'svm'. Regressoren: 'lin_reg', 'mlp_reg', 'rf_reg', 'svr'
        kwargs: Zusätzliche Parameter für das Modell
        """
        self.AVAILABLE_CLASSIFIERS = {
        # Klassifikatoren
        "mlp": "MLPClassifier",
        "rf": "RandomForestClassifier",
        "knn": "KNeighborsClassifier",
        "svm": "SVC"
        }
        self.AVAILABLE_REGRESSORS = {
        # Regressoren
        "lin_poly_reg": "Linear(Polynomial)Regression", 
        "mlp_reg": "MLPRegressor",
        "rf_reg": "RandomForestRegressor",
        "svr": "SVR"
        }
    
        self.is_trained = False
        self.is_running = False
        self.degree = 1
        # self.model = self._create_model(**kwargs)

    def configure_model(self, model_type, **kwargs):
        self.model_type = model_type
        self.model = self._create_model(**kwargs)
        print("Configuring model: "+self.model_type)
        self.is_trained = False

    def _create_model(self, **kwargs):
        """
        Erstellt ein Pipeline-Modell mit optionalem Preprocessing.
        """
        # === Classifiers ===
        
        if self.model_type == 'mlp':
            default_params = {
                'hidden_layer_sizes':(20,),     # kleineres Netz → weniger Overfitting
                'activation':'tanh',            # glattere Aktivierungsfunktion bei kleinen Daten sinnvoll
                'solver':'lbfgs',               # sehr gut für kleine Datenmengen (konvergiert stabil)
                'alpha':0.01,                   # stärkere Regularisierung hilft gegen Overfitting
                'max_iter':500,                 # mehr Iterationen bei kleinerem Netz okay
                'early_stopping':False,         # nicht nötig bei `solver:'lbfgs'`
                'random_state':42
            }
            # print("mlp created")
            params = {**default_params, **kwargs}
            model = MLPClassifier(**params)

        elif self.model_type == 'rf':
            default_params = {
                'n_estimators':100,           # Anzahl der Bäume im Wald; 100 ist ein robuster Standardwert
                'max_depth':10,               # Maximale Tiefe der Bäume; hilft, Overfitting zu verhindern
                'min_samples_split':4,        # Ein Knoten wird nur gesplittet, wenn er ≥ 4 Samples enthält
                'min_samples_leaf':2,         # Jeder Blattknoten muss mindestens 2 Samples enthalten → glattere Trennung
                'max_features':'sqrt',        # Anzahl der Merkmale pro Split: 'sqrt' ist Standard für Klassifikation
                'bootstrap':True,             # Ziehung mit Zurücklegen für jeden Baum → mehr Varianz im Wald
                'oob_score':True,             # Nutzt Out-of-Bag-Samples zur internen Validierung (nur bei bootstrap:True)
                'class_weight':'balanced',    # Automatische Gewichtung der Klassen bei unbalancierten Daten
                'random_state':42             # Für reproduzierbare Ergebnisse
            }
            # print("rf created")
            params = {**default_params, **kwargs}
            model = RandomForestClassifier(**params)
            
        elif self.model_type == 'svm':
            default_params = {
                'C':1.0,  					# Regulierungsterm. Höhere Werte → weniger Regularisierung (mehr Overfitting möglich). Kleinere Werte → stärkerer Regularisierungseffekt.
                'kernel':'rbf',  				# Kernel-Funktion. Gängige Werte: 'linear', 'poly', 'rbf', 'sigmoid'.
                'gamma':'scale', 				# Steuert die Reichweite des Einflusses einzelner Trainingspunkte bei 'rbf', 'poly' und 'sigmoid'. Höheres Gamma → engerer Einflussbereich → mögliches Overfitting.
                'class_weight':'balanced',	# Für unbalancierte Datensätze wichtig. 'balanced' passt Gewichte automatisch an Klassenverteilung an.
                'probability':True 			#Wenn True, berechnet das Modell Wahrscheinlichkeiten (predict_proba). Verlangsamt das Training.
            }
            params = {**default_params, **kwargs}
            model = SVC(**params)

        elif self.model_type == 'knn':
            default_params = {
                'n_neighbors':5,				# Anzahl der Nachbarn (k)
                'weights':'uniform',			# oder 'distance' (gewichtete Nachbarn)
                'metric':'minkowski',			# Standard ist Minkowski (p:2 → euklidisch)
                'p':2							# Parameter für Minkowski-Metrik
            }
            params = {**default_params, **kwargs}
            model = KNeighborsClassifier(**params)

            # === Regressors ====
        elif self.model_type == 'rf_reg':
            default_params = {
                'n_estimators':100,           # Anzahl der Bäume im Wald; 100 ist ein guter Standardwert
                'max_depth':10,               # Maximale Tiefe jedes Baums; verhindert Overfitting bei kleinen Daten
                'min_samples_split':4,        # Ein Knoten wird nur gesplittet, wenn er mindestens 4 Samples enthält
                'min_samples_leaf':2,         # Mindestens 2 Samples müssen in einem Blatt verbleiben → verhindert zu tiefe Blätter
                'max_features':'auto',        # Anzahl der Merkmale, die bei einem Split betrachtet werden
                                            # 'auto' : alle Features bei Regressor (entspricht None in neueren Versionen)
                'bootstrap':True,             # Stichprobe mit Zurücklegen → für Vielfalt in Bäumen
                'oob_score':True,             # Nutze "Out-of-Bag"-Samples zur internen Modellbewertung (nur wenn bootstrap:True)
                'random_state':42             # Setzt den Zufallsgenerator → macht Ergebnisse reproduzierbar
            }
            params = {**default_params, **kwargs}
            model = RandomForestRegressor(**params)
            
        elif self.model_type == 'lin_poly_reg':
            default_params = {
               'degree' : 2 
            }
            params = {**default_params, **kwargs}
            self.degree = params.pop('degree')
            model = LinearRegression(**params)
            
        elif self.model_type == 'mlp_reg':
            default_params = {
                 'hidden_layer_sizes':(20,),     # kleineres Netz (z. B. 20 Neuronen)
                'activation':'tanh',            # glattere Aktivierung bei wenig Daten
                'solver':'lbfgs',               # besser bei kleinen, dichten Datensätzen
                'alpha':0.001,                  # etwas stärkere Regularisierung
                'max_iter':1000,                # mehr Iterationen zur Sicherheit
                'random_state':42
            }
            params = {**default_params, **kwargs}
            model = MLPRegressor(**params)
        elif self.model_type == 'svr':
            default_params = {
                'kernel':'rbf',       # oder 'linear', 'poly', 'sigmoid'
                'C':1.0,              # Regularisierung (höher : weniger Fehler erlaubt)
                'epsilon':0.1,        # Toleranzzone, in der Fehler nicht bestraft werden
                'gamma':'scale',      # Wie stark sich einzelne Punkte auf die Form auswirken
            }
            params = {**default_params, **kwargs}
            model = SVR(**params)

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

    def get_classifiers(self):
        return self.AVAILABLE_CLASSIFIERS.items()
    
    def get_regressors(self):
        return self.AVAILABLE_REGRESSORS.items()

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
