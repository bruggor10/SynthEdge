from synthedge.io.osc_receiver import *
from synthedge.io.osc_sender import *
from synthedge.io.recorder import *
from synthedge.core.model_manager import *
from synthedge.connector.connector import MainApp
from PySide6.QtWidgets import QApplication
import sys

# ==== global objects =====
rec = Recorder(3) # for 3 inputs
model = ModelManager()
model.configure_model(model_type='rf')
sender = OSCSender(ip="127.0.0.1", port=5006)


def main():
    osc_in = OSCHandler(rec, model, sender)
    osc_in.start_osc()


    # try:
    #     while True:
    #         pass  # Keep main thread alive
    # except KeyboardInterrupt:
    #     osc_in.stop_osc()
    app = QApplication(sys.argv)
    window = MainApp(osc_in, model)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
