import numpy as np
import sys

from src.model import Model
from src.box import Box
from src.particle import Particle

def getOptimalModelCombination(models, box):
    def objFunction(ndxs, models, box):
        for i in range(0, len(ndxs)):
            total += models[i].scaledSolidVolume
        
        return total/box.scaledTotalVolume


    num_dimensions = 1
    numParticles = 1 if int( 0.20 * (len(models) - 1)) < 1 else int( 0.20 * (len(models) - 1))
    err_best_g = -1
    pos_best_g = []
    bounds = [(1,255)]
    vel_limit = [bounds[0][1]]

    swarm=[]
    for i in range(0,numParticles):
        swarm.append(Particle(num_dimensions, bounds, vel_limit))
    
    generation = 0
    while generation < 100:
        for j in range(0,numParticles):
            swarm[j].evaluate(objFunction, box)

            if swarm[j].err_i > err_best_g or err_best_g == -1:
                    pos_best_g=list(swarm[j].position_i)
                    err_best_g=float(swarm[j].err_i)
        
        for j in range(0,numParticles):
                swarm[j].updateVelocity(pos_best_g, num_dimensions)
                swarm[j].updatePosition(bounds, num_dimensions)

        generation+=1
    
    print(pos_best_g)
    input("....")