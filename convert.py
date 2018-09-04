import bpy
import sys
import os
from src.model import Model

#directory path to convert
convertdir = sys.argv[1]
#directory path to export
exportdir = sys.argv[2]

# get all filenames in convertdir
filenames = [f for f in os.listdir(convertdir+'/') if os.path.isfile(convertdir+'/'+f) and f.split('.')[1] == "obj"]

# create directory
if not os.path.exists(exportdir):
    os.path.makedirs(exportdir+"/tmp")

# convert files using blender
# define function for converting
def convert(fn):
    modelId = fn.split('.')[0]
    if os.path.isfile(exportdir+"/"+modelId+".x"):
        return
    model = Model(fn)
    # clear scene
    bpy.ops.object.delete(use_global = True)
    # import obj
    bpy.ops.import_scene.obj(filepath = convertdir+"/"+fn)
    # get selected object
    obj = bpy.context.selected_objects[0]
    # scale object
    obj.scale[0] = (model.dimX/1000)/(obj.dimensions[0])
    obj.scale[1] = (model.dimZ/1000)/(obj.dimensions[1])
    obj.scale[2] = (model.dimY/1000)/(obj.dimensions[2])
    # set origin
    bpy.ops.object.origin_set(type = "ORIGIN_GEOMETRY", center = 'BOUNDS')
    # change location to (0,0,0)
    obj.location = 0,0,0
    # modify material
    for mtl in bpy.data.materials:
        mtl.translucency = 1
        mtl.use_transparency = False
    # save collada
    bpy.ops.wm.collada_export(filepath = exportdir+"/tmp/"+modelId)
    # delete from scene
    bpy.ops.object.delete()
    # import collada
    bpy.ops.wm.collada_import(filepath = exportdir+"/tmp/"+modelId+'.dae')
    # get selected object
    obj = bpy.context.selected_objects[0]
    # modify material
    for mtl in bpy.data.materials:
        mtl.translucency = 1
    # save .x
    bpy.ops.export_scene.x(filepath = exportdir+"/"+modelId)
    # delete temp
    os.remove(exportdir+"/tmp/"+modelId+".dae")

# enable directx export
bpy.ops.wm.addon_enable(module = "io_scene_x")
# convert all files
for fn in filenames:
    convert(fn)
# remove temp
os.rmdir(exportdir+"/tmp")
