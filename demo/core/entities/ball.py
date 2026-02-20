import numpy as np

class Ball():
    def __init__(self, px, py, vx, vy, friction, radius):
        self.position = np.array([px, py], dtype=float)
        self.velocity = np.array([vx, vy], dtype=float)
        self.friction = friction  # Simple velocity decay (alpha)
        self.radius = radius

    def step(self, dt):
        self.position += self.velocity * dt
        self.velocity[0] *= self.friction * dt
        self.velocity[1] *= self.friction * dt

    def apply_kick(self,kick_force):
        self.velocity += kick_force