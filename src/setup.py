from os import listdir, system
from os.path import isfile, join
from src.model import Model
from src.optimization import optimize

import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TextNode, DirectionalLight, VBase4

def menu(models):
    """GUI Menu to display models and their attributes """

    menu = aspect2d.attachNewNode("Menu")

    i = 0

    def displayModels(idx = 0):
        """ Show models models """

        # hide menu items
        menu.hide()

        info = aspect2d.attachNewNode("Info")
        currentModel = loader.loadModel(models[idx].filename)

        # function to modve to next model loaded in memory: (1 to move to next, -1 to move to previous)
        def moveModel(inc):
            nonlocal i
            nonlocal models

            if inc == 1:
                i = (i+inc)%len(models)
            elif inc == -1:
                i = i - 1 if (i-1) > -1 else len(models)-1

            info.removeNode()
            currentModel.removeNode()
            displayModels(i)

        def moveNext():
            moveModel(1)

        def movePrevious():
            moveModel(-1)

        # display model info
        textObject = OnscreenText(text = "id: "+models[idx].id, pos = (-1.2,0.9),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "x-dimension: "+str(models[idx].dimX), pos = (-1.2,0.8),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "y-dimension: "+str(models[idx].dimY), pos = (-1.2,0.7),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "z-dimension: "+str(models[idx].dimZ), pos = (-1.2,0.6),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "Surface Volume: "+str(models[idx].surfaceVolume), pos = (1.2,0.9),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Solid Volume: "+str(models[idx].solidVolume), pos = (1.2,0.8),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Support Surface Area: "+str(models[idx].supportSurfaceArea), pos = (1.2,0.7),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Weight: "+str(models[idx].weight), pos = (1.2,0.6),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)
        textObject = OnscreenText(text = "Static Friction: "+str(models[idx].staticFriction), pos = (1.2,0.5),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ARight,mayChange=0)

        # next and back buttons
        nextButton = DirectButton(text = "Next",
        pos=(1.2,0,-0.9), parent=info, scale=.05, command = moveNext)
        backButton = DirectButton(text = "Back",
        pos=(-1.2,0,-0.9), parent=info, scale=.05, command = movePrevious)

        # display 3d model
        currentModel.setScale(0.3)
        currentModel.setPos(0,2,0)

        # lights
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(0.8, 0.8, 0.5, 1))
        dlnp = render.attachNewNode(dlight)
        dlnp.lookAt(currentModel)
        render.setLight(dlnp)

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
