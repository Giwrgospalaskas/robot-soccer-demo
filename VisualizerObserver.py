from observers.ObserverInterface import ObserverInterface
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from mplsoccer import Pitch  

class VisualizerObserver(ObserverInterface):

    def __init__(self, state):
        
        self.pitch = Pitch(pitch_type='custom', 
                           pitch_length=state["dims"]["width"], 
                           pitch_width=state["dims"]["height"],
                           pitch_color='#4d784e',     
                           line_color='white',        
                           stripe=True,               
                           stripe_color='#476f48')    
        
        
        self.fig, self.ax = self.pitch.draw(figsize=(10, 6))
        self.ax.set_aspect('equal')
        
        
        colors = {
            "A": "#1e90ff", 
            "B": "#ff4757"   
        }
        
        
        self.robots_team_a = [self.ax.add_patch(patches.Circle(
            (0,0), 
            state["teamA"][0].body_radius, 
            color=colors["A"],
            zorder=3)) 
            for _ in range(state["robots_per_team"])] 
        
        
        self.robots_team_b = [self.ax.add_patch(patches.Circle(
            (0,0),
            state["teamB"][0].body_radius, 
            color=colors["B"],
            zorder=3)) 
            for _ in range(state["robots_per_team"])] 
        
       
        self.arrow_team_a = self.ax.quiver(np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]), 
                                            color=colors["A"], 
                                            scale=18,
                                            zorder=4)
        
        self.arrow_team_b = self.ax.quiver(np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]), 
                                            color=colors["B"], 
                                            scale=18,
                                            zorder=4)
        
        
        self.goal_team_a = self.ax.add_patch(patches.Rectangle(
            (state["goalA"].position[0], state["goalA"].position[1]),
            state["goalA"].size["height"],
            state["goalA"].size["length"], 
            edgecolor='white',
            facecolor='#ffffff33', 
            linewidth=2,
            zorder=2))
        
        
        self.goal_team_b = self.ax.add_patch(patches.Rectangle(
             (state["goalB"].position[0], state["goalB"].position[1]),
             state["goalB"].size["height"],
             state["goalB"].size["length"], 
             edgecolor='white',
             facecolor='#ffffff33',
             linewidth=2,
             zorder=2))
        
        
        self.ball_artist = self.ax.add_patch(patches.Circle(
            (0,0), 
            state["ball_radius"], 
            edgecolor='black',
            facecolor='white',
            linewidth=1.5,
            zorder=5)) 
        
        self.fig.canvas.manager.set_window_title('Robot Soccer Arena')
        plt.ion() 
        plt.show()

    def update(self, state):
        x_positions_team_a = []
        y_positions_team_a = []
        u_directions_team_a = []
        v_directions_team_a = []
       
        x_positions_team_b = []
        y_positions_team_b = []
        u_directions_team_b = []
        v_directions_team_b = []
        
        for i, robot in enumerate(state["teamA"]):
            self.robots_team_a[i].center = (robot.state[0], robot.state[1])
            x_positions_team_a.append(robot.state[0])
            y_positions_team_a.append(robot.state[1])
            u_directions_team_a.append(np.cos(robot.state[2]))
            v_directions_team_a.append(np.sin(robot.state[2]))
        
        for i, robot in enumerate(state["teamB"]):
            self.robots_team_b[i].center = (robot.state[0], robot.state[1])
            x_positions_team_b.append(robot.state[0])
            y_positions_team_b.append(robot.state[1])
            u_directions_team_b.append(np.cos(robot.state[2]))
            v_directions_team_b.append(np.sin(robot.state[2]))
        
        self.arrow_team_a.set_offsets(np.hstack([np.array(x_positions_team_a)[:,None], 
                                                 np.array(y_positions_team_a)[:,None]]))
        self.arrow_team_a.set_UVC(u_directions_team_a, v_directions_team_a)
        
        self.arrow_team_b.set_offsets(np.hstack([np.array(x_positions_team_b)[:,None], 
                                                 np.array(y_positions_team_b)[:,None]]))
        self.arrow_team_b.set_UVC(u_directions_team_b, v_directions_team_b)
        
        self.ball_artist.center = (state["ball"].position[0], state["ball"].position[1])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()