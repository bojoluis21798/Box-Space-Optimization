from os import listdir, system
from os.path import isfile, join
from src.model import Model
from src.optimization import optimize
import math
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TextNode, DirectionalLight, VBase4
from direct.task import Task

def menu(models):
    """GUI Menu to display models and their attributes """

    menu = aspect2d.attachNewNode("Menu")

    i = 0
    spin = None
    def displayModels(idx = 0):
        """ Show models models """

        # hide menu items
        menu.hide()

        info = aspect2d.attachNewNode("Info")
        currentModel = loader.loadModel(models[idx].filename)

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

         # function to modve to next model loaded in memory: (1 to move to next, -1 to move to previous)
        def moveModel(inc):
            taskMgr.remove(spin)
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

        # next and back buttons
        nextButton = DirectButton(text = "Next",
        pos=(1.2,0,-0.9), parent=info, scale=.05, command = moveNext)
        backButton = DirectButton(text = "Back",
        pos=(-1.2,0,-0.9), parent=info, scale=.05, command = movePrevious)

        # define callback to go to main menu
        def goToMainMenu():
            info.removeNode()
            currentModel.removeNode()
            taskMgr.remove(spin)
            menu.show()

        # go back to main menu
        exit = DirectButton(text = "Exit to main menu",
        pos=(0,0,-0.9), parent=info, scale=.05, command = goToMainMenu)

        # set model position and scale
        currentModel.setPos(0,2,-0.2)
        currentModel.setScale(0.3)

        # lights
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(0.3, 0.3, 0.3, 0.7))
        dlnp = render.attachNewNode(dlight)
        dlnp.lookAt(currentModel)
        render.setLight(dlnp)

        # Define a procedure to move the object.
        def spinObjectTask(task):
            angleDegrees = task.time * 8.0
            currentModel.setHpr(angleDegrees, angleDegrees, angleDegrees)
            return Task.cont

        # Add the spinCameraTask procedure to the task manager.
        spin = taskMgr.add(spinObjectTask, "SpinObjectTask")

        # disable default camera control
        base.disableMouse()

        # render model
        currentModel.reparentTo(render)

    # function for displaying optimized models
    def displayOptimize():
        menu.hide()

        # create gui fields to enter length width and height
        boxParams = aspect2d.attachNewNode("BoxParams")

        length = 0
        width = 0
        height = 0

        lengthLabel = OnscreenText(text = "Enter Length of Box (in)",
        pos = (-0.6,0.5), parent = boxParams, scale = 0.05, align = TextNode.ALeft)

        def setLength(textEntered):
            length = textEntered

        length = DirectEntry(scale=.05, command=setLength, numLines = 1, focus=1,
        pos = (0,0,0.5), parent = boxParams)

        widthLabel = OnscreenText(text = "Enter Width of Box (in)",
        pos = (-0.6,0.4), parent = boxParams, scale = 0.05, align = TextNode.ALeft)

        def setWidth(textEntered):
            width = textEntered

        width = DirectEntry(scale=.05, command=setWidth, numLines = 1, focus=1,
        pos = (0,0,0.4), parent = boxParams)

        heightLabel = OnscreenText(text = "Enter Height of Box (in)",
        pos = (-0.6,0.3), parent = boxParams, scale = 0.05, align = TextNode.ALeft)

        def setHeight(textEntered):
            height = textEntered

        height = DirectEntry(scale=.05, command=setHeight, numLines = 1, focus=1,
        pos = (0,0,0.3), parent = boxParams)

        def optimize():
            nonlocal length, width, height
            length = float(length.get())
            width = float(width.get())
            height = float(height.get())
            print(length, width, height)

        optimizeButton = DirectButton(text = "Optimize", pos = (0,0,0.1),
        parent = boxParams, scale = 0.05, command = optimize)

        def goToMainMenu():
            boxParams.hide()
            menu.show()

        backToMenu = DirectButton(text = "Back to menu",
        pos=(0,0,0), parent=boxParams, scale=.05, command = goToMainMenu)


    bk_text = "Box Space Optimizer\n\nLoad models to data/stage"
    textObject = OnscreenText(text = bk_text, pos = (0,0.7),
    scale = 0.07,fg=(1,0.5,0.5,1), parent = menu, align=TextNode.ACenter,mayChange=0)

    loadedModels = DirectButton(text = "View Loaded Models",
        pos=(0,0,0.3), parent=menu, scale=.05, command = displayModels)
    optimize = DirectButton(text = "Optimize Loaded Models",
        pos=(0,0,0.2), parent=menu, scale=.05, command = displayOptimize)

    def exitApp():
        menu.removeNode()
        exit()

    exitButton = DirectButton(text = "Exit",
        pos=(0,0,0.1), parent=menu, scale=.05, command=exitApp)

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
