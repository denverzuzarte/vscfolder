from manim import *

class PointMovingOnShapes(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(UP)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        #self.play(MoveAlongPath(dot2, circle), run_time=2, rate_func=linear)
        self.remove(dot)
        self.play(Rotating(dot2, about_point=[0, 0, 0]), run_time=2)
        self.wait(1)

if __name__ == "__main__":
    test = PointMovingOnShapes()
    test.render()