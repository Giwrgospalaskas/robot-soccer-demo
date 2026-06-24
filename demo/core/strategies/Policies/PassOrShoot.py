import numpy as np
from strategies.policies import PoliciesInterface

class PassOrShootPolicy(PoliciesInterface):
    def compute_actions(self, robots,ball,goal):
        
        return