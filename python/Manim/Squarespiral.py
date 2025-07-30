from manim import *
import math

class Squarespiral(Scene):
    def construct(self):
        # Create a squareadditions to implement
        square = Square(side_length=20, color=BLUE)
        self.play(Create(square))
        n= 15
        m=4
        #self.play(Transform(square, smaller_square))
        side_length_s=15
        # Create a fractal pattern by recursively adding smaller squares
        for i in range(n*m+1):
            side_length_s=side_length_s/(math.sin(PI/n)+math.cos(PI/n))
            smaller_square= Square(side_length=side_length_s, color=WHITE, stroke_width=side_length_s/2).move_to(square.get_center()).rotate_about_origin(PI/n * i)
            self.add(smaller_square)
            self.wait(0.1)
        self.wait(1)  # Wait for 2 seconds before ending the scene
if __name__ == "__main__":
    test=Squarespiral()
    test.render()