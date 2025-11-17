# Generador y Análisis de Fractales en Python

Proyecto profesional de análisis matemático y visualización de fractales con zoom infinito y recálculo dinámico.

## Descripción

Este proyecto demuestra capacidades avanzadas en:
- Matemáticas computacionales y análisis numérico
- Visualización científica interactiva
- Programación orientada a objetos
- Optimización de algoritmos con NumPy

## Fractales Implementados

### 1. Conjunto de Mandelbrot
**Ecuación:** $$Z_{n+1} = Z_n^2 + C$$

El fractal más famoso. Cada punto C en el plano complejo se colorea según cuántas iteraciones toma para que Z diverja.

### 2. Conjunto de Julia
**Ecuación:** $$Z_{n+1} = Z_n^2 + C$$ (donde C es constante)

Familia de fractales relacionados con Mandelbrot. Diferentes valores de C producen patrones completamente distintos.

### 3. Burning Ship
**Ecuación:** $$Z_{n+1} = (|Re(Z_n)| + i|Im(Z_n)|)^2 + C$$

Fractal que utiliza valores absolutos de las componentes, creando estructuras que parecen barcos ardiendo.

### 4. Triángulo de Sierpinski
Fractal clásico generado mediante el método del caos (chaos game). Se construye iterativamente removiendo triángulos.

---

## Scripts Disponibles

### 1. `fractal_generator.py` - Generador Estático

**Uso:**
\`\`\`bash
python scripts/fractal_generator.py
\`\`\`

**Características:**
- Genera los 4 tipos de fractales automáticamente
- Incluye análisis matemático completo (entropía, dimensión fractal, etc.)
- Guarda archivos PNG (300 DPI) y HTML interactivos
- Formato de salida: `251117_Fractal_mandelbrot.png/html`

**Ideal para:** Generar rápidamente todos los fractales con análisis profesional

---

### 2. `fractal_flask_zoom.py` - Explorador con Zoom Infinito (RECOMENDADO)

**Uso:**
\`\`\`bash
python scripts/fractal_flask_zoom.py
\`\`\`

El navegador se abrirá automáticamente en `http://localhost:5000`

**Características:**
- ✅ Recálculo dinámico real al hacer zoom
- ✅ Sin pixelado - siempre alta resolución
- ✅ Controles para cambiar fractal e iteraciones
- ✅ Guarda PNG de alta resolución (1920x1080)
- ✅ Ecuaciones y explicaciones en la interfaz

**Cómo funciona el zoom infinito:**
1. Haces zoom arrastrando el mouse en el gráfico
2. El servidor Flask detecta la nueva región
3. Recalcula el fractal con 800x800 píxeles para esa área específica
4. Actualiza el gráfico instantáneamente

**Controles interactivos:**
- **Selector de fractal:** Cambia entre Mandelbrot, Julia, Burning Ship
- **Slider de iteraciones:** Ajusta el detalle (50-500 iteraciones)
- **Botón "Guardar PNG":** Descarga imagen de alta resolución
- **Zoom con mouse:** Arrastra para seleccionar área, doble click para resetear

**Ideal para:** Exploración profunda con máxima calidad visual

---

## Interpretación de Gráficos

### Ejes
- **Eje X (Re):** Parte real del número complejo
- **Eje Y (Im):** Parte imaginaria del número complejo

### Colores
Los colores representan el **número de iteraciones** antes de que el punto diverja:
- **Colores oscuros:** Puntos que pertenecen al conjunto (no divergen)
- **Colores brillantes:** Puntos que divergen rápidamente
- **Gradientes:** Regiones de transición con comportamiento complejo

### Métricas Calculadas

**Entropía:** Mide la complejidad y aleatoriedad del fractal
- Alta entropía = más caótico e impredecible

**Varianza:** Dispersión de los valores de iteración
- Alta varianza = mayor variedad de estructuras

**Dimensión Fractal:** Medida de auto-similitud (método box-counting)
- Valor típico entre 1.5 y 2.0 para fractales clásicos

---

## Aplicaciones Profesionales

1. **Análisis Numérico:** Algoritmos iterativos complejos optimizados
2. **Visualización Científica:** Presentación profesional de datos matemáticos
3. **Desarrollo Web:** Aplicaciones interactivas con Flask
4. **Optimización:** Uso eficiente de NumPy para cálculos vectorizados
5. **Arquitectura de Software:** Código modular, documentado y profesional

---

## Posibles extensiones

- Animaciones de zoom profundo con video
- Fractales 3D (Mandelbulb, Menger Sponge)
- Análisis de convergencia y órbitas
- Paralelización con multiprocessing
- Paletas de colores personalizables
- Exportación a PDF vectorial
- Sistema de waypoints para regiones interesantes

---

## Instalaciones necesarias

### Opción 1: Anaconda (RECOMENDADO)

Abre **Anaconda Prompt** y ejecuta:

\`\`\`bash
# Crear ambiente virtual (opcional pero recomendado)
conda create -n fractals python=3.10
conda activate fractals

# Instalar dependencias
conda install numpy matplotlib plotly
pip install kaleido flask
\`\`\`

### Opción 2: pip

\`\`\`bash
pip install numpy matplotlib plotly kaleido flask
\`\`\`

### Verificar Instalación

\`\`\`bash
# Verificar kaleido
pip show kaleido

# O desde Python
python -c "import numpy, plotly, flask, kaleido; print('✓ Todo instalado')"
\`\`\`

---

## Seguridad de uso - localhost:5000

### ¿Es seguro usar localhost:5000?

**SÍ, completamente seguro** para uso local:
- Solo es accesible desde tu computadora
- No está expuesto a internet
- Otras personas NO pueden acceder (ni en tu red)
- Se cierra cuando terminas el script

**Preocúpate si:**
- Configuras `host='0.0.0.0'` (acepta conexiones externas)
- Añades contraseñas directamente en el código
- Lo despliegas a un servidor público sin autenticación

---

## Ejemplos de Uso Programático

### Generar Mandelbrot personalizado

\`\`\`python
from fractal_generator import FractalGenerator, FractalVisualizer

generator = FractalGenerator(width=1000, height=1000)
data = generator.mandelbrot(
    xmin=-2.5, xmax=1.5,
    ymin=-2, ymax=2,
    max_iter=200
)

visualizer = FractalVisualizer()
visualizer.plot_fractal(data, 'Mandelbrot Personalizado', colormap='hot')
\`\`\`

### Explorar Julia Sets interesantes

\`\`\`python
# Parámetros que generan patrones únicos
julia1 = generator.julia(c_real=-0.7, c_imag=0.27015)  # Dragón de Douady
julia2 = generator.julia(c_real=-0.8, c_imag=0.156)    # Espiral
julia3 = generator.julia(c_real=0.285, c_imag=0.01)    # Dendritas

visualizer.compare_fractals(
    [julia1, julia2, julia3],
    ['Dragón', 'Espiral', 'Dendritas']
)
\`\`\`

---

## Estructura del Proyecto

\`\`\`
fractals/
├── scripts/
│   ├── fractal_generator.py           # Generador estático con análisis
│   └── fractal_flask_zoom.py          # Explorador avanzado (zoom infinito)
├── fractal_outputs/                   # Archivos generados (PNG y HTML)
│   ├── 251117_Fractal_mandelbrot.png
│   ├── 251117_Fractal_mandelbrot.html
│   └── ...
└── README.md                          # Este archivo
\`\`\`

---

## Solución de Problemas

### Error: "No module named 'kaleido'"
\`\`\`bash
pip install -U kaleido
\`\`\`

### Error: "No module named 'flask'"
\`\`\`bash
pip install flask
\`\`\`

### Error: "Address already in use" (Flask)
Otro programa está usando el puerto 5000. Cambia el puerto en el código:
\`\`\`python
app.run(port=5001, debug=False, use_reloader=False)
\`\`\`

### Los PNG no se guardan
- Verifica que kaleido esté instalado: `pip show kaleido`
- Los archivos HTML siempre se guardan y son completamente funcionales

### Ejecución lenta
- Reduce resolución: `width=600, height=600`
- Reduce iteraciones: `max_iter=100`
- Cierra otros programas que usen CPU

---

## Autora
@vcserrano248
**Temas relacionados:** análisis de datos, matemáticas computacionales y visualización científica.
**Tecnologías:** Python, NumPy, Matplotlib, Plotly, Flask
