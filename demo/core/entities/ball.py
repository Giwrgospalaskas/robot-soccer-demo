import numpy as np

class Ball():
    def __init__(self, px, py, vx, vy):
        self.position = np.array([px, py], dtype=float)
        self.velocity = np.array([vx, vy], dtype=float)
        self.friction = 0.99  # Simple velocity decay (alpha)

    def step(self, dt):
        self.position += self.velocity * dt
        self.velocity *= self.friction
