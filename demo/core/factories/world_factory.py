import json
from entities.world import World

class WorldBuilder():
    def __init__(self,path):
        self.conf_path = path
    
    def create_world(self):
        try:
            with open(self.conf_path, 'r') as f:
                config = json.load(f)
            return World(
                dimensions = config["dimensions"],
                ball = config["ball"],
                robot = config["robot"],
                robots_per_team = config["robots_per_team"], 
                goal = config["goal"],
                match_length = config["match_length"],
                dt = config["dt"]
                )
        
        except FileNotFoundError:
            print("Error: The file 'world.json' was not found.")
