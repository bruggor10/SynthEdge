from synthedge.io.osc_receiver import *
from synthedge.io.osc_sender import *
from synthedge.io.recorder import *
from synthedge.core.model_manager import *
from synthedge.connector.connector import MainApp
from PySide6.QtWidgets import QApplication
import sys

# ==== global objects =====
rec = Recorder() # for 3 inputs
model = ModelManager()
model.configure_model(model_type='lin_poly_reg')
sender = OSCSender(ip="127.0.0.1", port=5006)
osc_in = OSCHandler(rec, model, sender, port=5003)



def main():
    # try:
    #     while True:
    #         pass  # Keep main thread alive
    # except KeyboardInterrupt:
    #     osc_in.stop_osc()

    # osc_in.start_osc()
    app = QApplication(sys.argv)
    window = MainApp(osc_in, model, sender, rec)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
