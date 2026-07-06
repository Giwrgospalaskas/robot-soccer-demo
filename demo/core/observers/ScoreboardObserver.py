from observers.ObserverInterface import ObserverInterface
import matplotlib.pyplot as plt

class ScoreboardObserver(ObserverInterface):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        
        bg_color = "#083115"
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)
        self.ax.set_axis_off() 
        self.step = 0
        
        
        self.ax.text(0.5, 0.8, 
                     "MATCH SCORE", 
                     ha='center', 
                     fontsize=16, 
                     fontweight='bold',
                     color='white')
        
       
        self.score_display = self.ax.text(0.5, 0.5, 
                                        "0 - 0", 
                                        ha='center', 
                                        fontsize=45, 
                                        fontweight='bold', 
                                        color="#ffffff")
        
        
        self.time_display = self.ax.text(0.5, 0.2, 
                                         "Time: 0.0s", 
                                         ha='center', 
                                         fontsize=14,
                                         color="#ffffff")
        
        
        self.fig.canvas.manager.set_window_title('Live Scoreboard')
        
        plt.ion()
        plt.show()

    def update(self, state):
        self.step += 1
        
       
        score_str = f"{state['score']['teamA']} - {state['score']['teamB']}"
        self.score_display.set_text(score_str)
        
        current_time = self.step * state["dt"]
        self.time_display.set_text(f"Time: {current_time:.1f}s")
        
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()