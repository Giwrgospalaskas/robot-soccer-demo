import numpy as np
from strategies.dynamics import DynamicsModelInterface

class DiffernetialDriveDynamicsWithActuationNoise(DynamicsModelInterface):
    def __init__(self, r=1.0, b=1.0):
        self.r = r  
        self.b = b  
        self.noise = 0.000002

    def propagate(self, state, action, dt):
        x, y, theta = state
        v, w = action
        # vl_with_noise = vl + np.random.normal(0, self.noise)
        # vr_with_noise = vr + np.random.normal(0, self.noise)

        # v = (self.r / 2.0) * (vr_with_noise + vl_with_noise)
        # w = (self.r / self.b) * (vr_with_noise - vl_with_noise)

        new_x = x + v * np.cos(theta) * dt
        new_y = y + v * np.sin(theta) * dt
        new_theta = theta + w * dt

        return np.array([new_x, new_y, new_theta])