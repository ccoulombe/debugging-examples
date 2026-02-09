import time
import faulthandler

faulthandler.dump_traceback_later(3)

time.sleep(10)

"""
➜ python faulthandler-hang.py 
Timeout (0:00:03)!
Thread 0x00007f9a39ea6f00 [python] (most recent call first):
  File "faulthandler-hang.py", line 6 in <module>
"""