from src.model import Model
from src.box import Box
from src.locustParticle import LocustParticle

 # refer to fitness equation of document
 # stop the optimization if box is at 100% or near but cant add any more object
def terminationCriteria(item, box):

    # checks if item is container-like or not and gets appropriate volume
    addedVolume  = (item.surfaceVolume + box.totalObjectVolume) if item.isContainer == True else (item.solidVolume + box.totalObjectVolume)
    
    #maybe add insert operation here? or just do it to the calling function

    #check if addedVolume of objects inside box is less than volume of box
    return (addedVolume/box.totalVolume) if addedVolume <= box.totalVolume else -1

# this is the actual fitness equation for the optimization
def objectiveFunctionSpace(item, pos, box):

    def resetPosition(pos):
        return pos[0], pos[1], pos[2]

    freeSpace = 0
    # [x,y,z] is the starting position of the item location

    # search the radial location of the item location (bottom and sides)
    # increment x til an occupied cell is found or bound is reached
    # decrement x til an occupied cell is found or bound is reached
    # increment y til an occupied cell is found or bound is reached
    # decrement y til an occupied cell is found or bound is reached
    # increment z til an occupied cell is found or bound is reached
    # decrement z til an occupied cell is found or bound is reached

    #### alternative
    #### use of splice
    #### limit = box[posX:posX + item.dimX, posY:posY + item.dimY, posZ:posZ + item.dimZ]
    x,y,z = resetPosition(pos)

    #check addition or make sure passed position is available and valid
    sideArea_1  = box.boxgrid[x + item.dimX : box.length, y : item.dimY, z : item.dimZ]
    freeSpace   += (sideArea_1.size - np.count_nonzero(sideArea_1))

    sideArea_3  = box.boxgrid[x:0, y : item.dimY, z : item.dimZ]                                 # opposite of 1
    freeSpace   += (sideArea_3.size - np.count_nonzero(sideArea_3))

    sideArea_2  = box.boxgrid[x : item.dimX, y : item.dimY, z + item.dimZ : box.height]
    freeSpace   += (sideArea_2.size - np.count_nonzero(sideArea_2))

    sideArea_4  = box.boxgrid[x : item.dimX, y : item.dimY, z : 0]                               # opposite of 2
    freeSpace   += (sideArea_4.size - np.count_nonzero(sideArea_4))

    bottomArea  = box.boxgrid[x : item.dimX, y + item.dimY : box.width, z: item.dimZ]
    freeSpace   += (bottomArea.size - np.count_nonzero(bottomArea))

    topArea     = box.boxgrid[x: item.dimX, y : 0, z : item.dimZ]
    freeSpace   += (topArea.size - np.count_nonzero(topArea))

    # return number of empty cells found (mm)
    return freeSpace

# insert an item inside the box; assuming the given pos is an empty space
def insertToBox(box, item, pos, itemNum):    
    x = pos[0]
    while x < x + item.dimX:
        y = pos[1]
        while y < y + item.dimY:
            z = pos[2]
            while z < z + item.dimZ:
                boxgrid[i,j,k] = itemNum
                z+=1
            y+=1
        z+=1

# Do optimization here
def optimize(models):
    # start of solitary phase
        # initialization (identification)
        # updating       (verification)
        
    #initialization part one
    models_inside = [None]                                                      # None becuase modelid 0 is equivalent to empty in box
    models_position = [None]
    model_tracker = 0                                                           # assigns a model id to each item inserted
    mainBox = Box(18,18,24)                                                     # user input, but for now is not. box(length,width,height) in inches
    
    maxIter = 30 
    numParticles = 30
    initial = [0,0,0]                                                               #initial location of particles
    bounds = [(0,mainBox.length), (0,mainBox.width), (0,mainBox.height)]            #bounds for search space (min,max)

    problem_dimensions = len(initial)

    for model in models:
        volume = model.surfaceVolume if model.isContainer == True else model.solidVolume

        if volume > mainBox.totalVolume:
            break

        if volume > mainbox.totalVolume - mainbox.totalObjectVolume:
            continue
        
        models_inside.append(model)

        # identification (initialization part two)
        err_best_g = -1                                                         #global best error
        pos_best_g = []                                                         #global best position

        swarm = []                                                              #locust swarm
        for i in range(0,numParticles):
            swarm.append(LocustParticle(initial,problem_dimensions))
        
        #verification
        i = 0
        while i < maxIter:
            #insert locust work here on item
            for j in range(0, numParticles):
                swarm[j].addItem(model)
                swarm[j].evaluate(objectiveFunctionSpace, mainBox)
                
                # update global bests
                # add checker here
                # gregarious phase - analysis part 1
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = float(swarm[j].err_i)
            
            # cycle through swarm and update velocities and position
            # gregarious phase - analysis part 2
            for j in range(0,num_particles):
                swarm[j].update_velocity(pos_best_g, problem_dimensions)    
                swarm[j].update_position(bounds, problem_dimensions)        #questionnable due to space checking

            i+=1
        
        # solution (attack)
        model_tracker+=1
        insertToBox(box, model, pos_best_g, model_tracker)
        models_position.append(pos_best_g)
