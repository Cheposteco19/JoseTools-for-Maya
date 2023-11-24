from maya import cmds
import maya.mel as mm
from uv_tools import ui as uv_tools_ui

def select_objects(objects):
    cmds.selectMode(object=True)
    cmds.select(objects, replace=True)

def get_objects(selected_items):
    objects = []
    for item in selected_items:
        if objects.append(item.split('.')[0]) not in objects:
            objects.append(item.split('.')[0])
    return objects

def clean_selection(objects,new_selection):
    cmds.select(clear=True)
    cmds.select(objects, replace=True)
    cmds.hilite(objects)
    cmds.select(new_selection, replace=True)

def auto_unwrap(*args):

    selected_items=cmds.ls(selection=True)

    objects = get_objects(selected_items)

    #Populate faces
    for item in objects:
        face_index = cmds.polyEvaluate(item, face=True) - 1
        faces = '{}.f[0:{}]'.format(item, face_index)
        cmds.polyAutoProjection(faces)

    select_objects(objects)

def camera_based(*args):

    # Set the select tool
    cmds.SelectTool()

    # Get object from past selection
    cmds.selectMode(object=True)
    selected_items = cmds.ls(selection=True)

    faces=[]
    objects = get_objects(selected_items)

    #Populate faces
    for item in objects:
        face_index = cmds.polyEvaluate(item,face=True)-1
        faces.append('{}.f[0:{}]'.format(item,face_index))

    #Clean selection
    clean_selection(objects,faces)

    #Project the UVs
    cmds.polyProjection(type='Planar', mapDirection='p', constructionHistory=True)

    select_objects(objects)

def unfold(*args):

    #Set the select tool
    cmds.SelectTool()

    #Get object from past selection
    cmds.selectMode(object=True)
    selected_items = cmds.ls(selection=True)

    #Unfold
    for item in selected_items:
        cmds.unfold(item,i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=0, us=1, s=0.02)

    #Orient Shells
    mm.eval("texOrientShells;")

    #Layout
    cmds.polyMultiLayoutUV(lm=1,sc=1,rbf=1,fr=1,ps=0.2,l=2,gu=1,gv=1,psc=0,su=1,sv=1,ou=0,ov=0)

    # Set the user to UVmode
    cmds.selectMode(component=True)
    cmds.selectType(polymeshUV=True)

    select_objects(selected_items)

def set_cut_sew_tool(*args):
    cmds.SetCutSewUVTool()

def set_tileable_size(density,map_size):

    # Kill history and freeze numbers
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    selected_items = cmds.ls(selection=True)

    uv_maps = []
    objects=get_objects(selected_items)
    edges=[]
    edge_index={}

    #Populate map list and edge directory
    for item in objects:
        map_index = cmds.polyEvaluate(item, uvcoord=True) - 1
        edge_index[item]=cmds.polyEvaluate(item, edge=True)
        uv_maps.append('{}.map[0:{}]'.format(item, map_index))

    #clean selection
    clean_selection(objects,uv_maps)

    #Set texel density
    mm.eval("texSetTexelDensity {} {};".format(density,map_size))

    #OrientShells
    mm.eval("texOrientShells;")

    #UnstackShells
    mm.eval("texUnstackShells 1;")

    #Kill history and freeze numbers
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    #Set the user to edgemode
    cmds.selectMode(component=True)
    cmds.selectType(edge=True)

    #Get border edges
    for object in edge_index:
        for edge in range(edge_index[object]):
            name='{}.e[{}]'.format(object,edge)

            edges.append(name)

    # Kill history and freeze numbers
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    #Clean select edges
    clean_selection(objects,edges)


def reset_tools(*args):
    cmds.resetTool('Move')
    cmds.resetTool('Rotate')
    cmds.resetTool('Scale')
    cmds.setToolTo('Rotate')
    cmds.setToolTo('Scale')
    cmds.setToolTo('Move')
    uv_tools_ui.uncheck_preserve_uvs()

def preserve_uvs(*args):
    mm.eval('setTRSPreserveUVs true;')

def dont_preserve_uvs(*args):
    mm.eval('setTRSPreserveUVs false;')