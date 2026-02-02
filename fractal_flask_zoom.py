import numpy as np
from flask import Flask, render_template_string, request, jsonify
import webbrowser
import threading

def generate_mandelbrot(xmin, xmax, ymin, ymax, width=800, height=800, max_iter=150):
    """Genera el conjunto de Mandelbrot para una región específica"""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    Z = np.zeros_like(C)
    M = np.zeros(C.shape)
    
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + C[mask]
        M[mask] = i
    
    return M

def generate_julia(xmin, xmax, ymin, ymax, width=800, height=800, max_iter=150, c=-0.4+0.6j):
    """Genera el conjunto de Julia para una región específica"""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    M = np.zeros(Z.shape)
    
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + c
        M[mask] = i
    
    return M

def generate_burning_ship(xmin, xmax, ymin, ymax, width=800, height=800, max_iter=150):
    """Genera el fractal Burning Ship para una región específica"""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    Z = np.zeros_like(C)
    M = np.zeros(C.shape)
    
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag))**2 + C[mask]
        M[mask] = i
    
    return M

FRACTAL_INFO = {
    'mandelbrot': {
        'equation': 'z<sub>n+1</sub> = z<sub>n</sub><sup>2</sup> + c, donde z<sub>0</sub> = 0',
        'x_label': 'Re(c) - Parte Real',
        'y_label': 'Im(c) - Parte Imaginaria',
        'interpretation': ('Cada píxel representa un número complejo c. El color indica cuántas iteraciones '
                          'tarda en diverger (|z| > 2). Puntos negros permanecen acotados (pertenecen al conjunto). '
                          'Los colores cálidos divergen rápidamente, los fríos lentamente.')
    },
    'julia': {
        'equation': 'z<sub>n+1</sub> = z<sub>n</sub><sup>2</sup> + c, donde c = -0.4 + 0.6i (fijo)',
        'x_label': 'Re(z) - Parte Real',
        'y_label': 'Im(z) - Parte Imaginaria',
        'interpretation': ('Similar al Mandelbrot pero c es constante y variamos z<sub>0</sub>. '
                          'Muestra qué puntos iniciales permanecen acotados bajo iteración. '
                          'Patrones dendríticos y espirales son característicos de diferentes valores de c.')
    },
    'burning_ship': {
        'equation': 'z<sub>n+1</sub> = (|Re(z<sub>n</sub>)| + i|Im(z<sub>n</sub>)|)<sup>2</sup> + c',
        'x_label': 'Re(c) - Parte Real',
        'y_label': 'Im(c) - Parte Imaginaria',
        'interpretation': ('Variante del Mandelbrot que aplica valores absolutos antes de elevar al cuadrado. '
                          'Rompe la simetría generando estructuras que parecen un barco en llamas. '
                          'La estructura principal se asemeja a humo ascendente.')
    }
}

# Flask app
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Explorador de Fractales - Zoom Infinito</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .control-group {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }
        label {
            font-weight: bold;
            margin-right: 10px;
        }
        select, input {
            padding: 5px 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background-color: #45a049;
        }
        #fractal-plot {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .info-panel {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .equation-box {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #2196F3;
        }
        .interpretation-box {
            background: #fff9e6;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #ffc107;
        }
        .instructions {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            border-left: 4px solid #4CAF50;
        }
        #loading {
            display: none;
            text-align: center;
            color: #666;
            font-size: 18px;
            margin: 20px;
        }
        .metric {
            display: inline-block;
            margin: 5px 15px 5px 0;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <h1>🔬 Explorador de Fractales - Zoom Infinito Dinámico</h1>
    <div class="subtitle">Recálculo automático en alta resolución (800x800 px)</div>
    
    <div class="controls">
        <div class="control-group">
            <label>Tipo de Fractal:</label>
            <select id="fractal-type">
                <option value="mandelbrot">Mandelbrot</option>
                <option value="julia">Julia Set</option>
                <option value="burning_ship">Burning Ship</option>
            </select>
        </div>
        
        <div class="control-group">
            <label>Iteraciones:</label>
            <input type="number" id="iterations" value="150" min="50" max="500" step="10">
        </div>
        
        <div class="control-group">
            <button onclick="resetView()">↺ Reiniciar Vista</button>
            <button onclick="saveImage()">💾 Guardar PNG</button>
        </div>
    </div>
    
    <div id="loading">⏳ Recalculando fractal con alta resolución...</div>
    
    <div id="fractal-plot"></div>
    
    <div class="info-panel">
        <h3>📐 Ecuación Matemática</h3>
        <div class="equation-box" id="equation-box">
            Selecciona un fractal para ver su ecuación
        </div>
        
        <h3>💡 Interpretación</h3>
        <div class="interpretation-box" id="interpretation-box">
            La interpretación aparecerá aquí
        </div>
        
        <h3>📊 Región Actual</h3>
        <div class="equation-box">
            <div class="metric"><strong>Eje X:</strong> <span id="x-label">-</span></div><br>
            <div class="metric"><strong>Eje Y:</strong> <span id="y-label">-</span></div><br>
            <div class="metric"><strong>Rango X:</strong> <span id="x-range">-</span></div><br>
            <div class="metric"><strong>Rango Y:</strong> <span id="y-range">-</span></div><br>
            <div class="metric"><strong>Factor de Zoom:</strong> <span id="zoom-factor">1.00x</span></div>
        </div>
        
        <div class="instructions">
            <h3>🎯 Instrucciones de Uso</h3>
            <ul>
                <li><strong>Zoom:</strong> Arrastra con el mouse para seleccionar un área y hacer zoom</li>
                <li><strong>Pan:</strong> Shift + Arrastra para mover la vista sin zoom</li>
                <li><strong>Recálculo:</strong> El fractal se regenera automáticamente con 800x800 píxeles después de cada zoom</li>
                <li><strong>Iteraciones:</strong> Aumenta para ver más detalles (más lento pero más preciso)</li>
                <li><strong>Guardar:</strong> Exporta la vista actual en PNG de alta resolución (1920x1080)</li>
            </ul>
        </div>
    </div>
    
    <script>
        let currentBounds = {
            mandelbrot: {xmin: -2.5, xmax: 1.0, ymin: -1.25, ymax: 1.25},
            julia: {xmin: -2.0, xmax: 2.0, ymin: -1.5, ymax: 1.5},
            burning_ship: {xmin: -2.0, xmax: 1.0, ymin: -2.0, ymax: 1.0}
        };
        
        let initialBounds = JSON.parse(JSON.stringify(currentBounds));
        
        const fractalInfo = {
            mandelbrot: {
                equation: '$$z_{n+1} = z_n^2 + c$$, donde $$z_0 = 0$$',
                xLabel: 'Re(c) - Parte Real del parámetro complejo c',
                yLabel: 'Im(c) - Parte Imaginaria del parámetro complejo c',
                interpretation: 'Cada píxel representa un número complejo c. El color indica cuántas iteraciones tarda en diverger (|z| > 2). Puntos negros permanecen acotados (pertenecen al conjunto). Los colores cálidos divergen rápidamente, los fríos lentamente. Es autosimilar: cada zoom revela estructuras similares al todo.'
            },
            julia: {
                equation: '$$z_{n+1} = z_n^2 + c$$, donde $$c = -0.4 + 0.6i$$ (constante)',
                xLabel: 'Re(z) - Parte Real del punto inicial z₀',
                yLabel: 'Im(z) - Parte Imaginaria del punto inicial z₀',
                interpretation: 'Similar al Mandelbrot pero c es constante y variamos z₀. Muestra qué puntos iniciales permanecen acotados bajo iteración. Patrones dendríticos y espirales son característicos de diferentes valores de c. La forma depende crucialmente del parámetro c elegido.'
            },
            burning_ship: {
                equation: '$$z_{n+1} = (|\\text{Re}(z_n)| + i|\\text{Im}(z_n)|)^2 + c$$',
                xLabel: 'Re(c) - Parte Real del parámetro complejo c',
                yLabel: 'Im(c) - Parte Imaginaria del parámetro complejo c',
                interpretation: 'Variante del Mandelbrot que aplica valores absolutos a las componentes antes de elevar al cuadrado. Esto rompe la simetría generando estructuras que parecen un barco en llamas. La estructura principal se asemeja a humo ascendente. Único por su asimetría vertical.'
            }
        };
        
        function updateInfo(fractalType) {
            const info = fractalInfo[fractalType];
            document.getElementById('equation-box').innerHTML = info.equation;
            document.getElementById('interpretation-box').innerHTML = info.interpretation;
            document.getElementById('x-label').textContent = info.xLabel;
            document.getElementById('y-label').textContent = info.yLabel;
            
            // Rerender MathJax
            if (window.MathJax) {
                MathJax.typesetPromise();
            }
        }
        
        function calculateZoom(xmin, xmax, fractalType) {
            const initial = initialBounds[fractalType];
            const initialWidth = initial.xmax - initial.xmin;
            const currentWidth = xmax - xmin;
            const zoomFactor = initialWidth / currentWidth;
            document.getElementById('zoom-factor').textContent = zoomFactor.toFixed(2) + 'x';
        }
        
        function updateFractal(xmin, xmax, ymin, ymax) {
            const fractalType = document.getElementById('fractal-type').value;
            const iterations = document.getElementById('iterations').value;
            
            document.getElementById('loading').style.display = 'block';
            
            // Actualizar métricas
            document.getElementById('x-range').textContent = `[${xmin.toFixed(6)}, ${xmax.toFixed(6)}]`;
            document.getElementById('y-range').textContent = `[${ymin.toFixed(6)}, ${ymax.toFixed(6)}]`;
            calculateZoom(xmin, xmax, fractalType);
            updateInfo(fractalType);
            
            fetch('/update_fractal', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    fractal_type: fractalType,
                    xmin: xmin,
                    xmax: xmax,
                    ymin: ymin,
                    ymax: ymax,
                    max_iter: parseInt(iterations)
                })
            })
            .then(response => response.json())
            .then(data => {
                const layout = {
                    title: data.title,
                    xaxis: {title: data.x_label, range: [xmin, xmax]},
                    yaxis: {title: data.y_label, range: [ymin, ymax]},
                    width: 900,
                    height: 700,
                    margin: {t: 80, b: 80, l: 80, r: 50}
                };
                
                const config = {
                    modeBarButtonsToAdd: ['drawopenpath', 'eraseshape'],
                    displaylogo: false
                };
                
                Plotly.newPlot('fractal-plot', [data.plot_data], layout, config);
                
                // Detectar eventos de zoom
                document.getElementById('fractal-plot').on('plotly_relayout', function(eventdata) {
                    if (eventdata['xaxis.range[0]'] !== undefined) {
                        const newXmin = eventdata['xaxis.range[0]'];
                        const newXmax = eventdata['xaxis.range[1]'];
                        const newYmin = eventdata['yaxis.range[0]'];
                        const newYmax = eventdata['yaxis.range[1]'];
                        
                        // Recalcular fractal con nueva resolución
                        setTimeout(() => updateFractal(newXmin, newXmax, newYmin, newYmax), 500);
                    }
                });
                
                document.getElementById('loading').style.display = 'none';
            });
        }
        
        function resetView() {
            const fractalType = document.getElementById('fractal-type').value;
            const bounds = currentBounds[fractalType];
            updateFractal(bounds.xmin, bounds.xmax, bounds.ymin, bounds.ymax);
        }
        
        function saveImage() {
            const timestamp = new Date().toISOString().slice(2,10).replace(/-/g,'');
            const fractalType = document.getElementById('fractal-type').value;
            const filename = `${timestamp}_Fractal_${fractalType}_zoom.png`;
            
            Plotly.downloadImage('fractal-plot', {
                format: 'png',
                width: 1920,
                height: 1080,
                filename: filename
            });
        }
        
        // Cargar fractal inicial
        document.addEventListener('DOMContentLoaded', function() {
            resetView();
        });
        
        // Actualizar cuando cambian los controles
        document.getElementById('fractal-type').addEventListener('change', resetView);
        document.getElementById('iterations').addEventListener('change', function() {
            const fractalType = document.getElementById('fractal-type').value;
            const bounds = currentBounds[fractalType];
            updateFractal(bounds.xmin, bounds.xmax, bounds.ymin, bounds.ymax);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/update_fractal', methods=['POST'])
def update_fractal():
    data = request.json
    fractal_type = data['fractal_type']
    xmin = data['xmin']
    xmax = data['xmax']
    ymin = data['ymin']
    ymax = data['ymax']
    max_iter = data.get('max_iter', 150)
    
    # Obtener información del fractal
    info = FRACTAL_INFO[fractal_type]
    
    # Generar fractal según el tipo
    if fractal_type == 'mandelbrot':
        fractal_data = generate_mandelbrot(xmin, xmax, ymin, ymax, max_iter=max_iter)
        title = f'Conjunto de Mandelbrot<br><sub>{info["equation"]}</sub>'
    elif fractal_type == 'julia':
        fractal_data = generate_julia(xmin, xmax, ymin, ymax, max_iter=max_iter)
        title = f'Conjunto de Julia<br><sub>{info["equation"]}</sub>'
    elif fractal_type == 'burning_ship':
        fractal_data = generate_burning_ship(xmin, xmax, ymin, ymax, max_iter=max_iter)
        title = f'Burning Ship Fractal<br><sub>{info["equation"]}</sub>'
    
    # Crear datos para Plotly
    plot_data = {
        'type': 'heatmap',
        'z': fractal_data.tolist(),
        'colorscale': 'Hot',
        'showscale': True,
        'colorbar': {'title': 'Iteraciones'},
        'x': np.linspace(xmin, xmax, 800).tolist(),
        'y': np.linspace(ymin, ymax, 800).tolist()
    }
    
    return jsonify({
        'plot_data': plot_data,
        'title': title,
        'x_label': info['x_label'],
        'y_label': info['y_label']
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 EXPLORADOR DE FRACTALES CON ZOOM INFINITO")
    print("="*70)
    print("\n📍 Abre tu navegador en: http://localhost:5000")
    print("\n✨ Características:")
    print("   • Recálculo automático al hacer zoom")
    print("   • Resolución constante de 800x800 píxeles")
    print("   • Ecuaciones matemáticas y explicaciones detalladas")
    print("   • Labels de ejes con descripción de lo que representan")
    print("   • Cambio de tipo de fractal en tiempo real")
    print("   • Ajuste de iteraciones dinámico")
    print("   • Exportación a PNG de alta resolución")
    print("\n💡 Presiona Ctrl+C para detener el servidor")
    print("="*70 + "\n")
    
    # Abrir navegador automáticamente
    threading.Timer(1.5, lambda: webbrowser.open('http://localhost:5000')).start()
    
    # Ejecutar sin debug mode para evitar conflictos con IDEs
    app.run(debug=False, port=5000, use_reloader=False)
