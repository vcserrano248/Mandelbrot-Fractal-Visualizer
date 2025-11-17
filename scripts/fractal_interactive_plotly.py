"""
Generador Interactivo de Fractales con Plotly
Permite explorar diferentes regiones con zoom y pan en el navegador
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from fractal_generator import FractalGenerator
import os

class PlotlyFractalExplorer:
    """Explorador interactivo de fractales con Plotly"""
    
    def __init__(self):
        self.output_dir = "fractal_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        self.has_kaleido = self._check_kaleido()
        
    def _check_kaleido(self):
        """Verifica si kaleido está disponible para exportar PNG"""
        try:
            import kaleido
            return True
        except ImportError:
            print("\n⚠️  AVISO: Paquete 'kaleido' no disponible.")
            print("   Los fractales se guardarán solo en formato HTML interactivo.")
            print("   Para exportar PNG, instala: pip install kaleido")
            return False
    
    def create_interactive_fractal(self, fractal_type='mandelbrot', width=800, height=800, max_iter=200):
        """
        Crea un fractal interactivo con Plotly
        
        Args:
            fractal_type: 'mandelbrot', 'julia', 'burning_ship', o 'sierpinski'
            width: Ancho en píxeles
            height: Alto en píxeles
            max_iter: Máximo de iteraciones
        """
        generator = FractalGenerator(width=width, height=height)
        
        # Generar fractal según tipo
        if fractal_type == 'mandelbrot':
            data = generator.mandelbrot(max_iter=max_iter)
            title = f'251117_Fractal_Mandelbrot_Interactivo (iteraciones: {max_iter})'
            filename_base = f"{self.output_dir}/251117_Fractal_Mandelbrot_Interactivo"
        elif fractal_type == 'julia':
            data = generator.julia(c_real=-0.7, c_imag=0.27015, max_iter=max_iter)
            title = f'251117_Fractal_Julia_Interactivo (c=-0.7+0.27i, iter: {max_iter})'
            filename_base = f"{self.output_dir}/251117_Fractal_Julia_Interactivo"
        elif fractal_type == 'burning_ship':
            data = generator.burning_ship(max_iter=max_iter)
            title = f'251117_Fractal_BurningShip_Interactivo (iteraciones: {max_iter})'
            filename_base = f"{self.output_dir}/251117_Fractal_BurningShip_Interactivo"
        else:  # sierpinski
            data = generator.sierpinski_triangle(iterations=8)
            title = '251117_Fractal_Sierpinski_Interactivo'
            filename_base = f"{self.output_dir}/251117_Fractal_Sierpinski_Interactivo"
        
        # Normalizar datos para mejor visualización
        data_normalized = np.log(data + 1)
        
        # Crear figura interactiva
        fig = go.Figure(data=go.Heatmap(
            z=data_normalized,
            colorscale='Hot',
            showscale=True,
            colorbar=dict(
                title="Iteraciones<br>(log scale)",
                titleside="right",
                tickmode="linear",
                tick0=0,
                dtick=1
            ),
            hovertemplate='X: %{x}<br>Y: %{y}<br>Iteraciones: %{z:.2f}<extra></extra>'
        ))
        
        # Configurar layout interactivo
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial Black'}
            },
            xaxis=dict(
                title='Parte Real',
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                title='Parte Imaginaria',
                showgrid=False,
                zeroline=False,
                scaleanchor="x",
                scaleratio=1
            ),
            width=900,
            height=900,
            template='plotly_dark',
            hovermode='closest',
            dragmode='zoom',  # Permite hacer zoom arrastrando
            annotations=[
                dict(
                    text="Usa el mouse para hacer zoom y explorar<br>Doble clic para resetear vista",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=-0.1,
                    xanchor='center',
                    font=dict(size=12, color="white")
                )
            ]
        )
        
        # Guardar como HTML interactivo
        fig.write_html(
            f"{filename_base}.html",
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': filename_base.split('/')[-1],
                    'height': 1200,
                    'width': 1200,
                    'scale': 2
                }
            }
        )
        
        if self.has_kaleido:
            try:
                fig.write_image(f"{filename_base}.png", width=1200, height=1200, scale=2)
                print(f"\n✓ Fractal '{fractal_type}' generado exitosamente:")
                print(f"  - HTML interactivo: {filename_base}.html")
                print(f"  - PNG alta resolución: {filename_base}.png")
            except Exception as e:
                print(f"\n✓ Fractal '{fractal_type}' generado (solo HTML):")
                print(f"  - HTML interactivo: {filename_base}.html")
                print(f"  ⚠️  Error al exportar PNG: {e}")
        else:
            print(f"\n✓ Fractal '{fractal_type}' generado exitosamente:")
            print(f"  - HTML interactivo: {filename_base}.html")
            print(f"  - Abre el HTML en tu navegador para explorar interactivamente")
        
        # Mostrar en navegador
        fig.show()
        
        return fig
    
    def create_multi_fractal_dashboard(self):
        """Crea un dashboard con múltiples fractales para comparar"""
        print("\nGenerando dashboard interactivo con múltiples fractales...")
        
        generator = FractalGenerator(width=400, height=400)
        
        # Generar todos los fractales
        fractals = {
            'Mandelbrot': generator.mandelbrot(max_iter=150),
            'Julia': generator.julia(c_real=-0.7, c_imag=0.27015, max_iter=150),
            'Burning Ship': generator.burning_ship(max_iter=150),
            'Sierpinski': generator.sierpinski_triangle(iterations=8)
        }
        
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=list(fractals.keys()),
            horizontal_spacing=0.1,
            vertical_spacing=0.1
        )
        
        # Añadir cada fractal
        positions = [(1,1), (1,2), (2,1), (2,2)]
        for (name, data), (row, col) in zip(fractals.items(), positions):
            data_normalized = np.log(data + 1)
            
            fig.add_trace(
                go.Heatmap(
                    z=data_normalized,
                    colorscale='Hot',
                    showscale=False,
                    name=name,
                    hovertemplate=f'{name}<br>X: %{{x}}<br>Y: %{{y}}<br>Valor: %{{z:.2f}}<extra></extra>'
                ),
                row=row, col=col
            )
        
        # Configurar layout
        fig.update_layout(
            title={
                'text': '251117_Fractal_Dashboard_Comparativo',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'family': 'Arial Black'}
            },
            showlegend=False,
            width=1400,
            height=1400,
            template='plotly_dark'
        )
        
        # Quitar etiquetas de ejes
        fig.update_xaxes(showticklabels=False, showgrid=False)
        fig.update_yaxes(showticklabels=False, showgrid=False)
        
        # Guardar
        filename_base = f"{self.output_dir}/251117_Fractal_Dashboard_Comparativo"
        fig.write_html(f"{filename_base}.html")
        
        if self.has_kaleido:
            try:
                fig.write_image(f"{filename_base}.png", width=1600, height=1600, scale=2)
                print(f"\n✓ Dashboard generado exitosamente:")
                print(f"  - HTML interactivo: {filename_base}.html")
                print(f"  - PNG alta resolución: {filename_base}.png")
            except Exception as e:
                print(f"\n✓ Dashboard generado (solo HTML):")
                print(f"  - HTML interactivo: {filename_base}.html")
                print(f"  ⚠️  Error al exportar PNG: {e}")
        else:
            print(f"\n✓ Dashboard generado exitosamente:")
            print(f"  - HTML interactivo: {filename_base}.html")
            print(f"  - Abre el HTML en tu navegador para explorar")
        
        # Mostrar
        fig.show()
        
        return fig


def main():
    """Genera fractales interactivos con Plotly"""
    print("=" * 60)
    print("GENERADOR INTERACTIVO DE FRACTALES - PLOTLY")
    print("=" * 60)
    
    explorer = PlotlyFractalExplorer()
    
    # Generar fractales individuales interactivos
    print("\n[1/5] Generando Mandelbrot interactivo...")
    explorer.create_interactive_fractal('mandelbrot', max_iter=200)
    
    print("\n[2/5] Generando Julia interactivo...")
    explorer.create_interactive_fractal('julia', max_iter=200)
    
    print("\n[3/5] Generando Burning Ship interactivo...")
    explorer.create_interactive_fractal('burning_ship', max_iter=200)
    
    print("\n[4/5] Generando Sierpinski interactivo...")
    explorer.create_interactive_fractal('sierpinski')
    
    print("\n[5/5] Generando dashboard comparativo...")
    explorer.create_multi_fractal_dashboard()
    
    print("\n" + "=" * 60)
    print("¡COMPLETADO!")
    print("=" * 60)
    print("\nTodos los fractales se han guardado en 'fractal_outputs/'")
    print("Los archivos HTML se abrieron en tu navegador.")
    print("\nCONTROLES INTERACTIVOS:")
    print("  • Arrastrar: Hacer zoom en un área")
    print("  • Doble clic: Resetear vista")
    print("  • Scroll: Zoom in/out")
    print("  • Hover: Ver valores")
    print("  • Barra superior: Herramientas de pan, zoom, guardar imagen")


if __name__ == "__main__":
    main()
