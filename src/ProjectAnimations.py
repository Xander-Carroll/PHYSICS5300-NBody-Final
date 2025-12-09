# This file can be used to create a manim animation of an orbit.
# Usage: python ./ProjectAnimations.py

## External library includes
import numpy as np
import manim as mn

## Include the numerical solution code.
from ProjectSolution import NBodyOrbit

## Include tools that will be used to build the animation.
from AnimationTools import FadingTrail

## Modifiable Parameters

# The animation details.
A_OUTPUT_NAME = "three-body.mp4"
A_FPS = 15
A_HEIGHT = 480
A_BODY_SIZE = 0.05
A_TRAIL_TIME = 0.8


## This class will be used to make the animation.
class NBodyAnimation(mn.Scene):
    def __init__(self, r0, v0, m, t_pts):
        super().__init__()
        
        self.r0 = r0
        self.v0 = v0
        self.m = m
        self.t_pts = t_pts

        self.r, self.v = NBodyOrbit.leapfrog_solve(r0, v0, m, t_pts, G=1.0, eps=1e-3)

    # Used for building the animation.
    def construct(self):
        # Get the number of bodies.
        n = self.r.shape[1]

        # Make the time tracker.
        t_tracker = mn.ValueTracker(0.0)

        # Add dots for each body.
        B_COLORS = [mn.RED, mn.BLUE, mn.YELLOW]
        dots = [mn.Dot(point=(self.r[0, i, 0], self.r[0, i, 1], 0.0), radius=A_BODY_SIZE * np.sqrt(m[i]), color=B_COLORS[i]) for i in range(n)]
        for dot in dots: 
            self.add(dot)

        # Add trails for each body.
        trails = [FadingTrail(dot, t_tracker, fade_time=A_TRAIL_TIME) for dot in dots]
        for trail in trails: self.add(trail)

        # Add the updater for each body.
        for i, dot in enumerate(dots):
            dot.add_updater(lambda d, i=i: d.move_to([
                np.interp(t_tracker.get_value(), t_pts, self.r[:,i,0]),
                np.interp(t_tracker.get_value(), t_pts, self.r[:,i,1]),
                0.0
            ]))

        # Animate: move dots along the orbit path.
        run_time = int(t_pts[-1] - t_pts[0])
        self.play(t_tracker.animate.set_value(run_time), run_time=run_time, rate_func=mn.linear)


# Create the animation.
if __name__ == '__main__':
    # Configure output
    mn.config.pixel_height = A_HEIGHT
    mn.config.frame_rate = A_FPS
    mn.config.output_file = A_OUTPUT_NAME
    mn.config.preview = True

    # The details for each body.
    m = [1.0, 1.0, 1.0]

    # Figure 8
    r0 = [[-1, 0], [1, 0], [0, 0]]
    v0 = [[0.347111, 0.532728], [0.347111, 0.532728], [-0.694222, -1.065456]]  

    # The length and time step of the solution.
    t_pts = np.arange(0, 10, 0.01)

    # Create and render the scene.
    scene = NBodyAnimation(r0, v0, m, t_pts)
    scene.render()