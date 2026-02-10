from entities.robot import Robot
from entities.ball import Ball
from entities.world import World


class SoccerSimulator():
    def __init__(self, robots, ball, world ,dynamics, policies, observers, dt=0.1):
        self.robots = robots
        self.ball = ball
        self.dynamics = dynamics
        self.policies = policies
        self.observers = observers
        self.world = world
        self.dt = dt

    def step(self):
        # 1. Compute actions from policies
        # (Assuming policies return a list of actions for the robots)
        actions = []
        actions.extend(self.policies.compute_actions(self.robots, self.ball))
        print(actions)

        # 2. Propagate robot states
        for i, robot in enumerate(self.robots):
            if i < len(actions):
                robot.state = self.dynamics.propagate(robot.state, actions[i], self.dt)
            print(robot.state)

        # 3. Update ball state
        self.ball.step(self.dt)

        # 4. Enforce world rules (Boundaries, Goals - to be implemented)
        # self._enforce_boundaries()

        # 5. Notify observers
        for observer in self.observers:
            observer.update(self.robots, self.ball)