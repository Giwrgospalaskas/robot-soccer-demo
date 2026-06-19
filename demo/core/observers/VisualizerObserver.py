from observers.ObserverInterface import ObserverInterface
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class VisualizerObserver(ObserverInterface):

    def __init__(self, state):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0.0,state["dims"]["width"]) 
        self.ax.set_ylim(0.0,state["dims"]["height"]) 
        self.ax.set_aspect('equal')
        
        self.ax.set_xticks([])  #Remove to see the numbers on the axis, runs better if you dont for some reason
        self.ax.set_yticks([])
        
        colors = {
            "A": "blue",
            "B": "red"
        }

        # self.cursor_pos = np.array([0.0, 0.0]) # Initialize at origin
        # self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        
        
        #TeamA
        self.robots_team_a = [self.ax.add_patch(patches.Circle(
            (0,0), 
            state["teamA"][0].body_radius, 
            color = colors["A"])) 
            for _ in range(state["robots_per_team"])] 
        
        
        #TeamB
        self.robots_team_b = [self.ax.add_patch(patches.Circle(
            (0,0),
            state["teamB"][0].body_radius, 
            color = colors["B"])) 
            for _ in range(state["robots_per_team"])] 
        
        #Arrows
        self.arrow_team_a = self.ax.quiver(np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]), 
                                            color=colors["A"], 
                                            scale=18)
        
        
        self.arrow_team_b = self.ax.quiver(np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]),
                                            np.zeros(state["robots_per_team"]), 
                                            color=colors["B"], 
                                            scale=18)
       


        
        #GoalpostA
        self.goal_team_a = self.ax.add_patch(patches.Rectangle(
            (state["goalA"].position[0], state["goalA"].position[1]),
            state["goalA"].size["height"],
            state["goalA"].size["length"], 
            color=colors["A"]))
        
        
        #GoalpostB
        self.goal_team_b = self.ax.add_patch(patches.Rectangle(
             (state["goalB"].position[0], state["goalB"].position[1]),
             state["goalB"].size["height"],
             state["goalB"].size["length"], 
             color=colors["B"]))
        
        
        #Ball
        self.ball_artist = self.ax.add_patch(patches.Circle(
            (0,0), 
            state["ball_radius"], 
            color='black')) 
        
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


    # def on_move(self, event):
    #     if event.xdata is not None and event.ydata is not None:
    #         self.cursor_pos[0] = event.xdata
    #         self.cursor_pos[1] = event.ydata

    
    
