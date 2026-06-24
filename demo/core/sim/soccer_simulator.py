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
        
        # 1. Κίνηση μπάλας
        ball.step(self.dt)
        
        # 2. ΣΥΓΚΡΟΥΣΕΙΣ ΡΟΜΠΟΤ ΜΕΤΑΞΥ ΤΟΥΣ (Elastic Push)
        robot_collision_dist = 2 * self.world.state["teamA"][0].body_radius  # Διάμετρος ρομπότ
        ball_collision_dist = self.world.state["teamA"][0].body_radius + ball.radius
        
        for i in range(len(robots)):
            for j in range(i + 1, len(robots)):  # i+1 για να ελέγχουμε κάθε ζευγάρι ΜΟΝΟ μια φορά
                r1 = robots[i]
                r2 = robots[j]
                
                dist = np.linalg.norm(r1.state[:2] - r2.state[:2])
                if dist < robot_collision_dist:
                    # Διάνυσμα κατεύθυνσης από το r2 προς το r1
                    normal = (r1.state[:2] - r2.state[:2]) / (dist + 1e-5)
                    
                    # Πόσο πολύ έχουν εισχωρήσει το ένα μέσα στο άλλο
                    overlap = robot_collision_dist - dist
                    
                    # Σπρώχνουμε και τα δύο κατά το ήμισυ της διείσδυσης για να ξεκολλήσουν δίκαια
                    r1.state[:2] += normal * (overlap / 2.0)
                    r2.state[:2] -= normal * (overlap / 2.0)

        # 3. ΣΥΓΚΡΟΥΣΕΙΣ ΡΟΜΠΟΤ ΜΕ ΜΠΑΛΑ ΚΑΙ ΤΟΙΧΟΥΣ
        for robot in robots:
            ball_dist = np.linalg.norm(ball.position - robot.state[:2])
            
            if ball_dist < ball_collision_dist:
                normal = (ball.position - robot.state[:2]) / (ball_dist + 1e-5)
                
                # Η μπάλα παίρνει τη σωστή ώθηση προς τα έξω
                ball.velocity = normal * (np.linalg.norm(ball.velocity) + 0.3)
                # Clamping θέσης μπάλας
                ball.position = robot.state[:2] + normal * ball_collision_dist
 
            if robot.state[0] - robot.body_radius < 0:
                robot.state[0] = robot.body_radius
            elif robot.state[0] + robot.body_radius > self.world.world_width:
                robot.state[0] = self.world.world_width - robot.body_radius
            
            if robot.state[1] - robot.body_radius < 0:
                robot.state[1] = robot.body_radius
            elif robot.state[1] + robot.body_radius > self.world.world_height:
                robot.state[1] = self.world.world_height - robot.body_radius
        



        # 4. ΑΝΑΚΛΑΣΗ ΣΤΑ ΤΟΙΧΩΜΑΤΑ (Αυτά τα έχεις γράψει τέλεια!)
        restitution = 0.7
        if ball.position[1] - ball.radius < 0:
            ball.velocity[1] = abs(ball.velocity[1]) * restitution
            ball.position[1] = ball.radius
        elif ball.position[1] + ball.radius > self.world.world_height:
            ball.velocity[1] = -abs(ball.velocity[1]) * restitution
            ball.position[1] = self.world.world_height - ball.radius
            
        if ball.position[0] - ball.radius < 0:
            ball.velocity[0] = abs(ball.velocity[0]) * restitution
            ball.position[0] = ball.radius
        elif ball.position[0] + ball.radius > self.world.world_width:
            ball.velocity[0] = -abs(ball.velocity[0]) * restitution
            ball.position[0] = self.world.world_width - ball.radius



