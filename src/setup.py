from os import listdir, system
from os.path import isfile, join
from src.model import Model
from src.optimization import optimize
#from src.objloader import displayModel

def __displayAttrbs(model):
    """ Display attributes of model """
    system('cls')
    print ("id: "+str(model.id))
    print ("name: "+str(model.name))
    print ("category: "+str(model.category))
    print ("Dimension X: "+str(model.dimX) + " meters")
    print ("Dimension Y: "+str(model.dimY) + " meters")
    print ("Dimensions Z: "+str(model.dimZ)+ " meters")
    print ("isContainer: "+str(model.isContainer))
    print ("surfaceVolume: "+str(model.surfaceVolume))
    print ("solidVolume: "+str(model.solidVolume))
    print ("supportSurfaceArea: "+str(model.supportSurfaceArea))
    print ("weight: "+str(model.weight))
    print ("staticFriction: "+str(model.staticFriction))

    print ("Type 'd' to display 3d model")
    option = input("Type 'b' to go back to menu\n... ")

    if option == "b":
        return
    elif option == "d":
        displayModel(model)

def menu(models):
    """ Menu to display models and their attributes """

    while(True):
        system('cls')
        print ("Loaded models\n")

        # Loop through all loaded models
        for i in range(len(models)):
            print ("Model Number: "+str(i))
            print ("Name: "+models[i].name)
            print ("========================")

        # Print possible options
        print ('\nType the model number to access model info')
        print ("Type 'o' to optimize")
        option = input ("Type 'q' to exit\n... ")

        # Exit loop on exit command
        if option == "q":
            break

        # Optimize on optimize command
        if option == "o":
            optimize()

        # Display model info on display command
        elif option.isdigit():
            modelNum = int(option)
            __displayAttrbs(models[modelNum])

def modelsLoad():
    """ Load all models in ./data/stage to memory and get all attributes of object from metadata.csv """

    # Get all filenames in data/stage
    filenames = [f for f in listdir("./data/stage/") if isfile(join("./data/stage/", f))]

    # Make instance objects of each model and store to array
    models = []
    for fn in filenames:
        models.append(Model(fn))

    return models
