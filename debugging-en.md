# Python Debugging Examples Guide

You will find a detailed overview of the debugging examples contained in this repository. It details how each example works, the issues illustrated, the commands needed to run them, and how to interact with the debugging tools.

---

## Table of Contents
1. [Debugging Tools](#debugging-tools)
2. [PDB Examples (Interactive Python Debugger)](#pdb-examples-interactive-python-debugger)
   - [pdb-breakpoint.py — Breakpoints (breakpoint)](#1-pdb-breakpointpy--breakpoints-breakpoint)
   - [pdb-set_trace.py — Classic Method pdb.set_trace()](#2-pdb-set_tracepy--classic-method-pdbset_trace)
   - [pdb-average.py — Command-Line Debugging, Step-by-Step](#3-pdb-averagepy--command-line-debugging-step-by-step)
   - [pdb-condition.py — Conditional Breakpoints](#4-pdb-conditionpy--conditional-breakpoints)
   - [pdb-data.py — Command-Line Initialization (-c) and Type Mismatch](#5-pdb-datapy--command-line-initialization--c-and-type-mismatch)
   - [pdb-postmortem.py — Command-Line Post-Mortem Debugging (-c continue)](#6-pdb-postmortempy--command-line-post-mortem-debugging--c-continue)
3. [Faulthandler Examples (Low-Level Diagnostics)](#faulthandler-examples-low-level-diagnostics)
   - [faulthandler-segfault.py — Segmentation Faults (SIGSEGV)](#7-faulthandler-segfaultpy--segmentation-faults-sigsegv)
   - [faulthandler-sigill.py — Command-Line Activation (-X faulthandler)](#8-faulthandler-sigillpy--command-line-activation--x-faulthandler)
   - [faulthandler-hang.py — Hang Detection and Timeout](#9-faulthandler-hangpy--hang-detection-and-timeout)
   - [faulthandler-sigusr.py — On-Demand Signal Inspection and Process Attachment](#10-faulthandler-sigusrpy--on-demand-signal-inspection-and-process-attachment)
4. [Jupyter Examples (Notebooks)](#jupyter-examples-notebooks)
   - [pdb-breakpoint.ipynb — Interactive Debugging](#11-pdb-breakpointipynb--interactive-debugging)
   - [pdb-postmortem.ipynb — Post-Mortem Debugging with %pdb](#12-pdb-postmortemipynb--post-mortem-debugging-with-pdb)
   - [faulthandler-segfault.ipynb — Capturing Kernel Crashes to a Log File](#13-faulthandler-segfaultipynb--capturing-kernel-crashes-to-a-log-file)
5. [Practical Examples (Additional)](#practical-examples-additional)
   - [hpc-interactive-pdb.py — Interactive PDB on Compute Node](#14-hpc-interactive-pdbpy--interactive-pdb-on-compute-node)
   - [hpc-io-watchdog.py — I/O Block](#15-hpc-io-watchdogpy--io-block)
   - [hpc-slurm-sigterm.py — Infinite loop](#16-hpc-slurm-sigtermpy--infinite-loop)
   - [hpc-mpi-deadlock.py — MPI Deadlocks](#17-hpc-mpi-deadlockpy--mpi-deadlocks)
6. [Cheat Sheet](#cheat-sheet)

---

## Debugging Tools

1. **`pdb` (Python Debugger)**:
   The interactive source-code debugger included in Python's standard library. It supports setting breakpoints, stepping through code line-by-line (*step-by-step*), inspecting call stack frames (*stack frames*), and modifying variables dynamically at runtime.
2. **`faulthandler`**:
   Introduced in Python 3.3, this standard module catches low-level fault signals (such as `SIGSEGV`, `SIGFPE`, `SIGABRT`, `SIGBUS`, or `SIGILL`) as well as thread deadlocks. Because these brutal crashes terminate the Python runtime before `try...except` blocks can execute, `faulthandler` directly writes the Python call stack to standard error or to a file.
3. **IPython / Jupyter Debugging**:
   Interactive environments integrate `ipdb` (an enhanced version of PDB offering syntax highlighting and autocompletion) via magic commands like `%pdb` or `%debug`, as well as the `set_trace()` function.

---

## PDB Examples (Interactive Python Debugger)

### 1. `pdb-breakpoint.py` — Breakpoints (`breakpoint`)

File : [pdb-breakpoint.py](pdb-breakpoint.py)

#### Description
Introduced in Python 3.7 ([PEP 553](https://peps.python.org/pep-0553/)), the built-in `breakpoint()` function suspends program execution and drops directly into the configured debugger (by default `pdb`).
In this example, calling `double(val)` immediately hits `breakpoint()`, interrupts instruction flow, and opens the `(Pdb)` prompt.

```python
def double(x):
   breakpoint()
   return x * 2

val = 3
print(f"{val} * 2 is {double(val)}")
```

#### Execution
```bash
python pdb-breakpoint.py
```

#### Walkthrough
Upon startup, Python pauses at line 2 (`breakpoint()`):
```text
> pdb-breakpoint.py(2)double()
-> breakpoint()
(Pdb) ll
  1   def double(x):
  2  ->    breakpoint()
  3      return x * 2

(Pdb) n
> pdb-breakpoint.py(3)double()
-> return x * 2

(Pdb) p x
3

(Pdb) q
```
- `ll` (*long list*): Displays the complete source code of the active function, with `->` marking the current line.
- `n` (*next*): Executes the current line and stops at the next line (`return x * 2`).
- `p x` (*print*): Displays the value of argument `x` (`3`).
- `q` (*quit*): Quits the debugger and terminates the program.

#### Controlling `breakpoint()` via `PYTHONBREAKPOINT`
Unlike `pdb.set_trace()`, `breakpoint()` checks the `PYTHONBREAKPOINT` environment variable at runtime, allowing you to disable breakpoints or switch debuggers without modifying source code:
```bash
# Ignore all breakpoint() calls
PYTHONBREAKPOINT=0 python pdb-breakpoint.py

# Use an alternative debugger (e.g., ipdb or pudb)
PYTHONBREAKPOINT=ipdb.set_trace python pdb-breakpoint.py
```

---

### 2. `pdb-set_trace.py` — Classic Method `pdb.set_trace()`

File : [pdb-set_trace.py](pdb-set_trace.py)

#### Description
Illustrates the traditional approach used in Python versions prior to 3.7: explicitly importing the `pdb` module and calling `pdb.set_trace()`. The example also highlights the debugger's ability to directly evaluate Python expressions on the fly.

```python
import pdb

def double(x):
   pdb.set_trace()
   return x * 2

val = 3
print(f"{val} * 2 is {double(val)}")
```

#### Execution
```bash
python pdb-set_trace.py
```

#### Walkthrough
```text
> pdb-set_trace.py(4)double()
-> pdb.set_trace()
(Pdb) ll
  3   def double(x):
  4  ->    pdb.set_trace()
  5      return x * 2

(Pdb) p x
3

(Pdb) x * 2
6

(Pdb) c
3 * 2 is 6
```
- `p x`: Displays variable `x`.
- `x * 2`: Evaluates any valid Python expression within the local frame's context.
- `c` (*continue*): Resumes normal program execution until completion or the next breakpoint.

---

### 3. `pdb-average.py` — Command-Line Debugging, Step-by-Step

File : [pdb-average.py](pdb-average.py)

#### Description
Runs a script under PDB without modifying its source code using the `-m pdb` option.
The function calculates the average of a list of numbers. When invoked with an empty list `[]`, a `ZeroDivisionError` exception is raised during the `total / len(nums)` calculation.

```python
def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)

print(average([]))
```

#### Execution

##### Standard execution (reproducing the error):
```bash
python pdb-average.py
```
Output:
```text
Traceback (most recent call last):
  File "pdb-average.py", line 7, in <module>
    print(average([]))
  File "pdb-average.py", line 5, in average
    return total / len(nums)
ZeroDivisionError: division by zero
```

##### Launching with PDB from the first instruction:
```bash
python -m pdb pdb-average.py
```

#### Walkthrough
```text
> pdb-average.py(1)<module>()
-> def average(nums):

(Pdb) n
> pdb-average.py(7)<module>()
-> print(average([]))

(Pdb) s
--Call--
> pdb-average.py(1)average()
-> def average(nums):

(Pdb) ll
  1  -> def average(nums):
  2       total = 0
  3       for n in nums:
  4           total += n
  5       return total / len(nums)

(Pdb) n
> pdb-average.py(2)average()
-> total = 0

(Pdb) n
> pdb-average.py(3)average()
-> for n in nums:

(Pdb) n
> pdb-average.py(5)average()
-> return total / len(nums)

(Pdb) args
nums = []

(Pdb) nums = [1]

(Pdb) n
--Return--
> pdb-average.py(5)average()->0.0
-> return total / len(nums)

(Pdb) n
0.0
--Return--
> pdb-average.py(7)<module>()->None
-> print(average([]))

(Pdb) q
```
- `s` (*step into*): Steps into the `average()` function call.
- `args`: Displays the arguments received by the current function (`nums = []`).
- `nums = [1]`: Dynamically modifies a variable's state directly in the debugger, bypassing the zero division error and immediately testing subsequent behavior.

> **Tip (`display`)**: When stepping through a loop (for example if `nums = [10, 20, 30]`), use `display total` instead of typing `p total` after every step. PDB will automatically print `total` whenever its value changes (`display total: 10  [old: 0]`). Use `undisplay` to stop watching it.

---

### 4. `pdb-condition.py` — Conditional Breakpoints

File : [pdb-condition.py](pdb-condition.py)

#### Description
Setup of a conditional breakpoint that only interrupts the program when a specific condition is met.
In this loop, the function iterates over integers and must raise a `ValueError` as soon as a number is negative:

```python
def process(items):
    for i, x in enumerate(items):
        if x < 0:
            raise ValueError(f"Negative value at index {i}")
        print(i, x)

process([1, 2, 3, -1, 5])
```

#### Execution
```bash
python -m pdb pdb-condition.py
```

#### Walkthrough
```text
> pdb-condition.py(1)<module>()
-> def process(items):
(Pdb) ll
  1  -> def process(items):
  2       for i, x in enumerate(items):
  3           if x < 0:
  4               raise ValueError(f"Negative value at index {i}")
  5           print(i, x)
  6   
  7   process([1, 2, 3, -1, 5])

(Pdb) b 3, x<0
Breakpoint 1 at pdb-condition.py:3

(Pdb) c
0 1
1 2
2 3
> pdb-condition.py(3)process()
-> if x < 0:

(Pdb) p x
-1

(Pdb) args
items = [1, 2, 3, -1, 5]
```
- `b 3, x<0`: Creates breakpoint number 1 at line 3 with condition `x < 0`.
- `c` (*continue*): The program processes positive values (0, 1, 2) without interruption, then stops exactly at the iteration where `x == -1`.

---

### 5. `pdb-data.py` — Command-Line Initialization (`-c`) and Type Mismatch

File : [pdb-data.py](pdb-data.py)

#### Description
Illustrates two key concepts:
1. Automating the injection of debugging commands right at startup using the `-c` parameter.
2. Diagnosing and correcting in memory a `TypeError` exception caused by an attempt to add a string and an integer (`"12" + 5`).

```python
def load_data():
    return {"count": "12"}  # BUG: count should be int

def compute_total():
    data = load_data()
    return data["count"] + 5  # TypeError

def main():
    compute_total()

main()
```

#### Execution

##### Standard execution:
```bash
python pdb-data.py
```

##### Debugging with automatic breakpoint set at line 6:
```bash
python -m pdb -c "b 6" pdb-data.py
```

#### Walkthrough
```text
Breakpoint 1 at pdb-data.py:6
> pdb-data.py(1)<module>()
-> def load_data():

(Pdb) c
> pdb-data.py(6)compute_total()
-> return data["count"] + 5  # TypeError

(Pdb) p data
{'count': '12'}

(Pdb) type(data['count'])
<class 'str'>

(Pdb) data['count'] = 12

(Pdb) n
--Return--
> pdb-data.py(6)compute_total()->17
-> return data["count"] + 5  # TypeError

(Pdb) c
The program finished and will be restarted
> pdb-data.py(1)<module>()

(Pdb) q
```
- `-c "b 6"`: Sets the breakpoint at line 6 right upon debugger launch.
- `type(...)`: Reveals that the value stored under key `'count'` is a string (`str`).
- `data['count'] = 12`: Corrects the value in memory, allowing the addition to execute without error and return `17`.

---

### 6. `pdb-postmortem.py` — Command-Line Post-Mortem Debugging (`-c continue`)

File : [pdb-postmortem.py](pdb-postmortem.py)

#### Description
Runs a script at normal speed under PDB using `-c continue` (or `-c c`) without setting any breakpoints in advance. When an unhandled exception occurs inside a helper function (`ZeroDivisionError` in `invert(x)`), PDB automatically enters **post-mortem mode** at the exact point of failure, allowing you to inspect the call stack (`w`) and move up (`up`) to the caller frame (`process(nums)`) to see which loop iteration caused the crash.

```python
def invert(x):
    return 1 / x

def process(nums):
    for i, n in enumerate(nums):
        print(invert(n))

process([2, 4, 0, 8])
```

#### Execution
```bash
python -m pdb -c continue pdb-postmortem.py
```

#### Walkthrough
```text
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
```
- `-c continue`: Immediately starts execution without stopping at line 1, dropping into PDB only if an unhandled exception is raised.
- `w` (*where*): Displays the full call stack leading to the crash (`<module>()` -> `process()` -> `invert()`).
- `up`: Moves one frame up the call stack from `invert(x)` into `process(nums)` to inspect the loop index `i` (`2`) and current value `n` (`0`).

---

## Faulthandler Examples (Low-Level Diagnostics)

### 7. `faulthandler-segfault.py` — Segmentation Faults (`SIGSEGV`)

File : [faulthandler-segfault.py](faulthandler-segfault.py)

#### Description
Calling `ctypes.string_at(0)` forces a NULL pointer dereference (`0x0`), which immediately triggers a memory access violation (`SIGSEGV`).
Without `faulthandler`, the operating system would only display `Segmentation fault (core dumped)`. Thanks to `faulthandler.enable()`, the responsible Python code line as well as the C call stack are fully displayed before the process terminates.

```python
import faulthandler
faulthandler.enable()

print("About to crash...")

# Force a crash using ctypes
import ctypes
ctypes.string_at(0)   # invalid memory access → segfault
```

#### Execution
```bash
python faulthandler-segfault.py
```

#### Trace Output
```text
About to crash...
Fatal Python error: Segmentation fault

Current thread 0x00007fb552718f00 [python] (most recent call first):
  File ".../ctypes/__init__.py", line 619 in string_at
  File "faulthandler-segfault.py", line 8 in <module>

Current thread's C stack trace (most recent call first):
...
[1]    273236 segmentation fault (core dumped)  python faulthandler-segfault.py
```

---

### 8. `faulthandler-sigill.py` — Command-Line Activation (`-X faulthandler`)

File : [faulthandler-sigill.py](faulthandler-sigill.py)

#### Description
Shows how to enable `faulthandler` at the Python interpreter level without modifying a single line of source code, either with the CLI option `-X faulthandler`, or with the environment variable `PYTHONFAULTHANDLER=1`. The script deliberately emits the illegal hardware instruction signal (`SIGILL`).

```python
import signal

signal.raise_signal(signal.SIGILL)
```

#### Execution

##### Execution without faulthandler (raw crash without context):
```bash
python faulthandler-sigill.py
```
Output:
```text
illegal hardware instruction (core dumped)  python faulthandler-sigill.py
```

##### Execution with faulthandler enabled via command line:
```bash
python -q -X faulthandler faulthandler-sigill.py
```
Or alternatively:
```bash
PYTHONFAULTHANDLER=1 python faulthandler-sigill.py
```

#### Trace Output
```text
Fatal Python error: Illegal instruction

Current thread 0x00007f2c55b28f00 [python] (most recent call first):
  File "faulthandler-sigill.py", line 3 in <module>

Current thread's C stack trace (most recent call first):
  Binary file "/lib64/libpython3.14.so.1.0", at _Py_DumpStack+...
  ...
```

---

### 9. `faulthandler-hang.py` — Hang Detection and Timeout

File : [faulthandler-hang.py](faulthandler-hang.py)

#### Description
Allows identifying deadlocks (*deadlocks*) or infinite loops (*spinlocks*) using `faulthandler.dump_traceback_later(timeout)`. If execution time exceeds the specified timeout (here 3 seconds), `faulthandler` displays the traceback of all Python threads on standard error (`sys.stderr`) without interrupting the process.

```python
import time
import faulthandler

faulthandler.dump_traceback_later(3)

time.sleep(10)
```

#### Execution
```bash
python faulthandler-hang.py
```

#### Trace Output
After exactly 3 seconds, the following traceback is emitted while the script continues sleeping until reaching 10 seconds:
```text
Timeout (0:00:03)!
Thread 0x00007f9a39ea6f00 [python] (most recent call first):
  File "faulthandler-hang.py", line 6 in <module>
```

---

### 10. `faulthandler-sigusr.py` — On-Demand Signal Inspection and Process Attachment

File : [faulthandler-sigusr.py](faulthandler-sigusr.py)

#### Description
Presents two advanced techniques for examining a running or stuck Python process:
1. Registering a signal handler with `faulthandler.register(signal.SIGUSR1)`. Upon receiving the `SIGUSR1` signal, the process immediately displays its execution stack without stopping.
2. Attaching an interactive PDB debugger to a running process via the command `python -m pdb -p <PID>`.

```python
import faulthandler
import signal
import time

faulthandler.register(signal.SIGUSR1)

print("Send SIGUSR1")

while True:
    time.sleep(2)
```

#### Execution

##### Terminal 1: Starting the script
```bash
python faulthandler-sigusr.py
```
Output:
```text
Send SIGUSR1
```

##### Terminal 2 (Option A): Sending the SIGUSR1 signal
```bash
kill -USR1 $(pgrep -f faulthandler-sigusr.py)
```
In Terminal 1, the instantaneous traceback appears immediately and the loop continues execution:
```text
Current thread 0x00007fa455c49f00 [python] (most recent call first):
  File "faulthandler-sigusr.py", line 10 in <module>
```

##### Terminal 2 (Option B): Attaching to the process
```bash
python -m pdb -p $(pgrep -f faulthandler-sigusr.py)
```
Output:
```text
> faulthandler-sigusr.py(10)<module>()
-> time.sleep(2)
(Pdb) 
```

---

## Jupyter Examples (Notebooks)

### 11. `pdb-breakpoint.ipynb` — Interactive Debugging

File : [pdb-breakpoint.ipynb](pdb-breakpoint.ipynb)

#### Description
Using a breakpoint directly inside a Jupyter notebook cell using `IPython.core.debugger.set_trace()`. When evaluating the cell, an interactive `ipdb` prompt appears directly in the cell's output area.

#### Content:
- **Cell 1**:
  ```python
  from IPython.core.debugger import set_trace

  def average(nums):
      total = 0
      set_trace() # Breakpoint here
      for n in nums:
          total += n
      return total / len(nums)
  ```
- **Cell 2**:
  ```python
  print(average([]))
  ```

#### Execution
1. Start Jupyter:
   ```bash
   jupyter lab
   ```
2. Open [`pdb-breakpoint.ipynb`](pdb-breakpoint.ipynb).
3. Run Cell 1 to load the function.
4. Run Cell 2: execution halts at `set_trace()` and the `ipdb>` prompt opens, ready to receive your commands (`n`, `p nums`, `q`).

---

### 12. `pdb-postmortem.ipynb` — Post-Mortem Debugging with `%pdb`

File : [pdb-postmortem.ipynb](pdb-postmortem.ipynb)

#### Description
Using IPython's automatic post-mortem mode via `%pdb on` (or `%debug`). When an uncaught exception occurs (here `TypeError: can only concatenate str (not "int") to str`), IPython automatically drops into `ipdb` at the exact location of the faulty line.

#### Content:
- **Cell 1**:
  ```python
  def load_data():
      return {"count": "12"}  # BUG: count should be int

  def compute_total():
      data = load_data()
      return data["count"] + 5  # TypeError

  def main():
      return compute_total()
  ```
- **Cell 2**:
  ```python
  %pdb on
  main()

  # or using the %debug magic command
  ```
- **Cell 3**:
  ```python
  %pdb off
  ```

#### Execution
1. Open [`pdb-postmortem.ipynb`](pdb-postmortem.ipynb) in Jupyter.
2. Run Cell 1.
3. Run Cell 2: `%pdb on` activates the automatic debugger. As soon as `main()` raises the `TypeError` exception, the `ipdb>` session opens:
   ```text
   Automatic pdb calling has been turned ON
   TypeError: can only concatenate str (not "int") to str
   > compute_total()
   ----> 6 return data["count"] + 5
   ipdb> data["count"]
   '12'
   ipdb> type(data['count'])
   <class 'str'>
   ipdb> q
   ```
4. Run Cell 3 (`%pdb off`) to deactivate the automatic debugger trigger.

---

### 13. `faulthandler-segfault.ipynb` — Capturing Kernel Crashes to a Log File

File : [faulthandler-segfault.ipynb](faulthandler-segfault.ipynb)

#### Description
When a Jupyter notebook suffers a fatal C-level error (a segmentation fault for example), the kernel process dies suddenly, often causing the loss of standard error messages in the web interface.
This example shows how to configure `faulthandler.enable(open("faults.log", "w"))` to redirect the crash trace to a persistent log file ([`faults.log`](faults.log)).

#### Content:
- **Cell 1**:
  ```python
  import faulthandler
  faulthandler.enable(open("faults.log", "w"))
  ```
- **Cell 2**:
  ```python
  print("About to crash...")

  # Force a crash using ctypes
  import ctypes
  ctypes.string_at(0)   # invalid memory access → segfault
  ```

#### Execution
1. Open [`faulthandler-segfault.ipynb`](faulthandler-segfault.ipynb) in Jupyter.
2. Run Cell 1 to redirect `faulthandler` output to `faults.log`.
3. Run Cell 2: the Jupyter kernel crashes abruptly (*"Kernel died / restarting"*).
4. Inspect the generated [`faults.log`](faults.log) file with an editor or in a terminal:
   ```bash
   cat faults.log
   ```
   You will find that the complete call stack was successfully recorded to disk, precisely isolating the `ctypes/__init__.py` function and the offending cell!

---

## Practical Examples (Additional)

### 14. `hpc-interactive-pdb.py` — Interactive PDB on Compute Node

File : [hpc-interactive-pdb.py](hpc-interactive-pdb.py)

#### Description
Inserting `breakpoint()` in a script submitted via `sbatch` causes an immediate crash (`BdbQuit` or `EOFError`) because the background task has no terminal (TTY) or standard input to interact with.
To use PDB interactively, it is essential to request an interactive session (`salloc` or `srun --pty`) in order to debug the process.

```python
def heavy_computation_with_bug(matrix_size):
    print(f"Allocating a {matrix_size}x{matrix_size} matrix...")
    breakpoint()
    return matrix_size * 2

if __name__ == "__main__":
    result = heavy_computation_with_bug(10000)
    print(f"Result: {result}")
```

#### Execution
In Slurm, first obtain an interactive shell:
```text
$ salloc -c 2 --mem=10G
salloc: Pending job allocation 3447848
salloc: job 3447848 queued and waiting for resources
salloc: job 3447848 has been allocated resources
salloc: Granted job allocation 3447848
salloc: Waiting for resource configuration
salloc: Nodes nc20142 are ready for job
```
Then launch the debugger:
```text
$ python hpc-interactive-pdb.py
Allocating a 10000x10000 matrix...
> /workspace/hpc-interactive-pdb.py(4)heavy_computation_with_bug()
-> return matrix_size * 2
(Pdb) p matrix_size
10000
(Pdb) c
Result: 20000
```

---

### 15. `hpc-io-watchdog.py` — I/O Block

File : [hpc-io-watchdog.py](hpc-io-watchdog.py)

#### Description
HPC shared filesystems can experience severe latency spikes, blocking input/output operations (`np.load()`, `h5py` reads) in an uninterruptible sleep state. `faulthandler.dump_traceback_later()` allows you to display the call stack when the time has elapsed.

```python
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
```

#### Execution
```text
$ python hpc-io-watchdog.py
Simulating reading file...
Timeout (0:00:03)!
Thread 0x00007f9a39ea6f00 (most recent call first):
  File "hpc-io-watchdog.py", line 9 in <module>
I/O successfully completed.
```

---

### 16. `hpc-slurm-sigterm.py` — Infinite loop

File : [hpc-slurm-sigterm.py](hpc-slurm-sigterm.py)

#### Description
In a High-Performance Computing (HPC) environment, a job that exceeds its time limit (`#SBATCH --time=...`), either because it runs infinitely or simply reaches the end of its allocated time, will be terminated. When the job is stopped by Slurm, a 60-second grace period is granted during which `SIGTERM` is sent before receiving a final `SIGKILL`. By intercepting `SIGTERM` with `faulthandler`, you can force the call stack to be printed in the output file (`slurm-%j.out`) to identify exactly where the infinite loop occurs or where your code execution was interrupted.

```python
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
```

#### Execution (Simulation)
```text
$ srun -c 2 --mem=10G python hpc-slurm-sigterm.py &
[1] 1663615
srun: job 3447846 queued and waiting for resources
srun: job 3447846 has been allocated resources
Starting...

$ scancel 3447846
srun: Job step aborted: Waiting up to 62 seconds for job step to finish.
slurmstepd: error: *** STEP 3447846.0 ON nc20142 CANCELLED AT 2026-09-19T16:52:24 DUE to SIGNAL Terminated ***
Current thread 0x0000150e66b84740 (most recent call first):
  File "hpc-slurm-sigterm.py", line 11 in heavy_computation
  File "hpc-slurm-sigterm.py", line 13 in <module>
```

---

### 17. `hpc-mpi-deadlock.py` — MPI Deadlocks

File : [hpc-mpi-deadlock.py](hpc-mpi-deadlock.py)

#### Description
When using `mpi4py` distributed across multiple compute nodes, each MPI rank runs as a separate process and can hang waiting indefinitely for a message. By binding a custom signal (like `SIGUSR1`) to `faulthandler` in each process (`all_threads=True` also includes any threads within that rank's process), you can broadcast the signal to all ranks via `scancel` (or `kill`) to display the state of each rank.

```python
import faulthandler
import signal
from mpi4py import MPI

# Registers SIGUSR1 in each MPI rank (process) to print its traceback
faulthandler.register(signal.SIGUSR1, all_threads=True)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    print("Rank 0 is waiting for rank 1...")
    # Bug: Rank 0 waits for a message that will never be sent
    data = comm.recv(source=1, tag=11)  # Rank 0 process blocks here
else:
    print(f"Rank {rank} is busy...")
    import time
    while True:
        time.sleep(1)  # Other rank process loops here
```

#### Execution
Inside an allocation:
```text
$ srun -n 2 python hpc-mpi-deadlock.py &
[1] 1663616
Rank 0 is waiting for rank 1...
Rank 1 is busy...

$ kill -USR1 $!
Current thread 0x0000150e66b84741 (most recent call first):
  File "hpc-mpi-deadlock.py", line 19 in <module>
Current thread 0x0000150e66b84740 (most recent call first):
  File "hpc-mpi-deadlock.py", line 14 in <module>
```
or from a login node:
```text
$ srun -n 2 python hpc-mpi-deadlock.py &
[1] 1663617
srun: job 3447847 queued and waiting for resources
srun: job 3447847 has been allocated resources
Rank 0 is waiting for rank 1...
Rank 1 is busy...

$ scancel --signal=SIGUSR1 3447847
Current thread 0x0000150e66b84741 (most recent call first):
  File "hpc-mpi-deadlock.py", line 19 in <module>
Current thread 0x0000150e66b84740 (most recent call first):
  File "hpc-mpi-deadlock.py", line 14 in <module>
```

---

## Cheat Sheet

### Essential PDB Commands

| Command | Shortcut | Description |
| :--- | :--- | :--- |
| `next` | `n` | Step over: execute current line without entering called functions. |
| `step` | `s` | Step into: enter called function at current line. |
| `continue` | `c` | Continue execution until the next breakpoint or completion. |
| `return` | `r` | Continue execution until the current function returns. |
| `longlist` | `ll` | Display complete source code of the active function. |
| `list` | `l` | Display 11 lines of code around current line. |
| `print` | `p <expr>` | Evaluate and display value of variable or expression. |
| `pp` | `pp <expr>` | Pretty-print structure of complex variable. |
| `display` | `display <expr>` | Automatically display value of `<expr>` each time it changes when execution stops. |
| `undisplay` | `undisplay <expr>` | Stop automatically displaying `<expr>`. |
| `args` | `a` | Display list of arguments received by current function. |
| `break` | `b <line>` | Set breakpoint at specified line number. |
| `break` (cond) | `b <line>, <cond>` | Set conditional breakpoint triggering only if `<cond>` is true. |
| `where` | `w` | Display call stack (*stack trace*), most recent frame at bottom. |
| `up` / `down` | `u` / `d` | Move up or down one level in stack frames. |
| `quit` | `q` | Quit debugger and terminate execution. |

> **Note (`PYTHONBREAKPOINT`)**: Set `PYTHONBREAKPOINT=0` in the environment to disable all `breakpoint()` calls without editing code, or `PYTHONBREAKPOINT=<module>.<callable>` (e.g., `ipdb.set_trace`) to use an alternative debugger.

### Faulthandler Commands and Options

| Context | Method / Option | Description |
| :--- | :--- | :--- |
| In code | `faulthandler.enable(file=sys.stderr)` | Enable handling of fatal signals (`SIGSEGV`, `SIGFPE`, `SIGABRT`, `SIGBUS`, `SIGILL`). |
| In code | `faulthandler.dump_traceback_later(timeout)` | Dump trace of all threads after a delay of `timeout` seconds. |
| In code | `faulthandler.register(signal)` | Dump trace upon receipt of specific OS signal (e.g. `SIGUSR1`). |
| Command-line option | `python -X faulthandler script.py` | Enable `faulthandler` module on interpreter startup without modifying script. |
| Environment variable | `export PYTHONFAULTHANDLER=1` | Enable `faulthandler` globally for all Python processes in session. |

### IPython / Jupyter Magic Commands

| Magic Command | Description |
| :--- | :--- |
| `%pdb on` | Automatically opens `ipdb` whenever an unhandled exception occurs. |
| `%pdb off` | Disables automatic post-mortem debugger launch. |
| `%debug` | Opens `ipdb` in post-mortem mode on the last unhandled exception. |
