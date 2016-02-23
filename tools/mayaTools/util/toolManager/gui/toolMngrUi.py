from coreSys import pFile
from PyQt4 import QtGui, QtCore
from mayaCore.cmds import pUtil
from _ui import toolManagerUI
from mayaTools.util.toolManager.gui import toolMngrWgts, toolMngrCmds


class ToolManager(QtGui.QMainWindow, toolManagerUI.Ui_mw_toolManager):
    """
    ToolManager class: Manage maya tools

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :param parent: Maya main window
    :type parent: QtCore.QObject
    """

    __rootDir__ = 'mayaTools'
    __rootPath__ = '/'.join(pFile.conformPath(__file__).split('/')[:-4])

    def __init__(self, logLvl='info', parent=None):
        self.log = pFile.Logger(title=self.__class__.__name__, level=logLvl)
        self.log.info("########## Launching %s Ui ##########" % self.__class__.__name__, newLinesBefore=1)
        super(ToolManager, self).__init__(parent)
        self.toolsDict = dict()
        self._setupUi()

    def _setupUi(self):
        """
        Setup ToolManager ui
        """
        self.log.debug("Setup %s ui ..." % self.__class__.__name__)
        self.setupUi(self)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setMargin(0)
        #--- Fonts ---#
        self.categoryFont = QtGui.QFont()
        self.categoryFont.setBold(True)
        #--- Refresh ---#
        self.buildTree()

    def collecteTools(self):
        """
        Collecte tools from rootPath.

        Tool is detected if roolPackage contains '__tm__.py' file
        :return: Tools dict
        :rtype: dict
        """
        self.log.info("Collecting tools ...")
        self.toolsDict = toolMngrCmds.collecteTools(self.__rootPath__)

    def buildTree(self):
        """
        Build tools tree
        """
        self.log.debug("Init tree ...")
        self.tw_tools.clear()
        self.collecteTools()
        #--- Add Category ---#
        self.log.debug("Building tree ...")
        for category in sorted(self.toolsDict.keys()):
            catItem = self.new_categoryItem(category)
            self.tw_tools.addTopLevelItem(catItem)
            #--- Add Tool ---#
            for tool in sorted(self.toolsDict[category].keys()):
                toolItem = self.new_toolItem(tool, self.toolsDict[category][tool])
                catItem.addChild(toolItem)
                self.tw_tools.setItemWidget(toolItem, 0, toolItem.itemWidget)
        #--- Refresh ---#
        self.tw_tools.collapseAll()

    def new_treeItem(self, **kwargs):
        newItem = QtGui.QTreeWidgetItem()
        return newItem

    def new_categoryItem(self, itemName):
        """
        Create 'Category' tree item

        :param itemName: Category name
        :type itemName: str
        :return: Category item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemName = itemName
        newItem.itemtype = 'category'
        newItem.setText(0, '%s%s' % (itemName[0].upper(),itemName[1:]))
        newItem.setFont(0, self.categoryFont)
        return newItem

    def new_toolItem(self, itemName, tmFile):
        """
        Create 'Tool' tree item

        :param itemName: Tool name
        :type itemName: str
        :param tmFile: __tm__.py file fullPath
        :type tmFile: str
        :return: Tool item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemName = itemName
        newItem.itemtype = 'tool'
        newItem.itemWidget = toolMngrWgts.ToolNode(self, newItem)
        newItem.tmFile = tmFile
        return newItem



def mayaLaunch(logLvl='detail'):
    """
    Launch ToolManager

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :return: Launched window, Dock layout
    :rtype: ToolManager, mc.dockControl
    """
    window, dock = pUtil.launchQtWindow('ToolManager', 'mw_toolManager', ToolManager,
                                        toolKwargs=dict(logLvl=logLvl), dockName='td_toolManager')
    return window, dock
