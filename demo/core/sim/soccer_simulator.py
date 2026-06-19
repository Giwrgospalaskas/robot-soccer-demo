from entities.robot import Robot
from entities.ball import Ball
import numpy as np


class SoccerSimulator():
    def __init__(self, world,referee,dynamics, policies, observers):
        self.world = world
        self.referee = referee
        self.ball = self.world.state["ball"]
        self.teamA = self.world.state["teamA"]
        self.teamB = self.world.state["teamB"]
        self.dims = self.world.state["dims"]
        self.goalA = self.world.state["goalA"]
        self.goalB = self.world.state["goalB"]
        self.dynamics = dynamics
        self.policy = policies
        self.observers = observers
        self.dt = self.world.state["dt"]

    def step(self):
        # 1. Compute actions from policies
        # (Assuming policies return a list of actions for the robots)

        actionsA = []
        actionsB = []

        # current_cursor = self.observers.observers[0].cursor_pos

        actionsA.extend(self.policy.compute_actions(self.teamA,self.ball,self.goalB))
        actionsB.extend(self.policy.compute_actions(self.teamB,self.ball,self.goalA))
        actions = actionsA + actionsB


        # 2. Propagate robot states
        for i, robot in enumerate(self.teamA):
            if i < len(actionsA):
                robot.state = self.dynamics.propagate(robot.state, actionsA[i], self.dt)
       
        for i, robot in enumerate(self.teamB):
            if i < len(actionsB):
                robot.state = self.dynamics.propagate(robot.state, actionsB[i], self.dt)

        # 3. Update ball state and physics
        self.enforce_physics()

        

        # 4. Enforce world rules (Boundaries, Goals - to be implemented)
        self.referee.enforce_rules(self.world.state, actions)

        # 5. Notify observers
        self.observers.notify(self.world.state)

    
    def enforce_physics(self):
        ball = self.ball
        robots = self.teamA + self.teamB
        
        ball.step(self.dt)
        
        # for robot in robots:
        #     dist = np.linalg.norm(ball.position - robot.state[:2])
        #     collision_dist = robot.body_radius + ball.radius
            
        #     if dist < collision_dist:
        #         normal = (ball.position - robot.state[:2]) / (dist + 1e-5)
        #         ball.velocity = normal * (np.linalg.norm(ball.velocity) + 0.2)
        #         ball.position = robot.state[:2] + normal * collision_dist

        # Έλεγχος για ανάκλαση στα τοιχώματα του γηπέδου
        if ball.position[1] < 0 or ball.position[1] > self.world.world_height:
            ball.velocity[1] = -ball.velocity[1] * 0.8
            ball.position[1] = np.clip(ball.position[1], 0, self.world.world_height)
            
        if (ball.position[0] < 0 or ball.position[0] > self.world.world_width):
            ball.velocity[0] = -ball.velocity[0] * 0.8
            ball.position[0] = np.clip(ball.position[0], 0, self.world.world_width)



