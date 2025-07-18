from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QTimer
from ..gui.ui_main import Ui_MainWindow
from ..io.osc_receiver import *
from ..core.model_manager import ModelManager
import sys

class MainApp(QMainWindow):
    def __init__(self, osc_in, model, sender):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.osc_in=osc_in
        self.osc_out = sender
        self.model = model
        
        self.ui.models.currentIndexChanged.connect(self.model_selected)     
        self.ui.model_type_classifiers.toggled.connect(self.classifiers_checked)
        self.ui.model_type_regressors.toggled.connect(self.regressors_checked)

        
        # blink widgets
        self.input_blink_widget = BlinkWidget(self.ui.data_in_blink)
        self.output_blink_widget = BlinkWidget(self.ui.data_out_blink)
        # self.input_blink_widget.start_blinking()
        self.osc_in.trigger_blink.connect(self.input_blink_widget.start_blinking)
        self.osc_out.trigger_blink.connect(self.output_blink_widget.start_blinking)
    def model_selected(self,index):
        selection = self.ui.models.currentText()
        all_models = dict(self.model.get_classifiers()) | dict(self.model.get_regressors())
        key = next((k for k, v in all_models.items() if v == selection), None)
        if key: self.model.configure_model(model_type=key)

    def classifiers_checked(self, checked):
        if checked:
            self.ui.models.clear()
            self.ui.models.addItems(list(k for v, k in self.model.get_classifiers())) 
    
    def regressors_checked(self, checked):
        if checked:
            self.ui.models.clear()
            self.ui.models.addItems(list(k for v, k in self.model.get_regressors())) 
    
    
    
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

class BlinkWidget(QTimer):
    def __init__(self, widget):
        super().__init__(widget)
        # init blink widget
        self.blink_widget = widget
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_blink)
        self.blink_state = False
        self.default_stylesheet = self.blink_widget.styleSheet()
         # Timer zum Beenden des Blinkens
        self.blink_duration_timer = QTimer(self)
        self.blink_duration_timer.setSingleShot(True)
        self.blink_duration_timer.timeout.connect(self.stop_blinking)
    
    # === BLINK WIDGET ===
    def start_blinking(self):
        self.blink_state = False
        self.blink_timer.start(100)  # 500 ms Intervall
        self.blink_duration_timer.start(1000)  # 3 Sekunden lang blinken

    def stop_blinking(self):
        self.blink_timer.stop()
        self.blink_widget.setStyleSheet(self.default_stylesheet)  # zurücksetzen

    def toggle_blink(self):
        if self.blink_state:
            self.blink_widget.setStyleSheet(self.default_stylesheet)
        else:
            self.blink_widget.setStyleSheet(self.default_stylesheet + "background-color: rgba(151, 243, 132, 1);")
        self.blink_state = not self.blink_state