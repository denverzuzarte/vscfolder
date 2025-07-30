from manim import *
import numpy as np
import matplotlib.pyplot as plt
from manim import ImageMobject, FadeIn

class ClaudeMandelbrotSet(Scene):  # Must inherit from Scene
    def construct(self):
        # Create mandelbrot function
        def mandelbrot(c, max_iter=100):
            z = 0
            for n in range(max_iter):
                if abs(z) > 2:
                    return n
                z = z*z + c
            return max_iter
        
        # Create the fractal
        resolution = 200
        x_min, x_max = -2.5, 1.5
        y_min, y_max = -2, 2
        
        x = np.linspace(x_min, x_max, resolution)
        y = np.linspace(y_min, y_max, resolution)
        X, Y = np.meshgrid(x, y)
        C = X + 1j*Y
        
        # Calculate mandelbrot values
        mandelbrot_set = np.zeros((resolution, resolution))
        for i in range(resolution):
            for j in range(resolution):
                mandelbrot_set[i, j] = mandelbrot(C[i, j])
        
        # Save as image file first
        plt.figure(figsize=(8, 8))
        plt.imshow(mandelbrot_set, extent=[x_min, x_max, y_min, y_max], 
                   cmap='hot', origin='lower')
        plt.axis('off')
        plt.savefig('mandelbrot.png', bbox_inches='tight', dpi=150)
        plt.close()
        
        # Create image mobject from file
        fractal_image = ImageMobject("mandelbrot.png")
        fractal_image.scale(2)
        
        self.play(FadeIn(fractal_image))
        self.wait(2)