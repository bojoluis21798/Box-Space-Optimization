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
    if posX + item.scaledX < box.scaledLength and posY + item.scaledY < box.scaledWidth and posZ + item.scaledZ < box.scaledHeight :
        limit = box.boxgrid[posX:posX + item.scaledX, posY:posY + item.scaledY, posZ:posZ + item.scaledZ]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("front1")
            ret = True

    # z,y,x position (front - 2)
    if posX + item.scaledZ < box.scaledLength and posY + item.scaledY < box.scaledWidth and posZ + item.scaledX < box.scaledHeight :
        limit = box.boxgrid[posX:posX + item.scaledZ, posY:posY + item.scaledY, posZ:posZ + item.scaledX]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("front2")
            ret = True

    # y,x,z position (side - 1)
    if posX + item.scaledY < box.scaledLength and posY + item.scaledX < box.scaledWidth and posZ + item.scaledZ < box.scaledHeight :
        limit = box.boxgrid[posX:posX + item.scaledY, posY:posY + item.scaledX, posZ:posZ + item.scaledZ]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("side1")
            ret = True

    # z,x,y position (side - 2)
    if posX + item.scaledZ < box.scaledLength and posY + item.scaledX < box.scaledWidth and posZ + item.scaledY < box.scaledHeight :
        limit = box.boxgrid[posX:posX + item.scaledZ, posY:posY + item.scaledX, posZ:posZ + item.scaledY]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("side2")
            ret = True

    # y,z,x position (up - 1)
    if posX + item.scaledY < box.scaledLength and posY + item.scaledZ < box.scaledWidth and posZ + item.scaledX < box.scaledHeight :
        limit = box.boxgrid[posX:posX + item.scaledY, posY:posY + item.scaledZ, posZ:posZ + item.scaledX]
        #check if all in splice is 0, otherwise return false
        if np.count_nonzero(limit) == 0:
            item.pos_state.append("up1")
            ret = True

    # x,z,y position (up - 2)
    if posX + item.scaledX < box.scaledLength and posY + item.scaledZ < box.scaledWidth and posZ + item.scaledY < box.scaledHeight :
        limit = box.boxgrid[posX:posX + item.scaledX, posY:posY + item.scaledZ, posZ:posZ + item.scaledY]
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
    if (posX < box.scaledLength and posX + item.scaledX < box.scaledLength) and (posY < box.scaledWidth and posY + item.scaledY < box.scaledWidth) and (posZ < box.scaledHeight and posZ + item.scaledZ < box.scaledHeight):
        ret = False
    # z,y,x position (front - 2)
    elif (posX < box.scaledLength and posX + item.scaledZ < box.scaledLength) and (posY < box.scaledWidth and posY + item.scaledY < box.scaledWidth) and (posZ < box.scaledHeight and posZ + item.scaledX < box.scaledHeight):
        ret = False
    # y,x,z position (side - 1)
    elif (posX < box.scaledLength and posX + item.scaledY < box.scaledLength) and (posY < box.scaledWidth and posY + item.scaledX < box.scaledWidth) and (posZ < box.scaledHeight and posZ + item.scaledZ < box.scaledHeight):
        ret = False
    # z,x,y position (side - 2)
    elif (posX < box.scaledLength and posX + item.scaledZ < box.scaledLength) and (posY < box.scaledWidth and posY + item.scaledX < box.scaledWidth) and (posZ < box.scaledHeight and posZ + item.scaledY < box.scaledHeight):
        ret = False
    # y,z,x position (up - 1)
    elif (posX < box.scaledLength and posX + item.scaledY < box.scaledLength) and (posY < box.scaledWidth and posY + item.scaledZ < box.scaledWidth) and (posZ < box.scaledHeight and posZ + item.scaledX < box.scaledHeight):
        ret = False
    # x,z,y position (up - 2)
    elif (posX < box.scaledLength and posX + item.scaledX < box.scaledLength) and (posY < box.scaledWidth and posY + item.scaledZ < box.scaledWidth) and (posZ < box.scaledHeight and posZ + item.scaledY < box.scaledHeight):
        ret = False

    return ret

# counts the number of free space around a position
def countFreeSpace(box, position, scaledX, scaledY, scaledZ):
    freeSpace = 0
    x,y,z = position[0], position[1], position[2]
    sideArea_1  = box.boxgrid[x + scaledX : box.scaledLength, y : y + scaledY, z : z + scaledZ]
    freeSpace   += (sideArea_1.size - np.count_nonzero(sideArea_1))

    sideArea_3  = box.boxgrid[x : 0, y : y + scaledY, z : z + scaledZ]                                    # opposite of 1
    freeSpace   += (sideArea_3.size - np.count_nonzero(sideArea_3))

    sideArea_2  = box.boxgrid[x : x + scaledX, y : y + scaledY, z + scaledZ : box.scaledHeight]
    freeSpace   += (sideArea_2.size - np.count_nonzero(sideArea_2))

    sideArea_4  = box.boxgrid[x : x + scaledX, y : y + scaledY, z : 0]                                    # opposite of 2
    freeSpace   += (sideArea_4.size - np.count_nonzero(sideArea_4))

    bottomArea  = box.boxgrid[x : x + scaledX, y + scaledY : box.scaledWidth, z: z + scaledZ]
    freeSpace   += (bottomArea.size - np.count_nonzero(bottomArea))

    topArea     = box.boxgrid[x : x + scaledX, y : 0, z : z + scaledZ]
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
            temp_spaceholder = countFreeSpace(box,pos, item.scaledX, item.scaledY, item.scaledZ)
        elif state == "front2":
            temp_spaceholder = countFreeSpace(box,pos, item.scaledZ, item.scaledY, item.scaledX)
        elif state == "side1":
            temp_spaceholder = countFreeSpace(box,pos, item.scaledY, item.scaledX, item.scaledZ)
        elif state == "side2":
            temp_spaceholder = countFreeSpace(box,pos, item.scaledZ, item.scaledX, item.scaledY)
        elif state == "up1":
            temp_spaceholder = countFreeSpace(box,pos, item.scaledY, item.scaledZ, item.scaledX)
        elif state == "up2":
            temp_spaceholder = countFreeSpace(box,pos, item.scaledX, item.scaledZ, item.scaledY)

        if temp_spaceholder < freeSpace:
            freeSpace = temp_spaceholder
            final_state = state
            # put adjustment of up and front here

    item.pos_state.clear()
    item.pos_state.append(final_state)

    return freeSpace

def getArrangementBasedFromState(item, baseX, baseY, baseZ):
    limitX = baseX + item.scaledX
    limitY = baseY + item.scaledY
    limitZ = baseZ + item.scaledZ
    #insert transformation here
    item.rotation = [0,0,0]
    if item.pos_state[0] == "front2":
        limitX = baseX + item.scaledZ
        limitY = baseY + item.scaledY
        limitZ = baseZ + item.scaledX
        #insert transformation here
        item.rotation = [0,90,0]
    elif item.pos_state[0] == "side1":
        limitX = baseX + item.scaledY
        limitY = baseY + item.scaledX
        limitZ = baseZ + item.scaledZ
        #insert transformation here
        item.rotation = [0,0,90]
    elif item.pos_state[0] == "side2":
        limitX = baseX + item.scaledZ
        limitY = baseY + item.scaledX
        limitZ = baseZ + item.scaledY
        #insert transformation here
        item.rotation = [90,0,90]
    elif item.pos_state[0] == "up1":
        limitX = baseX + item.scaledY
        limitY = baseY + item.scaledZ
        limitZ = baseZ + item.scaledX
        #insert transformation here
        item.rotation = [90,90,0]
    elif item.pos_state[0] == "up2":
        limitX = baseX + item.scaledX
        limitY = baseY + item.scaledZ
        limitZ = baseZ + item.scaledY
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

#transforms positions to center of the box
def scaleToCenter(ary_pos, items, box):
    newX = int(box.scaledLength / 2)
    newY = int(box.scaledWidth / 2)
    newZ = int(box.scaledHeight / 2)

    for i in range(1, len(ary_pos)):

        if items[i].pos_state[0] == "front1":
            localX = int((ary_pos[i][0] + items[i].scaledX - 1) / 2)
            localY = int((ary_pos[i][1] + items[i].scaledY - 1) / 2)
            localZ = int((ary_pos[i][2] + items[i].scaledZ - 1) / 2)
        elif items[i].pos_state[0] == "front2":
            localX = int((ary_pos[i][0] + items[i].scaledZ - 1) / 2)
            localY = int((ary_pos[i][1] + items[i].scaledY - 1) / 2)
            localZ = int((ary_pos[i][2] + items[i].scaledX - 1) / 2)
        elif items[i].pos_state[0] == "side1":
            localX = int((ary_pos[i][0] + items[i].scaledY - 1) / 2)
            localY = int((ary_pos[i][1] + items[i].scaledX - 1) / 2)
            localZ = int((ary_pos[i][2] + items[i].scaledZ - 1) / 2)
        elif items[i].pos_state[0] == "side2":
            localX = int((ary_pos[i][0] + items[i].scaledZ - 1) / 2)
            localY = int((ary_pos[i][1] + items[i].scaledX - 1) / 2)
            localZ = int((ary_pos[i][2] + items[i].scaledY - 1) / 2)
        elif items[i].pos_state[0] == "up1":
            localX = int((ary_pos[i][0] + items[i].scaledY - 1) / 2)
            localY = int((ary_pos[i][1] + items[i].scaledZ - 1) / 2)
            localZ = int((ary_pos[i][2] + items[i].scaledX - 1) / 2)
        elif items[i].pos_state[0] == "up2":
            localX = int((ary_pos[i][0] + items[i].scaledX - 1) / 2)
            localY = int((ary_pos[i][1] + items[i].scaledZ - 1) / 2)
            localZ = int((ary_pos[i][2] + items[i].scaledY - 1) / 2)

        ary_pos[i][0] = localX - newX
        ary_pos[i][1] = localY - newY
        ary_pos[i][2] = localZ - newZ


# Do optimization here
def optimize(models, scaledLength, scaledWidth, scaledHeight):
    pass
    best_mainBox = None
    best_models_inside = []
    best_models_position = []
    best_percentage = 0
    best_error = sys.maxsize

    termination_counter = 0                         # counts the number of convergence of optimization
    maingen = 0
    while termination_counter < 10:
        # start of solitary phase
            # initialization (identification)
            # updating       (verification)

        #initialization part one
        models_inside = [None]                                                      # None becuase modelid 0 is equivalent to empty in box
        models_position = [None]
        mainBox = Box(scaledLength,scaledWidth,scaledHeight)                                                  # user input, but for now is not. box(scaledLength,scaledWidth,scaledHeight) in inches
        models_local_error = sys.maxsize

        sample_solution = [0,0,0]
        numParticles = 30
        bounds = [(0,mainBox.scaledLength-1), (0,mainBox.scaledWidth-1), (0,mainBox.scaledHeight-1)]            #bounds for search space (min,max)

        problem_dimensions = len(sample_solution)
        vel_limit = [int(bounds[0][1] * 0.10), int(bounds[1][1] * 0.10), int(bounds[2][1] * 0.10)]

        for model in models:
            is_insertable = True
            if model.id == sys.maxsize:
                continue

            #assume everything is filled and not a container //limitation
            volume = model.scaledSolidVolume

            if volume > mainBox.scaledTotalVolume:
                break

            if volume > mainBox.scaledTotalVolume - mainBox.scaledTotalObjectVolume:
                continue

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

                subgen+=1

            if is_insertable == False:
                continue

            # solution (attack)
            models_inside.append(model)
            insertToBox(mainBox, model, pos_best_g, model.modelNum)
            mainBox.scaledTotalObjectVolume += volume
            mainBox.totalObjectVolume += model.solidVolume
            models_position.append(pos_best_g)
            models_local_error = err_best_g
            print(f"Generated coordinates for Model Num = {model.modelNum} is {pos_best_g}")

        if len(models_inside) == 1:
            input("cant fit anything side the box")
            break

        current_percentage = (mainBox.scaledTotalObjectVolume/mainBox.scaledTotalVolume)*100
        if float(best_percentage) == float(current_percentage):
            termination_counter+=1
            if best_error > models_local_error:
                best_mainBox = mainBox
                best_models_inside = models_inside
                best_models_position = models_position
                best_percentage = current_percentage
                best_error = models_local_error

        if current_percentage > best_percentage:
            best_mainBox = mainBox
            best_models_inside = models_inside
            best_models_position = models_position
            best_percentage = current_percentage
            best_error = models_local_error
            termination_counter = 0
        
        print(f">>>>>Generation {maingen} solution: {best_models_position}")
        print(f"current best_error = {best_error}")
        maingen+=1

    if len(best_models_inside) != 0:
        print(f"Best box space optimization: {best_percentage}")
        print(f"Models position: {best_models_position}")
        scaleToCenter(best_models_position,best_models_inside, best_mainBox)
        print(f"Models position scaled: {best_models_position}")
        print(f"Number of loaded models over inserted: {len(models) -1} / {len(best_models_inside) -1}")
        states = [best_models_inside[i].pos_state for i in range(1,len(best_models_inside))]
        print(f" states: {states}")
        input("Press enter to visualize results ")

    else:
        input("use a bigger box ..")

    return best_mainBox, best_models_inside, best_models_position
    
    

