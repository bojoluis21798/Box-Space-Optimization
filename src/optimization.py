from src.model import Model
from src.box import Box

# Do optimization here
def optimize(models):
    pass
    
    #refer to fitness equation of document
    def objectiveFunc(items, box):
        total = 0
        for item in items:
            #checks if item is container like or not and gets appropriate volume
            total += (item.solidVolume, item.surfaceVolume)[item.isContainer == True]
        
        #check if total volume of objects inside box is less than volume of box
        return (-1,box.totalVolume/total)[total <= box.totalVolume]
        
