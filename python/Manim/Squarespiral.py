from manim import *
import math

class FractalTest(Scene):
    def construct(self):
        # Create a square
        square = Square(side_length=20, color=BLUE)
        self.play(Create(square))
        n= 100
        #self.play(Transform(square, smaller_square))
        side_length_s=8.5
        # Create a fractal pattern by recursively adding smaller squares
        for i in range(n+1):
            side_length_s=side_length_s/(math.sin(PI/n)+math.cos(PI/n))
            smaller_square= Square(side_length=side_length_s, color=WHITE).move_to(square.get_center()).rotate_about_origin(PI/n * i)
            self.play(Create(smaller_square))
        self.wait(1)  # Wait for 2 seconds before ending the scene
if __name__ == "__main__":
    test=FractalTest()
    test.render()