import numpy as np
# from entities.world import World

class Policies():

    def compute_actions(self, robots, ball):
        raise NotImplementedError
    
    # def check_rules(self,robots,ball,world):
    #     world_rules = world
    #     for robot in robots:
    #         if robot.state[0] < 0 or robot.state[0] > world.dim[0]:
    #             return False
    #         if robot.state[1] < 0 or robot.state[1] > world.dim[1]:
    #             return False
    #     if ball.position[0] < 0 or ball.position[0] > world.dim[0]:
    #         return False
    #     if ball.position[1] < 0 or ball.position[1] > world.dim[1]:
    #         return False
    #     return True


    

class GoToPointPolicy(Policies):
    def __init__(self, robot_drive_k=2.0, max_speed = 25.0, min_speed = 0.0):
        self.robot_drive_k = robot_drive_k
        self.max_speed = max_speed
        self.min_speed = min_speed



    def compute_actions(self, robots, ball, target_point = None):
        if target_point is None:
            target_point = ball.position
        for i, robot in enumerate(robots):
            u_des= target_point - robot.state[:2]
            theta_des = np.arctan2(u_des[1], u_des[0])
            head_err = theta_des - robot.state[2]
            head_err = wrap(head_err)
            omega = self.robot_drive_k * head_err
            u_raw = np.linalg.norm(u_des)
            u_clamped = max(0, min(u_raw, self.max_speed))
            yield np.array([u_clamped, omega])

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
        return []
    

def wrap(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi