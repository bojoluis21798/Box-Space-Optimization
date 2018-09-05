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

    topArea     = box.boxgrid[x : x + scaledX, y : y + scaledY, z + scaledZ : box.scaledHeight]
    freeSpace   += (topArea.size - np.count_nonzero(topArea))

    bottomArea  = box.boxgrid[x : x + scaledX, y : y + scaledY, z : 0]                                    # opposite of 2
    freeSpace   += (bottomArea.size - np.count_nonzero(bottomArea))

    sideArea_2  = box.boxgrid[x : x + scaledX, y + scaledY : box.scaledWidth, z: z + scaledZ]
    freeSpace   += (sideArea_2.size - np.count_nonzero(sideArea_2))

    sideArea_4  = box.boxgrid[x : x + scaledX, y : 0, z : z + scaledZ]
    freeSpace   += (sideArea_4.size - np.count_nonzero(sideArea_4))
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
        temp_spaceholder = -1

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

    item.pos_state.clear()
    item.pos_state.append(final_state)
    return freeSpace

def getArrangementBasedFromState(item, baseX, baseY, baseZ):
    limitX = baseX + item.scaledX
    limitY = baseY + item.scaledY
    limitZ = baseZ + item.scaledZ

    item.rotation = [0,0,0]
    if item.pos_state[0] == "front2":
        limitX = baseX + item.scaledZ
        limitY = baseY + item.scaledY
        limitZ = baseZ + item.scaledX
        item.rotation = [0,90,0]
    elif item.pos_state[0] == "side1":
        limitX = baseX + item.scaledY
        limitY = baseY + item.scaledX
        limitZ = baseZ + item.scaledZ
        item.rotation = [0,0,90]
    elif item.pos_state[0] == "side2":
        limitX = baseX + item.scaledZ
        limitY = baseY + item.scaledX
        limitZ = baseZ + item.scaledY
        item.rotation = [90,0,90]
    elif item.pos_state[0] == "up1":
        limitX = baseX + item.scaledY
        limitY = baseY + item.scaledZ
        limitZ = baseZ + item.scaledX
        item.rotation = [90,90,0]
    elif item.pos_state[0] == "up2":
        limitX = baseX + item.scaledX
        limitY = baseY + item.scaledZ
        limitZ = baseZ + item.scaledY
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

def findCenterCoordinate(pos, relX, relY, relZ):
    x,y,z = pos[0], pos[1], pos[2]
    #bottom square
    bottom = []
    bottom.append(pos)
    temp = [x, y + relY, z]
    bottom.append(temp)
    temp = [x + relX, y, z]
    bottom.append(temp)
    temp = [x + relX, y + relY, z]
    bottom.append(temp)
    midpoint_bottom_x = float( (bottom[0][0] + bottom[2][0]) /2)
    midpoint_bottom_y = float( (bottom[0][1] + bottom[1][1]) /2)
    midpoint_bottom_z = z
    #up
    up = []
    temp = [x + relX, y, z + relZ]
    up.append(temp)
    temp = [x,y,z + relZ]
    up.append(temp)
    temp = [x + relX, y + relY, z + relZ]
    up.append(temp)
    temp = [x, y + relY, z + relZ]
    up.append(temp)
    midpoint_up_x = float( (up[1][0] + up[2][0]) /2)
    midpoint_up_y = float( (up[0][1] + up[2][1]) /2)
    midpoint_up_z = z + relZ

    midpoint = [(midpoint_bottom_x + midpoint_up_x)/2 , (midpoint_bottom_y + midpoint_up_y)/2, (midpoint_bottom_z + midpoint_up_z)/2]
    return midpoint[0], midpoint[1], midpoint[2]

# transforms positions to center of the box
def scaleToCenter(ary_pos, items, box):
    centeredOriginX = int(box.scaledLength / 2)
    centeredOriginY = int(box.scaledWidth / 2)
    centeredOriginZ = int(box.scaledHeight / 2)

    for i in range(1, len(ary_pos)):
        if items[i].pos_state[0] == "front1":
            newX, newY, newZ = findCenterCoordinate(ary_pos[i], items[i].scaledX - 1, items[i].scaledY - 1, items[i].scaledZ - 1)
        elif items[i].pos_state[0] == "front2":
            newX, newY, newZ = findCenterCoordinate(ary_pos[i], items[i].scaledZ - 1, items[i].scaledY - 1, items[i].scaledX - 1)
        elif items[i].pos_state[0] == "side1":
            newX, newY, newZ = findCenterCoordinate(ary_pos[i], items[i].scaledY - 1, items[i].scaledX - 1, items[i].scaledZ - 1)
        elif items[i].pos_state[0] == "side2":
            newX, newY, newZ = findCenterCoordinate(ary_pos[i], items[i].scaledZ - 1, items[i].scaledX - 1, items[i].scaledY - 1)
        elif items[i].pos_state[0] == "up1":
            newX, newY, newZ = findCenterCoordinate(ary_pos[i], items[i].scaledY - 1, items[i].scaledZ - 1, items[i].scaledX - 1)
        elif items[i].pos_state[0] == "up2":
            newX, newY, newZ = findCenterCoordinate(ary_pos[i], items[i].scaledX - 1, items[i].scaledZ - 1, items[i].scaledY - 1)

        ary_pos[i][0] = newX - centeredOriginX
        ary_pos[i][1] = newY - centeredOriginY
        ary_pos[i][2] = newZ - centeredOriginZ


def scaleToMeter(models_position):
    meterConstant = 1000
    for i in range(1, len(models_position)):
        models_position[i][0] = float(models_position[i][0] / meterConstant)
        models_position[i][1] = float(models_position[i][1] / meterConstant)
        models_position[i][2] = float(models_position[i][2] / meterConstant)

def reInitialize(swarm, numParticles, problem_dimensions, bounds, vel_limit):
    for i in range(0, len(swarm)):
        swarm[i].reset(problem_dimensions, bounds, vel_limit)

# Do optimization here
def optimize(models, scaledLength, scaledWidth, scaledHeight):
    print(f"passed inches for box : {scaledLength}, {scaledWidth}, {scaledHeight}")
    # start of solitary phase
            # initialization (identification)
            # updating       (verification)

    #initialization part one
    models_inside = [None]                                                      # None becuase modelid 0 is equivalent to empty in box
    models_position = [None]
    mainBox = Box(scaledLength,scaledWidth,scaledHeight)                                                  # user input, but for now is not. box(scaledLength,scaledWidth,scaledHeight) in inches
    models_local_error = sys.maxsize

    sample_solution = [0,0,0]
    numParticles = 246
    bounds = [(0,mainBox.scaledLength-1), (0,mainBox.scaledWidth-1), (0,mainBox.scaledHeight-1)]            #bounds for search space (min,max)

    problem_dimensions = len(sample_solution)
    vel_limit = [int(bounds[0][1] * 0.10), int(bounds[1][1] * 0.10), int(bounds[2][1] * 0.10)]

    for model in models:
        if model.id == sys.maxsize:
            continue

        print(f"model dimensions: {model.scaledX}, {model.scaledY}, {model.scaledZ}")
        print(f"box dimensions: {mainBox.scaledLength}, {mainBox.scaledWidth}, {mainBox.scaledHeight}")
        if model.scaledSolidVolume > mainBox.scaledTotalVolume:
            print("item toobig")
            continue

        if model.scaledSolidVolume > mainBox.scaledTotalVolume - mainBox.scaledTotalObjectVolume:
            print("box cannot accomodate another object of this size")
            continue

        print(model.scaledSolidVolume, mainBox.scaledTotalVolume)
        print("processing ... please dont close")
        # identification (initialization part two)
        is_insertable = True
        err_best_g = -1                                                         # global best error
        pos_best_g = []                                                         # global best position
        current_err_best = sys.maxsize
        
        swarm = []                                                              # locust swarm
        for i in range(0,numParticles):
            swarm.append(LocustParticle(problem_dimensions,bounds,vel_limit))

        #verification
        inside_convergence = 0
        stagnation_counter = 0
        generation = 0
        while generation < 500 and stagnation_counter < 10:
            # insert locust work here on item
            for j in range(0, numParticles):
                swarm[j].addItem(model)
                swarm[j].evaluate(objectiveFunctionSpace, mainBox)

                # update global bests
                # gregarious phase - analysis part 1
                if swarm[j].err_i <= err_best_g or err_best_g == -1:
                    model = swarm[j].item                                   # in case the particle updated the model attributes
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = int(swarm[j].err_i)

            if current_err_best > err_best_g:
                current_err_best = err_best_g
                inside_convergence = 0
                stagnation_counter = 0
            elif current_err_best <= err_best_g:
                inside_convergence+=1
                if inside_convergence == 10:
                    stagnation_counter+=1
                    reInitialize(swarm, numParticles, problem_dimensions, bounds, vel_limit)
                    inside_convergence = 0
                    generation+=1
                    #print("restarting swarm due to stagnation of solution ...")
                    continue

            # cycle through swarm and update velocities and position
            # gregarious phase - analysis part 2
            for j in range(0,numParticles):
                swarm[j].updateVelocity(pos_best_g, problem_dimensions)
                swarm[j].updatePosition(bounds, problem_dimensions)

            generation+=1

        if current_err_best == sys.maxsize:
            # proceed to another item since this item cannot be inserted
            continue

        # solution (attack)
        models_inside.append(model)
        print(model.pos_state)
        insertToBox(mainBox, model, pos_best_g, model.modelNum)
        mainBox.scaledTotalObjectVolume += model.scaledSolidVolume
        mainBox.totalObjectVolume += model.solidVolume
        models_position.append(pos_best_g)
        models_local_error = err_best_g
        print(f"Generated coordinates for Model Num = {model.modelNum} is {pos_best_g} with error {err_best_g}")

    if len(models_inside) == 1:
        print("cant fit anything inside the box. we suggest to use a bigger box ")
        input("boj please check do argument check where if it is not empty display, else display an error message ..")

    box_percentage = (mainBox.scaledTotalObjectVolume / mainBox.scaledTotalVolume) * 100
    print(f"box percentage maximized: {box_percentage}")
    print(models_position)
    scaleToCenter(models_position, models_inside, mainBox)
    print(models_position)
    scaleToMeter(models_position)
    print(models_position)
    print(models_inside[1].pos_state)
    input("proceed to visualizing")
    return mainBox, models_inside, models_position, box_percentage
    
    

