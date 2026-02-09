import faulthandler
import signal
import time

faulthandler.register(signal.SIGUSR1)

print("Send SIGUSR1")

while True:
    time.sleep(2)


"""
➜ python faulthandler-sigusr.py     
Send SIGUSR1

....
Current thread 0x00007fa455c49f00 [python] (most recent call first):
  File "faulthandler-sigusr.py", line 19 in <module>

# In a second terminal
➜ kill -USR1 $(pgrep -f faulthandler)

# In a second terminal
➜ python3.14 -m pdb -p $(pgrep -f faulthandler)
> faulthandler-sigusr.py(19)<module>()
-> time.sleep(2)
(Pdb) 

"""