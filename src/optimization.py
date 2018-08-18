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

    sideArea_1  = box.boxgrid[x + item.dimX : box.length, y : y + item.dimY, z : z + item.dimZ]
    freeSpace   += (sideArea_1.size - np.count_nonzero(sideArea_1))

    sideArea_3  = box.boxgrid[x : 0, y : y + item.dimY, z : z + item.dimZ]                                 # opposite of 1
    freeSpace   += (sideArea_3.size - np.count_nonzero(sideArea_3))

    sideArea_2  = box.boxgrid[x : x + item.dimX, y : y + item.dimY, z + item.dimZ : box.height]
    freeSpace   += (sideArea_2.size - np.count_nonzero(sideArea_2))

    sideArea_4  = box.boxgrid[x : x + item.dimX, y : y + item.dimY, z : 0]                               # opposite of 2
    freeSpace   += (sideArea_4.size - np.count_nonzero(sideArea_4))

    bottomArea  = box.boxgrid[x : x + item.dimX, y + item.dimY : box.width, z: z + item.dimZ]
    freeSpace   += (bottomArea.size - np.count_nonzero(bottomArea))

    topArea     = box.boxgrid[x : x + item.dimX, y : 0, z : z + item.dimZ]
    freeSpace   += (topArea.size - np.count_nonzero(topArea))

    # return number of empty cells found (mm)
    return freeSpace

# insert an item inside the box
# dont need to return anything since arrays are passed by reference
def insertToBox(box, item, pos, itemNum):    
    x,y,z = pos[0], pos[1], pos[2]
    limitX, limitY, limitZ = x + item.dimX, y + item.dimY, z + item.dimZ
    while x < limitX:
        y = pos[1]
        while y < limitY:
            z = pos[2]
            while z < limitZ:
                box.boxgrid[x,y,z] = itemNum
                z+=1
            y+=1
        x+=1

# Do optimization here
def optimize(models):
    pass
    best_mainBox = None
    best_models_inside = []
    best_models_position = []
    best_percentage = 0

    termination_counter = 0                         # counts the number of convergence of optimization
    maingen = 0
    while termination_counter < 10:
        print(f">>>>>>>>>>>Generation {maingen}")
        # start of solitary phase
            # initialization (identification)
            # updating       (verification)
            
        #initialization part one
        models_inside = [None]                                                      # None becuase modelid 0 is equivalent to empty in box
        models_position = [None]
        mainBox = Box(18,18,24)                                                     # user input, but for now is not. box(length,width,height) in inches
        
        numParticles = 30
        initial = [0,0,0]                                                               #initial location of particles
        bounds = [(0,mainBox.length-1), (0,mainBox.width-1), (0,mainBox.height-1)]            #bounds for search space (min,max)

        problem_dimensions = len(initial)
        vel_limit = int(mainBox.height * 0.10)

        for model in models:
            is_insertable = True
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
                swarm.append(LocustParticle(initial,problem_dimensions,bounds,vel_limit))
            
            #verification
            inside_termination_ctr = 0
            subgen = 0
            while inside_termination_ctr < 10:
                print("=====================================================")
                print(f"Generation # {maingen}{subgen}")
                #insert locust work here on item
                current_err_best = err_best_g
                for j in range(0, numParticles):
                    swarm[j].addItem(model)
                    swarm[j].evaluate(objectiveFunctionSpace, mainBox)
                    
                    # update global bests
                    # gregarious phase - analysis part 1
                    if swarm[j].err_i < err_best_g or err_best_g == -1:
                        pos_best_g = list(swarm[j].position_i)
                        err_best_g = int(swarm[j].err_i)
                        inside_termination_ctr = 0
                    
                if current_err_best == err_best_g:
                    inside_termination_ctr+=1
                
                if err_best_g == sys.maxsize:
                    is_insertable = False
                    break

                # cycle through swarm and update velocities and position
                # gregarious phase - analysis part 2
                for j in range(0,numParticles):
                    swarm[j].updateVelocity(pos_best_g, problem_dimensions)    
                    swarm[j].updatePosition(bounds, problem_dimensions)

                print(f"Current pos_best_g {pos_best_g}")
                subgen+=1
            
            if is_insertable == False:
                print(f"Skipped Model with ID = {model.id} and Model Num = {model.modelNum} due to space unavailability")
                continue
                
            # solution (attack)
            insertToBox(mainBox, model, pos_best_g, model.modelNum)
            mainBox.totalObjectVolume += volume
            models_position.append(pos_best_g)
            print(f"Generated coordinates for Model Num = {model.modelNum} is {pos_best_g}")
            input("Press enter to work on the next model ... ")

        print(f"total object volume = {mainBox.totalObjectVolume} and box total volume = {mainBox.totalVolume}")
        current_percentage = mainBox.totalObjectVolume/mainBox.totalVolume)*100
        print(f"Current optimized space for box = {(current_percentage}%")

        if float(best_percentage) == round(current_percentage, 1):
            termination_counter+=1

        if current_percentage > best_percentage:
            best_mainBox = mainBox
            best_models_inside = models_inside
            best_models_position = models_position
            best_percentage = current_percentage
            termination_counter = 0
        
        print(f">>>>>Generation {maingen} solution: {best_models_position}")
        maingen+=1
        input("Press enter to go back to menu .... ")
    