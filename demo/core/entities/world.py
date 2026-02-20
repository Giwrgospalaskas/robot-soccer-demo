from entities.robot import Robot
from entities.ball import Ball
from entities.goal import Goal
import random
import numpy as np

class World():
    def __init__(self,dimensions,ball, robot,goal,robots_per_team,match_length,dt):
        
        self.dims = dimensions
        self.world_width = dimensions["width"]
        self.world_height = dimensions["height"]
        self.teamA = []
        self.teamB = []
        self.robot_wheel_radius = robot["wheel_radius"]
        self.robot_wheel_base = robot["wheel_base"]
        self.robot_body_radius = robot["body_radius"]
        self.ball_radius = ball["radius"]
        self.ball_friction = ball["friction"]
        self.score = {"teamA": 0, "teamB": 0}
        self.dt = dt
        
        self.ball = Ball(
            self.dims["width"]/2,
            self.dims["height"]/2,0,0, 
            self.ball_radius, 
            self.ball_friction)
        
        
        self.goal= goal
        self.robots_per_team = robots_per_team
        
        
        self.goalA = Goal(
            (self.world_width - self.goal["length"])/2, 
            0.0,
            self.goal,
            "A")
        
        self.goalB = Goal(
            (self.world_width - self.goal["length"])/2, 
            self.world_height-self.goal["height"],
            self.goal,
            "B")
        
        self.match_length = match_length

        for i in range(self.robots_per_team):
            self.teamA.append(Robot(random.uniform(0.0,self.dims["width"]),random.uniform(1,self.dims["height"]/2),0.0,"A",i,robot["wheel_radius"],robot["wheel_base"],robot["body_radius"]))
            self.teamB.append(Robot(random.uniform(0.0,self.dims["width"]),random.uniform(self.dims["height"]/2,self.dims["height"]),np.pi,"B",-i,robot["wheel_radius"],robot["wheel_base"],robot["body_radius"]))
        



        self.state = {
            "ball": self.ball,
            "teamA": self.teamA,
            "teamB": self.teamB,
            "robots_per_team": self.robots_per_team,
            "robot_wheel_radius": self.robot_wheel_radius,
            "robot_wheel_base": self.robot_wheel_base,
            "robot_body_radius": self.robot_body_radius,
            "ball_radius": self.ball_radius,
            "ball_friction": self.ball_friction,
            "dims": self.dims, 
            "goalA": self.goalA,
            "goalB": self.goalB,
            "match_length": self.match_length,
            "score": self.score,
            "dt": 0.1
        }

    def reset_positions(self):
        for robot in self.teamA:
            robot.state[0] = random.uniform(0.0,self.dims["width"])
            robot.state[1] = random.uniform(1,self.dims["height"]/2)
            robot.state[2] = 0.0
        for robot in self.teamB:
            robot.state[0] = random.uniform(0.0,self.dims["width"])
            robot.state[1] = random.uniform(self.dims["height"]/2,self.dims["height"])  
            robot.state[2] = np.pi
        self.ball.position[0] = self.dims["width"]/2
        self.ball.position[1] = self.dims["height"]/2
        self.ball.velocity[0] = 0
        self.ball.velocity[1] = 0



