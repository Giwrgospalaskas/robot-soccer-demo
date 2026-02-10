from entities.robot import Robot
from entities.ball import Ball
# from entities.world import World


class SoccerSimulator():
    def __init__(self, world,dynamics, policies, observers, dt=0.1):
        self.world = world
        self.ball = self.world.state["ball"]
        self.teamA = self.world.state["teamA"]
        self.teamB = self.world.state["teamB"]
        self.dims = self.world.state["dims"]
        self.dynamics = dynamics
        self.policies = policies
        self.observers = observers
        self.dt = dt

    def step(self):
        # 1. Compute actions from policies
        # (Assuming policies return a list of actions for the robots)
        actionsA = []
        actionsB = []
        actionsA.extend(self.policies.compute_actions(self.teamA, self.ball))
        actionsB.extend(self.policies.compute_actions(self.teamB, self.ball))

        # 2. Propagate robot states
        for i, robot in enumerate(self.teamA):
            if i < len(actionsA):
                robot.state = self.dynamics.propagate(robot.state, actionsA[i], self.dt)
       
        for i, robot in enumerate(self.teamB):
            if i < len(actionsB):
                robot.state = self.dynamics.propagate(robot.state, actionsB[i], self.dt)

        # 3. Update ball state
        self.ball.step(self.dt)

        

        # 4. Enforce world rules (Boundaries, Goals - to be implemented)
        # self._enforce_boundaries()

        # 5. Notify observers
        for observer in self.observers:
            observer.update(self.world.state)