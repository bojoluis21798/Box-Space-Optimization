class LocustParticle:
    def __init__():
        self.state = 0          # 0 - solitary, 1 - gregarious
        self.position_i = []    # particle position
        self.pos_best_i = []    # best position (self, not group)
        self.err_best_i=-1      # best error individual
        self.err_i=-1           # error individual

    # evaluate this particle's current fitness
    def evaluate(self, costFunc, box):
        self.err_i=costFunc(self.position_i, box)
        
        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i
            self.err_best_i = self.err_i
