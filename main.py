from synthedge.io.osc_receiver import *
from synthedge.io.osc_sender import *
from synthedge.io.recorder import *
from synthedge.core.model_manager import *

# ==== global objects =====
rec = Recorder(3) # for 3 inputs
model = ModelManager(model_type='svr')
sender = OSCSender(ip="127.0.0.1", port=5006)
# sender.send_message("/wek/outputs", *args)


def main():
    osc_in = OSCHandler(rec, model)
    osc_in.start_osc()

    try:
        while True:
            pass  # Keep main thread alive
    except KeyboardInterrupt:
        osc_in.stop_osc()
    

if __name__ == "__main__":
    main()