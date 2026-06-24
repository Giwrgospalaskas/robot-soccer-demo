import json
from strategies.Policies.GoToPoint import GoToPointPolicy
from strategies.Policies.FormationConsensus import FormationConsensusPolicy




class PolicyFactory():
    def __init__(self,path):
        self.conf_path = path
        

    def create_policy(self):
        try:
            with open(self.conf_path, 'r') as f:
                config = json.load(f)
            params = config.get("parameters", {})
            policy = config.get("Policy")

            if policy == "GoToPointPolicy":
                return GoToPointPolicy(params["robot_turn_drive_k"], 
                                       params["max_speed"], 
                                       params["min_speed"], 
                                       params["kick_radius"], 
                                       params["kick_force"])
            elif policy == "FormationConsensusPolicy":
                return FormationConsensusPolicy(params["robot_turn_drive_k"], 
                                                params["max_speed"], 
                                                params["min_speed"],
                                                params["kick_radius"], 
                                                params["kick_force"])
            else:
                raise ValueError(f"Unknown policy: {config['policy']}")
            
       

        except FileNotFoundError:
            print("Error: The file 'policies.json' was not found.")