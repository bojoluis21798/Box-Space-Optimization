import numpy as np
import sys

from src.model import Model
from src.box import Box
from src.locustParticle import LocustParticle

# @params item = self.item
# @params position = given particle position
# @params box = box space being  worked on (probably bounds)
# this function is used assuming a particle position is the beginning of the space
def isSpaceAvailable(item, position, box):
    #get item dimensions
    #compare with position if available in box
    ret = False
    posX = position[0]
    posY = position[1]
    posZ = position[2]
    #check if not over the box dimensions
    if posX + item.dimX < box.length) and posY + item.dimY < box.width  and posZ < box.height :
        limit = box.boxgrid[posX:posX + item.dimX, posY:posY + item.dimY, posZ:posZ + item.dimZ]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            ret = True       
    return ret

def isOverBound(item, position, box):
    ret = True
    posX = position[0]
    posY = position[1]
    posZ = position[2]
    if (posX < box.length and posX + item.dimX < box.length) and (posY < box.width and posY + item.dimY < box.width) and (posZ < box.height and posZ + item.dimZ < box.height):
        ret = False
    
    return ret

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
    freeSpace = 0
    x,y,z = pos[0], pos[1], pos[2]
    
    if isOverBound(item, pos, box):
        return sys.maxsize

    if not isSpaceAvailable(item, pos, box):
        return sys.maxsize

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
# dont need to return anything since arrays are passed by reference
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
    pass
    # start of solitary phase
        # initialization (identification)
        # updating       (verification)
        
    #initialization part one
    models_inside = [None]                                                      # None becuase modelid 0 is equivalent to empty in box
    models_position = [None]
    mainBox = Box(18,18,24)                                                     # user input, but for now is not. box(length,width,height) in inches
    
    maxIter = 30 
    numParticles = 30
    initial = [0,0,0]                                                               #initial location of particles
    bounds = [(0,mainBox.length), (0,mainBox.width), (0,mainBox.height)]            #bounds for search space (min,max)

    problem_dimensions = len(initial)

    for model in models:
        if model.id == sys.maxsize:
            continue

        print(f"Working on {model.name} with ID = {model.id} and Model Num ={model.modelNum}")
        volume = model.surfaceVolume if model.isContainer == True else model.solidVolume

        if volume > mainBox.totalVolume:
            break

        if volume > mainBox.totalVolume - mainBox.totalObjectVolume:
            print(f"Skipped Model with ID = {model.id} and Model Num = {model.modelNum} due to space unavailability")
            continue
        
        models_inside.append(model)
        print(f"Optimizing on {model.name} with Model Num = {model.modelNum}")
        # identification (initialization part two)
        err_best_g = -1                                                         #global best error
        pos_best_g = []                                                         #global best position

        swarm = []                                                              #locust swarm
        for i in range(0,numParticles):
            swarm.append(LocustParticle(initial,problem_dimensions))
        
        #verification
        i = 0
        while i < maxIter:
            print("=====================================================")
            print(f"Generation # {i}")
            #insert locust work here on item
            for j in range(0, numParticles):
                swarm[j].addItem(model)
                swarm[j].evaluate(objectiveFunctionSpace, mainBox)
                
                # update global bests
                # gregarious phase - analysis part 1
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = float(swarm[j].err_i)
            
            # cycle through swarm and update velocities and position
            # gregarious phase - analysis part 2
            for j in range(0,numParticles):
                swarm[j].updateVelocity(pos_best_g, problem_dimensions)    
                swarm[j].updatePosition(bounds, problem_dimensions)

            print(f"Current pos_best_g {pos_best_g}")
            i+=1
        
        # solution (attack)
        insertToBox(box, model, pos_best_g, model.modelNum)
        models_position.append(pos_best_g)
        print(f"Generated coordinates for Model Num = {model.modelNum} is {pos_best_g}")
