from src.optimization import objectiveFunc

class LocustParticle:
    def __init__():
        self.state = 0          # 0 - solitary, 1 - gregarious
        self.position_i = []    # particle position
        self.pos_best_i = []    # best position (self, not group)
        self.err_best_i=-1      # best error individual
        self.err_i=-1           # error individual

