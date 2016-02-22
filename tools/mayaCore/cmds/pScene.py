import os
try:
    import maya.cmds as mc
    import maya.OpenMaya as om
except:
    pass


def workspaceToDict():
    """
    Store workspace info to dict

    :return: Workspace info
    :rtype: dict
    """
    wsDict = {'projectName': mc.workspace(q=True, fn=True).split('/')[-1],
              'projectPath': mc.workspace(q=True, fn=True), 'fileRules': {}}
    fr = mc.workspace(q=True, fr=True)
    for n in range(0, len(fr), 2):
        wsDict['fileRules'][fr[n]] = fr[n+1]
    return wsDict

def workspaceDictToStr(wsDict=None):
    """
    Convert workspace dict to string

    :param wsDict: Workspace info (If None, use current workspace)
    :type wsDict: dict
    :return: Workspace info
    :rtype: str
    """
    if wsDict is None:
        wsDict = workspaceToDict
    txt = ["#-- Workspace Info --#",
           "Project Name = %s" % wsDict['projectName'],
           "Project Path = %s" % wsDict['projectPath'],
           "#-- File Rules --#"]
    for k, v in wsDict['fileRules'].iteritems():
        txt.append("%s = %s" % (k, v))
    return '\n'.join(txt)

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

def createGroups(grpDict, force=False):
    """
    Create groups from given dict

    :param grpDict: {index: {'GroupName': 'ParentName'}}
    :type grpDict: dict
    :param force: Delete group if already exists
    :type force: bool
    """
    for n in sorted(grpDict.keys()):
        for k, v in grpDict[n].iteritems():
            #--- Check if grp exists ---#
            grpExists = False
            if mc.objExists(k):
                grpExists = True
                if force:
                    mc.delete(k)
                    grpExists = False
            #--- Create Group ---#
            if not grpExists:
                print "Creating group: %s ..." % k
                if v is None:
                    mc.group(em=True, n=k, w=True)
                else:
                    mc.group(em=True, n=k, p=v)
            else:
                print "!!! WARNING: Group %r already exists, skipp creation !!!" % k

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

def createAndConnectNode(nodeName, nodeType, connectionDict, clearNode=False, useExisting=False, _raiseError=False):
    """
    Create and connect new node

    :param nodeName: Node Name
    :type nodeName: str
    :param nodeType: Node Type
    :type nodeType: str
    :param connectionDict: Node connections
    :type connectionDict: dict
    :param clearNode: Delete node if exists
    :type clearNode: bool
    :param useExisting: Use existing node
    :type useExisting: bool
    :param _raiseError: Raise an error if node already exists
    :type _raiseError: bool
    :return: New node name
    :rtype: str
    """
    #--- Check NodeName ---#
    if mc.objExists(nodeName):
        if _raiseError:
            raise IOError("!!! ERROR: Node already exists: %s !!!" % nodeName)
        if clearNode:
            print "Node %r found, delete !" % nodeName
            mc.delete(nodeName)
        if useExisting:
            nodeName = nodeName
    else:
        nodeName = mc.createNode(nodeType, n=nodeName)
    #--- Connect NodeName ---#
    for k, v in connectionDict.iteritems():
        if not v.split('.')[0] == nodeName:
            v.replace(v.split('.')[0], nodeName)
        if isinstance(v, list):
            for conn in v:
                try:
                    mc.connectAttr(k, conn, f=True)
                except:
                    pass
        else:
            try:
                mc.connectAttr(k, v, f=True)
            except:
                pass
    #--- Result ---#
    return nodeName

def disconnectAll(nodeName):
    """
    Disconnect all given node connections

    :param nodeName: Node name
    :type nodeName: str
    """
    conns = mc.listConnections(nodeName, s=True, d=True, p=True, c=True)
    for n in range(0, len(conns), 2):
        try:
            if mc.connectionInfo(conns[n], isSource=True):
                mc.disconnectAttr(conns[n], conns[n+1])
            else:
                mc.disconnectAttr(conns[n+1], conns[n])
        except:
            print "Warning: Can not disconnect %s" % conns[n]
