# This file can be used to create a manim animation of an orbit.
# Usage: python ./SolarSystenAnimation.py

## External library includes
import numpy as np
import manim as mn

## Include the numerical solution code.
from ProjectSolution import NBodyOrbit

## Modifiable Parameters

# The animation details.
A_OUTPUT_NAME = "solar-system-with-belt.mp4"
A_FPS = 60
A_HEIGHT = 1080
A_BODY_SIZE = 0.05
A_TRAIL_TIMES = [0.0, 0.1, 0.1, 0.1, 0.2, 1.0, 3.0, 5.0, 8.0]

N_ASTEROIDS = 1000

## This class will be used to make the animation.
class NBodyAnimation(mn.Scene):
    def __init__(self, r0, v0, m, t_pts):
        super().__init__()
        
        self.r0 = r0
        self.v0 = v0
        self.m = m
        self.t_pts = t_pts

        self.r, self.v = NBodyOrbit.leapfrog_solve(r0, v0, m, t_pts, G=1.0, eps=1e-10)

    # Used for building the animation.
    def construct(self):
        ## ---- Display the title first. ----
        title = mn.Text("Solar System Simulation", font_size=48)
        subtitle = mn.Text("AU25, Physics 5300, Xander Carroll", font_size=24)
        subtitle.next_to(title, mn.DOWN, buff=0.5)
        self.add(title, subtitle) 
        self.wait(3)
        self.play(mn.FadeOut(title, subtitle), run_time=1.0)


        ## ---- Display the coordinate axis second.
        axes = mn.Axes(
            x_range=[0, 1, 1],
            y_range=[0, 1, 1],
            x_length=4,
            y_length=4,
            tips=True
        )
        x_label = mn.MathTex(r"\hat{x}").next_to(axes.x_axis.get_end(), mn.RIGHT)
        y_label = mn.MathTex(r"\hat{y}").next_to(axes.y_axis.get_end(), mn.UP)
        self.play(mn.Create(axes), mn.Write(x_label), mn.Write(y_label))
        self.wait(3)
        self.play(mn.FadeOut(axes, x_label, y_label), run_time=1.0)


        ## ---- Then display the solar system case. ----
        objs = []

        # Get the number of bodies.
        n = self.r.shape[1]

        # Make the time tracker.
        t_tracker = mn.ValueTracker(0.0)

        # Add dots for each body.
        B_COLORS = [mn.RED, mn.GREY, mn.WHITE, mn.GREEN, mn.RED, mn.DARK_BROWN, mn.YELLOW, mn.BLUE_A, mn.BLUE]
        dots = []
        for i in range(n):
            if self.m[i] < 1e-8: 
                radius = A_BODY_SIZE/5
                color = mn.WHITE
            else: 
                radius = A_BODY_SIZE
                color = B_COLORS[i]
                

            dot = mn.Dot(point=(self.r[0, i, 0], self.r[0, i, 1], 0.0), radius=radius, color=color)
            dots.append(dot)
        
        for dot in dots: objs.append(dot)

        # Add trails for each body.
        for i in range(len(B_COLORS)):
            trail = mn.TracedPath(dots[i].get_center, stroke_color=dots[i].get_color(), stroke_width=2, stroke_opacity=0.3, dissipating_time=A_TRAIL_TIMES[i])
            objs.append(trail)            

        # Add the updater for each body.
        for i, dot in enumerate(dots):
            dot.add_updater(lambda d, i=i: d.move_to([
                np.interp(t_tracker.get_value(), t_pts, self.r[:,i,0]),
                np.interp(t_tracker.get_value(), t_pts, self.r[:,i,1]),
                0.0
            ]))

        # Add all of the bodies and trails to the scene.
        self.play(*(mn.FadeIn(obj) for obj in objs), run_time=1.0)

        # Animate: move dots along the orbit path.
        run_time = int(t_pts[-1] - t_pts[0])
        self.play(t_tracker.animate.set_value(run_time), run_time=run_time/2, rate_func=mn.linear)


# Create the animation.
if __name__ == '__main__':
    # Configure output
    mn.config.pixel_height = A_HEIGHT
    mn.config.frame_rate = A_FPS
    mn.config.output_file = A_OUTPUT_NAME
    mn.config.preview = True

    mn.config.frame_height = 16
    mn.config.frame_width = 16

    # The details for each body.
    m = [
        1.0,        # The Sun
        1.66E-7,    # Mercury
        2.45E-6,    # Venus
        3.00E-6,    # Earth
        3.23E-7,    # Mars
        9.55e-4,    # Jupiter
        2.86E-4,    # Saturn
        4.37E-5,    # Uranus
        5.15E-5     # Neptune
    ]

    r0 = [
        [0.0, 0.0],         # Sun
        [0.39, 0.0],        # Mercury
        [0.72, 0.0],        # Venus
        [1.0, 0.0],         # Earth
        [1.52, 0.0],        # Mars
        [5.20, 0.0],        # Jupiter
        [9.58, 0.0],        # Saturn
        [19.2, 0.0],        # Uranus
        [30.1, 0.0]         # Neptune
    ]

    v0 = [
        [0.0, 0.0],         # Sun
        [0.0, 1.601281],    # Mercury
        [0.0, 1.178511],    # Venus
        [0.0, 1.0],         # Earth
        [0.0, 0.811107],    # Mars
        [0.0, 0.438529],    # Jupiter
        [0.0, 0.323085],    # Saturn
        [0.0, 0.228217],    # Uranus
        [0.0, 0.182270]     # Neptune
    ]

    # Add asteroids to the belt.
    radii = np.random.uniform(2.0, 3.5, N_ASTEROIDS)
    angles = np.random.uniform(0, 2*np.pi, N_ASTEROIDS)

    speeds = np.sqrt(1.0 / radii)
    vx = -speeds * np.sin(angles)
    vy = speeds * np.cos(angles)

    asteroid_r0 = np.column_stack((radii * np.cos(angles), radii * np.sin(angles)))
    asteroid_v0 = np.column_stack((vx, vy))

    r0 = np.vstack([r0, asteroid_r0])
    v0 = np.vstack([v0, asteroid_v0])
    m.extend([1e-10] * N_ASTEROIDS)

    # Rescale the inital conditions to smaller units (units manim expects).
    sf = 0.4
    r0 = np.array(r0) * sf
    v0 = np.array(v0) / np.sqrt(sf)

    # The length and time step of the solution.
    t_pts = np.arange(0, 60, 0.001)

    # Create and render the scene.
    scene = NBodyAnimation(r0, v0, m, t_pts)
    scene.render()