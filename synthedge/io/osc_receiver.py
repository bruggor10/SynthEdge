from pythonosc import dispatcher
from pythonosc import osc_server
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox, QFileDialog
import numpy as np
import threading

class OSCReceiver:
    def __init__(self, ip, port):
        """
        Initialisiert den OSC Server.
        :param ip: IP-Adresse zum Binden (meist 0.0.0.0 für alle)
        :param port: Port, auf dem der Server horcht
        """
        self.ip = ip
        self.port = port
        self.dispatcher = dispatcher.Dispatcher()
        self.server = None
        self.thread = None
        self.message_handler = None



    def add_handler(self, address, handler_func):
        """
        Fügt einen Handler für eine bestimmte OSC-Address hinzu.
        :param address: OSC-Adresse (z.B. "/synthedge/inputs")
        :param handler_func: Funktion mit Signatur handler_func(address, *args)
        """
        self.dispatcher.map(address, handler_func)

    def start(self):
        """
        Startet den OSC-Server in einem separaten Thread.
        """
        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        print(f"OSC Server läuft auf {self.ip}:{self.port}")
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def stop(self):
        """
        Stoppt den OSC-Server.
        """
        if self.server:
            self.server.shutdown()
            self.thread.join()
            print("OSC Server gestoppt.")

    
                


class OSCHandler(QObject):
    trigger_blink = Signal()
    rec_led = Signal(bool)
    run_led = Signal(bool)
    trigger_save = Signal(str)
    trigger_load = Signal(str)
    error_occurred = Signal(str)
    logger = Signal(str)
    def __init__(self, recorder, model, sender, port):
        super().__init__()
        self.ip = "0.0.0.0"
        self.port = port
        self.rec = recorder
        self.model = model
        self.sender = sender


    # ============ Handlers ==========
    def data_handler(self, address, *args):
        self.trigger_blink.emit()
        if(self.rec.is_recording):
            self.rec.add_input(list(args))
        if(self.model.is_running):
            if self.model.is_trained: 
                try:
                    X_input = np.array(args).reshape(1, -1)
                    self.sender.send_message("/synthedge/outputs", *self.model.predict(X_input).tolist())
                except Exception as e:
                    self.logger.emit(str(e))
            else:
                self.logger.emit("Train model first")



    def recorder_handler(self, address, recstate):
        recstate = bool(recstate)
        self.rec.is_recording = recstate
        self.rec_led.emit(recstate)
        if(self.model.is_running):
            self.model.is_running = False
            self.logger.emit("Disabling Run mode")
        # print(f"Recording: {self.rec.is_recording}")
        self.logger.emit(f"Recording: {self.rec.is_recording}")


    def save_handler(self, address, path):
        self.trigger_save.emit(path)

    def load_handler(self, address, path):
        self.trigger_load.emit(path)

    def train_handler(self, *args):
        X,y = self.rec.get_data()
        self.model.train(X, y.reshape((y.shape[0], y.shape[2])))

    def reset_handler(self, address):
        self.rec.reset()
        self.model.is_trained = False
        self.model.toggle_trainingstate.emit(False)
        self.run_led.emit(self.model.is_running)

    def label_handler(self, address, *args):
        self.rec.set_label(args)

    def run_handler(self, address, runstate):
        if self.model.is_trained:
            self.model.is_running = bool(runstate)
            self.logger.emit(f"Running state: {self.model.is_running}")
            self.run_led.emit(self.model.is_running)
            if(self.rec.is_recording):
                self.logger.emit("Disabling recording of data")
                self.rec.is_recording = False
        else:
            self.error_occurred.emit("Train model first")
            self.logger.emit("Train model first")



    def start_osc(self):
        ## handle OSC Inputs
        self.receiver = OSCReceiver(ip=self.ip, port=self.port)
        self.receiver.add_handler("/synthedge/inputs", self.data_handler)
        self.receiver.add_handler("/synthedge/record_inputs", self.recorder_handler)
        self.receiver.add_handler("/synthedge/save", self.save_handler)
        self.receiver.add_handler("/synthedge/load", self.load_handler)
        self.receiver.add_handler("/synthedge/train", self.train_handler)
        self.receiver.add_handler("/synthedge/reset", self.reset_handler)
        self.receiver.add_handler("/synthedge/label", self.label_handler)
        self.receiver.add_handler("/synthedge/run", self.run_handler)
        self.receiver.start()

    def stop_osc(self):
        ## stop osc receiving thread
        self.receiver.stop()
        