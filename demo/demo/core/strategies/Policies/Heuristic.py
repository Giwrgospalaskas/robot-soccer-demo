import numpy as np
from strategies.policies import PoliciesInterface
from strategies.Policies.GoToPoint import GoToPointPolicy
from strategies.Policies.FormationConsensus import FormationConsensusPolicy
from strategies.Policies.PassOrShoot import PassOrShootPolicy


class SoccerHeuristicPolicy(PoliciesInterface):
    def __init__(self, robot_drive_k, max_speed, min_speed, kick_radius, kick_force):
        super().__init__(robot_drive_k, max_speed, min_speed, kick_radius, kick_force)
        
        self.leader_policy = GoToPointPolicy(
            robot_drive_k, max_speed, min_speed, kick_radius, kick_force
        )
        self.decision_policy = PassOrShootPolicy(robot_drive_k, max_speed, min_speed, kick_radius, kick_force
        )
        self.defenders_policy = FormationConsensusPolicy(
            robot_drive_k, max_speed, min_speed, kick_radius, kick_force
        )

    def compute_actions(self, own_robots,enemy_robots, ball, goal):
        N = len(own_robots)
        actions = [None] * N
        
        leader_indx = 0
        min_dist = np.linalg.norm(own_robots[0].state[:2] - ball.position)
        
        for i in range(1, N):
            dist = np.linalg.norm(own_robots[i].state[:2] - ball.position)
            if dist < min_dist:
                min_dist = dist
                leader_indx = i
                
        leader = own_robots[leader_indx]
        leader.robot_id = f"Team {leader.team} Leader"
        
        defenders = []
        defenders_indx = []
        for i, robot in enumerate(own_robots):
            if i != leader_indx:
                robot.robot_id = f"Team {robot.team} Defender"
                defenders.append(robot)
                defenders_indx.append(i)

        if min_dist > self.kick_radius * 0.97:
            leader_action = self.leader_policy.compute_actions([leader], enemy_robots, ball, goal)[0]
            actions[leader_indx] = leader_action
        else:
            leader_action = self.decision_policy.compute_actions([leader] + defenders, enemy_robots, ball, goal)[0]
            actions[leader_indx] = leader_action
        if len(defenders) > 0:
            class VirtualLeader:
                def __init__(self, position):
                    self.position = position
            
            virtual_ball = VirtualLeader(leader.state[:2])
            
            defenders_actions = self.defenders_policy.compute_actions([leader]+defenders,enemy_robots, virtual_ball, goal)
            
            for i, idx in enumerate(defenders_indx):
                actions[idx] = defenders_actions[i]

        return actions