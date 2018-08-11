from src.model import Model
from src.box import Box
from src.locustParticle import LocustParticle

 #refer to fitness equation of document
def objectiveFuncBox(item, box):

    # checks if item is container-like or not and gets appropriate volume
    addedVolume  = (item.surfaceVolume + box.totalObjectVolume) if item.isContainer == True else (item.solidVolume + box.totalObjectVolume)
    
    #maybe add insert operation here? or just do it to the calling function

    #check if addedVolume of objects inside box is less than volume of box
    return (addedVolume/box.totalVolume) if addedVolume <= box.totalVolume else -1

# Do optimization here
def optimize(models):
    pass
    # start of solitary phase
        # initialization (identification)
        # updating       (verification)
        
    #initialization part one
    models_inside = []
    models_position = []
    mainBox = Box(18,18,24)                                                     #user input, but for now is not. box(length,width,height) in inches
    
    maxIter = 30 
    numParticles = 30
    initial = []                                                            #initial location of particles
    bounds = [(0,mainBox.length), (0,mainBox.width), (0,mainBox.height)]    #bounds for search space (min,max)

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
                swarm[j].evaluate(objectiveFuncBox, mainBox)    #passing objectiveFunc for items, not box space
                
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
                swarm[j].update_position(bounds, problem_dimensions)

            i+=1
        
        # solution (attack)
        models_position.append(pos_best_g)
