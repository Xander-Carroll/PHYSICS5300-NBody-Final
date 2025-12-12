# This file can be used to create a manim animation of an orbit.
# Usage: python ./ProjectAnimations.py

## External library includes
import numpy as np
import manim as mn

## Include the numerical solution code.
from ProjectSolution import NBodyOrbit

## Modifiable Parameters

# The animation details.
A_OUTPUT_NAME = "three-body.mp4"        # The name of the video that will be produced.
A_FPS = 60                              # The FPS that the video should run at.
A_HEIGHT = 1080                         # The height of the video in pixels.
A_RUN_TIME = 25                         # How many seconds the output video should be.
A_NUM_PERIODS = 2.5                     # How many periods should be shown in the video.
A_BODY_SIZE = 0.05                      # The size of the bodies in the video.
A_TRAIL_SIZE = 0.50                     # The length of the trail as a percentage of the period.



class NBodyAnimation(mn.Scene):
    def __init__(self, r0_cases, v0_cases, periods, run_time=20):
        super().__init__()
        
        self.r0_cases = r0_cases
        self.v0_cases = v0_cases
        self.periods = periods
        self.run_time = run_time
        self.trail_time = A_TRAIL_SIZE / A_NUM_PERIODS * self.run_time
        self.m = [1.0, 1.0, 1.0]

        # Solve all cases and store animation times
        self.solutions = []
        self.t_anims = []

        for r0_case, v0_case, period in zip(self.r0_cases, self.v0_cases, self.periods):
            # Simulate three periods for each case.
            t_pts = np.arange(0, A_NUM_PERIODS * period, 0.001)
            r, v = NBodyOrbit.leapfrog_solve(r0_case, v0_case, self.m, t_pts, G=1.0, eps=1e-3)

            # Rescale the positions to be in the range [-1, 1]
            max_val = np.max(np.abs(r))
            r_scaled = r / max_val

            # Store the solution.
            self.solutions.append((r_scaled, v))

            # Rescale the simulation time to animation time.
            t_anim = np.linspace(0, self.run_time, len(t_pts))
            self.t_anims.append(t_anim)

    def construct(self):
        ## ---- Display the title first. ----
        title = mn.Text("Periodic Solutions For the 3-Body Problem", font_size=48)
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

        ## ---- Then display the grid of 3-body cases. ----
        n_cases = len(self.solutions)
        n_bodies = len(self.m)

        # calculate the possible grid_positions
        grid_size = int(np.ceil(np.sqrt(n_cases)))
        cell_size = 3
        grid_positions = []
        for idx in range(n_cases):
            row = idx // grid_size
            col = idx % grid_size
            x = (col - (grid_size-1)/2) * cell_size
            y = ((grid_size-1)/2 - row) * cell_size
            grid_positions.append(mn.RIGHT*x + mn.UP*y)

        # Create the time tracker.
        t_tracker = mn.ValueTracker(0.0)

        # The possible colors for each body.
        B_COLORS = [mn.RED, mn.BLUE, mn.YELLOW]

        # Create objects for each solution and add it to the grid.
        objs = []
        for case_idx, (r, _) in enumerate(self.solutions):
            pos_shift = grid_positions[case_idx]
            t_anim = self.t_anims[case_idx]

            # Add dots for each body
            dots = [
                mn.Dot(point=(r[0,i,0], r[0,i,1], 0.0), radius=A_BODY_SIZE*np.sqrt(self.m[i]), color=B_COLORS[i])
                for i in range(n_bodies)
            ]
            for dot in dots:
                dot.shift(pos_shift)
                objs.append(dot)

            # Add fading trails            
            trails = [mn.TracedPath(dot.get_center, stroke_color=dot.get_color(), stroke_width=2, stroke_opacity=0.3, dissipating_time=self.trail_time) for dot in dots]
            for trail in trails: objs.append(trail)

            # Updaters
            for j, dot in enumerate(dots):
                dot.add_updater(lambda d, j=j, r=r, t_anim=t_anim, shift=pos_shift: d.move_to([
                    np.interp(t_tracker.get_value(), t_anim, r[:,j,0] + shift[0]),
                    np.interp(t_tracker.get_value(), t_anim, r[:,j,1] + shift[1]),
                    0.0
                ]))

    
        # Add all of the bodies and trails to the scene.
        self.play(*(mn.FadeIn(obj) for obj in objs), run_time=1.0)

        # Play the animation.
        self.play(t_tracker.animate.set_value(self.run_time), run_time=self.run_time, rate_func=mn.linear)



# Create the animation.
if __name__ == '__main__':
    # Configure output
    mn.config.pixel_height = A_HEIGHT
    mn.config.frame_rate = A_FPS
    mn.config.output_file = A_OUTPUT_NAME
    mn.config.preview = True

    mn.config.frame_height = 16
    mn.config.frame_width = 16

    # The periodic cases.
    r0 = [
        [[1, 0], [-0.5, 0.866025], [-0.5, -0.866025]],                                              # Circle
        [[-1, 0], [1, 0], [0, 0]],                                                                  # Figure 8
        [[ 0.666163752, -0.08192185], [-0.02519266368, 0.4544485758], [-0.1030132, -0.76580620]],   # Traingles
        [[0.8733047091, 0], [-0.6254030288, 0], [-0.2479016803, 0]],                                # Broucke R4
        [[-0.989262, 0], [2.209617, 0], [-1.220355, 0]],                                            # Broucke A1
        [[-0.1095519101, 0], [1.6613533905, 0], [-1.5518014804, 0]],                                # Broucke A7
        [[0.0132604844, 0], [1.4157286016, 0], [-1.4289890859, 0]],                                 # Broucke A11
        [[-0.5426216182, 0], [2.5274928067, 0], [-1.9848711885, 0]],                                # Broucke A10
        [[-0.8965015243, 0], [3.2352526189, 0], [-2.3387510946, 0]],                                # Broucke A13
    ]

    v0 = [
        [[0, 0.759836], [-0.658037, -0.379918], [0.658037, -0.379918]],             # Circle
        [[0.347111, 0.532728], [0.347111, 0.532728], [-0.694222, -1.065456]],       # Figure 8
        [[0.841202, 0.029746], [0.142642, -0.492315], [-0.983845,  0.462569]],      # Traingles
        [[0, 1.0107764436], [0, -1.6833533458], [0, 0.6725769022]],                 # Broucke R4
        [[0, 1.916924], [0, 0.191026], [0, -2.107951]],                             # Broucke A1
        [[0, 0.9913358338], [0, -0.1569959746], [0, -0.8343398592]],                # Broucke A7
        [[0, 1.054151921], [0, -0.2101466639], [0, -0.8440052572]],                 # Broucke A11
        [[0, 0.8750200467], [0, -0.0526955841], [0, -0.8223244626]],                # Broucke A10
        [[0, 0.8285556923], [0, -0.0056478094], [0, -0.8229078829]],                # Broucke A13
    ]

    periods = [
        8.26913690,     # Circle
        6.324449,       # Figure 8
        3.8207613,      # Traingles
        5.395826,       # Broucke R4
        6.283213,       # Broucke A1
        12.055859,      # Broucke A7
        32.584945,      # Broucke A11
        32.610953,      # Broucke A10
        59.716075,      # Broucke A13
    ]


    # Create and render the scene.
    scene = NBodyAnimation(r0, v0, periods, run_time=A_RUN_TIME)
    scene.render()