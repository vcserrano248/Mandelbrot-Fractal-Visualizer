# Generador y Análisis de Fractales en Python

## Descripción

Proyecto profesional de análisis matemático y visualización de fractales, desarrollado en Python. Demuestra capacidades en:
- Matemáticas computacionales
- Análisis numérico
- Visualización científica
- Programación orientada a objetos

## Fractales Implementados

### 1. Conjunto de Mandelbrot
El fractal más famoso, definido por la iteración: **Z = Z² + C**

### 2. Conjunto de Julia
Familia de fractales relacionados con Mandelbrot, con parámetros personalizables

### 3. Burning Ship
Fractal que utiliza valores absolutos: **Z = (|Re(Z)| + i|Im(Z)|)² + C**

### 4. Triángulo de Sierpinski
Fractal clásico generado mediante el método de caos (chaos game)

## Características

✓ Generación de múltiples tipos de fractales
✓ Análisis matemático de complejidad y dimensión fractal
✓ Visualizaciones profesionales con mapas de color personalizados
✓ Explorador interactivo con controles en tiempo real
✓ Comparación lado a lado de diferentes fractales
✓ Análisis de zoom y detalles infinitos

## Requisitos

\`\`\`
numpy
matplotlib
\`\`\`

## Uso

### Generación Básica

\`\`\`python
python scripts/fractal_generator.py
\`\`\`

Esto ejecutará el script principal que genera todos los tipos de fractales con análisis completo.

### Explorador Interactivo

\`\`\`python
python scripts/fractal_interactive.py
\`\`\`

Abre una interfaz interactiva donde puedes:
- Cambiar entre tipos de fractales
- Ajustar el número de iteraciones
- Modificar parámetros del conjunto de Julia en tiempo real

## Análisis Matemático

El proyecto incluye análisis de:
- **Entropía**: Medida de complejidad e información
- **Varianza**: Distribución de valores
- **Gradiente promedio**: Cambios locales en el fractal
- **Dimensión fractal**: Usando el método box-counting
- **Ratio de ocupación**: Densidad del fractal

## Ejemplos de Código

### Generar un Mandelbrot personalizado

\`\`\`python
from fractal_generator import FractalGenerator, FractalVisualizer

generator = FractalGenerator(width=800, height=800)
data = generator.mandelbrot(xmin=-2.5, xmax=1.5, ymin=-2, ymax=2, max_iter=150)

visualizer = FractalVisualizer()
visualizer.plot_fractal(data, 'Mi Mandelbrot', colormap='sunset')
\`\`\`

### Explorar diferentes Julia sets

\`\`\`python
# Julia sets interesantes
julia1 = generator.julia(c_real=-0.7, c_imag=0.27015)
julia2 = generator.julia(c_real=-0.8, c_imag=0.156)
julia3 = generator.julia(c_real=0.285, c_imag=0.01)

visualizer.compare_fractals([julia1, julia2, julia3], 
                           ['Julia 1', 'Julia 2', 'Julia 3'],
                           colormap='ocean')
\`\`\`

## Aplicaciones Profesionales

Este proyecto demuestra competencias en:

1. **Análisis Numérico**: Implementación de algoritmos iterativos complejos
2. **Visualización Científica**: Presentación profesional de datos matemáticos
3. **Optimización**: Uso eficiente de NumPy para cálculos vectorizados
4. **Arquitectura de Software**: Código modular y orientado a objetos
5. **Documentación**: Código bien documentado y profesional

## Posibles Extensiones

- Animaciones de zoom en fractales
- Renderizado de alta resolución para impresión
- Fractales 3D (Mandelbulb, Menger Sponge)
- Análisis de convergencia y estabilidad
- Exportación a diferentes formatos (PNG, SVG, PDF)
- Paralelización con multiprocessing para mayor velocidad

## Autor

Proyecto desarrollado como parte de portafolio profesional en análisis de datos y matemáticas computacionales.
