import numpy as np
from strategies.policies import PoliciesInterface



class FormationConsensusPolicy(PoliciesInterface):
    def __init__(self, robot_drive_k, max_speed, min_speed, kick_radius, kick_force):
        super().__init__(robot_drive_k, max_speed, min_speed, kick_radius, kick_force)
        self.drive_k = 0.5

    def compute_actions(self, own_robots,enemy_robots,ball,goal):
        actions = []
        N = len(own_robots[1:])
        m = 2 
        teamate_dist = np.linalg.norm(own_robots[0].state[:2]-ball.position)
        attack = False
        
        # 1. Laplacian Construction
        A = np.ones((N, N)) - np.eye(N) 
        D = np.diag(np.sum(A, axis=1))
        L = D - A
        
        # Mandatory Matrix Asserts
        assert A.shape == (N, N)
        assert np.allclose(L @ np.ones(N), 0)

        # 2. State Stacking
        p_stacked = np.array([[r.state[0], r.state[1]] for r in own_robots[1:]]).reshape(-1, 1)
        
        offsets = []
        radius_formation = 40.0 # Η ακτίνα απόστασης από τον Leader (σε pixels)
        
        if N == 1:
        
            offsets.append([-radius_formation, 0.0])
        else:
            min_angle = -np.radians(60)
            max_angle = np.radians(60)
            angles = np.linspace(min_angle, max_angle, N)
            
            for angle in angles:
                for enemy_robot in enemy_robots:
                    if np.linalg.norm(enemy_robot.state[:2]-ball.position) > teamate_dist:
                        attack = True
                if attack:
                    dx = radius_formation * np.cos(angle)
                    dy = radius_formation * np.sin(angle)
                    offsets.append([dx, dy])
                else:
                    dx = -radius_formation * np.cos(angle)
                    dy = radius_formation * np.sin(angle)
                    offsets.append([dx, dy])

        p_star = []
        for offset in offsets:
            p_star.extend([offset[0], offset[1]])
        p_star = np.array(p_star).reshape(-1, 1)

        L_ext = np.kron(L, np.eye(m))
        v_des_stacked = -self.drive_k * (L_ext @ (p_stacked - p_star))
        
        v_individual = v_des_stacked.reshape(N, 2)

        for i in range(N):
            distance_to_target = np.linalg.norm(v_individual[i])
            desired_field_pos = ball.position + np.array(offsets[i])
            
            error_to_leader = desired_field_pos - own_robots[1+i].state[:2]
            
            v_individual[i] += error_to_leader

           
            vx = v_individual[i, 0]
            vy = v_individual[i, 1]
            
            v_mag = np.sqrt(vx**2 + vy**2)
            theta_des = np.arctan2(vy, vx)
            
            theta_err = self.wrap(theta_des - own_robots[1+i].state[2])
            
            u_clamped = min(v_mag, self.max_speed) 
            omega = self.robot_drive_k * theta_err

            actions.append(np.array([u_clamped, omega]))
        
        return actions