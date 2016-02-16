import sip
from PyQt4 import QtCore
try:
    import maya.cmds as mc
    import maya.OpenMayaUI as mOpen
except:
    pass


def getMayaMainWindow():
    """
    Get maya main window

    :return: Maya main window
    :rtype: QtCore.QObject
    """
    return sip.wrapinstance(long(mOpen.MQtUtil.mainWindow()), QtCore.QObject)

def mayaWarning(message):
    """
    Display maya warning

    :param message: Warning to print
    :type message: str
    """
    mc.warning(message)

def mayaError(message):
    """
    Display maya error

    :param message: Error to print
    :type message: str
    """
    mc.error(message)

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

def getPlugNode(connectionPlug):
    """
    Get plug node from given connection

    :param connectionPlug: Connection plug
    :type connectionPlug: str
    :return: Plug node name
    :rtype: str
    """
    return connectionPlug.split('.')[0]

def getPlugAttr(connectionPlug):
    """
    Get plug attribute from given connection

    :param connectionPlug: Connection plug
    :type connectionPlug: str
    :return: Plug attribute name
    :rtype: str
    """
    return '.'.join(connectionPlug.split('.')[1:])

def getNextFreeMultiIndex(attr, start=0):
    """
    Returns the next multi index that's available for the given destination attribute

    :param attr:  Name of the multi attribute
    :type attr: str
    :param start: the first index to check from (use 0 if last index is not known)
    :type start: int
    :return: Available index
    :rtype: int
    """
    #// assume a max of 10 million connections
    for n in range(start, 10000000, 1):
        conn = mc.connectionInfo('%s[%s]' % (attr, n), sfd=True)
        if not conn:
            return n
    return 0

def attrIsLocked(nodeFullName):
    """
    Check if given node attribute is locked

    :param nodeFullName: 'nodeName.nodeAttr'
    :type nodeFullName: str
    :return: Attribute lock state
    :rtype: bool
    """
    if mc.objExists(nodeFullName):
        return mc.getAttr(nodeFullName, l=True)
    print "!!! WARNING: Node not found: %s !!!" % nodeFullName

def setAttrLock(nodeFullName, state):
    """
    Set given nodeAttr lock on or off

    :param nodeFullName: 'nodeName.nodeAttr'
    :type nodeFullName: str
    :param state: Attribute lock state
    :type state: bool
    :return: True if success, else False
    :rtype: bool
    """
    if mc.objExists(nodeFullName):
        try:
            mc.setAttr(nodeFullName, l=state)
            return True
        except:
            return False
    print "!!! WARNING: Node not found: %s !!!" % nodeFullName
    return False

def getAttrType(nodeName, nodeAttr):
    """
    Get given nodeAttr value

    :param nodeName: Node full name
    :type nodeName: str
    :param nodeAttr: Node attribute
    :type nodeAttr: str
    :return: Node attribute type
    :rtype: str
    """
    if mc.objExists("%s.%s" % (nodeName, nodeAttr)):
        return mc.getAttr("%s.%s" % (nodeName, nodeAttr), type=True)

def getAttr(nodeName, nodeAttr):
    """
    Get given nodeAttr value

    :param nodeName: Node full name
    :type nodeName: str
    :param nodeAttr: Node attribute
    :type nodeAttr: str
    :return: Node attribute value
    :rtype: float | list
    """
    if mc.objExists("%s.%s" % (nodeName, nodeAttr)):
        return mc.getAttr("%s.%s" % (nodeName, nodeAttr))

def setNodeAttr(nodeName, attrName, attrValue, dataType='string', lock=False):
    """
    Add or set given attribute on given nodeName with given value

    :param nodeName: Node name
    :type nodeName: str
    :param attrName: Attribute name
    :type attrName: str
    :param attrValue: Attribute value
    :type attrValue: str || int || float || tuple
    :param dataType: 'string', 'double3'
    :type dataType: str
    :param lock: Lock state
    :type lock: bool
    """
    #--- Add Attribute ---#
    if not mc.objExists('%s.%s' % (nodeName, attrName)):
        if dataType == 'double3':
            mc.addAttr(nodeName, ln=attrName, at='double3', k=True)
            for axe in ['X', 'Y', 'Z']:
                mc.addAttr(nodeName, ln='%s%s' % (attrName, axe), at='double', p=attrName, k=True)
        elif dataType == 'string':
            mc.addAttr(nodeName, ln=attrName, dt='string')
        elif dataType == 'bool':
            mc.addAttr(nodeName, ln=attrName, at='bool')
        elif dataType in ['int', 'long']:
            mc.addAttr(nodeName, ln=attrName, at='long')
        elif dataType == 'message':
            mc.addAttr(nodeName, ln=attrName, at='message')
    #--- Set Attribute ---#
    if dataType == 'double3':
        mc.setAttr('%s.%s' % (nodeName, attrName), attrValue[0], attrValue[1], attrValue[2], l=lock)
    elif dataType == 'string':
        mc.setAttr('%s.%s' % (nodeName, attrName), attrValue, type='string', l=lock)
    elif dataType == 'message':
        pass
    else:
        mc.setAttr('%s.%s' % (nodeName, attrName), attrValue, l=lock)

def listTransforms(mesh):
    """
    get transform from given mesh

    :param mesh: Mesh node name
    :type mesh: str
    :return: Transform node
    :rtype: list
    """
    return mc.listRelatives(mesh, p=True, pa=True)

def findTypeInHistory(obj, objType, future=False, past=False):
    """
    returns the node of the specified type that is the closest traversal to the input object

    :param obj: Object name
    :type obj: str
    :param objType: Object type list
    :type objType: str | list
    :param future: Future depth
    :type future: bool
    :param past: Past depth
    :type past: bool
    :return: Connected objType nodes
    :rtype: list
    """
    #// Test with list return instead of closest connected node
    #// Replace return pastObjs with return pastObjs[0] etc
    if past and future:
        #// In the case that the object type exists in both past and future,
        #// find the one that is fewer connections away.
        pastList = mc.listHistory(obj, f=False, bf=True, af=True)
        futureList = mc.listHistory(obj, f=True, bf=True, af=True)
        pastObjs = mc.ls(pastList, type=objType)
        futureObjs = mc.ls(futureList, type=objType)
        if pastObjs:
            if futureObjs:
                mini = len(futureList)
                if len(pastList) < mini:
                    mini = len(pastList)
                for i in range(mini):
                    if pastList[i] in pastObjs:
                        return pastObjs
                    if futureList[i] in futureObjs:
                        return futureObjs
            else:
                return pastObjs
        elif futureObjs:
            return futureObjs
    else:
        if past:
            hist = mc.listHistory(obj, f=False, bf=True, af=True)
            objs = mc.ls(hist, type=objType)
            if objs:
                return objs
        if future:
            hist = mc.listHistory(obj, f=True, bf=True, af=True)
            objs = mc.ls(hist, type=objType)
            if objs:
                return objs
