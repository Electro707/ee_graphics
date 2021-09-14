from manim import *
import manim


class BisectionMethod(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.7,
            zoomed_display_height=3,
            zoomed_display_width=3,
            image_frame_stroke_width=10,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    @staticmethod
    def _func(x: float):
        return x**2 - 2

    def _bisection_method(self, x1, x2):
        x_mid = (x1+x2)/2

        if self._func(x1)*self._func(x_mid) < 0:
            x2 = x_mid
            # Otherwise adjust the left interval to the middle
        else:
            x1 = x_mid

        return x1, x2, x_mid

    def construct(self):
        x1 = 1
        x2 = 2

        ax = Axes(
            x_range=[0, 3], axis_config={"include_tip": False}
        )
        labels = ax.get_axis_labels()

        graph = ax.get_graph(self._func, color=MAROON)

        value_ts = {
            'x1': ValueTracker(x1),
            'x2': ValueTracker(x2),
            }
        dots = {'prev_x': []}
        for k in value_ts:
            dots[k] = Dot(point=[ax.coords_to_point(value_ts[k].get_value(), self._func(value_ts[k].get_value()))])
            dots[k].add_updater(lambda x, k=k: x.move_to(ax.c2p(value_ts[k].get_value(), self._func(value_ts[k].get_value()))))

        all_dots = VGroup(dots['x1'], dots['x2'])

        self.play(Create(ax))
        self.play(Create(graph))

        self.wait(0.25)

        self.play(FadeIn(all_dots))

        self.zoomed_camera.frame.move_to(ax.coords_to_point(1.41, self._func(1.41)))
        self.activate_zooming(animate=True)

        for i in range(7):
            x1_prev, x2_prev = x1, x2
            x1, x2, xmid = self._bisection_method(x1, x2)

            if x1 != x1_prev:
                index = 'x1'
            else:
                index = 'x2'
                
            mid_dot = Dot(point=[ax.coords_to_point(xmid, self._func(xmid))], color=BLUE)
            mid_dot.width=dots[index].width
            self.play(Create(mid_dot))

            prev_dot = Dot(point=[ax.coords_to_point(value_ts[index].get_value(), self._func(value_ts[index].get_value()))])
            prev_dot.width=dots[index].width

            self.add(prev_dot)
            print(dots[index].radius, dots[index].radius*0.5)

            self.play(*[
                value_ts[index].animate.set_value(xmid),
                prev_dot.animate.set_fill(ORANGE),
                dots[index].animate.set_width(dots[index].width*(10-i)*0.75/10),
                self.zoomed_camera.frame.animate.scale(0.75),
                FadeOut(mid_dot)
                ])
            #self.play(*[dots[i].animate.set(radius=dots[i].radius/2) for i in ['x1', 'x2']])
            #[dots[i].animate.set(color=RED) for i in ['x1', 'x2']]

            dots['prev_x'].append(prev_dot)
            self.wait(0.5)
