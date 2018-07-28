import random

# doesnt conform to a 3D box yet, just 1d array pa
class LocustParticle:
    def __init__(self, bounds, num_dimensions):
        self.state = 0              # 0 - solitary, 1 - gregarious
        self.position_i = []        # particle position
        self.velocity_i = []        # particle current velocity
        self.pos_best_i = []        # best position (self, not group)
        self.err_best_i=-1          # best error individual
        self.err_i=-1               # error individual
        self.c1 = 1                 # cognitive parameter constant
        self.c2 = 2                 # social parameter constant
        self.w = 0.5                # inertia constant

        for i in range(0,num_dimensions):
            self.velocity_i.append(random.uniform(-1,1)) #### why (-1,1)
            self.position_i.append(bounds[i])

    # evaluate this particle's current fitness
    def evaluate(self, costFunc, box):
        self.err_i=costFunc(self.position_i, box)
        
        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i
            self.err_best_i = self.err_i

    # update particles velocity
    def updateVelocity(self, pos_best_g, num_dimensions):
        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = self.c1 * r1 * ( self.pos_best_i[i] - self.position_i[i] )
            vel_social = self.c2 * r2 * ( pos_best_g[i] - self.position_i[i] )
            self.velocity_i[i] = self.w * self.velocity_i[i] + vel_cognitive +vel_social 
