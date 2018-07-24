from os import listdir, system
from os.path import isfile, join
from src.model import Model

def menu(models):
    """ Menu to display models and their attributes """
    while(True):
        system('cls')
        print ("Loaded models\n")

        for i in range(len(models)):
            print ("Model Number: "+str(i))
            print ("Name: "+models[i].name)
            print ("========================")

        modelNum = input('Enter model number (-1 to exit): ')

        if int(modelNum) == -1:
            break

def modelsLoad():
    """ Load all models in ./data/stage to memory and get all attributes of object from metadata.csv """

    # Get all filenames in data/stage
    filenames = [f for f in listdir("./data/stage/") if isfile(join("./data/stage/", f))]

    # Make instance objects of each model and store to array
    models = []
    for fn in filenames:
        models.append(Model(fn))

    return models
