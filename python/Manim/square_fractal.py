from manim import *
import math     
class SquareFractal(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = BLACK
        self.camera.frame_width = 10    
        self.camera.frame_height = 10
        self.camera.frame_center = ORIGIN
        self.camera.frame.save_state()
    def left_square(self, square, side_length_s):
        left
        return leftsquare
    def right_square(self, square, side_length_s):

    def construct(self):
        side_length_s = 3
        # Create a square
        square = Square(side_length=side_length_s, color=RED)

        self.play(Create(square))
        n = 3

        for i in range(n):
            corner1 = square.get_corner(UP + LEFT)  
            corner2 = square.get_corner(UP + RIGHT)
            side_length_s=side_length_s/2


if __name__ == "__main__":
    test = SquareFractal()
    test.render()