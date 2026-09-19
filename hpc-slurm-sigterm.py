import faulthandler
import signal
import time

# Prints the trace in the Slurm output upon receiving SIGTERM
faulthandler.register(signal.SIGTERM)

def heavy_computation():
    print("Starting...")
    while True:
        time.sleep(1)

heavy_computation()
