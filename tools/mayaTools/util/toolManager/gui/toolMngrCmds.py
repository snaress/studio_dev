import os
from coreSys import pFile


def collecteTools(rootPath):
    """
    Collecte tools from rootPath.

    Tool is detected if roolPackage contains '__tm__.py' file
    :param rootPath: Tools root path
    :type rootPath: str
    :return: Tools dict
    :rtype: dict
    """
    toolsDict = dict()
    treeDict = pFile.pathToDict(rootPath, conformed=True)
    #--- Parsing ---#
    for root in treeDict['_order']:
        for f in treeDict[root]['files']:
            if f == '__tm__.py':
                #--- Store Tool ---#
                category = root.split('/')[-2]
                toolName = root.split('/')[-1]
                if not category in toolsDict.keys():
                    toolsDict[category] = dict()
                toolsDict[category][toolName] = os.path.join(root, f)
    #--- Result ---#
    return toolsDict
