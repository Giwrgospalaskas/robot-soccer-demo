from sim.soccer_simulator import SoccerSimulator
from entities.robot import Robot
from entities.ball import Ball
from factories.world_factory import WorldBuilder
from factories.dynamics_factory import DynamicsFactory
from factories.policy_factory import PolicyFactory
from observers.VisualizerObserver import VisualizerObserver




dynamics_path = "configs/dynamics.json"
policies_path = "configs/policies.json"
world_path = "configs/world.json"

#policy_path = "/configs/policy.json

world = WorldBuilder(world_path).create_world()

match_length = world.state["match_length"]
robots_per_team = world.state["robots_per_team"]
dims = world.state["dims"]




dynamics = DynamicsFactory(dynamics_path).create_dynamics()

policy = PolicyFactory(policies_path).create_policy()

observer = VisualizerObserver(robots_per_team, dims)

simulator = SoccerSimulator(world,dynamics, policy, [observer], dt=0.1)

for _ in range(match_length):
    simulator.step()