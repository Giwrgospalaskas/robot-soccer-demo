from entities.robot import Robot
from entities.ball import Ball
# from entities.world import World


class SoccerSimulator():
    def __init__(self, world,referee,dynamics, policies, observers):
        self.world = world
        self.referee = referee
        self.ball = self.world.state["ball"]
        self.teamA = self.world.state["teamA"]
        self.teamB = self.world.state["teamB"]
        self.dims = self.world.state["dims"]
        self.goalA = self.world.state["goalA"]
        self.goalB = self.world.state["goalB"]
        self.dynamics = dynamics
        self.policy = policies
        self.observers = observers
        self.dt = self.world.state["dt"]

    def step(self):
        # 1. Compute actions from policies
        # (Assuming policies return a list of actions for the robots)

        actionsA = []
        actionsB = []

        current_cursor = self.observers.observers[0].cursor_pos

        actionsA.extend(self.policy.compute_actions(self.teamA, self.ball))
        actionsB.extend(self.policy.compute_actions(self.teamB, self.ball))


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
        self.referee.enforce_rules(self.world.state)

        # 5. Notify observers
        self.observers.notify(self.world.state)

    