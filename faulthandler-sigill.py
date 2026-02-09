import signal

signal.raise_signal(signal.SIGILL)

"""
➜ python faulthandler-sigill.py 
[1]    273373 illegal hardware instruction (core dumped)  python faulthandler-sigill.py

➜ python -q -X faulthandler faulthandler-sigill.py
Fatal Python error: Illegal instruction

Current thread 0x00007f2c55b28f00 [python] (most recent call first):
  File "faulthandler-sigill.py", line 3 in <module>

Current thread's C stack trace (most recent call first):
  Binary file "/lib64/libpython3.14.so.1.0", at _Py_DumpStack+0x4c [0x7f2c5551f1fd]
  Binary file "/lib64/libpython3.14.so.1.0", at +0x11fe69 [0x7f2c5551fe69]
  Binary file "/lib64/libc.so.6", at +0x1a040 [0x7f2c55229040]
  Binary file "/lib64/libc.so.6", at +0x73e5c [0x7f2c55282e5c]
  Binary file "/lib64/libc.so.6", at gsignal+0x1e [0x7f2c55228f0e]
  Binary file "/lib64/libpython3.14.so.1.0", at +0x12f178 [0x7f2c5552f178]
  Binary file "/lib64/libpython3.14.so.1.0", at PyObject_Vectorcall+0x37 [0x7f2c5555ba37]
  Binary file "/lib64/libpython3.14.so.1.0", at _PyEval_EvalFrameDefault+0xd24 [0x7f2c55570af4]
  Binary file "/lib64/libpython3.14.so.1.0", at +0x16c505 [0x7f2c5556c505]
  Binary file "/lib64/libpython3.14.so.1.0", at PyEval_EvalCode+0xb7 [0x7f2c5565d657]
  Binary file "/lib64/libpython3.14.so.1.0", at +0x29e139 [0x7f2c5569e139]
  Binary file "/lib64/libpython3.14.so.1.0", at +0x29d45a [0x7f2c5569d45a]
  Binary file "/lib64/libpython3.14.so.1.0", at +0x29cf24 [0x7f2c5569cf24]
  Binary file "/lib64/libpython3.14.so.1.0", at +0x29cd05 [0x7f2c5569cd05]
  Binary file "/lib64/libpython3.14.so.1.0", at Py_RunMain+0x499 [0x7f2c55651b69]
  Binary file "/lib64/libpython3.14.so.1.0", at Py_BytesMain+0x3b [0x7f2c5564ba5b]
  Binary file "/lib64/libc.so.6", at +0x3575 [0x7f2c55212575]
  Binary file "/lib64/libc.so.6", at __libc_start_main+0x88 [0x7f2c55212628]
  Binary file "python", at _start+0x25 [0x55ee44dcf3d5]
[1]    273451 illegal hardware instruction (core dumped)  python -q -X faulthandler faulthandler-sigill.py
"""