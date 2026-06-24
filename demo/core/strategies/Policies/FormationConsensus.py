import numpy as np
from strategies.policies import PoliciesInterface



class FormationConsensusPolicy(PoliciesInterface):
    def __init__(self, robot_drive_k, max_speed, min_speed, kick_radius, kick_force):
        super().__init__(robot_drive_k, max_speed, min_speed, kick_radius, kick_force)
        self.drive_k = 1.0

    def compute_actions(self, robots,ball,goal):
        N = len(robots)
        m = 2 # 2D space
        
        # 1. Laplacian Construction
        A = np.ones((N, N)) - np.eye(N) 
        D = np.diag(np.sum(A, axis=1))
        L = D - A
        
        # Mandatory Matrix Asserts
        assert A.shape == (N, N)
        assert np.allclose(L @ np.ones(N), 0)

        # 2. State Stacking
        p_stacked = np.array([[r.state[0], r.state[1]] for r in robots]).reshape(-1, 1)
        
        offsets = [[0, 0], [30, 10], [-30, -10]]
        # 3. Target (P*) Calculation
        p_star = []
        for offset in offsets: # offsets loaded from JSON
            p_star.extend([robots[0].state[0] + offset[0], robots[0].state[1] + offset[1]])
        p_star = np.array(p_star).reshape(-1, 1)

        # 4. Consensus Law
        L_ext = np.kron(L, np.eye(m))
        v_des_stacked = -self.drive_k * (L_ext @ (p_stacked - p_star))
        
        # Return unstacked vectors for the controller
        v_individual = v_des_stacked.reshape(N, 2)

        for i in range(N):
            distance_to_target = np.linalg.norm(v_individual[i])
            if distance_to_target < 1:
                v_mag = 0
                theta_err = 0
            else:
                vx = v_individual[i, 0]
                vy = v_individual[i, 1]
                
                # 1. Convert [vx, vy] to a desired speed and heading
                v_mag = np.sqrt(vx**2 + vy**2)
                theta_des = np.arctan2(vy, vx)
                
                # 2. Use your 'wrap' function to find the shortest turn
                # current_theta comes from the robot's state[2]
                theta_err = self.wrap(theta_des - robots[i].state[2])
            
            # 3. Apply gains and CLAMP (mandatory)
            u_clamped = min(v_mag, self.max_speed) 
            omega = self.robot_drive_k * theta_err

            yield np.array([u_clamped, omega])