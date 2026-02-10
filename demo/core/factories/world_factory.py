import json
from entities.world import World

class WorldBuilder():
    def __init__(self,path):
        self.conf_path = path
    
    def create_world(self):
        try:
            with open(self.conf_path, 'r') as f:
                config = json.load(f)
            return World(config["dimensions"], config["robots_per_team"], config["match_length"])
        
        except FileNotFoundError:
            print("Error: The file 'world.json' was not found.")
