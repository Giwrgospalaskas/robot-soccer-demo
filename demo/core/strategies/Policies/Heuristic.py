import numpy as np
from strategies.policies import PoliciesInterface

class SoccerHeuristicPolicy(PoliciesInterface):
    def compute_actions(self):
        return