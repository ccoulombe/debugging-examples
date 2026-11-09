# debugging-examples
PDB + Faulthandler simple examples

## Documentation

- **English**: [debugging-examples](https://ccoulombe.github.io/debugging-examples/)
- **Français**: [exemples débogage](https://ccoulombe.github.io/debugging-examples/fr/)

## Prerequisites

> [!NOTE]
> - **Linux only**: This repository is designed for **Linux only** (several examples rely on POSIX signals and low-level Linux diagnostics such as `SIGUSR1`, `SIGTERM`, and `faulthandler.register`).
> - Python **3.14 or higher** is required for some examples (e.g., low-level `faulthandler` diagnostics and signal handling).

## Installation

1. **Clone the repository**:
   ```bash
   git clone --depth 1 https://github.com/ccoulombe/debugging-examples.git
   cd debugging-examples
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running Examples

### Python Scripts

Run a script with embedded breakpoints:
```bash
python pdb-breakpoint.py
```

Or debug step-by-step from the command line without modifying the code:
```bash
python -m pdb pdb-average.py
```

### Jupyter Notebooks

1. Launch Jupyter:
   ```bash
   jupyter lab
   ```

2. Open [`pdb-breakpoint.ipynb`](pdb-breakpoint.ipynb).
3. Run the cells sequentially. Execution pauses at `set_trace()`, opening the interactive `ipdb>` prompt directly in the cell output area.
