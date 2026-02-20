import numpy as np
# from entities.world import World

class Policies():

    def compute_actions(self):
        raise NotImplementedError
    

    

class GoToPointPolicy(Policies):
    def __init__(self, robot_drive_k, max_speed, min_speed, kick_radius, kick_force ):
        self.robot_drive_k = robot_drive_k
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.kick_radius = kick_radius
        self.kick_force = kick_force





    def compute_actions(self, robots, ball, target_point = None):
        if target_point is None:
            target_point = ball.position
        for i, robot in enumerate(robots):
            u_des= target_point - robot.state[:2]
            theta_des = np.arctan2(u_des[1], u_des[0])
            head_err = wrap(theta_des - robot.state[2])
            omega = self.robot_drive_k * head_err
            u_raw = np.linalg.norm(u_des)
            if u_raw < self.kick_radius+ball.radius+robot.body_radius:
                u_clamped = 0
                kick = np.array([self.kick_force*np.cos(theta_des), self.kick_force*np.sin(theta_des)], dtype=float)
                ball.apply_kick(kick)
            else:
                u_clamped = max(0, min(u_raw, self.max_speed))
            yield np.array([u_clamped, omega])

class FormationConsensusPolicy(Policies):
    def __init__(self, robot_drive_k, max_speed, min_speed):
        self.robot_drive_k = robot_drive_k
        self.max_v = max_speed
        self.min_v = min_speed
        self.offsets = [[1, 1], [-1, -1], [-1, 1]]


    def compute_actions(self, robots, ball):
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

        # 3. Target (P*) Calculation
        p_star = []
        for offset in self.offsets: # offsets loaded from JSON
            p_star.extend([ball.position[0] + offset[0], ball.position[1] + offset[1]])
        p_star = np.array(p_star).reshape(-1, 1)

        # 4. Consensus Law
        L_ext = np.kron(L, np.eye(m))
        v_des_stacked = -self.robot_drive_k * (L_ext @ (p_stacked - p_star))
        
        # Return unstacked vectors for the controller
        v_individual = v_des_stacked.reshape(N, 2)

        actions = []
        for i in range(N):
            vx = v_individual[i, 0]
            vy = v_individual[i, 1]
            
            # 1. Convert [vx, vy] to a desired speed and heading
            v_mag = np.sqrt(vx**2 + vy**2)
            theta_des = np.arctan2(vy, vx)
            
            # 2. Use your 'wrap' function to find the shortest turn
            # current_theta comes from the robot's state[2]
            theta_err = wrap(theta_des - robots[i].state[2])
            
            # 3. Apply gains and CLAMP (mandatory)
            u_clamped = min(v_mag, self.max_v) 
            omega_clamped = self.robot_drive_k * theta_err
            
            actions.append((u_clamped, omega_clamped))
        return np.array(actions)
        
        
    

def wrap(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi