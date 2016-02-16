import pUtil
try:
    import maya.cmds as mc
    import maya.mel as ml
except:
    pass


def createWrap(driver, mesh, **kwargs):
    """
    Create wrap deformer

    :param driver: Wrap driver mesh
    :type driver: str
    :param mesh: Wrap driven mesh
    :type mesh: str
    :param kwargs: Wrap options: Weight Treshold (float)
                                 Max Distance (float)
                                 Exclusive Bind (bool)
                                 Auto Weight Treshold (bool)
                                 Falloff Mode (int)
    :return: BaseMesh name, wrapNode name
    :rtype: (str, str)
    """
    #--- Get Wrap Options ---#
    influenceShape = mc.listRelatives(driver, shapes=True)[0]
    weightThreshold = kwargs.get('weightThreshold', 0.0)
    maxDistance = kwargs.get('maxDistance', 1.0)
    exclusiveBind = kwargs.get('exclusiveBind', False)
    autoWeightThreshold = kwargs.get('autoWeightThreshold', True)
    falloffMode = kwargs.get('falloffMode', 0)
    #--- Create Wrap Deformer ---#
    wrapNode = mc.deformer(mesh, type='wrap')[0]
    mc.setAttr("%s.weightThreshold" % wrapNode, weightThreshold)
    mc.setAttr("%s.maxDistance" % wrapNode, maxDistance)
    mc.setAttr("%s.exclusiveBind" % wrapNode, exclusiveBind)
    mc.setAttr("%s.autoWeightThreshold" % wrapNode, autoWeightThreshold)
    mc.setAttr("%s.falloffMode" % wrapNode, falloffMode)
    mc.connectAttr("%s.worldMatrix[0]" % mesh, "%s.geomMatrix" % wrapNode)
    #--- Add Influence ---#
    base = mc.duplicate(driver, name="%sBase" % driver)[0]
    baseShape = mc.listRelatives(base, shapes=True)[0]
    mc.hide(base)
    #--- Create Dropoff ---#
    if not mc.attributeQuery('dropoff', n=driver, exists=True):
        mc.addAttr(driver, sn='dr', ln='dropoff', dv=4.0, min=0.0, max=20.0)
        mc.setAttr("%s.dr" % driver, k=True)
    #--- Type Mesh ---#
    if mc.nodeType(influenceShape) == 'mesh':
        #// Create smoothness attr if it doesn't exist
        if not mc.attributeQuery('smoothness', n=driver, exists=True):
            mc.addAttr(driver, sn='smt', ln='smoothness', dv=0.0, min=0.0)
            mc.setAttr("%s.smt" % driver, k=True)
        #// Create the inflType attr if it doesn't exist
        if not mc.attributeQuery('inflType', n=driver, exists=True):
            mc.addAttr(driver, at='short', sn='ift', ln='inflType', dv=2, min=1, max=2)
        mc.connectAttr("%s.worldMesh" % influenceShape, "%s.driverPoints[0]" % wrapNode)
        mc.connectAttr("%s.worldMesh" % baseShape, "%s.basePoints[0]" % wrapNode)
        mc.connectAttr("%s.inflType" % driver, "%s.inflType[0]" % wrapNode)
        mc.connectAttr("%s.smoothness" % driver, "%s.smoothness[0]" % wrapNode)
    #--- Type NurbsCurve or NurbsSurface ---#
    if mc.nodeType(influenceShape) == 'nurbsCurve' or mc.nodeType(influenceShape) == 'nurbsSurface':
        #// Create the wrapSamples attr if it doesn't exist
        if not mc.attributeQuery('wrapSamples', n=driver, exists=True):
            mc.addAttr(driver, at='short', sn='wsm', ln='wrapSamples', dv=10, min=1)
            mc.setAttr("%s.wsm" % driver, k=True)
        mc.connectAttr("%s.ws" % influenceShape, "%s.driverPoints[0]" % wrapNode)
        mc.connectAttr("%s.ws" % baseShape, "%s.basePoints[0]" % wrapNode)
        mc.connectAttr("%s.wsm" % driver, "%s.nurbsSamples[0]" % wrapNode)
    #--- Connect Dropoff ---#
    mc.connectAttr("%s.dropoff" % driver, "%s.dropoff[0]" % wrapNode)
    return base, wrapNode

def transfertWrapConns(wrapPlugs, newNode):
    """
    Given a list of wrap plugs, transfer the connections from

    their current source to the given newNode.
    :param wrapPlugs: Wrap connection plugs
    :type wrapPlugs: list
    :param newNode: Destination node
    :type newNode: str
    """
    for wrapPlug in wrapPlugs:
        wrapAttr = pUtil.getPlugAttr(wrapPlug)
        for attr in ['driverPoints', 'basePoints']:
            if wrapAttr.startswith(attr):
                meshConns = mc.listConnections(wrapPlug, s=True, p=True, sh=True, type='mesh')
                if meshConns:
                    #--- Transfert connections ---#
                    meshAttr = pUtil.getPlugAttr(meshConns[0])
                    mc.disconnectAttr(meshConns[0], wrapPlug)
                    mc.connectAttr('%s.%s' % (newNode, meshAttr), wrapPlug)

def getDeformers(baseObj, _type=list()):
    """
    Get the list of deformers found on in_obj filtered by in type

    :param baseObj: The object that give deformers
    :type baseObj: str
    :param _type: type of deformers to filter : ['skinCluster', 'blendShape', 'cluster' ]
    :type _type: str || list
    :return: list of found deformers
    :rtype: list
    """
    result = list()
    history = mc.ls(mc.listHistory(baseObj, pruneDagObjects=True), type='geometryFilter') or list()
    #--- Get Deformers ---#
    for item in history:
        if len(_type) > 0:
            if mc.nodeType(item) in _type:
                result.append(str(item))
        else:
            result.append(str(item))
    #--- Result ---#
    return result
