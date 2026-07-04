import numpy as np
from strategies.policies import PoliciesInterface
from strategies.Policies.PassOrShoot import PassOrShootPolicy




class GoToPointPolicy(PoliciesInterface):
    def __init__(self, robot_drive_k, max_speed, min_speed, kick_radius, kick_force):
       super().__init__(robot_drive_k, max_speed, min_speed, kick_radius, kick_force)
       self.action_policy = PassOrShootPolicy(robot_drive_k, max_speed, min_speed, kick_radius, kick_force)




    def compute_actions(self, own_robots,enemy_robots, ball, goal):
        actions = []
        
        shoot_vector = goal.center - ball.position
        shoot_dist = np.linalg.norm(shoot_vector) + 1e-5
        shoot_dir = shoot_vector / shoot_dist
        
        reach_distance = self.kick_radius
        target_point = ball.position - shoot_dir * (reach_distance * 0.97)
        
        for i, robot in enumerate(own_robots):
            u_des = target_point - robot.state[:2]
            dist_to_target = np.linalg.norm(u_des)
            
            weight_shoot = max(0.0, 1.0 - dist_to_target / 20.0) 
            
            u_des_dir = u_des / (dist_to_target + 1e-5)
            
            combined_dir = (1.0 - weight_shoot) * u_des_dir + weight_shoot * shoot_dir
            
            theta_des = np.arctan2(combined_dir[1], combined_dir[0])
            
            if dist_to_target > 0.07:
                u_clamped = min(dist_to_target * 1.5, self.max_speed)
            else:
                u_clamped = 0
            
            head_err = self.wrap(theta_des - robot.state[2])
            omega = self.robot_drive_k * head_err
            
            
            actions.append(np.array([u_clamped, omega]))
            
        return actions