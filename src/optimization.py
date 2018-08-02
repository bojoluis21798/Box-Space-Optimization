from src.model import Model
from src.box import Box

 #refer to fitness equation of document
def objectiveFuncBox(item, box):

    # checks if item is container-like or not and gets appropriate volume
    # (falsevalue,truevalue)[condition]
    addedVolume = (item.solidVolume + box.totalObjectVolume, item.surfaceVolume + box.totalObjectVolume)[item.isContainer == True]

    #check if addedVolume of objects inside box is less than volume of box
    return (-1,addedVolume/box.totalVolume)[addedVolume <= box.totalVolume]

# Do optimization here
def optimize(models):
    pass
    
    #start of solitary phase
        #initialization (identification)
        #updating       (verification)
    
    # identification
    maxIter = 30 
    numParticles = 30
    mainBox = Box(18,18,24) #user input, but for now is not. box(length,width,height) in inches

