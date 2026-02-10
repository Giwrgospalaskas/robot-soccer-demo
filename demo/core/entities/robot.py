import numpy as np

class Robot():
    def __init__(self, px=50.0, py=50.0, theta=0.0):
        self.state = np.array([px, py, theta], dtype=float)
