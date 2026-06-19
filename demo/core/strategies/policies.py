import numpy as np

class PoliciesInterface():
    def __init__(self,robot_drive_k, max_speed, min_speed, kick_radius, kick_force ):
        self.robot_drive_k = robot_drive_k
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.kick_radius = kick_radius
        self.kick_force = kick_force

    def wrap(self,angle):
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def compute_actions(self):
        raise NotImplementedError
        
class SoccerHeuristicPolicy(PoliciesInterface):
    def compute_actions(self):
        return
