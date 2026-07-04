import numpy as np

class Goal():
    def __init__(self, px, py, size,team):
        self.position = np.array([px, py], dtype=float)
        self.size = size
        self.center = np.array([px, py+size["length"]/2], dtype=float)
        self.team = team