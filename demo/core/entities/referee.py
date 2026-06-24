import numpy as np

class Referee():

    def __init__(self, world):
        self.time = 0
        self.world = world
        self.upper_field_boundary = world.dims["height"]
        self.lower_field_boundary = 0
        self.left_field_boundary = 0
        self.right_field_boundary = world.dims["width"]

    def enforce_rules(self,state, actions):
        self.time += 1
        # self.check_boundaries_robots(state)
        self.check_goal(state)
            
        
    # def check_boundaries_robots(self, state):
    #     for robot in state["teamA"]:
    #         if robot.state[0] >= self.right_field_boundary or robot.state[0] <= self.left_field_boundary or robot.state[1] >= self.upper_field_boundary or robot.state[1] <= self.lower_field_boundary:
    #             self.world.reset_positions() #Ideally it should penalty the robot by making it stay off field for a couple seconds
    #             print(f"robot #{robot.robot_id} on team {robot.team} penalized for leaving boundaries")
    #     for robot in state["teamB"]:
    #         if robot.state[0] >= self.right_field_boundary or robot.state[0] <= self.left_field_boundary or robot.state[1] >= self.upper_field_boundary or robot.state[1] <= self.lower_field_boundary:
    #             self.world.reset_positions()
    #             print(f"robot #{robot.robot_id} on team {robot.team} penalized for leaving boundaries")

    def check_goal(self,state):
        if state["ball"].position[0] <= state["goalA"].position[0] + state["goalA"].size["height"] and state["ball"].position[1] <= state["goalA"].position[1] + state["goalA"].size["length"] and state["ball"].position[1] >= state["goalA"].position[1]:
            state["score"]["teamB"] += 1
            self.world.reset_positions()
            print("team B scored")
        if state["ball"].position[0] >= state["goalB"].position[0] and state["ball"].position[1] <= state["goalB"].position[1]+ state["goalB"].size["length"] and state["ball"].position[1] >= state["goalB"].position[1]:
            state["score"]["teamA"] += 1
            self.world.reset_positions()
            print("team A scored")
