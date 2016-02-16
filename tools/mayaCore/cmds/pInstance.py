try:
    import maya.OpenMaya as om
except:
    pass


def getInstances():
    """
    Get scene instances

    :return: Instances list
    :rtype: list
    """
    instances = []
    iterDag = om.MItDag(om.MItDag.kBreadthFirst)
    while not iterDag.isDone():
        instanced = om.MItDag.isInstanced(iterDag)
        if instanced:
            instances.append(iterDag.fullPathName())
        iterDag.next()
    return instances
