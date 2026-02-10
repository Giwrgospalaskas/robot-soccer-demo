from observers.ObserverInterface import ObserverInterface
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class VisualizerObserver(ObserverInterface):

    def __init__(self, robots_per_team, dims):
        super().__init__()
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-dims["width"]/2,dims["width"]/2) 
        self.ax.set_ylim(-dims["height"]/2,dims["height"]/2) 
        self.ax.set_aspect('equal')
        
        
        # Initialize Robot Artists (3 per team recommended)
        self.robots_team_a = [self.ax.add_patch(patches.Circle((0,0), 1.0, color='blue')) for _ in range(robots_per_team)] 
        self.robots_team_b = [self.ax.add_patch(patches.Circle((0,0),1.0, color='red')) for _ in range(robots_per_team)] 
        self.ball_artist = self.ax.add_patch(patches.Circle((0,0), 0.5, color='black')) 
        
        plt.ion() # Turn on interactive mode
        plt.show()



    
    def update(self, state):
        # Implementation for visualizing the current state of robots and ball
        # print(f"\nVisualizing: {len(state["teamA"])+len(state["teamB"])} robots and ball")
        for i, robot in enumerate(state["teamA"]):
            self.robots_team_a[i].center = (robot.state[0], robot.state[1])
            # print(f"Robot {robot.robot_id} at ({robot.state[0]}, {robot.state[1]} with theta = {robot.state[2]})")
        for i, robot in enumerate(state["teamB"]):
            self.robots_team_b[i].center = (robot.state[0], robot.state[1])
            # print(f"Robot {robot.robot_id} at ({robot.state[0]}, {robot.state[1]} with theta = {robot.state[2]})")
        # print(f"Ball at ({state["ball"].position[0]}, {state["ball"].position[1]})")
        self.ball_artist.center = (state["ball"].position[0], state["ball"].position[1])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    
    
    
