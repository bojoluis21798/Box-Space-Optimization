from os import listdir, system
from os.path import isfile, join
from src.model import Model
from src.optimization import optimize

import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TextNode

def menu(models):
    """GUI Menu to display models and their attributes """

    menu = aspect2d.attachNewNode("Menu")

    def displayModels():
        """ Show models models """

        # hide menu items
        menu.hide()

        i = 0

        # display model info
        info = aspect2d.attachNewNode("Info")

        textObject = OnscreenText(text = "id: "+models[i].id, pos = (-1.2,0.9),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "x-dimension: "+str(models[i].dimX), pos = (-1.2,0.8),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "y-dimension: "+str(models[i].dimY), pos = (-1.2,0.7),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "z-dimension: "+str(models[i].dimZ), pos = (-1.2,0.6),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "Surface Volume: "+str(models[i].surfaceVolume), pos = (1.2,0.9),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Solid Volume: "+str(models[i].solidVolume), pos = (1.2,0.8),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Support Surface Area: "+str(models[i].supportSurfaceArea), pos = (1.2,0.7),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Weight: "+str(models[i].weight), pos = (1.2,0.6),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Static Friction: "+str(models[i].staticFriction), pos = (1.2,0.5),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)

        # display 3d model
        currentModel = loader.loadModel(models[i].filename)
        currentModel.setScale(models[i].unit*15)
        currentModel.setPos(-0.1,2,-0.2)

        currentModel.reparentTo(render)

    bk_text = "Box Space Optimizer\n\nLoad models to data/stage"
    textObject = OnscreenText(text = bk_text, pos = (0,0.7),
    scale = 0.07,fg=(1,0.5,0.5,1), parent = menu, align=TextNode.ACenter,mayChange=0)

    loadedModels = DirectButton(text = "View Loaded Models",
        pos=(0,0,0.3), parent=menu, scale=.05, command = displayModels)
    optimize = DirectButton(text = "Optimize Loaded Models",
        pos=(0,0,0.2), parent=menu, scale=.05)


    # Callback to display models

    base.run()

def modelsLoad():
    """ Load all models in ./data/stage to memory and get all attributes of object from metadata.csv """

    # Get all filenames in data/stage
    filenames = [f for f in listdir("./data/stage/") if isfile(join("./data/stage/", f))]

    # Make instance objects of each model and store to array
    models = []
    for fn in filenames:
        models.append(Model(fn))

    return models
