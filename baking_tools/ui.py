from baking_tools import core as bake_tester_core
from maya import cmds
import maya.mel as mm
import json
import os

#Window components names
WINDOW_NAME='bake_test_ui'
CHECK_BOX_NAME='auto_unwrap_check_box'
LOW_POLY_PATH_TEXT_BOX_NAME='low_poly_path_text_box'
HIGH_POLY_PATH_TEXT_BOX_NAME='high_poly_path_text_box'
EXTRA_PATH_TEXT_BOX_NAME_1='extra_path_text_box_1'
EXTRA_PATH_TEXT_BOX_NAME_2='extra_path_text_box_2'
EXTRA_PATH_TEXT_BOX_NAME_3='extra_path_text_box_3'
EXTRA_PATH_TEXT_BOX_NAME_4='extra_path_text_box_4'
EXTRA_PATH_TEXT_BOX_NAME_5='extra_path_text_box_5'
EXTRA_PATH_TEXT_BOX_NAME_6='extra_path_text_box_6'
DOCK_CONTROL_NAME='bake_tester_dock_control'

#Save preferances settings
DIRECTORY_HISTORY_NAME='directory_history'
DIRECTORY_HISTORY_ROOT_DIR = mm.eval('getenv "MAYA_APP_DIR";')
DIRECTORY_HISTORY_EXT= 'json'

def show_ui():
    """

    Creates the window

    """
    # Delete old window
    if cmds.window(WINDOW_NAME, exists=True,query=True):
        cmds.deleteUI(WINDOW_NAME)

    if cmds.dockControl(DOCK_CONTROL_NAME, exists=True,query=True):
        cmds.deleteUI(DOCK_CONTROL_NAME)
    paths_dict=read_directory_from_file()

    # Create new window
    cmds.window(WINDOW_NAME, title='Baking tools', widthHeight=(500,120))

    #Auto-Unwrap
    cmds.columnLayout(adjustableColumn=True, columnOffset=('both',10))
    cmds.checkBox(CHECK_BOX_NAME,label="Auto-Unwrap Slot 1",annotation="auto-unwrap/unfold/unlock normals/soften-harden texture borders/kills history and numbers")

    # Browse Low Export
    cmds.rowLayout(numberOfColumns=4,adjustableColumn=2)
    cmds.text(label='1 ')
    if paths_dict.get(LOW_POLY_PATH_TEXT_BOX_NAME) is not None:
        cmds.textField(LOW_POLY_PATH_TEXT_BOX_NAME, text=paths_dict[LOW_POLY_PATH_TEXT_BOX_NAME])
    else:
        cmds.textField(LOW_POLY_PATH_TEXT_BOX_NAME)
    cmds.button(label='...',command=browse_low)
    cmds.button(label='Export LOW',command=low_exportFBX,width=73)
    cmds.setParent('..')

    # Browse High Export
    cmds.rowLayout(numberOfColumns=4,adjustableColumn=2)
    cmds.text(label='2 ')
    if paths_dict.get(HIGH_POLY_PATH_TEXT_BOX_NAME) is not None:
        cmds.textField(HIGH_POLY_PATH_TEXT_BOX_NAME, text=paths_dict[HIGH_POLY_PATH_TEXT_BOX_NAME])
    else:
        cmds.textField(HIGH_POLY_PATH_TEXT_BOX_NAME)
    cmds.button(label='...',command=browse_high)
    cmds.button(label='Export HIGH',command=high_exportFBX)
    cmds.setParent('..')

    cmds.frameLayout('Extra slots',collapsable=True,collapse=True)
    # Browse Extra Export 1
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=2)
    cmds.text(label='3 ')
    if paths_dict.get(EXTRA_PATH_TEXT_BOX_NAME_1) is not None:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_1, text=paths_dict[EXTRA_PATH_TEXT_BOX_NAME_1])
    else:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_1)
    cmds.button(label='...', command=browse_extra_1)
    cmds.button(label='Export', command=extra_exportFBX1)
    cmds.setParent('..')

    # Browse Extra Export 2
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=2)
    cmds.text(label='4 ')
    if paths_dict.get(EXTRA_PATH_TEXT_BOX_NAME_2) is not None:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_2, text=paths_dict[EXTRA_PATH_TEXT_BOX_NAME_2])
    else:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_2)
    cmds.button(label='...', command=browse_extra_2)
    cmds.button(label='Export', command=extra_exportFBX2)
    cmds.setParent('..')

    # Browse Extra Export 3
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=2)
    cmds.text(label='5 ')
    if paths_dict.get(EXTRA_PATH_TEXT_BOX_NAME_3) is not None:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_3, text=paths_dict[EXTRA_PATH_TEXT_BOX_NAME_3])
    else:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_3)
    cmds.button(label='...', command=browse_extra_3)
    cmds.button(label='Export', command=extra_exportFBX3)
    cmds.setParent('..')

    # Browse Extra Export 4
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=2)
    cmds.text(label='6 ')
    if paths_dict.get(EXTRA_PATH_TEXT_BOX_NAME_4) is not None:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_4, text=paths_dict[EXTRA_PATH_TEXT_BOX_NAME_4])
    else:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_4)
    cmds.button(label='...', command=browse_extra_4)
    cmds.button(label='Export', command=extra_exportFBX4)
    cmds.setParent('..')

    # Browse Extra Export 5
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=2)
    cmds.text(label='7 ')
    if paths_dict.get(EXTRA_PATH_TEXT_BOX_NAME_5) is not None:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_5, text=paths_dict[EXTRA_PATH_TEXT_BOX_NAME_5])
    else:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_5)
    cmds.button(label='...', command=browse_extra_5)
    cmds.button(label='Export', command=extra_exportFBX5)
    cmds.setParent('..')

    # Browse Extra Export 6
    cmds.rowLayout(numberOfColumns=4, adjustableColumn=2)
    cmds.text(label='8 ')
    if paths_dict.get(EXTRA_PATH_TEXT_BOX_NAME_6) is not None:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_6, text=paths_dict[EXTRA_PATH_TEXT_BOX_NAME_6])
    else:
        cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_6)
    cmds.button(label='...', command=browse_extra_6)
    cmds.button(label='Export', command=extra_exportFBX6)
    cmds.setParent('..')

    cmds.setParent('..')

    #Credits
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label='V 1.1.0')
    cmds.text(label='GD67_JoseMunguia   ', align='right')

    cmds.setParent('..')
    cmds.dockControl(DOCK_CONTROL_NAME,floating=True,label='Bake tester',content=WINDOW_NAME,area='left',width=500,height=100,allowedArea=('top','bottom'))

    # Show window
    cmds.showWindow()

    # Browse defined
def browse_low(*args):
    """Browses for low"""
    browse(LOW_POLY_PATH_TEXT_BOX_NAME)

def browse_high(*args):
    """browses for high"""
    browse(HIGH_POLY_PATH_TEXT_BOX_NAME)

def browse_extra_1(*args):
    """browses for high"""
    browse(EXTRA_PATH_TEXT_BOX_NAME_1)

def browse_extra_2(*args):
    """browses for high"""
    browse(EXTRA_PATH_TEXT_BOX_NAME_2)

def browse_extra_3(*args):
    """browses for high"""
    browse(EXTRA_PATH_TEXT_BOX_NAME_3)

def browse_extra_4(*args):
    """browses for high"""
    browse(EXTRA_PATH_TEXT_BOX_NAME_4)

def browse_extra_5(*args):
    """browses for high"""
    browse(EXTRA_PATH_TEXT_BOX_NAME_5)

def browse_extra_6(*args):
    """browses for high"""
    browse(EXTRA_PATH_TEXT_BOX_NAME_6)

def browse(textbox):
    """
    Browses
    Args:
        textbox: for writing the user input when he browses
    """
    path = cmds.fileDialog2(fileFilter="*.fbx", dialogStyle=2)
    cmds.textField(textbox, edit=True, text=path[0])

#Export buttons
def low_exportFBX(*args):
    """Checks if auto unwrap is necesary and exports the selectction to the low poly path"""
    if cmds.checkBox(CHECK_BOX_NAME,query=True,value=True)==True:
        bake_tester_core.auto_unwrap()
    exportFBX(LOW_POLY_PATH_TEXT_BOX_NAME)

def high_exportFBX(*args):
    """Exports the selecton to the high poly path"""
    exportFBX(HIGH_POLY_PATH_TEXT_BOX_NAME)

def extra_exportFBX1(*args):
    """Exports the selecton to the high poly path"""
    exportFBX(EXTRA_PATH_TEXT_BOX_NAME_1)

def extra_exportFBX2(*args):
    """Exports the selecton to the high poly path"""
    exportFBX(EXTRA_PATH_TEXT_BOX_NAME_2)

def extra_exportFBX3(*args):
    """Exports the selecton to the high poly path"""
    exportFBX(EXTRA_PATH_TEXT_BOX_NAME_3)

def extra_exportFBX4(*args):
    """Exports the selecton to the high poly path"""
    exportFBX(EXTRA_PATH_TEXT_BOX_NAME_4)

def extra_exportFBX5(*args):
    """Exports the selecton to the high poly path"""
    exportFBX(EXTRA_PATH_TEXT_BOX_NAME_5)

def extra_exportFBX6(*args):
    """Exports the selecton to the high poly path"""
    exportFBX(EXTRA_PATH_TEXT_BOX_NAME_6)

def exportFBX(text_box):
    """
    Gets the user input path, saves it and exports the FBX
    Args:
        text_box:which text box is the one to be read
    """
    paths_dict = save_paths_to_file()
    path_to_export = paths_dict[text_box]
    cmds.file(path_to_export, force=True, options='v=0;', type='FBX export', exportSelected=True, preserveReferences=True)

def save_paths_to_file():
    """
    Saves paths in user preferences
    Returns: previous paths dictionary
    """
    paths_dict = read_directories_from_text_boxes()
    write_directory_to_file(DIRECTORY_HISTORY_NAME, paths_dict)
    return paths_dict

def read_directories_from_text_boxes():
    """
    Reads paths from user input
    Returns: paths dictionary read
    """
    paths_dict={}
    paths_dict[HIGH_POLY_PATH_TEXT_BOX_NAME] = cmds.textField(HIGH_POLY_PATH_TEXT_BOX_NAME, query=True, text=True)
    paths_dict[LOW_POLY_PATH_TEXT_BOX_NAME] = cmds.textField(LOW_POLY_PATH_TEXT_BOX_NAME, query=True, text=True)
    paths_dict[EXTRA_PATH_TEXT_BOX_NAME_1] = cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_1, query=True, text=True)
    paths_dict[EXTRA_PATH_TEXT_BOX_NAME_2] = cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_2, query=True, text=True)
    paths_dict[EXTRA_PATH_TEXT_BOX_NAME_3] = cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_3, query=True, text=True)
    paths_dict[EXTRA_PATH_TEXT_BOX_NAME_4] = cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_4, query=True, text=True)
    paths_dict[EXTRA_PATH_TEXT_BOX_NAME_5] = cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_5, query=True, text=True)
    paths_dict[EXTRA_PATH_TEXT_BOX_NAME_6] = cmds.textField(EXTRA_PATH_TEXT_BOX_NAME_6, query=True, text=True)
    return paths_dict

def write_directory_to_file(directory_history_name, directory_dict):
    """Writes paths into user preferences"""
    file_name='{}.{}'.format(directory_history_name, DIRECTORY_HISTORY_EXT)
    file_path=os.path.join(DIRECTORY_HISTORY_ROOT_DIR, file_name)

    with open(file_path,'w') as f:
        json.dump(directory_dict, f, indent=4)

def read_directory_from_file():
    """
    Reads paths from user preferences
    Returns: paths dictionary read
    """
    file_path = r'{}\{}.{}'.format(DIRECTORY_HISTORY_ROOT_DIR,DIRECTORY_HISTORY_NAME,DIRECTORY_HISTORY_EXT)
    if not os.path.exists(file_path):
        directory_dict={}
        directory_dict[HIGH_POLY_PATH_TEXT_BOX_NAME]=''
        directory_dict[LOW_POLY_PATH_TEXT_BOX_NAME]=''
        directory_dict[EXTRA_PATH_TEXT_BOX_NAME_1]=''
        directory_dict[EXTRA_PATH_TEXT_BOX_NAME_2]=''
        directory_dict[EXTRA_PATH_TEXT_BOX_NAME_3]=''
        directory_dict[EXTRA_PATH_TEXT_BOX_NAME_4]=''
        directory_dict[EXTRA_PATH_TEXT_BOX_NAME_5]=''
        directory_dict[EXTRA_PATH_TEXT_BOX_NAME_6]=''
        return directory_dict
    with open(file_path, 'r') as f:
        directory_dict = json.load(f)
    return directory_dict