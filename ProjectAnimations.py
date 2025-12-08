# This file can be used to create a manim animation of an orbit.
# Usage: manim -pq<x> ProjectAnimations.py NBodyAnimation    ; replace <x> with l=low, m=medium, or h=high


## External library includes
import numpy as np
import manim as mn


## Include the numerical solution code.
from ProjectSolution import NBodyOrbit


## Modifiable Parameters

# The details for each body.
m = [1.0, 1.0, 1.0]
r0 = [[-0.970004,  0.243087, 0.0], [ 0.970004, -0.243087, 0.0], [ 0.000000,  0.000000, 0.0]]
v0 = [[-0.466203, -0.432365, 0.0], [-0.466203, -0.432365, 0.0], [ 0.932407,  0.864731, 0.0]]

# The length and time step of the solution.
t_pts = np.linspace(0, 20, 2000)


## This class will be used to make the animation.
class NBodyAnimation(mn.Scene):
    def construct(self):
        ## Solve the problem.
        r, _ = NBodyOrbit.leapfrog_solve(r0, v0, m, t_pts, G=1.0, eps=1e-3)

        # Get the number of bodies.
        n = r.shape[1]

        # Get the number of frames.
        nt = len(t_pts)

        # Make the time tracker.
        t_tracker = mn.ValueTracker(0.0)

        # Add dots for each body.
        dots = [mn.Dot(point=(r[0, i, 0], r[0, i, 1], 0.0)) for i in range(n)]
        for dot in dots: 
            self.add(dot)

        # Add trails for each body.
        trails = [mn.TracedPath(dot.get_center, stroke_color=dot.get_color(), stroke_width=2) for dot in dots]
        for trail in trails: self.add(trail)

        # Add the update for each body.
        for i, dot in enumerate(dots):
            dot.add_updater(lambda d, i=i: d.move_to([
                np.interp(t_tracker.get_value(), t_pts, r[:,i,0]),
                np.interp(t_tracker.get_value(), t_pts, r[:,i,1]),
                0.0
            ]))

        # Animate: move dots along the orbit path.
        run_time = int(t_pts[-1] - t_pts[0])
        self.play(t_tracker.animate.set_value(run_time), run_time=run_time, rate_func=mn.linear)
        self.wait(1)