# Python Fractal Generator and Analysis

Professional project for mathematical analysis and visualization of fractals with infinite zoom and dynamic recalculation.

## Description

This project demonstrates advanced capabilities in:
- Computational mathematics and numerical analysis
- Interactive scientific visualization
- Object-oriented programming
- Algorithm optimization with NumPy

## Implemented Fractals

### 1. Mandelbrot Set
**Equation:** $$Z_{n+1} = Z_n^2 + C$$

The most famous fractal. Each point C in the complex plane is colored according to how many iterations it takes for Z to diverge.

### 2. Julia Set
**Equation:** $$Z_{n+1} = Z_n^2 + C$$ (where C is constant)

Family of fractals related to Mandelbrot. Different C values produce completely different patterns.

### 3. Burning Ship
**Equation:** $$Z_{n+1} = (|Re(Z_n)| + i|Im(Z_n)|)^2 + C$$

Fractal that uses absolute values of components, creating structures resembling burning ships.

### 4. Sierpinski Triangle
Classic fractal generated through the chaos game method. Built iteratively by removing triangles.

---

## Available Scripts

### 1. `fractal_generator.py` - Static Generator

**Usage:**
\`\`\`bash
python scripts/fractal_generator.py
\`\`\`

**Features:**
- Automatically generates all 4 fractal types
- Includes complete mathematical analysis (entropy, fractal dimension, etc.)
- Saves PNG files (300 DPI) and interactive HTML
- Output format: `251117_Fractal_mandelbrot.png/html`

**Ideal for:** Quickly generating all fractals with professional analysis

---

### 2. `fractal_flask_zoom.py` - Infinite Zoom Explorer (RECOMMENDED)

**Usage:**
\`\`\`bash
python scripts/fractal_flask_zoom.py
\`\`\`

Browser will automatically open at `http://localhost:5000`

**Features:**
- ✅ Real dynamic recalculation on zoom
- ✅ No pixelation - always high resolution
- ✅ Controls to change fractal and iterations
- ✅ Saves high-resolution PNG (1920x1080)
- ✅ Equations and explanations in the interface

**How infinite zoom works:**
1. Zoom by dragging mouse on the plot
2. Flask server detects the new region
3. Recalculates the fractal with 800x800 pixels for that specific area
4. Updates the plot instantly

**Interactive controls:**
- **Fractal selector:** Switch between Mandelbrot, Julia, Burning Ship
- **Iterations slider:** Adjust detail (50-500 iterations)
- **"Save PNG" button:** Download high-resolution image
- **Mouse zoom:** Drag to select area, double-click to reset

**Ideal for:** Deep exploration with maximum visual quality

---

## Plot Interpretation

### Axes
- **X-axis (Re):** Real part of the complex number
- **Y-axis (Im):** Imaginary part of the complex number

### Colors
Colors represent the **number of iterations** before the point diverges:
- **Dark colors:** Points belonging to the set (do not diverge)
- **Bright colors:** Points that diverge quickly
- **Gradients:** Transition regions with complex behavior

### Calculated Metrics

**Entropy:** Measures the complexity and randomness of the fractal
- High entropy = more chaotic and unpredictable

**Variance:** Dispersion of iteration values
- High variance = greater variety of structures

**Fractal Dimension:** Measure of self-similarity (box-counting method)
- Typical value between 1.5 and 2.0 for classic fractals

---

## Professional Applications

1. **Numerical Analysis:** Optimized complex iterative algorithms
2. **Scientific Visualization:** Professional presentation of mathematical data
3. **Web Development:** Interactive applications with Flask
4. **Optimization:** Efficient use of NumPy for vectorized calculations
5. **Software Architecture:** Modular, documented, and professional code

---

## Possible Extensions

- Deep zoom animations with video
- 3D fractals (Mandelbulb, Menger Sponge)
- Convergence and orbit analysis
- Parallelization with multiprocessing
- Customizable color palettes
- Vector PDF export
- Waypoint system for interesting regions

---

## Required Installations

### Option 1: Anaconda (RECOMMENDED)

Open **Anaconda Prompt** and run:

\`\`\`bash
# Create virtual environment (optional but recommended)
conda create -n fractals python=3.10
conda activate fractals

# Install dependencies
conda install numpy matplotlib plotly
pip install kaleido flask
\`\`\`

### Option 2: pip

\`\`\`bash
pip install numpy matplotlib plotly kaleido flask
\`\`\`

### Verify Installation

\`\`\`bash
# Verify kaleido
pip show kaleido

# Or from Python
python -c "import numpy, plotly, flask, kaleido; print('✓ Everything installed')"
\`\`\`

---

## Security - localhost:5000

### Is localhost:5000 safe?

**YES, completely safe** for local use:
- Only accessible from your computer
- Not exposed to the internet
- Other people CANNOT access it (not even on your network)
- Closes when you stop the script

**Be concerned if:**
- You configure `host='0.0.0.0'` (accepts external connections)
- You add passwords directly in the code
- You deploy it to a public server without authentication

---

## Programmatic Usage Examples

### Generate custom Mandelbrot

\`\`\`python
from fractal_generator import FractalGenerator, FractalVisualizer

generator = FractalGenerator(width=1000, height=1000)
data = generator.mandelbrot(
    xmin=-2.5, xmax=1.5,
    ymin=-2, ymax=2,
    max_iter=200
)

visualizer = FractalVisualizer()
visualizer.plot_fractal(data, 'Custom Mandelbrot', colormap='hot')
\`\`\`

### Explore interesting Julia Sets

\`\`\`python
# Parameters that generate unique patterns
julia1 = generator.julia(c_real=-0.7, c_imag=0.27015)  # Douady's Dragon
julia2 = generator.julia(c_real=-0.8, c_imag=0.156)    # Spiral
julia3 = generator.julia(c_real=0.285, c_imag=0.01)    # Dendrites

visualizer.compare_fractals(
    [julia1, julia2, julia3],
    ['Dragon', 'Spiral', 'Dendrites']
)
\`\`\`

---

## Project Structure

\`\`\`
fractals/
├── scripts/
│   ├── fractal_generator.py           # Static generator with analysis
│   └── fractal_flask_zoom.py          # Advanced explorer (infinite zoom)
├── fractal_outputs/                   # Generated files (PNG and HTML)
│   ├── 251117_Fractal_mandelbrot.png
│   ├── 251117_Fractal_mandelbrot.html
│   └── ...
└── README.md                          # This file
\`\`\`

---

## Troubleshooting

### Error: "No module named 'kaleido'"
\`\`\`bash
pip install -U kaleido
\`\`\`

### Error: "No module named 'flask'"
\`\`\`bash
pip install flask
\`\`\`

### Error: "Address already in use" (Flask)
Another program is using port 5000. Change the port in the code:
\`\`\`python
app.run(port=5001, debug=False, use_reloader=False)
\`\`\`

### PNGs not saving
- Verify kaleido is installed: `pip show kaleido`
- HTML files always save and are fully functional

### Slow execution
- Reduce resolution: `width=600, height=600`
- Reduce iterations: `max_iter=100`
- Close other CPU-intensive programs

---

## Author
**Author & Project Director:** vcserrano248 using AI-assisted development tools.
**Related topics:** data analysis, computational mathematics, and scientific visualization.
**Technologies:** Python, NumPy, Matplotlib, Plotly, Flask

This project was conceptualized, designed, and directed by Veronica Serrano. The implementation leverages AI as a development accelerator, with all architectural decisions, mathematical formulations, feature specifications, code review, and quality assurance performed by the author.

This project demonstrates proficiency in:
- Mathematical modeling and fractal theory conceptualization
- Technical requirements analysis and specification
- AI prompt engineering and iterative development
- Code architecture and design decisions
- Quality assurance and functional verification
- Python scientific computing and visualization
