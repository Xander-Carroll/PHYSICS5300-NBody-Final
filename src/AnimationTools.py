## Standard library includes
from collections import deque


## External library includes
import numpy as np
import manim as mn


## This class can be used to make a trail that fades behind the bodies.
class FadingTrail(mn.VMobject):
    def __init__(self, target, t_tracker, fade_time=1.0, width=2, **kwargs):
        # Call the parent constructor.
        super().__init__(**kwargs)

        self.target = target
        self.t_tracker = t_tracker
        self.fade_time = fade_time
        self.buffer = deque()
        self.set_stroke(target.get_color(), width=width)
        self.buffer.append((self.target.get_center(), t_tracker.get_value()))

        self.add_updater(self._update_trail)
    
    def _update_trail(self, trail: mn.VMobject):
        now = self.t_tracker.get_value()

        self.buffer.append((self.target.get_center(), now))
        while self.buffer and (now - self.buffer[0][1]) > self.fade_time: 
            self.buffer.popleft()

        pts = [p[0] for p in self.buffer]
        trail.set_points_as_corners(pts)

        ages = np.array([now - t for (_, t) in self.buffer])
        alpha = 1.0 - np.clip(ages / self.fade_time, 0, 1)
        trail.set_stroke(opacity=alpha)


## Tell the user that they are using this file incorrectly.
if __name__ == '__main__':
    print("[NOTICE]: This file should be included and used in your project. It should not be run as a stand-alone script.")