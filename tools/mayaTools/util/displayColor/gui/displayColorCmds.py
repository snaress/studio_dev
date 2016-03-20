from mayaCore.cmds import pUtil
import maya.cmds as mc


def getColorFromIndex(index):
    """
    Get rgb color from given index

    :param index: Override color index
    :type index: int
    :return: rgb color
    :rtype: list
    """
    if index >= 32:
        pUtil.mayaWarning("Color index out-of-range (must be less than 32)")
    return mc.colorIndex(int(index), q=True)

def overrideColor(index):
    """
    Override display color

    :param index:
    :return:
    """
    pUtil.overrideDisplayColor(index)