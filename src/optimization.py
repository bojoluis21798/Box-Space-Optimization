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

    #start of solitary phase
        #initialization (identification)
        #updating       (verification)
    
    # identification
    maxIter = 30 
    numParticles = 30
    mainBox = Box(18,18,24)                                                 #user input, but for now is not. box(length,width,height) in inches
    initial = []                                                            #initial location of particles
    bounds = [(0,mainBox.length), (0,mainBox.width), (0,mainBox.height)]    #bounds for search space (min,max)

    problem_dimensions = len(initial)
    err_best_g = -1                                                         #global best error
    pos_best_g = []                                                         #global best position

    swarm = []                                                              #locust swarm
    for i in range(0,numParticles):
        swarm.append(LocustParticle(bounds,problem_dimensions))
        
    #verification
    for model in models:
        volume = model.surfaceVolume if model.isContainer == True else model.solidVolume

        if volume > mainBox.totalVolume or volume > mainbox.totalVolume - mainbox.totalObjectVolume:
            continue
        
        #insert locust work here on item

