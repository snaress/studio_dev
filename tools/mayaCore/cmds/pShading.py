import pUtil
try:
    import maya.cmds as mc
except:
    pass


def newMat(matType, matName):
    """
    Create new material

    :param matType: New material type
    :type matType: str
    :param matName: New material name
    :type matName: str
    :return: matName, matSgName
    :rtype: str, str
    """
    print "Creating new %s material named %s" % (matType, matName)
    #-- Create New Shader --#
    mat = mc.shadingNode(matType, asShader=True, n=matName)
    if mat is None:
        mat = mc.createNode(matType, n=matName)
    matSg = mc.sets(n="%sSG" % mat, r=True, nss=True, em=True)
    #-- Connect Shader To Sg --#
    mc.connectAttr("%s.outColor" % mat, "%s.surfaceShader" % matSg, f=True)
    return mat, matSg

def assignMat(shaderSg, objects=None):
    """
    Assign given shader to the object list

    :param shaderSg: ShaderSg name
    :type shaderSg: str
    :param objects: Objects list
    :type objects: list
    """
    if objects is not None:
        for mesh in objects:
            try:
                mc.sets(mesh, e=True, fe=shaderSg)
                print "%s connected to %s" % (mesh, shaderSg)
            except:
                pass

def getShadingEngine(model):
    """
    Get shading engine from given mesh

    :param model: Transform name or mesh name
    :type model: str
    :return: Shading engine
    :rtype: str
    """
    if mc.objectType(model, isType='transform'):
        sets = mc.listSets(type=1, o=model, ets=True)
    elif mc.objectType(model, isType='mesh'):
        sets = mc.listSets(type=1, o=model, ets=False)
    else:
        sets = pUtil.findTypeInHistory(model, 'shadingEngine', past=True, future=True)
    if not sets:
        print "!!! Error: Shading engine not found."
    else:
        return sets

def overrideShader(colorIndex, objects=None, matName=None, useExisting=True):
    """
    create display override shader

    :param colorIndex: Maya color index
    :type colorIndex: int
    :param objects: Objects to assign
    :type objects: list
    :param matName: Material name
    :type matName: str
    :param useExisting: Use existing shader
    :type useExisting: bool
    """
    #--- Get Objects ---#
    if objects is None:
        objects = mc.ls(sl=True) or []
    else:
        if isinstance(objects, basestring):
            objects = [objects]
    #--- Get Mat Name ---#
    if matName is None:
        matName = 'mat_overrideColor_%s' % colorIndex
    #--- Assign Shader ---#
    color = pUtil.getColorFromIndex(colorIndex)
    if useExisting:
        if mc.objExists(matName):
            mat = matName
            sg = getShadingEngine(mat)
        else:
            mat, sg = newMat('lambert', matName)
            pUtil.setNodeAttr(mat, 'color', color, dataType='double3')
        assignMat(sg[0], objects)
    else:
        for obj in objects:
            mat, sg = newMat('lambert', matName)
            pUtil.setNodeAttr(mat, 'color', color, dataType='double3')
            assignMat(sg[0], [obj])

def defaultShader(objects=None):
    """
    Assign default shader

    :param objects: Objects to assign
    :type objects: list
    """
    #--- Get Objects ---#
    if objects is None:
        objects = mc.ls(sl=True) or []
    else:
        if isinstance(objects, basestring):
            objects = [objects]
    #--- Assign Shader ---#
    assignMat('initialShadingGroup', objects)
