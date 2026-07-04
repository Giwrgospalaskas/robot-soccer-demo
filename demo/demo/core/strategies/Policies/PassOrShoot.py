import numpy as np
from strategies.policies import PoliciesInterface

class PassOrShootPolicy(PoliciesInterface):
    def __init__(self, robot_drive_k, max_speed, min_speed, kick_radius, kick_force):
         super().__init__(robot_drive_k, max_speed, min_speed, kick_radius, kick_force)
   
    def compute_actions(self, own_robots, enemy_robots, ball, goal):
        striker = own_robots[0]
        striker_pos = striker.state[:2]
        striker_theta = striker.state[2]
        
        d_heading = np.array([np.cos(striker_theta), np.sin(striker_theta)])
        
        w_g = 2.0  
        w_o = 5.0  
        
        candidates = [("shoot", goal.center, None)]
        
        
        for teammate in own_robots[1:]:  
            candidates.append(("pass", teammate.state[:2], teammate.robot_id))
            
        best_score = -float('inf')
        best_candidate = None
        
        for c_type, target_pos, teammate_id in candidates:
            to_target = target_pos - ball.position
            dist_to_target = np.linalg.norm(to_target) + 1e-5
            d_target = to_target / dist_to_target
            
            max_obs = -1.0  
            for enemy in enemy_robots:
                to_enemy = enemy.state[:2] - ball.position
                dist_to_enemy = np.linalg.norm(to_enemy) + 1e-5
                d_enemy = to_enemy / dist_to_enemy
                
                obs = np.dot(d_target, d_enemy)
                if obs > max_obs:
                    max_obs = obs
            
            alignment = np.dot(d_target, d_heading)
            score = w_g * alignment - w_o * max_obs
            
            if score > best_score:
                best_score = score
                best_candidate = (c_type, d_target)
                
        decision_type, kick_dir = best_candidate
        kick_vector = kick_dir * self.kick_force

        ball.apply_kick(kick_vector)
        
        return [np.array([0.0, 0.0])]