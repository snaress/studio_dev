import pUtil, pScene
try:
    import maya.cmds as mc
    from maya import OpenMaya as om
except:
    pass


def getVertexPosition(obj, toRound=5, ws=True) :
    """
    Get object vertex position, with approximation

    :param obj = obj to get vtx
    :type obj = str
    :param toRound = approximation
    :type toRound = int
    :param ws: World space state
    :type ws: bool
    :return: Vertex position
    :rtype: list
    """
    toR = []
    if not mc.ls(obj+".vtx[*]") :
        return toR
    tpos = mc.xform(obj+".vtx[*]", q=1, ws=ws, t=1)
    pos = zip(tpos[::3], tpos[1::3], tpos[2::3])
    for vtx in pos :
        x = round(vtx[0] , toRound)
        y = round(vtx[1] , toRound)
        z = round(vtx[2] , toRound)
        toR.append((x,y,z))
    return toR

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
    #--- Check Object List ---#
    if selObjects is None:
        objectList = mc.ls(sl=True)
    else:
        if isinstance(selObjects, basestring):
            objectList = [selObjects]
        else:
            objectList = selObjects
    #--- Duplicate Objects ---#
    cpList = []
    for obj in objectList:
        if name is None:
            cpName = "%s__cp#" % obj.split(':')[-1].split('__')[0]
        else:
            cpName = name
        cpObject = mc.duplicate(obj, n=cpName)
        newName = cpObject
        #--- Parent To World ---#
        if worldParent:
            if mc.listRelatives(cpObject[0], p=True) is not None:
                newName = mc.parent(cpObject[0], w=True)
        cpList.append(newName[0])
    return cpList

def duplicateGeom(selObjects=None, name=None):
    """
    Duplicate and parent to world selected objects via outMesh / inMesh

    :param selObjects: Objects to duplicate.
                       If None, duplicate selected scene nodes.
    :type selObjects: str | list
    :param name: New object name
    :type name: str
    :return: Duplicate objects
    :rtype: list
    """
    #--- Check Object List ---#
    if selObjects is None:
        objectList = mc.ls(sl=True)
    else:
        if isinstance(selObjects, basestring):
            objectList = [selObjects]
        else:
            objectList = selObjects
    #--- Duplicate Objects ---#
    cpList = []
    for obj in objectList:
        #--- Create Base Object ---#
        if name is None:
            cpName = "%s__cp#" % obj.split(':')[-1].split('__')[0]
        else:
            cpName = name
        baseObj = mc.polySphere(n=cpName)[0]
        mc.delete(baseObj, ch=True)
        baseMesh = mc.listRelatives(baseObj, s=True, ni=True)[0]
        #--- Get Shape ---#
        if not mc.nodeType(obj) == 'mesh':
            meshName = mc.listRelatives(obj, s=True, ni=True)[0]
        else:
            meshName = obj
        #--- Transfert Geom ---#
        updateOutMesh(srcMesh=meshName, outMesh=baseMesh, force=True)
        cpList.append(baseObj)
    #--- Result ---#
    return cpList

def decoupeMesh():
    """
    Extract selected faces via duplicate

    :return: New mesh name
    :rtype: str
    """
    #--- Check Selection ---#
    selObject = mc.ls(sl=True, o=True)
    if not len(selObject) == 1:
        raise IOError("!!! Select only one object !!!")
    #--- Get Selected Components ---#
    selection = mc.ls(sl=True, fl=True)
    selFaces = []
    for sel in selection:
        selFaces.append(int(sel.split('.')[-1].replace('f[', '').replace(']', '')))
    #--- Duplique Object ---#
    tForm = mc.listRelatives(selObject[0], p=True)[0]
    dup = duplicateGeom(selObjects=tForm, name='%s__cut#' % tForm)
    mc.select(cl=True)
    for f in selFaces:
        mc.select('%s.f[%s]' % (dup[0], f), add=True)
    #--- Remove Unselected ---#
    pScene.invertSelection()
    mc.delete()
    #--- Add Info ---#
    pUtil.setNodeAttr(dup[0], 'baseObject', tForm, lock=True)
    mc.select(cl=True)
    return dup[0]

def symmetrizePose(baseObj, srcObj, dstObj, axe=(-1, 1, 1), delta=0.01):
    """
    Symmetrize Pose

    :param baseObj: Base object (bind pose)
    :type baseObj: str
    :param srcObj: Source object (morph pose)
    :type srcObj: str
    :param dstObj: Destination object (symmetry pose)
    :type dstObj: str
    :param axe: Symmetry axe (defaultAxe = 'X')
    :type axe: tuple
    :param delta: Precision coef
    :type delta: float
    """
    print "#--- Symmetrize Pose ---#"
    #--- Get Base Datas ---#
    base = mc.xform(baseObj + ".vtx[*]", q=True, os=True, t=True)
    basePos = zip(base[::3], base[1::3], base[2::3])
    basePosPoints = [om.MPoint(*v) for v in basePos]
    #--- Get Source Datas ---#
    base = mc.xform(srcObj + ".vtx[*]", q=True, os=True, t=True)
    srcPos = zip(base[::3], base[1::3], base[2::3])
    srcPosPoints = [om.MPoint(*v) for v in srcPos]
    #--- Get Matrix ---#
    number = len(mc.getAttr(baseObj + ".pnts[*]"))
    mirrorMatrix = om.MTransformationMatrix()
    scaleUtil = om.MScriptUtil()
    scaleUtil.createFromDouble(*axe)
    scalePtr = scaleUtil.asDoublePtr()
    mirrorMatrix.setScale(scalePtr, om.MSpace.kObject)
    mirrorMatrix = mirrorMatrix.asScaleMatrix()
    #--- Mapping loop ---#
    pointMap = {}
    for i in xrange(number):
        bpp = basePosPoints[i]
        for j in xrange(number):
            if i == j:
                continue
            cmpPos = basePosPoints[j]
            if bpp == cmpPos:
                mc.warning("Index %s and %s have the same position, check them..." % (i, j))
            mirrPos = bpp * mirrorMatrix
            if (mirrPos.x - delta <= cmpPos.x <= mirrPos.x + delta and
                mirrPos.y - delta <= cmpPos.y <= mirrPos.y + delta and
                mirrPos.z - delta <= cmpPos.z <= mirrPos.z + delta):
                pointMap[i] = j
    #--- Transfert Datas ---#
    for i in xrange(number):
        if not i in pointMap:
            pointMap[i] = i
        dstPosPoints = srcPosPoints[i] * mirrorMatrix
        mc.xform("%s.vtx[%s]" % (dstObj, pointMap[i]), os=True, t=[dstPosPoints.x, dstPosPoints.y, dstPosPoints.z])
    mc.select(dstObj, r=True)
    print "---> %s symmetrized: %s" % (srcObj, dstObj)

def connectOutMesh(srcMesh=None, outMesh=None, force=True):
    """
    Connect srcMesh.worldMesh to outMesh.inMesh

    :param srcMesh: Source mesh
    :type srcMesh: str
    :param outMesh: Out mesh
    :type outMesh: str
    :param force: Force connection
    :type force: True
    """
    #--- Check Object List ---#
    if srcMesh is None and outMesh is None:
        selObjects = mc.ls(sl=True)
        if not selObjects:
            print "!!! Error: Select srcMesh, then outMesh !!!"
        else:
            srcMesh = selObjects[0]
            outMesh = selObjects[1]
    #--- Connect Attr ---#
    ind = pUtil.getNextFreeMultiIndex("%s.worldMesh" % srcMesh)
    mc.connectAttr("%s.worldMesh[%s]" % (srcMesh, ind), "%s.inMesh" % outMesh, f=force)
    print "// Connect %s.worldMesh ---> %s.inMesh" % (srcMesh, outMesh)

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
    #--- Check Object List ---#
    if srcMesh is None and outMesh is None:
        selObjects = mc.ls(sl=True)
        print selObjects
        if not selObjects:
            print "!!! Error: Select srcMesh, then outMesh !!!"
        else:
            srcMesh = selObjects[0]
            outMesh = selObjects[1]
    #--- Update Mesh ---#
    connectOutMesh(srcMesh, outMesh, force=force)
    mc.refresh()
    mc.disconnectAttr("%s.worldMesh" % srcMesh, "%s.inMesh" % outMesh)
    print "// Update %s.worldMesh ---> %s.inMesh" % (srcMesh, outMesh)

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
    #--- Check Object List ---#
    if selObjects is None:
        selObjects = mc.ls(sl=True)
    else:
        if isinstance(selObjects, str):
            selObjects = [selObjects]
    #--- Create OutMesh ---#
    outList = []
    for obj in selObjects:
        if name is None:
            outName = "%s__out#" % obj.split(':')[-1].split('__')[0]
        else:
            outName = name
        outMesh = duplicateSelected(selObjects=str(obj), name=str(outName), worldParent=worldParent)[0]
        if isinstance(outMesh, list):
            connectOutMesh(srcMesh=str(obj), outMesh=str(outMesh[0]))
            outList.append(outMesh[0])
        else:
            connectOutMesh(srcMesh=str(obj), outMesh=str(outMesh))
            outList.append(outMesh)
    return outList
