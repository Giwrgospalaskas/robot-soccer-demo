from sim.soccer_simulator import SoccerSimulator
from factories.world_factory import WorldBuilder
from factories.dynamics_factory import DynamicsFactory
from factories.policy_factory import PolicyFactory
from observers.VisualizerObserver import VisualizerObserver
from observers.ScoreboardObserver import ScoreboardObserver
from observers.ObserverInterface import ObserverInterface
from entities.referee import Referee




dynamics_path = "configs/dynamics.json"
policies_path = "configs/policies.json"
world_path = "configs/world.json"


world = WorldBuilder(world_path).create_world()
referee = Referee(world)


match_length = world.state["match_length"]




dynamics = DynamicsFactory(dynamics_path).create_dynamics()

policies = PolicyFactory(policies_path).create_policy()

observers = ObserverInterface()

visualizer_observer = VisualizerObserver(world.state)
scoreboard_observer = ScoreboardObserver()

observers.attach(visualizer_observer)
observers.attach(scoreboard_observer)


simulator = SoccerSimulator(world,referee,dynamics, policies, observers)

if __name__ == "__main__":
    for _ in range(match_length):
        simulator.step()