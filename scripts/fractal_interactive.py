"""
Generador Interactivo de Fractales
Permite explorar diferentes parámetros y regiones de los fractales
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from fractal_generator import FractalGenerator, FractalVisualizer
import os

class InteractiveFractalExplorer:
    """Explorador interactivo de fractales con controles deslizantes"""
    
    def __init__(self):
        self.generator = FractalGenerator(width=400, height=400)
        self.current_fractal_type = 'mandelbrot'
        self.output_dir = "fractal_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Parámetros iniciales
        self.params = {
            'max_iter': 100,
            'julia_real': -0.7,
            'julia_imag': 0.27015,
            'xmin': -2.5,
            'xmax': 1.5,
            'ymin': -2.0,
            'ymax': 2.0
        }
        
        self.setup_plot()
    
    def setup_plot(self):
        """Configura la interfaz gráfica interactiva"""
        self.fig = plt.figure(figsize=(14, 8))
        
        # Área principal del fractal
        self.ax_main = plt.subplot2grid((4, 3), (0, 0), rowspan=4, colspan=2)
        
        # Controles
        ax_type = plt.subplot2grid((4, 3), (0, 2))
        ax_iter = plt.subplot2grid((4, 3), (1, 2))
        ax_julia_real = plt.subplot2grid((4, 3), (2, 2))
        ax_julia_imag = plt.subplot2grid((4, 3), (3, 2))
        
        ax_save = plt.axes([0.7, 0.02, 0.15, 0.04])
        self.btn_save = Button(ax_save, 'Guardar Fractal')
        self.btn_save.on_clicked(self.save_current_fractal)
        
        # Radio buttons para tipo de fractal
        self.radio = RadioButtons(ax_type, ('Mandelbrot', 'Julia', 'Burning Ship'))
        self.radio.on_clicked(self.change_fractal_type)
        
        # Sliders
        self.slider_iter = Slider(ax_iter, 'Iteraciones', 10, 300, 
                                  valinit=self.params['max_iter'], valstep=10)
        self.slider_julia_real = Slider(ax_julia_real, 'Julia Real', -1.5, 1.5, 
                                        valinit=self.params['julia_real'], valfmt='%.3f')
        self.slider_julia_imag = Slider(ax_julia_imag, 'Julia Imag', -1.5, 1.5, 
                                        valinit=self.params['julia_imag'], valfmt='%.3f')
        
        # Conectar eventos
        self.slider_iter.on_changed(self.update)
        self.slider_julia_real.on_changed(self.update)
        self.slider_julia_imag.on_changed(self.update)
        
        # Generar fractal inicial
        self.update(None)
        
        plt.show()
    
    def change_fractal_type(self, label):
        """Cambia el tipo de fractal"""
        self.current_fractal_type = label.lower().replace(' ', '_')
        self.update(None)
    
    def save_current_fractal(self, event):
        """Guarda el fractal actual en PNG y HTML"""
        max_iter = int(self.slider_iter.val)
        julia_real = self.slider_julia_real.val
        julia_imag = self.slider_julia_imag.val
        
        # Generar con mayor resolución
        high_res_gen = FractalGenerator(width=800, height=800)
        
        if self.current_fractal_type == 'mandelbrot':
            data = high_res_gen.mandelbrot(max_iter=max_iter)
            filename = f"{self.output_dir}/251117_Fractal_Mandelbrot_Custom"
            title = f'Mandelbrot (iter={max_iter})'
        elif self.current_fractal_type == 'julia':
            data = high_res_gen.julia(c_real=julia_real, c_imag=julia_imag, max_iter=max_iter)
            filename = f"{self.output_dir}/251117_Fractal_Julia_Custom"
            title = f'Julia: c = {julia_real:.3f} + {julia_imag:.3f}i (iter={max_iter})'
        else:
            data = high_res_gen.burning_ship(max_iter=max_iter)
            filename = f"{self.output_dir}/251117_Fractal_BurningShip_Custom"
            title = f'Burning Ship (iter={max_iter})'
        
        # Guardar sin mostrar
        FractalVisualizer.plot_fractal(data, title, colormap='sunset', filename_base=filename)
        plt.close()  # Cerrar la ventana de guardado
        
        print(f"\n¡Fractal guardado exitosamente!")
        print(f"  - PNG: {filename}.png")
        print(f"  - HTML: {filename}.html\n")
    
    def update(self, val):
        """Actualiza el fractal con nuevos parámetros"""
        self.ax_main.clear()
        
        # Obtener valores actuales
        max_iter = int(self.slider_iter.val)
        julia_real = self.slider_julia_real.val
        julia_imag = self.slider_julia_imag.val
        
        # Generar fractal según tipo
        if self.current_fractal_type == 'mandelbrot':
            data = self.generator.mandelbrot(max_iter=max_iter)
            title = f'Mandelbrot (iter={max_iter})'
        elif self.current_fractal_type == 'julia':
            data = self.generator.julia(c_real=julia_real, c_imag=julia_imag, 
                                       max_iter=max_iter)
            title = f'Julia: c = {julia_real:.3f} + {julia_imag:.3f}i (iter={max_iter})'
        else:  # burning_ship
            data = self.generator.burning_ship(max_iter=max_iter)
            title = f'Burning Ship (iter={max_iter})'
        
        # Visualizar
        data_normalized = np.log(data + 1)
        cmap = FractalVisualizer.create_colormap('sunset')
        
        self.ax_main.imshow(data_normalized, cmap=cmap, 
                           interpolation='bilinear', origin='lower')
        self.ax_main.set_title(title, fontsize=14, fontweight='bold')
        self.ax_main.axis('off')
        
        self.fig.canvas.draw_idle()


def main():
    """Inicia el explorador interactivo"""
    print("Iniciando Explorador Interactivo de Fractales...")
    print("Usa los controles para cambiar el tipo de fractal y sus parámetros")
    print("Haz clic en 'Guardar Fractal' para exportar en PNG y HTML")
    
    explorer = InteractiveFractalExplorer()


if __name__ == "__main__":
    main()
