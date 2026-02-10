import numpy as np

class DynamicsModelInterface():

    def propagate(self, state, action, dt):
        raise NotImplementedError

    def state_dim(self) -> int:
        return 3

class DifferentialDriveDynamics(DynamicsModelInterface):
    def __init__(self, r=1.0, b=1.0):
        self.r = r  # Wheel radius
        self.b = b  # Wheel base

    def propagate(self, state, action, dt):
        # state: [x, y, theta]
        # action: [v, omega]
        x, y, theta = state
        v,w = action

        vL = (1/self.r)*(v-w*self.b/2)
        vR = (1/self.r)*(v+w*self.b/2) 

        # Discrete time update (Page 2 of PDF)
        new_x = x + v * np.cos(theta) * dt
        new_y = y + v * np.sin(theta) * dt
        new_theta = theta + w * dt

        return np.array([new_x, new_y, new_theta])
    
class DiffernetialDriveDynamicsWithActuationNoise(DynamicsModelInterface):
    def __init__(self, r=1.0, b=1.0):
        self.r = r  # Wheel radius
        self.b = b  # Wheel base

    def propagate(self, state, action, dt):
        x, y, theta = state
        vl, vr = action
        vl_with_noise = vl + np.random.normal(0, self.noise)
        vr_with_noise = vr + np.random.normal(0, self.noise)

        v = (self.r / 2.0) * (vr + vl)
        w = (self.r / self.b) * (vr - vl)

        # Discrete time update (Page 2 of PDF)
        new_x = x + v * np.cos(theta) * dt
        new_y = y + v * np.sin(theta) * dt
        new_theta = theta + w * dt

        return np.array([new_x, new_y, new_theta])
