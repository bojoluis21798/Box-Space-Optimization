import random

# doesnt conform to a 3D box yet, just 1d array pa
class LocustParticle:

    def __init__(self, initials, num_dimensions, item = None):
        self.state = 0              # 0 - solitary, 1 - gregarious
        self.position_i = []        # particle position
        self.velocity_i = []        # particle current velocity
        self.pos_best_i = []        # best position (self, not group)
        self.err_best_i=-1          # best error individual
        self.err_i=-1               # error individual
        self.c1 = 1                 # cognitive parameter constant
        self.c2 = 2                 # social parameter constant
        self.w = 0.5                # inertia constant
        self.item = item            # the item it currently is looking for an optimal space

        for i in range(0,num_dimensions):
            self.velocity_i.append(random.uniform(-1,1))    #### why (-1,1)
            self.position_i.append(initials[i])             #check if space is available;
                                                            #can also be randomed

    def addItem(self, item):
        self.item = item           # add item for particle to find space for
    
    # evaluate this particle's current fitness
    # needs adjustment
    def evaluate(self, costFunc, box):
        self.err_i = costFunc(self.position_i, box)
        
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
            self.velocity_i[i] = self.w * self.velocity_i[i] + vel_cognitive + vel_social

    # update particles position
    # questionnable because this position is 1d
    def updatePosition(self, bounds, num_dimensions):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i] + self.velocity_i[i] #check if space is available

            # adjust maximum position if necessary
            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i] = bounds[i][0]

    # @params item = self.item
    # @params position = given particle position
    # @params box = box space being  worked on (probably bounds)
    # this function is used assuming a particle position is the beginning of the space
    def checkSpaceAvailability(item, position, box):
        #get item dimensions
        #compare with position if available in box
        ret = False
        posX = position[0]
        posY = position[1]
        posZ = position[2]
        #check if not over the box dimensions
        if posX + item.dimX < box.convertMeterToMilli(box.length) and posY + item.dimY < convertMeterToMilli(box.width)  and posZ < convertMeterToMilli(box.height) :
            limit = box[posX:posX + item.dimX, posY:posY + item.dimY, posZ:posZ + item.dimZ]
            #check if all in splice is 0, otherwise return false
            if np.count_nonzero(limit) == 0:
                ret = True
        
        return ret
        

