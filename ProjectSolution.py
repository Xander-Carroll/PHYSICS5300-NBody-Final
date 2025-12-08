# This file contains a class which can be used to solve the N-Body problem numerically. 
# It is an adapted version of the code shown in "FinalProject.ipynb".


# External library include
import numpy as np

# A static class which contains the methods used to solve the N-Body problem numerically.
class NBodyOrbit:
    @staticmethod
    def accelerations(r, m, G=1.0, eps=1e-3):
        """
        Given the position of each body, computes the acceleration using the equations of motion.

        Parameters
        ----------
        r   : float tuple array : positions [(rx1, ry1, rz1), ...]
        m   : float array       : masses [m1, m2, ...]
        G   : float             : gravitational constant
        eps : float             : softening parameter

        Return
        ----------
        return : float tuple array : accelerations [(ax1, ay1, az1), ...]
        """

        # Compute ri - rj.
        rij = r[:, None, :] - r[None, :, :]

        # Compute the 1/rij^3 between all pairs (with eps as a softening parameter).
        d3 = (np.sum(rij**2, axis=-1) + eps**2) ** -1.5

        # Compute acceleration.
        a = np.sum((-G * m[None, :] * d3)[:, :, None] * rij, axis=1)

        return a

    @staticmethod
    def leapfrog_solve(r0, v0, m, t_pts, G=1.0, eps=1e-3):
        """
        Returns filled arrays r0 and v0 which correspond to each time step in t_pts.

        Parameters
        ----------
        r0      : float tuple array : initial positions [(rx1, ry1, rz1), ...]
        v0      : float tuple array : initial velocities [(vx1, vy1, vz1), ...]
        m       : float array       : masses [m1, m2, ...]
        t_pts   : float array       : an array of evenly spaced time steps when positions and velocites should be found.
        G       : float             : gravitational constant
        eps     : float             : softening parameter

        Return
        ----------
        return[0] : float tuple array : positions [(rx1, ry1, rz1), ...]
        return[1] : float tuple array : velocities [(vx1, vy1, vz1), ...]
        """

        # Convert the input to numpy arrays.
        m = np.array(m)
        r0 = np.array(r0, dtype=float)
        v0 = np.array(v0, dtype=float)

        # Sanity check.
        if len(r0) != len(v0):
            print("[ERROR]: The position array and velocity array must have the same number of bodies!")
            return None, None

        # Determine the time-step.
        dt = t_pts[1] - t_pts[0]

        # Initalize the arrays.
        n, dim = r0.shape
        nt = len(t_pts)

        r = np.zeros((nt, n, dim))
        v = np.zeros((nt, n, dim))

        # Use the initial conditions.
        r[0] = r0
        v[0] = v0

        # Apply the leapfrog algorithm.
        for i in np.arange(nt-1):
            v_half = v[i] + NBodyOrbit.accelerations(r[i], m, G, eps) * dt * 0.5        # Update the velocity by a half step.
            r[i+1] = r[i] + v_half * dt                                                 # Update the position.
            v[i+1] = v_half + NBodyOrbit.accelerations(r[i+1], m, G, eps) * dt * 0.5    # Update the velocity by a half step.

        # Return the updated results.
        return r, v


# Tell the user that they are using this file incorrectly.
if __name__ == '__main__':
    print("[NOTICE]: This file should be included and used in your project. It should not be run as a stand-alone script.")