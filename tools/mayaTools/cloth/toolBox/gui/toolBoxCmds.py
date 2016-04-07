import sys
from mayaCore.cmds import pMode
try:
    import maya.cmds as mc
except:
    pass

#============================== CLOTH MODE ==============================#

def duplicateSelected(selObjects=None, name=None, worldParent=True):
    """
    Duplicate and parent to world selected objects

    :param selObjects: Objects to duplicate.
                       If None, duplicate selected scene nodes.
    :type selObjects: str | list
    :param name: New object name
    :type name: str
    :param worldParent: Parent new object to world
    :type worldParent: bool
    :return: Duplicate objects
    :rtype: list
    """
    return pMode.duplicateSelected(selObjects=selObjects, name=name, worldParent=worldParent)

def duplicateGeom(selObjects=None, name=None):
    """
    Duplicate and parent to world selected objects

    :param selObjects: Objects to duplicate.
                       If None, duplicate selected scene nodes.
    :type selObjects: str | list
    :param name: New object name
    :type name: str
    :return: Duplicate objects
    :rtype: list
    """
    return pMode.duplicateGeom(selObjects=selObjects, name=name)

def decoupeMesh():
    """
    Extract selected faces via duplicate

    :return: New mesh name
    :rtype: str
    """
    return pMode.decoupeMesh()

def symmetrizePose(axe=(-1, 1, 1), delta=0.01):
    """
    Symmetrize pose, selection order: 1=basePose, 2=srcPose, 3=dstPose

    :param axe: Symmetry axe (defaultAxe = 'X')
    :type axe: tuple
    :param delta: Precision coef
    :type delta: float
    """
    sel = mc.ls(sl=True)
    if not len(sel) in [2, 3]:
        raise IOError("!!! selection order: 1=basePose, 2=srcPose, 3=dstPose !!!")
    basePose = sel[0]
    srcPose = sel[1]
    if len(sel) == 2:
        dstPose = srcPose
    else:
        dstPose = sel[2]
    pMode.symmetrizePose(basePose, srcPose, dstPose, axe=axe, delta=delta)

def createOutMesh(selObjects=None, name=None, worldParent=True):
    """
    Create outMesh from selected objects

    :param selObjects: Objects to duplicate and connect.
                       If None, duplicate selected scene nodes.
    :type selObjects: str | list
    :param name: New object name
    :type name: str
    :param worldParent: Parent new object to world
    :type worldParent: bool
    :return: OutMesh objects
    :rtype: list
    """
    return pMode.createOutMesh(selObjects=selObjects, name=name, worldParent=worldParent)

def connectOutMesh(srcMesh=None, outMesh=None, force=True):
    """
    Connect srcMesh.outMesh to outMesh.inMesh

    :param srcMesh: Source mesh
    :type srcMesh: str
    :param outMesh: Out mesh
    :type outMesh: str
    :param force: Force connection
    :type force: True
    """
    pMode.connectOutMesh(srcMesh=srcMesh, outMesh=outMesh, force=force)

def updateOutMesh(srcMesh=None, outMesh=None, force=True):
    """
    Update given outMesh, then remove connection

    :param srcMesh: Source mesh
    :type srcMesh: str
    :param outMesh: Out mesh
    :type outMesh: str
    :param force: Force connection
    :type force: True
    """
    pMode.updateOutMesh(srcMesh=srcMesh, outMesh=outMesh, force=force)

#============================== CLOTH RIGG ==============================#

def launchRiggerUi():
    from mayaTools.cloth.rigger import __tm__
    reload(__tm__)
    print sys.argv