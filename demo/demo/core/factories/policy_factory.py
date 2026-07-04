import json
from strategies.Policies.GoToPoint import GoToPointPolicy
from strategies.Policies.FormationConsensus import FormationConsensusPolicy
from strategies.Policies.Heuristic import SoccerHeuristicPolicy





class PolicyFactory():
    def __init__(self,path):
        self.conf_path = path
        

    def create_policy(self):
        try:
            with open(self.conf_path, 'r') as f:
                config = json.load(f)
            params = config.get("parameters", {})
            TeamApolicy = config.get("TeamAPolicy")
            TeamBpolicy = config.get("TeamBPolicy")

            if TeamApolicy == "GoToPointPolicy":
                APolicy = GoToPointPolicy(params["robot_turn_drive_k"], 
                                       params["max_speed"], 
                                       params["min_speed"], 
                                       params["kick_radius"], 
                                       params["kick_force"])
            elif TeamApolicy == "FormationConsensusPolicy":
                APolicy = FormationConsensusPolicy(params["robot_turn_drive_k"], 
                                                params["max_speed"], 
                                                params["min_speed"],
                                                params["kick_radius"], 
                                                params["kick_force"])
            elif TeamApolicy == "SoccerHeuristicPolicy":
                APolicy =  SoccerHeuristicPolicy(params["robot_turn_drive_k"], 
                                                params["max_speed"], 
                                                params["min_speed"],
                                                params["kick_radius"], 
                                                params["kick_force"])
            else:
                raise ValueError(f"Unknown policy: {config['TeamBpolicy']}")
                
            if TeamBpolicy == "GoToPointPolicy":
                BPolicy = GoToPointPolicy(params["robot_turn_drive_k"], 
                                       params["max_speed"], 
                                       params["min_speed"], 
                                       params["kick_radius"], 
                                       params["kick_force"])
            elif TeamBpolicy == "FormationConsensusPolicy":
                BPolicy = FormationConsensusPolicy(params["robot_turn_drive_k"], 
                                                params["max_speed"], 
                                                params["min_speed"],
                                                params["kick_radius"], 
                                                params["kick_force"])
            elif TeamBpolicy == "SoccerHeuristicPolicy":
                BPolicy =  SoccerHeuristicPolicy(params["robot_turn_drive_k"], 
                                                params["max_speed"], 
                                                params["min_speed"],
                                                params["kick_radius"], 
                                                params["kick_force"])   
            else:
                raise ValueError(f"Unknown policy: {config['TeamBpolicy']}")
            
            return [APolicy,BPolicy]
       

        except FileNotFoundError:
            print("Error: The file 'policies.json' was not found.")