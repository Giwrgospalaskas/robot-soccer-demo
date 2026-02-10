from entities.robot import Robot
from entities.ball import Ball
import random
import numpy as np

class World():
    def __init__(self,dimensions,N, match_length):
        self.dims = dimensions
        self.world_width = dimensions["width"]
        self.world_height = dimensions["height"]
        self.teamA = []
        self.teamB = []
        self.ball = Ball(0.0,0.0,0,0)
        self.match_length = match_length

        for i in range(N):
            self.teamA.append(Robot(random.uniform(1,50),random.uniform(1,50),0.0,"A",i))
            self.teamB.append(Robot(random.uniform(-1,-50),random.uniform(-1,-50),np.pi,"B",-i))
        
        
        self.state = {
            "ball": self.ball,
            "teamA": self.teamA,
            "teamB": self.teamB,
            "robots_per_team": N,
            "dims": self.dims, 
            "match_length": self.match_length
        }


