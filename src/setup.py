from os import listdir, system
from os.path import isfile, join, exists
from src.model import Model
from src.optimization import optimize
import math
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TextNode, DirectionalLight, VBase4, TransparencyAttrib
from direct.task import Task
import bpy

def menu(models):
    """GUI Menu to display models and their attributes """
    menu = aspect2d.attachNewNode("Menu")
    spin = None
    chosenModels = {}
    def displayModels(idx = 1):
        # hide menu items
        camera.setPos(0,0,0)
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
        textObject = OnscreenText(text = "x-dimension (scaled): "+str(models[idx].scaledX), pos = (-1.2,0.5),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "y-dimension (scaled): "+str(models[idx].scaledY), pos = (-1.2,0.4),
        scale = 0.06,fg=(1,0.5,0.5,1), parent = info, align=TextNode.ALeft,mayChange=0)
        textObject = OnscreenText(text = "z-dimension (scaled): "+str(models[idx].scaledZ), pos = (-1.2,0.3),
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
            nonlocal idx
            if inc == 1:
                idx = (idx+inc)%len(models)
                if idx == 0:
                    idx = 1
            elif inc == -1:
                idx = idx - 1 if (idx-1) > 0 else len(models)-1

            info.removeNode()
            currentModel.removeNode()
            return displayModels(idx)

        def moveNext():
            moveModel(1)

        def movePrevious():
            moveModel(-1)

        # next and back buttons
        nextButton = DirectButton(text = "Next",
        pos=(1.2,0,-0.9), parent=info, scale=.05, command = moveNext)
        backButton = DirectButton(text = "Back",
        pos=(-1.2,0,-0.9), parent=info, scale=.05, command = movePrevious)

        chosenStatus = "Select model"
        def chooseModel(status):
            if(status):
                chosenModels[idx] = models[idx]
            else:
                del chosenModels[idx]

        selectButton = DirectCheckButton(text = chosenStatus, scale = 0.1,
            command = chooseModel, pos = (0,0,-0.8), parent = info,
            indicatorValue = idx in chosenModels)

        # define callback to go to main menu
        def goToMainMenu():
            info.removeNode()
            currentModel.removeNode()
            taskMgr.remove(spin)
            menu.show()
            return

        # go back to main menu
        exit = DirectButton(text = "Exit to main menu",
        pos=(0,0,-0.9), parent=info, scale=.05, command = goToMainMenu)

        # set model position and scale
        currentModel.setScale(3)
        currentModel.setPos(0,2,0)

        # lights
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(0.2, 0.2, 0.2, 0.2))
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

        lengthLabel = OnscreenText(text = "Enter Width (x) of Box (in)",
        pos = (-0.6,0.5), parent = boxParams, scale = 0.05, align = TextNode.ALeft)

        def setLength(textEntered):
            length = textEntered

        length = DirectEntry(scale=.05, command=setLength, numLines = 1, focus=1,
        pos = (0,0,0.5), parent = boxParams)

        widthLabel = OnscreenText(text = "Enter Height (y) of Box (in)",
        pos = (-0.6,0.4), parent = boxParams, scale = 0.05, align = TextNode.ALeft)

        def setWidth(textEntered):
            width = textEntered

        width = DirectEntry(scale=.05, command=setWidth, numLines = 1, focus=1,
        pos = (0,0,0.4), parent = boxParams)

        heightLabel = OnscreenText(text = "Enter Length (z) of Box (in)",
        pos = (-0.6,0.3), parent = boxParams, scale = 0.05, align = TextNode.ALeft)

        def setHeight(textEntered):
            height = textEntered

        height = DirectEntry(scale=.05, command=setHeight, numLines = 1, focus=1,
        pos = (0,0,0.3), parent = boxParams)

        # For the actual displaying
        def optimizeDisplay():
            modelsNode = render.attachNewNode("ModelSNode")
            uiNode = aspect2d.attachNewNode("UINODE")
            # convert chosenModels to list
            modelsList = []
            modelsList.append(Model(""))
            for i in chosenModels:
                modelsList.append(chosenModels[i])

            for i in range(1,len(modelsList)):
                modelsList[i].modelNum = i

            nonlocal length, width, height
            length = float(length.get()) # convert to meters
            width = float(width.get()) # convert to meters
            height = float(height.get()) # convert to meters

            # call optimize model here
            mainBox, modelsInside, modelsPosition, boxPercentage = optimize(modelsList, length, width, height)
            ###
            if len(modelsInside) == 1:
                exitToMainMenu()

            # create box using blender
            box = bpy.context.selected_objects[0]
            for mtl in bpy.data.materials:
                mtl.use_transparency = True
                mtl.alpha = 0.2
            box.scale[0] = (int((length/2)*25.4)/1000)/2
            box.scale[1] = (int((width/2)*25.4)/1000)/2
            box.scale[2] = (int((height/2)*25.4)/1000)/2
            bpy.ops.object.origin_set(type = "ORIGIN_GEOMETRY", center = "BOUNDS")
            box.location = 0,0,0
            bpy.ops.wm.addon_enable(module = "io_scene_x")
            bpy.ops.export_scene.x(filepath = './data/box')

            # load box to panda
            box = loader.loadModel('./data/box.x')
            box.reparentTo(render)
            # load models
            mdlsPanda = []
            mdlsPanda.append(None)
            for i in range(1, len(modelsInside)):
                mdlsPanda.append(loader.loadModel(modelsInside[i].filename))
                mdlsPanda[i].reparentTo(modelsNode)
                mdlsPanda[i].setPos((modelsPosition[i][0]), (modelsPosition[i][1]), (modelsPosition[i][2]))
                print("=====================\n"+modelsInside[i].id)
                print("Rotation: "+str(modelsInside[i].rotation))
                print("Box Position: "+str((box.getX(), box.getY(), box.getZ())))
                print("Position: "+str(((modelsPosition[i][0]), (modelsPosition[i][1]), (modelsPosition[i][2]))))
                print("Box Dimensions: "+str((length*0.0254, width*0.0254, height*0.0254)))
                mdlsPanda[i].setHpr(modelsInside[i].rotation[0], modelsInside[i].rotation[1], modelsInside[i].rotation[2])

            percentageDisp = OnscreenText(text = "Volume: "+str(boxPercentage), scale = 0.05,
                pos = (0,-0.9), align = TextNode.ACenter, parent = uiNode)

            def cameraBack():
                camera.setPos(0,camera.getY()-0.05,0)
            def cameraForward():
                camera.setPos(0,camera.getY()+0.05,0)
            def rotateLeft():
                box.setH(box.getH()-4)
            def rotateRight():
                box.setH(box.getH()+4)
            def rotateUp():
                box.setP(box.getP()-4)
            def rotateDown():
                box.setP(box.getP()+4)
            back = DirectButton(text = "Back", pos = (-0.8, 0, 0),
                command = cameraBack, scale = 0.05, parent = uiNode)
            forward = DirectButton(text = "Forward", pos = (-0.8, 0, -0.2),
                command = cameraForward, scale = 0.05, parent = uiNode)
            rleft = DirectButton(text = "Rotate left", pos = (0.5, 0, -0.2),
                command = rotateLeft, scale = 0.05, parent = uiNode)
            rright = DirectButton(text = "Rotate right", pos = (0.8, 0, -0.2),
                command = rotateRight, scale = 0.05, parent= uiNode)
            rup = DirectButton(text = "Rotate Up", pos = (0.7, 0, 0),
                command = rotateUp, scale = 0.05, parent= uiNode)
            rdown = DirectButton(text = "Rotate Down", pos = (0.7, 0, -0.4),
                command = rotateDown, scale = 0.05, parent= uiNode)
            modelsNode.reparentTo(box)
            box.setScale(2)
            camera.setPos(0,-1,0)
            base.camLens.setNear(0.2)
            def exitToMainMenu():
                uiNode.removeNode()
                box.removeNode()
                modelsNode.removeNode()
                menu.show()
                return

            # exit button
            exitButton = DirectButton(text = "Exit to main menu",
                pos = (0,0,-0.8), scale = 0.1, command = exitToMainMenu, parent = uiNode)

            # lights
            dlight = DirectionalLight('dlight')
            dlight.setColor(VBase4(0.3, 0.3, 0.3, 0.3))
            dlnp = render.attachNewNode(dlight)
            dlnp.lookAt(box)
            render.setLight(dlnp)
            boxParams.removeNode()

        optimizeButton = DirectButton(text = "Optimize", pos = (0,0,0.1),
        parent = boxParams, scale = 0.05, command = optimizeDisplay)

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
    optimizeDirect = DirectButton(text = "Optimize Loaded Models",
        pos=(0,0,0.2), parent=menu, scale=.05, command = displayOptimize)

    def exitApp():
        menu.removeNode()
        base.destroy()
        exit()

    exitButton = DirectButton(text = "Exit",
        pos=(0,0,0.1), parent=menu, scale=.05, command=exitApp)

    # Callback to display models
    base.run()

def modelsLoad():
    """ Load all models in ./data/stage to memory and get all attributes of object from metadata.csv """

    # Get all filenames in data/stage
    filenames = [f for f in listdir("./data/models/") if isfile(join("./data/models/", f))]

    # Make instance objects of each model and store to array
    models = []

    #initialize index 0 as a null object
    for fn in filenames:
        models.append(Model(fn))

    models.sort(key = lambda x: x.surfaceVolume)
    models.insert(0, Model(""))

    return models
