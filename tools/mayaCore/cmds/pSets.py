try:
    import maya.cmds as mc
except:
    pass


def getAllSets(suffixes=None):
    """
    Get all sets ending with given suffixes

    :param suffixes: Set suffixes
    :type suffixes: list
    :return: Sets list
    :rtype: list
    """
    setList = []
    for s in mc.ls(type='objectSet') or []:
        for ext in suffixes:
            if suffixes is None:
                setList.append(s)
            else:
                if s.endswith(ext):
                    setList.append(s)
    return setList

def removeSets(sets=None, suffixes=None):
    """
    Delete given sets or all sets given by 'getAllSets()'

    :param sets: Sets list to delete
    :type sets: list
    :param suffixes: Set suffixes
    :type suffixes: list
    """
    #--- Get Sets ---#
    if sets is None:
        allSets = getAllSets(suffixes=suffixes)
    else:
        allSets = sets
    #--- Remove Sets ---#
    while allSets:
        for s in allSets:
            try:
                mc.delete(s)
                print 'delete', s
            except:
                pass
        allSets = getAllSets()
