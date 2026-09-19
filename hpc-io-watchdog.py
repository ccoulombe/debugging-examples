import faulthandler
import time

# Starting a watchdog timer (here 3 seconds for demonstration)
faulthandler.dump_traceback_later(3)

try:
    print("Simulating reading file...")
    time.sleep(10) # Simulates a prolonged hang
finally:
    # Immediate cancellation upon success within the time limit
    faulthandler.cancel_dump_traceback_later()

print("I/O successfully completed.")
