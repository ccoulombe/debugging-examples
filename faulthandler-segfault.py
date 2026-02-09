import faulthandler
faulthandler.enable()

print("About to crash...")

# Force a crash using ctypes
import ctypes
ctypes.string_at(0)   # invalid memory access → segfault

"""
➜ python faulthandler-segfault.py 
About to crash...
Fatal Python error: Segmentation fault

Current thread 0x00007fb552718f00 [python] (most recent call first):
  File "/usr/lib64/python3.14/ctypes/__init__.py", line 619 in string_at
  File "faulthandler-segfault.py", line 8 in <module>

Current thread's C stack trace (most recent call first):
...
[1]    273236 segmentation fault (core dumped)  python faulthandler-segfault.py
"""