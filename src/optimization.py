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
    # x,y,z position (front - 1)
    if posX + item.dimX < box.length and posY + item.dimY < box.width and posZ + item.dimZ < box.height :
        limit = box.boxgrid[posX:posX + item.dimX, posY:posY + item.dimY, posZ:posZ + item.dimZ]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("front1")
            ret = True
    
    # z,y,x position (front - 2)
    if posX + item.dimZ < box.length and posY + item.dimY < box.width and posZ + item.dimX < box.height :
        limit = box.boxgrid[posX:posX + item.dimZ, posY:posY + item.dimY, posZ:posZ + item.dimX]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("front2")
            ret = True

    # y,x,z position (side - 1)
    if posX + item.dimY < box.length and posY + item.dimX < box.width and posZ + item.dimZ < box.height :
        limit = box.boxgrid[posX:posX + item.dimY, posY:posY + item.dimX, posZ:posZ + item.dimZ]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("side1")
            ret = True

    # z,x,y position (side - 2)
    if posX + item.dimZ < box.length and posY + item.dimX < box.width and posZ + item.dimY < box.height :
        limit = box.boxgrid[posX:posX + item.dimZ, posY:posY + item.dimX, posZ:posZ + item.dimY]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("side2")
            ret = True
    
    # y,z,x position (up - 1)
    if posX + item.dimY < box.length and posY + item.dimZ < box.width and posZ + item.dimX < box.height :
        limit = box.boxgrid[posX:posX + item.dimY, posY:posY + item.dimZ, posZ:posZ + item.dimX]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("up1")
            ret = True
    
    # x,z,y position (up - 2)
    if posX + item.dimX < box.length and posY + item.dimZ < box.width and posZ + item.dimY < box.height :
        limit = box.boxgrid[posX:posX + item.dimX, posY:posY + item.dimZ, posZ:posZ + item.dimY]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("up2")
            ret = True
       
    return ret

def isOverBound(item, position, box):
    ret = True
    posX = position[0]
    posY = position[1]
    posZ = position[2]
    #can be made into one condition but is not very readable
    # x,y,z position (front - 1)
    if (posX < box.length and posX + item.dimX < box.length) and (posY < box.width and posY + item.dimY < box.width) and (posZ < box.height and posZ + item.dimZ < box.height):
        ret = False
    # z,y,x position (front - 2)
    elif (posX < box.length and posX + item.dimZ < box.length) and (posY < box.width and posY + item.dimY < box.width) and (posZ < box.height and posZ + item.dimX < box.height):
        ret = False
    # y,x,z position (side - 1)
    elif (posX < box.length and posX + item.dimY < box.length) and (posY < box.width and posY + item.dimX < box.width) and (posZ < box.height and posZ + item.dimZ < box.height):
        ret = False
    # z,x,y position (side - 2)
    elif (posX < box.length and posX + item.dimZ < box.length) and (posY < box.width and posY + item.dimX < box.width) and (posZ < box.height and posZ + item.dimY < box.height):
        ret = False
    # y,z,x position (up - 1)
    elif (posX < box.length and posX + item.dimY < box.length) and (posY < box.width and posY + item.dimZ < box.width) and (posZ < box.height and posZ + item.dimX < box.height):
        ret = False
    # x,z,y position (up - 2)
    elif (posX < box.length and posX + item.dimX < box.length) and (posY < box.width and posY + item.dimZ < box.width) and (posZ < box.height and posZ + item.dimY < box.height):
        ret = False

    return ret

# counts the number of free space around a position
def countFreeSpace(box, position, dimX, dimY, dimZ):
    freeSpace = 0
    x,y,z = position[0], position[1], position[2]
    sideArea_1  = box.boxgrid[x + dimX : box.length, y : y + dimY, z : z + dimZ]
    freeSpace   += (sideArea_1.size - np.count_nonzero(sideArea_1))

    sideArea_3  = box.boxgrid[x : 0, y : y + dimY, z : z + dimZ]                                    # opposite of 1
    freeSpace   += (sideArea_3.size - np.count_nonzero(sideArea_3))

    sideArea_2  = box.boxgrid[x : x + dimX, y : y + dimY, z + dimZ : box.height]
    freeSpace   += (sideArea_2.size - np.count_nonzero(sideArea_2))

    sideArea_4  = box.boxgrid[x : x + dimX, y : y + dimY, z : 0]                                    # opposite of 2
    freeSpace   += (sideArea_4.size - np.count_nonzero(sideArea_4))

    bottomArea  = box.boxgrid[x : x + dimX, y + dimY : box.width, z: z + dimZ]
    freeSpace   += (bottomArea.size - np.count_nonzero(bottomArea))

    topArea     = box.boxgrid[x : x + dimX, y : 0, z : z + dimZ]
    freeSpace   += (topArea.size - np.count_nonzero(topArea))

    # return number of empty cells found (mm)
    return freeSpace

# this is the actual fitness equation for the optimization
def objectiveFunctionSpace(item, pos, box):
    freeSpace = sys.maxsize
    x,y,z = pos[0], pos[1], pos[2]
    
    if isOverBound(item, pos, box):
        return sys.maxsize

    if not isSpaceAvailable(item, pos, box):
        return sys.maxsize
    
    final_state = "front1"
    # enter comparison of pos_state heree
    for state in item.pos_state:
        temp_spaceholder = 0

        if state == "front1":
            temp_spaceholder = countFreeSpace(box,pos, item.dimX, item.dimY, item.dimZ)
        elif state == "front2":
            temp_spaceholder = countFreeSpace(box,pos, item.dimZ, item.dimY, item.dimX)
        elif state == "side1":
            temp_spaceholder = countFreeSpace(box,pos, item.dimY, item.dimX, item.dimZ)
        elif state == "side2":
            temp_spaceholder = countFreeSpace(box,pos, item.dimZ, item.dimX, item.dimY)
        elif state == "up1":
            temp_spaceholder = countFreeSpace(box,pos, item.dimY, item.dimZ, item.dimX)
        elif state == "up2":
            temp_spaceholder = countFreeSpace(box,pos, item.dimX, item.dimZ, item.dimY)
        
        if temp_spaceholder < freeSpace:
            freeSpace = temp_spaceholder
            final_state = state
            # put adjustment of up and front here

    item.pos_state.clear()
    item.pos_state.append(final_state)

    return freeSpace

def getArrangementBasedFromState(item, baseX, baseY, baseZ):
    limitX = baseX + item.dimX
    limitY = baseY + item.dimY
    limitZ = baseZ + item.dimZ
    #insert transformation here
    item.rotation = [0,0,0]
    if item.pos_state[0] == "front2":
        limitX = baseX + item.dimZ
        limitY = baseY + item.dimY
        limitZ = baseZ + item.dimX
        #insert transformation here
        item.rotation = [0,90,0]
    elif item.pos_state[0] == "side1":
        limitX = baseX + item.dimY
        limitY = baseY + item.dimX
        limitZ = baseZ + item.dimZ
        #insert transformation here
        item.rotation = [0,0,90]
    elif item.pos_state[0] == "side2":
        limitX = baseX + item.dimZ
        limitY = baseY + item.dimX
        limitZ = baseZ + item.dimY
        #insert transformation here
        item.rotation = [90,0,90]
    elif item.pos_state[0] == "up1":
        limitX = baseX + item.dimY
        limitY = baseY + item.dimZ
        limitZ = baseZ + item.dimX
        #insert transformation here
        item.rotation = [90,90,0]
    elif item.pos_state[0] == "up2":
        limitX = baseX + item.dimX
        limitY = baseY + item.dimZ
        limitZ = baseZ + item.dimY
        #insert transformation here
        item.rotation = [90,0,0]
        
    return limitX, limitY, limitZ

# insert an item inside the box
# dont need to return anything since arrays are passed by reference
def insertToBox(box, item, pos, itemNum):
    x,y,z = pos[0], pos[1], pos[2]
    limitX, limitY, limitZ = getArrangementBasedFromState(item,x,y,z)
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
        
        sample_solution = [0,0,0]
        numParticles = 30
        bounds = [(0,mainBox.length-1), (0,mainBox.width-1), (0,mainBox.height-1)]            #bounds for search space (min,max)

        problem_dimensions = len(sample_solution)
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
            
            print(f"Optimizing on {model.name} with Model Num = {model.modelNum}")
            # identification (initialization part two)
            err_best_g = -1                                                         #global best error
            pos_best_g = []                                                         #global best position

            swarm = []                                                              #locust swarm
            for i in range(0,numParticles):
                swarm.append(LocustParticle(problem_dimensions,bounds,vel_limit))
            
            #verification
            inside_termination_ctr = 0
            subgen = 0
            while inside_termination_ctr < 10:
                print("=====================================================")
                print(f"Generation # {maingen}-{subgen}")
                #insert locust work here on item
                current_err_best = err_best_g
                for j in range(0, numParticles):
                    swarm[j].addItem(model)
                    swarm[j].evaluate(objectiveFunctionSpace, mainBox)
                    
                    # update global bests
                    # gregarious phase - analysis part 1
                    if swarm[j].err_i < err_best_g or err_best_g == -1:
                        model = swarm[j].item                                   # in case the particle updated the model attributes
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
                print(f"Current err_best: {err_best_g}")
                subgen+=1
            
            if is_insertable == False:
                print(f"Skipped Model with ID = {model.id} and Model Num = {model.modelNum} due to space unavailability")
                continue
                
            # solution (attack)
            models_inside.append(model)
            insertToBox(mainBox, model, pos_best_g, model.modelNum)
            mainBox.totalObjectVolume += volume
            models_position.append(pos_best_g)
            print(f"Generated coordinates for Model Num = {model.modelNum} is {pos_best_g}")

        print(f"total object volume = {mainBox.totalObjectVolume} and box total volume = {mainBox.totalVolume}")
        current_percentage = (mainBox.totalObjectVolume/mainBox.totalVolume)*100
        print(f"Current optimized space for box = {(current_percentage)}%")
        print(f"Number of loaded models over inserted: {len(models) -1} / {len(models_inside) -1}")

        if float(best_percentage) == float(current_percentage):
            termination_counter+=1

        if current_percentage > best_percentage:
            best_mainBox = mainBox
            best_models_inside = models_inside
            best_models_position = models_position
            best_percentage = current_percentage
            termination_counter = 0
        
        print(f">>>>>Generation {maingen} solution: {best_models_position}")
        maingen+=1

    print(f"Best box space optimization: {best_percentage}")
    print(f"Models position: {best_models_position}")
    print(f"Number of loaded models over inserted: {len(models) -1} / {len(best_models_inside) -1}")
    states = [best_models_inside[i].pos_state for i in range(1,len(best_models_inside))]
    print(f" states: {states}")
    input("Press enter to visualize results ")
    