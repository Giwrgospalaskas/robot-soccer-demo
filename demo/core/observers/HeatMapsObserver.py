from observers.ObserverInterface import ObserverInterface
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import mplsoccer
import csv

class HeatMapsObserver(ObserverInterface):
    def __init__(self, state):
        self.pitch_length = state["dims"]["width"]
        self.pitch_width = state["dims"]["height"]
        
        
        self.x_offset = self.pitch_length / 2.0
        self.y_offset = self.pitch_width / 2.0
        
        
        self.ball_positions = []
        self.ball_possession = []
        self.time_steps = []
        self.formation_errors_red = []
        self.formation_errors_blue = []
        
       
        self.cmap_blue = mcolors.LinearSegmentedColormap.from_list('Custom blue', ['#4d784e', 'blue'])
        self.cmap_red = mcolors.LinearSegmentedColormap.from_list('Custom red', ['#4d784e', 'red'])

    def update(self, state):
       
        # Αποθήκευση θέσης μπάλας και κατοχής
        if "ball" in state and state["ball"] is not None:
            self.ball_positions.append((state["ball"].position[0], state["ball"].position[1]))
        else:
            self.ball_positions.append((0.0, 0.0))
            
       
        current_possession = state.get("possession", "none")
        self.ball_possession.append(current_possession)
        
       
        # self.formation_errors_red.append(state.get("formation_error_red", 0))
        # self.formation_errors_blue.append(state.get("formation_error_blue", 0))
        # self.time_steps.append(len(self.ball_positions) * state.get("dt", 0.1))

    def generate_plots_and_csv(self):
        
        
        
        if not self.ball_positions:
            print("There are no statistics to create the heatmap.")
            return

       
        raw_x = [pos[0] for pos in self.ball_positions]
        raw_y = [pos[1] for pos in self.ball_positions]
        corrected_x = [x + self.x_offset for x in raw_x]
        corrected_y = [y + self.y_offset for y in raw_y]

        df = pd.DataFrame({
            'x': corrected_x, 
            'y': corrected_y, 
            'team': self.ball_possession,
            'outcomeType': ['Successful'] * len(self.ball_positions)
        })
        
        df_blue = df[(df['team'] == 'blue') & (df['outcomeType'] == 'Successful')]
        df_red = df[(df['team'] == 'red') & (df['outcomeType'] == 'Successful')]
        
        pitch = mplsoccer.VerticalPitch(
            pitch_type='custom', pitch_length=self.pitch_length, pitch_width=self.pitch_width, 
            pitch_color='#4d784e', line_color='white', line_zorder=2, stripe=True
        )

        
        fig1, ax1 = pitch.draw(figsize=(6, 10))
        fig1.set_facecolor('black')
        if not df_blue.empty:
            pitch.kdeplot(df_blue['y'], df_blue['x'], ax=ax1, cmap=self.cmap_blue, fill=True, levels=50, zorder=1, alpha=0.7)
        fig1.suptitle('HeatMap of BLUE team', color='white', fontsize=14, y=0.95)
        fig1.savefig('heatmap_blue.png', bbox_inches='tight', dpi=150)
        plt.close(fig1)
        
        
        fig2, ax2 = pitch.draw(figsize=(6, 10))
        fig2.set_facecolor('black')
        if not df_red.empty:
            pitch.kdeplot(df_red['y'], df_red['x'], ax=ax2, cmap=self.cmap_red, fill=True, levels=50, zorder=1, alpha=0.7)
        fig2.suptitle('HeatMap of RED team', color='white', fontsize=14, y=0.95)
        fig2.savefig('heatmap_red.png', bbox_inches='tight', dpi=150)
        plt.close(fig2)
        
       
        fig3, ax3 = pitch.draw(figsize=(6, 10))
        fig3.set_facecolor('black')
        if not df_blue.empty:
            pitch.kdeplot(df_blue['y'], df_blue['x'], ax=ax3, cmap=self.cmap_blue, fill=True, levels=50, zorder=1, alpha=0.5)
        if not df_red.empty:
            pitch.kdeplot(df_red['y'], df_red['x'], ax=ax3, cmap=self.cmap_red, fill=True, levels=50, zorder=1, alpha=0.5)
        fig3.suptitle('Combined HeatMap', color='white', fontsize=14, y=0.95)
        fig3.savefig('heatmap_combined.png', bbox_inches='tight', dpi=150)
        plt.close(fig3)
        