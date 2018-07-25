import numpy as np
import matplotlib.pyplot as plt

class Box:
    #maintained meters for attributes, but not in grid system which is in milli
    def __init__(self, length, width, height):
        self.length = length
        self.width  = width
        self.height = height
        self.totalVolume = length * width * height
        self.numObjects = 0
        self.boxgrid = np.zeros((length * 1000, width * 1000, height * 1000), dtype = 'u1')
    
    #for attribute conversion
    def convertMeterToMilli(meter):
        return meter*1000