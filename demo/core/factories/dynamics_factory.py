import json
from strategies.dynamics import DifferentialDriveDynamics, DiffernetialDriveDynamicsWithActuationNoise


class DynamicsFactory():
    def __init__(self,path):
        self.conf_path = path

    def create_dynamics(self):
        try:
            with open(self.conf_path, 'r') as f:
                config = json.load(f)
            params = config.get("parameters", {})
            dtype = config.get("dynamicsModel")

            if dtype == "DifferentialDriveDynamics":
                return DifferentialDriveDynamics(params["r"], b=params["b"])
            elif dtype == "DiffernetialDriveDynamicsWithActuationNoise":
                return DiffernetialDriveDynamicsWithActuationNoise(params["r"], b=params["b"])
            else:
                raise ValueError(f"Unknown dynamics model: {config['dynamicsModel']}")
        
        except FileNotFoundError:
            print("Error: The file 'dynamics.json' was not found.")
        
