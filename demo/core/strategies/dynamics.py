import numpy as np

class DynamicsModelInterface():

    def propagate(self, state, action, dt):
        raise NotImplementedError

    def state_dim(self) -> int:
        return 3