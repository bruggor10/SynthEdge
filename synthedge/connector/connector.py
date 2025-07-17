import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ..gui.ui_main import Ui_MainWindow
from ..io.osc_receiver import *
from ..core.model_manager import ModelManager
class MainApp(QMainWindow):
    def __init__(self, osc_in, model):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.osc_in=osc_in
        self.model = model
        self.ui.models.addItems(list(v for k, v in self.model.get_classifiers())) 
        self.ui.models.currentIndexChanged.connect(self.model_selected)     
        self.ui.model_type_classifiers.toggled.connect(self.classifiers_checked)

    def model_selected(self,index):
        selection = list(self.model.get_classifiers())
        # print(selection[index][0])
        self.model.configure_model(model_type=str(selection[index][0]))

    def classifiers_checked(self, checked):
        if checked:
            print("check")
    def closeEvent(self, event):
        # Eigene Funktion ausführen
        self.on_close()

        # Fenster trotzdem schließen lassen
        event.accept()

        # Wenn du das Schließen verhindern willst, verwende: event.ignore()

    def on_close(self):
        # Beispielhafte Funktion beim Schließen
        print("Fenster wird geschlossen. Aufräumen oder Speichern ...")
        self.osc_in.stop_osc()
        # Optional z.B. ein Dialog:
        # QMessageBox.information(self, "Bye!", "Das Fenster wird jetzt geschlossen.")