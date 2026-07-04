import numpy as np
from strategies.dynamics import DynamicsModelInterface

class DifferentialDriveDynamics(DynamicsModelInterface):
    def __init__(self, r=1.0, b=1.0):
        self.r = r  
        self.b = b  

    def propagate(self, state, action, dt):
        x, y, theta = state
        v,w = action

        # vL = (1/self.r)*(v-w*self.b/2)
        # vR = (1/self.r)*(v+w*self.b/2) 
        
        new_x = x + v * np.cos(theta) * dt
        new_y = y + v * np.sin(theta) * dt
        new_theta = theta + w * dt

        return np.array([new_x, new_y, new_theta])