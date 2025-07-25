from manim import *
import math     
class SquareFractal(Scene):
    '''def construct(self):
        side_length_s = 2
        # Create a square
        square = Square(side_length=side_length_s, color=RED)

        self.play(Create(square))
        n = 3

        for i in range(n):
            corner1 = square.get_corner(UP + LEFT)  
            corner2 = square.get_corner(UP + RIGHT) '''

    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait(1)

if __name__ == "__main__":
    test = SquareFractal()
    test.render()