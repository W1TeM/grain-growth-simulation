# Fast Grain Growth Simulation

A high-performance, Python-based scientific simulation of microstructure evolution and crystallization. The computational engine is fully optimized using NumPy vectorization and the Moore neighborhood.

## ✨ Features

* **High Performance**: No nested `for` loops. Pure NumPy tensor operations.
* **CLI Interface**: Fully configurable via command-line arguments.
* **Visualization Modes**: Live animation, static final-frame rendering, or exporting to `.gif`.
* **Advanced Physics**: 
  * Toggle between Periodic Boundary Conditions (PBC) and Hard Walls.
  * Continuous nucleation (JMAK kinetics) support.
* **Custom Colormap**: Generates visually distinct, pastel-toned colors for an unlimited number of grains.

## 🚀 How to Start

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the simulation using the command line. 

### Basic Usage
Run with default parameters (200x200 grid, 50 initial grains, live animation):
```bash
python grain_growth.py
```

### CLI Arguments

You can customize the simulation using the following flags:

* `--length` (int): Length of the grid (default: 200).
* `--width` (int): Width of the grid (default: 200).
* `--grains` (int): Number of starting crystallization grains (default: 50).
* `--mode` (str): Visualization mode. Choose from `animate`, `static`, or `save` (default: `animate`).
* `--file_name` (str): Name of the output file if mode is `save` (default: `grains.gif`).
* `--pbc`: Flag to enable Periodic Boundary Conditions. If not passed, hard boundaries are used.
* `--nucl_rate` (int): Number of new grains spawning at each time step (default: 0).

### 💡 Cool Examples

**1. Heavy Continuous Nucleation (Snowflake effect):**
```bash
python grain_growth.py --length 300 --width 300 --grains 5 --nucl_rate 3
```

**2. Fast Background Calculation & Save to GIF:**
```bash
python grain_growth.py --mode save --length 150 --width 150 --file_name my_sim.gif
```

**3. Large Grid Static Render with Periodic Boundaries:**
```bash
python grain_growth.py --mode static --length 500 --width 500 --grains 200 --pbc
```