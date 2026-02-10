import json
from entities.world import World

class WorldBuilder():
    def __init__(self,path):
        self.conf_path = path
    
    def create_world(self):
        try:
            with open(self.conf_path, 'r') as f:
                config = json.load(f)
            params = config.get("parameters", {})
            return World(params["width"], params["height"])
        
        except FileNotFoundError:
            print("Error: The file 'world.json' was not found.")
