import numpy as np

class Robot():
    def __init__(self, px, py, theta, team, robot_id, wheel_radius, wheel_base, body_radius):
        self.state = np.array([px, py, theta], dtype=float)
        self.team = team
        self.robot_id = robot_id
        self.wheel_radius = wheel_radius
        self.wheel_base = wheel_base
        self.body_radius = body_radius


