"""
Generador de Fractales - Proyecto de Análisis Matemático
Crea y analiza diferentes tipos de fractales con visualizaciones profesionales
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go
import plotly.express as px
import time
import os

class FractalGenerator:
    """Clase para generar y visualizar diferentes tipos de fractales"""
    
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.output_dir = "fractal_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def mandelbrot(self, xmin=-2.5, xmax=1.5, ymin=-2, ymax=2, max_iter=256):
        """
        Genera el conjunto de Mandelbrot
        
        Args:
            xmin, xmax: Límites del eje real
            ymin, ymax: Límites del eje imaginario
            max_iter: Número máximo de iteraciones
        
        Returns:
            Array 2D con los valores de iteración
        """
        print(f"[v0] Generando Mandelbrot con {max_iter} iteraciones...")
        start_time = time.time()
        
        # Crear grid de números complejos
        x = np.linspace(xmin, xmax, self.width)
        y = np.linspace(ymin, ymax, self.height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        # Inicializar arrays
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        
        # Iterar el algoritmo de Mandelbrot: Z = Z² + C
        for i in range(max_iter):
            # Máscara para valores que no han divergido
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i
        
        elapsed = time.time() - start_time
        print(f"[v0] Mandelbrot generado en {elapsed:.2f} segundos")
        
        return M
    
    def julia(self, c_real=-0.7, c_imag=0.27015, xmin=-2, xmax=2, ymin=-2, ymax=2, max_iter=256):
        """
        Genera el conjunto de Julia
        
        Args:
            c_real, c_imag: Parámetros del conjunto de Julia
            max_iter: Número máximo de iteraciones
        
        Returns:
            Array 2D con los valores de iteración
        """
        print(f"[v0] Generando Julia con c = {c_real} + {c_imag}i...")
        start_time = time.time()
        
        # Crear grid
        x = np.linspace(xmin, xmax, self.width)
        y = np.linspace(ymin, ymax, self.height)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        
        # Constante compleja
        C = complex(c_real, c_imag)
        
        # Array de resultados
        M = np.zeros(Z.shape)
        
        # Iterar: Z = Z² + C
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C
            M[mask] = i
        
        elapsed = time.time() - start_time
        print(f"[v0] Julia generado en {elapsed:.2f} segundos")
        
        return M
    
    def burning_ship(self, xmin=-2, xmax=1, ymin=-2, ymax=1, max_iter=256):
        """
        Genera el fractal Burning Ship
        
        Returns:
            Array 2D con los valores de iteración
        """
        print(f"[v0] Generando Burning Ship...")
        start_time = time.time()
        
        x = np.linspace(xmin, xmax, self.width)
        y = np.linspace(ymin, ymax, self.height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        
        # Burning Ship usa valores absolutos: Z = (|Re(Z)| + i|Im(Z)|)² + C
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            # Aplicar valor absoluto a las partes real e imaginaria
            Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag))**2 + C[mask]
            M[mask] = i
        
        elapsed = time.time() - start_time
        print(f"[v0] Burning Ship generado en {elapsed:.2f} segundos")
        
        return M
    
    def sierpinski_triangle(self, iterations=7):
        """
        Genera el triángulo de Sierpinski usando el método de puntos
        
        Args:
            iterations: Número de puntos a generar (2^iterations)
        
        Returns:
            Arrays de coordenadas x, y
        """
        print(f"[v0] Generando Triángulo de Sierpinski...")
        
        # Vértices del triángulo
        vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])
        
        # Punto inicial
        point = np.array([0.5, 0.25])
        
        # Generar puntos
        num_points = 2 ** iterations
        x_points = np.zeros(num_points)
        y_points = np.zeros(num_points)
        
        for i in range(num_points):
            # Elegir vértice aleatorio
            vertex = vertices[np.random.randint(0, 3)]
            # Mover punto a mitad de camino hacia el vértice
            point = (point + vertex) / 2
            x_points[i] = point[0]
            y_points[i] = point[1]
        
        print(f"[v0] {num_points} puntos generados")
        
        return x_points, y_points


class FractalVisualizer:
    """Clase para visualizar fractales con diferentes estilos"""
    
    @staticmethod
    def create_colormap(name='viridis'):
        """Crea mapas de color personalizados"""
        if name == 'fire':
            colors = ['#000000', '#1a0033', '#4d0066', '#800080', '#ff0080', '#ff6600', '#ffff00', '#ffffff']
            return LinearSegmentedColormap.from_list('fire', colors)
        elif name == 'ocean':
            colors = ['#000033', '#000066', '#0033cc', '#0066ff', '#00ccff', '#66ffff', '#ffffff']
            return LinearSegmentedColormap.from_list('ocean', colors)
        elif name == 'sunset':
            colors = ['#0d0221', '#2b0b3f', '#752e5b', '#c74b50', '#f49d37', '#ffcb69']
            return LinearSegmentedColormap.from_list('sunset', colors)
        else:
            return plt.cm.get_cmap(name)
    
    @staticmethod
    def plot_fractal(data, title, colormap='viridis', filename_base=None):
        """
        Visualiza un fractal y lo guarda en PNG y HTML
        
        Args:
            data: Array 2D con datos del fractal
            title: Título del gráfico
            colormap: Nombre del mapa de color
            filename_base: Nombre base del archivo (sin extensión)
        """
        data_normalized = np.log(data + 1)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        cmap = FractalVisualizer.create_colormap(colormap)
        
        im = ax.imshow(data_normalized, cmap=cmap, interpolation='bilinear', origin='lower')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Agregar colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Iteraciones (log scale)', rotation=270, labelpad=20)
        
        plt.tight_layout()
        
        if filename_base:
            png_filename = f"{filename_base}.png"
            plt.savefig(png_filename, dpi=300, bbox_inches='tight')
            print(f"Imagen PNG guardada: {png_filename}")
        
        plt.show()
        
        if filename_base:
            fig_plotly = go.Figure(data=go.Heatmap(
                z=data_normalized,
                colorscale=colormap if colormap in ['viridis', 'plasma', 'inferno'] else 'viridis',
                colorbar=dict(title="Iteraciones (log)")
            ))
            
            fig_plotly.update_layout(
                title=title,
                width=1200,
                height=1000,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            
            html_filename = f"{filename_base}.html"
            fig_plotly.write_html(html_filename)
            print(f"Gráfico HTML interactivo guardado: {html_filename}")
    
    @staticmethod
    def plot_sierpinski(x, y, title, filename_base=None):
        """Visualiza el triángulo de Sierpinski y lo guarda en PNG y HTML"""
        fig, ax = plt.subplots(figsize=(10, 10))
        
        ax.scatter(x, y, s=0.1, c='#0066cc', alpha=0.5)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_aspect('equal')
        ax.axis('off')
        
        plt.tight_layout()
        
        if filename_base:
            png_filename = f"{filename_base}.png"
            plt.savefig(png_filename, dpi=300, bbox_inches='tight')
            print(f"Imagen PNG guardada: {png_filename}")
        
        plt.show()
        
        if filename_base:
            fig_plotly = go.Figure(data=go.Scatter(
                x=x, y=y,
                mode='markers',
                marker=dict(size=1, color='#0066cc', opacity=0.5)
            ))
            
            fig_plotly.update_layout(
                title=title,
                width=1000,
                height=1000,
                xaxis=dict(visible=False),
                yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
                showlegend=False
            )
            
            html_filename = f"{filename_base}.html"
            fig_plotly.write_html(html_filename)
            print(f"Gráfico HTML interactivo guardado: {html_filename}")
    
    @staticmethod
    def compare_fractals(fractals_data, titles, colormap='viridis'):
        """
        Compara múltiples fractales lado a lado
        
        Args:
            fractals_data: Lista de arrays 2D
            titles: Lista de títulos
            colormap: Mapa de color a usar
        """
        n = len(fractals_data)
        fig, axes = plt.subplots(1, n, figsize=(6*n, 6))
        
        if n == 1:
            axes = [axes]
        
        cmap = FractalVisualizer.create_colormap(colormap)
        
        for ax, data, title in zip(axes, fractals_data, titles):
            data_normalized = np.log(data + 1)
            ax.imshow(data_normalized, cmap=cmap, interpolation='bilinear', origin='lower')
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.axis('off')
        
        plt.tight_layout()
        plt.show()


class FractalAnalyzer:
    """Clase para análisis matemático de fractales"""
    
    @staticmethod
    def calculate_dimension(data, box_sizes=None):
        """
        Calcula la dimensión fractal usando box-counting
        
        Args:
            data: Array 2D binario del fractal
            box_sizes: Lista de tamaños de caja a usar
        
        Returns:
            Dimensión fractal estimada
        """
        if box_sizes is None:
            box_sizes = [2, 4, 8, 16, 32, 64]
        
        counts = []
        
        # Binarizar datos
        binary_data = (data > 0).astype(int)
        
        for box_size in box_sizes:
            count = 0
            # Dividir en cajas
            for i in range(0, data.shape[0], box_size):
                for j in range(0, data.shape[1], box_size):
                    box = binary_data[i:i+box_size, j:j+box_size]
                    if np.any(box):
                        count += 1
            counts.append(count)
        
        # Calcular dimensión usando regresión lineal en espacio log-log
        log_boxes = np.log(box_sizes)
        log_counts = np.log(counts)
        
        # Pendiente = dimensión fractal
        dimension = -np.polyfit(log_boxes, log_counts, 1)[0]
        
        return dimension
    
    @staticmethod
    def analyze_complexity(data):
        """
        Analiza la complejidad del fractal
        
        Returns:
            Diccionario con métricas de complejidad
        """
        # Normalizar datos
        normalized = (data - data.min()) / (data.max() - data.min() + 1e-10)
        
        # Calcular entropía
        hist, _ = np.histogram(normalized.flatten(), bins=50, density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log2(hist))
        
        # Calcular varianza
        variance = np.var(normalized)
        
        # Calcular gradientes (cambios locales)
        grad_x = np.gradient(normalized, axis=0)
        grad_y = np.gradient(normalized, axis=1)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        avg_gradient = np.mean(gradient_magnitude)
        
        return {
            'entropy': entropy,
            'variance': variance,
            'avg_gradient': avg_gradient,
            'fill_ratio': np.sum(data > 0) / data.size
        }


def main():
    """Función principal - Genera ejemplos de cada tipo de fractal"""
    
    print("=" * 60)
    print("GENERADOR DE FRACTALES - Análisis Matemático")
    print("=" * 60)
    print()
    
    generator = FractalGenerator(width=600, height=600)
    visualizer = FractalVisualizer()
    analyzer = FractalAnalyzer()
    
    output_dir = generator.output_dir
    
    # 1. Mandelbrot Set
    print("\n1. CONJUNTO DE MANDELBROT")
    print("-" * 60)
    mandelbrot_data = generator.mandelbrot(max_iter=100)
    visualizer.plot_fractal(
        mandelbrot_data, 
        'Conjunto de Mandelbrot', 
        colormap='sunset',
        filename_base=f"{output_dir}/251117_Fractal_Mandelbrot"
    )
    
    # Análisis
    stats = analyzer.analyze_complexity(mandelbrot_data)
    print(f"\nAnálisis de Complejidad:")
    print(f"  - Entropía: {stats['entropy']:.4f}")
    print(f"  - Varianza: {stats['variance']:.4f}")
    print(f"  - Gradiente promedio: {stats['avg_gradient']:.4f}")
    print(f"  - Ratio de ocupación: {stats['fill_ratio']:.4f}")
    
    # 2. Julia Set
    print("\n\n2. CONJUNTO DE JULIA")
    print("-" * 60)
    julia_data = generator.julia(c_real=-0.7, c_imag=0.27015, max_iter=100)
    visualizer.plot_fractal(
        julia_data, 
        'Conjunto de Julia (c = -0.7 + 0.27i)', 
        colormap='ocean',
        filename_base=f"{output_dir}/251117_Fractal_Julia_Classic"
    )
    
    # 3. Burning Ship
    print("\n\n3. BURNING SHIP FRACTAL")
    print("-" * 60)
    burning_data = generator.burning_ship(max_iter=100)
    visualizer.plot_fractal(
        burning_data, 
        'Burning Ship Fractal', 
        colormap='fire',
        filename_base=f"{output_dir}/251117_Fractal_BurningShip"
    )
    
    # 4. Sierpinski Triangle
    print("\n\n4. TRIÁNGULO DE SIERPINSKI")
    print("-" * 60)
    x, y = generator.sierpinski_triangle(iterations=15)
    visualizer.plot_sierpinski(
        x, y, 
        'Triángulo de Sierpinski',
        filename_base=f"{output_dir}/251117_Fractal_Sierpinski"
    )
    
    # 5. Comparación de diferentes Julia sets
    print("\n\n5. COMPARACIÓN DE CONJUNTOS DE JULIA")
    print("-" * 60)
    julia_params = [
        (-0.7, 0.27015, "Dendrite"),
        (-0.8, 0.156, "Douady_Rabbit"),
        (0.285, 0.01, "Siegel_Disk")
    ]
    
    julia_fractals = []
    julia_titles = []
    
    for c_real, c_imag, name in julia_params:
        data = generator.julia(c_real, c_imag, max_iter=80)
        julia_fractals.append(data)
        julia_titles.append(f'Julia: c = {c_real} + {c_imag}i')
        
        # Guardar individualmente
        visualizer.plot_fractal(
            data,
            f'Julia {name}: c = {c_real} + {c_imag}i',
            colormap='viridis',
            filename_base=f"{output_dir}/251117_Fractal_Julia_{name}"
        )
    
    visualizer.compare_fractals(julia_fractals, julia_titles, colormap='viridis')
    
    # 6. Zoom en Mandelbrot
    print("\n\n6. ZOOM EN MANDELBROT")
    print("-" * 60)
    zoom_data = generator.mandelbrot(xmin=-0.8, xmax=-0.4, 
                                     ymin=-0.2, ymax=0.2, 
                                     max_iter=150)
    visualizer.plot_fractal(
        zoom_data, 
        'Mandelbrot - Zoom Detail', 
        colormap='sunset',
        filename_base=f"{output_dir}/251117_Fractal_Mandelbrot_Zoom"
    )
    
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETADO")
    print(f"Todos los gráficos guardados en la carpeta: {output_dir}/")
    print("Formatos: PNG (alta resolución) y HTML (interactivo)")
    print("=" * 60)


if __name__ == "__main__":
    main()
