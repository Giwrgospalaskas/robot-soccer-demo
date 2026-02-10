from sim.soccer_simulator import SoccerSimulator
from entities.robot import Robot
from entities.ball import Ball
from sim.world_builder import WorldBuilder
from factories.dynamics_factory import DynamicsFactory
from factories.policy_factory import PolicyFactory

dynamics_path = "configs/dynamics.json"
policies_path = "configs/policies.json"
world_path = "configs/world.json"

#policy_path = "/configs/policy.json





robot1 = Robot(px=50.0, py=50.0, theta=0.0)
robot2 = Robot(px=60.0, py=60.0, theta=0.0)
robots = [robot1, robot2]

ball = Ball(px=100.0, py=240.0, vx=0.0, vy=0.0)

world = WorldBuilder(world_path).create_world()


dynamics = DynamicsFactory(dynamics_path).create_dynamics()

policy = PolicyFactory(policies_path).create_policy()


simulator = SoccerSimulator(robots, ball, world ,dynamics, policy, [], dt=0.1)

for _ in range(100):
    simulator.step()