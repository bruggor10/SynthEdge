import numpy as np
from threading import Lock
from PySide6.QtCore import QObject, Signal

class Recorder(QObject):
    logger = Signal(str)
    def __init__(self, auto_label=True):
        """
        Initialisiert den Recorder.
        :param input_dim: Anzahl der Input-Features pro Datenpunkt
        :param auto_label: Wenn True, wird ein Zähler als Label verwendet
        """
        self.inputs = []
        self.labels = []
        self.current_label = 0
        self.lock = Lock()
        self.auto_label = auto_label
        self.is_recording = False
        super().__init__()

    def add_input(self, data):
        """
        Fügt einen neuen Eingabevektor hinzu.
        :param data: Tuple oder Liste mit Features (z. B. vom OSC-Handler)
        """
        with self.lock:
            self.inputs.append(np.array(data))
            if self.auto_label:
                self.labels.append(self.current_label)
            else:
                self.labels.append(None)  # Kann später gesetzt werden
            self.logger.emit(f"✅ Eingabe aufgenommen: {data}")

    def set_label(self, *args):
        """
        Setzt das aktuelle Label, das beim nächsten Input verwendet wird.
        :param label: z. B. int oder str
        """
        with self.lock:
            self.current_label = np.array(args)
            self.logger.emit(f"🔖 Aktuelles Label gesetzt: {np.array(args)}")

    # def save(self, input_path="inputs.npy", label_path="labels.npy"):
    #     """
    #     Speichert die aufgenommenen Daten.
    #     """
    #     with self.lock:
    #         X = np.array(self.inputs)
    #         y = np.array(self.labels)
    #         np.save(input_path, X)
    #         np.save(label_path, y)
    #         print(f"💾 Daten gespeichert unter: {input_path}, {label_path}")

    def reset(self):
        """
        Setzt die Aufnahme zurück.
        """
        with self.lock:
            self.inputs = []
            self.labels = []
            self.logger.emit("🔄 Aufnahme zurückgesetzt.")

    # def load(self, input_path="inputs.npy", label_path="labels.npy"):
    #     """
    #     Lädt gespeicherte Daten aus .npy Dateien und ersetzt die aktuellen Inhalte.
    #     """
    #     with self.lock:
    #         try:
    #             self.inputs = np.load(input_path).tolist()
    #             self.labels = np.load(label_path).tolist()
    #             print(f"📂 Daten geladen aus: {input_path}, {label_path}")
    #         except FileNotFoundError:
    #             print(f"⚠️ Dateien nicht gefunden: {input_path} oder {label_path}")
    #         except Exception as e:
    #             print(f"⚠️ Fehler beim Laden: {e}")

    def get_data(self):
        X = np.array(self.inputs)
        y = np.array(self.labels)
        return X, y