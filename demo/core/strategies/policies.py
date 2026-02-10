import numpy as np
from entities.world import World

class Policies():
    def compute_actions(self, robots, ball):
        raise NotImplementedError
    
    def check_rules(self,robots,ball,world):
        world_rules = world
        for robot in robots:
            if robot.state[0] < 0 or robot.state[0] > world.dim[0]:
                return False
            if robot.state[1] < 0 or robot.state[1] > world.dim[1]:
                return False
        if ball.position[0] < 0 or ball.position[0] > world.dim[0]:
            return False
        if ball.position[1] < 0 or ball.position[1] > world.dim[1]:
            return False
        return True


    

class GoToPointPolicy(Policies):
    def __init__(self, target_point=None):
        self.target_point = target_point
        self.robot_speed = 1000.0
        self.theta_error = 0.005


    def compute_actions(self, robots, ball):
        if self.target_point is None:
            self.target_point = ball.position
        for i, robot in enumerate(robots):
            direction = self.target_point - robot.state[:2]
            theta_goal = np.arctan2(direction[1], direction[0])
            theta_diff = theta_goal - robot.state[2]
            if theta_diff > 0+self.theta_error:
                vL = 0
                vR = self.robot_speed
            elif theta_diff < 0 - self.theta_error:
                vL = self.robot_speed
                vR = 0
            else:
                vL = self.robot_speed
                vR = self.robot_speed
            print(theta_diff)
            yield np.array([vL, vR])

class FormationConsensusPolicy(Policies):
    def __init__(self):
        pass

    def compute_actions(self, robots, ball):
        pass
        return []

class ManualControlPolicy(Policies):
    def __init__(self):
        pass

    def compute_actions(self, robots, ball):