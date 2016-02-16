import os
try:
    import maya.cmds as mc
    import maya.OpenMaya as om
except:
    pass


def getCurrentSceneName():
    """
    Get current maya scene name

    We don't just use cmds.file(q=1, sceneName=1)
    because it was sometimes returning an empty string,
    even when there was a valid file

    :return: Current scene full path
    :rtype: str
    """
    # noinspection PyArgumentList
    return str(om.MFileIO.currentFile())

def loadScene(sceneName, force=True):
    """
    Open given maya scene

    :param sceneName: Scene absolut path
    :type sceneName: str
    :param force: Force opening
    :type force: bool
    """
    print "Opening Maya Scene: %s" % sceneName
    mc.file(sceneName, o=True, f=force)

def importScene(sceneName, namespace=None):
    """
    Import given scene

    :param sceneName: Scene absolut path
    :type sceneName: str
    :param namespace: Import namespace
    :type namespace: str
    """
    print "Importing Maya Scene: %s" % sceneName
    if namespace is None:
        mc.file(sceneName, i=True)
    else:
        mc.file(sceneName, i=True, ns=namespace)

def referenceScene(sceneName, namespace):
    """
    Reference given maya scene

    :param sceneName: Scene absolut path
    :type sceneName: str
    :param namespace: Reference namespace
    :type namespace: str
    """
    print "Referencing Maya Scene: %s" % sceneName
    return mc.file(sceneName, r=True, ns=namespace)

def saveSceneAs(sceneName, force=False, keepCurrentName=False):
    """
    Save scene with given name

    :param sceneName: Scene absolute path
    :type sceneName: str
    :param force: Save without prompt
    :type force: bool
    :param keepCurrentName: Keep original scene name
    :type keepCurrentName: bool
    :return: Saved file
    :rtype: str
    """
    #--- Store Current Scene Name ---#
    currentSceneName = getCurrentSceneName()
    mc.file(rn=sceneName)
    ext = os.path.splitext(sceneName)[-1]
    #--- Save Scene ---#
    print "Saving Maya Scene: %s" % sceneName
    if ext == '.ma':
        result = mc.file(s=True, type="mayaAscii", f=force)
    elif ext == '.mb':
        result = mc.file(s=True, type="mayaBinary", f=force)
    else:
        raise IOError, "Error: Unrecognize extention: %s" % ext
    #--- Restore Scene Name ---#
    if keepCurrentName:
        print "Keep Scene Name: %s" % currentSceneName
        mc.file(rn=currentSceneName)
    #--- Result ---#
    return result

def exportSelection(sceneName, force=True):
    """
    Save selection with given name

    :param sceneName: Scene absolute path
    :type sceneName: str
    :param force: Export without prompt
    :type force: bool
    """
    ext = os.path.splitext(sceneName)[-1]
    if ext == '.ma':
        print "Saving Maya Scene from ascii file: %s" % sceneName
        mc.file(sceneName, es=True, f=force, op="v=0", typ="mayaAscii", pr=True)
    elif ext == '.mb':
        print "Saving Maya Scene from binary file: %s" % sceneName
        mc.file(sceneName, es=True, f=force, op="v=0", typ="mayaBinary", pr=True)
    else:
        raise IOError, "Error: Unrecognized extention: %s" % ext

def getTimeRange():
    """
    Get scene time range

    :return: time range info
    :rtype: dict
    """
    return {'sliderStart': mc.playbackOptions(q=True, min=True),
            'sliderStop': mc.playbackOptions(q=True, max=True),
            'rangeStart': mc.playbackOptions(q=True, ast=True),
            'rangeStop': mc.playbackOptions(q=True, aet=True)}

def getSceneSelection(**kwargs):
    """
    Get scene selection considering kwargs

    :param kwargs: ls cmd args
    :type kwargs: dict
    :return: Scene selection
    :rtype: list
    """
    return mc.ls(sl=True, **kwargs)

def selectObjects(objects, replace=True):
    """
    Select given objects

    :param objects: Object names
    :type objects: str || list
    :param replace: Replace current selection
    :type replace: bool
    """
    mc.select(objects, r=replace)

def clearSelection():
    """
    Clear vertex selection on model
    """
    mc.select(cl=True)

def invertSelection():
    """
    Invert current selection

    Preference is given to objects if both objects and components are selected.
    there is no user case where the user wants to invert a mixed selection of objects and components
    """
    #// determine if anything is selected
    selection = mc.ls(sl=True)
    if selection:
        #// now determine if any objects are selected
        objects = mc.ls(sl=True, dag=True, v=True)
        if objects:
            mc.select(tgl=True, ado=True, vis=True)
            #//check if selection is in a hierarchy
            parents = mc.listRelatives()
            if parents:
                mc.select(parents, d=True)
                for parent in parents:
                    children = mc.listRelatives(parent, c=True, path=True)
                    mc.select(children, add=True)
                #// make sure the original objects are not selected
                mc.select(selection, d=True)
        else:
            #// must be a component selected
            newComponents = []
            for component in selection:
                newComponents.append('%s[*]' % component.split('[')[0])
            mc.select(newComponents, r=True)
            mc.select(selection, d=True)
    else:
        #// nothing is selected
        print "!!! Nothing is selected !!!"

def polySelectTraverse(traversal=1):
    """
    Grow polyComponent selection

    :param traversal: 0 = Off.
                      1 = More : will add current selection border to current selection.
                      2 = Less : will remove current selection border from current selection.
                      3 = Border : will keep only current selection border.
                      4 = Contiguous Edges : Add edges aligned with the current edges selected
    :type traversal: int
    """
    #--- Vertex ---#
    result = mc.polyListComponentConversion(fv=True, tv=True)
    if result:
        mc.polySelectConstraint(pp=traversal, t=0x0001)
    else:
        #--- Edge ---#
        result = mc.polyListComponentConversion(fe=True, te=True)
        if result:
            mc.polySelectConstraint(pp=traversal, t=0x8000)
        else:
            #--- Face ---#
            result = mc.polyListComponentConversion(ff=True, tf=True)
            if result:
                mc.polySelectConstraint(pp=traversal, t=0x0008)
            else:
                #--- Uv ---#
                result = mc.polyListComponentConversion(fuv=True, tuv=True)
                if result:
                    mc.polySelectConstraint(pp=traversal, t=0x0010)
