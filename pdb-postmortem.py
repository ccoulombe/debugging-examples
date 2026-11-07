def invert(x):
    return 1 / x

def process(nums):
    for i, n in enumerate(nums):
        print(invert(n))

process([2, 4, 0, 8])

"""
➜ python -m pdb -c continue pdb-postmortem.py
0.5
0.25
Traceback (most recent call last):
  File "pdb-postmortem.py", line 8, in <module>
    process([2, 4, 0, 8])
  File "pdb-postmortem.py", line 6, in process
    print(invert(n))
  File "pdb-postmortem.py", line 2, in invert
    return 1 / x
ZeroDivisionError: division by zero
Uncaught exception. Entering post mortem debugging
Running 'cont' or 'step' will restart the program
> pdb-postmortem.py(2)invert()
-> return 1 / x

(Pdb) p x
0

(Pdb) w
  pdb-postmortem.py(8)<module>()
-> process([2, 4, 0, 8])
  pdb-postmortem.py(6)process()
-> print(invert(n))
> pdb-postmortem.py(2)invert()
-> return 1 / x

(Pdb) up
> pdb-postmortem.py(6)process()
-> print(invert(n))

(Pdb) p i, n
(2, 0)

(Pdb) q
"""
