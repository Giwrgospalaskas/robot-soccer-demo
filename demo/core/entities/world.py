from robot import Robot
from ball import Ball

class World():
    def __init__(self,width,height,N):
        self.dim = [width,height]
        self.robots = []
        self.ball = Ball(width/2,height/2,0,0)
        for _ in range(N):
            self.robots.append(Robot())
        return [self.dim,self.robots,self.ball]


