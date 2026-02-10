import json
from strategies.policies import GoToPointPolicy, FormationConsensusPolicy



class PolicyFactory():
    def __init__(self,path):
        self.conf_path = path

    def create_policy(self):
        try:
            with open(self.conf_path, 'r') as f:
                config = json.load(f)
            params = config.get("parameters", {})
            dtype = config.get("policy")

            if dtype == "GoToPointPolicy":
                return GoToPointPolicy(params["robot_drive_k"], params["max_speed"], params["min_speed"])
            elif dtype == "FormationConsensusPolicy":
                return FormationConsensusPolicy(params["robot_drive_k"], params["max_speed"], params["min_speed"])
            else:
                raise ValueError(f"Unknown policy: {config['policy']}")
        
        except FileNotFoundError:
            print("Error: The file 'policies.json' was not found.")