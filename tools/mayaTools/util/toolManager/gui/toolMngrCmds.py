import os, sys
from coreSys import pFile
from mayaCore.cmds import pUtil


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

def launchTools(toolName, toolFile, logLvl='info'):
    """
    launch maya tool

    :param toolName: Maya tool name
    :type toolName: str
    :param toolFile: ToolManager file (__tm__.py)
    :type toolFile: str
    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    """
    sys.argv = [toolName, logLvl, pUtil.getMayaMainWindow()]
    execfile(toolFile)
