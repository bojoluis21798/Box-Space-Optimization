from os import walk

def modelsLoad():
    """ Load all models in ./data/stage to memory and get all attributes of object from metadata.csv"""

    for __, __, files in walk("./data/stage/"):
        print (files)
