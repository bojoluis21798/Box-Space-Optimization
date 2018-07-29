import numpy as np
import matplotlib.pyplot as plt

class Box:
    #maintained meters for attributes, but not in grid system which is in milli
    def __init__(self, length, width, height):
        self.length = length
        self.width  = width
        self.height = height
        self.totalVolume = length * width * height
        self.numObjects = 0        # number of objects inserted in box
        self.totalObjectVolume = 0 # gives the total occupied volume of the objects inside box

        #3dbox with l x w x h mm dimension with datatype 'u1' = 8bit unsigned int (0 to 160)
        self.boxgrid = np.zeros( ( int(length * 1000), int(width * 1000), int(height * 1000) ), dtype = 'u1')
    
    #for attribute conversion
    def convertMeterToMilli(meter):
        return meter*1000