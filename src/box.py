import numpy as np
import matplotlib.pyplot as plt

class Box:
    #maintained meters for attributes, but not in grid system which is in milli
    def __init__(self, length, width, height):
        self.convertionFactor = 25.4                                        # 1 inch == 25.4 mm
        self.length = int( (length * self.convertionFactor) / 2 )                 # convert inch
        self.width  = int( (width * self.convertionFactor) / 2  )                 # convert inch
        self.height = int( (height * self.convertionFactor) / 2 )                 # convert inch
        self.totalVolume = int( self.length * self.width * self.height )
        self.numObjects = 0                                 # number of objects inserted in box
        self.totalObjectVolume = 0                          # gives the total occupied volume of the objects inside box

        #3dbox with l x w x h mm dimension with datatype 'u1' = 8bit unsigned int (0 to 160)
        self.boxgrid = np.zeros( ( self.length, self.width, self.height ), dtype = 'u1')
    
    #for attribute conversion
    def convertMilliToInch(self,milli):
        return float(milli/self.convertionFactor)