import numpy as np
from strategies.policies import PoliciesInterface


class GoToPointPolicy(PoliciesInterface):
    def __init__(self, robot_drive_k, max_speed, min_speed, kick_radius, kick_force):
       super().__init__(robot_drive_k, max_speed, min_speed, kick_radius, kick_force)


    def compute_actions(self, robots, ball, goal):
        actions = []
        
        # 1. Διάνυσμα από την μπάλα προς το τέρμα (κατεύθυνση του σουτ)
        shoot_vector = goal.center - ball.position
        shoot_dist = np.linalg.norm(shoot_vector) + 1e-5
        shoot_dir = shoot_vector / shoot_dist
        
        # 2. Το target_point είναι ΠΙΣΩ από την μπάλα, στην ευθεία του σουτ
        # Στεκόμαστε σε απόσταση (kick_radius * 0.8) για να είμαστε σίγουρα εντός εμβέλειας
        target_point = ball.position - shoot_dir * self.kick_radius
        
        for i, robot in enumerate(robots):
            # Διάνυσμα προς το σημείο στόχο
            u_des = target_point - robot.state[:2]
            dist_to_target = np.linalg.norm(u_des)
            
            # Υπολογισμός επιθυμητής γωνίας για κίνηση
            if dist_to_target > 0.05:
                theta_des = np.arctan2(u_des[1], u_des[0])
                # Κίνηση: ανάλογη της απόστασης, clamped στη μέγιστη ταχύτητα
                u_raw = dist_to_target
                u_clamped = min(u_raw, self.max_speed)
            else:
                # Έφτασε στο σημείο! Τώρα ευθυγραμμίζεται με το τέρμα για να σουτάρει
                theta_des = np.arctan2(shoot_dir[1], shoot_dir[0])
                u_clamped = 0.0
                
                # Αν κοιτάει σωστά το τέρμα (σφάλμα < 5 μοίρες), σουτάρει!
                head_err = self.wrap(theta_des - robot.state[2])
                if abs(head_err) <= np.radians(5):
                    kick = np.array([np.cos(robot.state[2]), np.sin(robot.state[2])]) * self.kick_force
                    ball.apply_kick(kick)
            
            # Υπολογισμός σφάλματος γωνίας και ωμέγα
            head_err = self.wrap(theta_des - robot.state[2])
            omega = self.robot_drive_k * head_err
            
            # ΜΕΤΑΤΡΟΠΗ ΣΕ WHEEL COMMANDS (vL, vR) όπως ζητάει η εκφώνηση (Σελίδα 4)
            # Αποθήκευση με βάση το index του ρομπότ
            actions.append(np.array([u_clamped, omega]))
            
        return actions
