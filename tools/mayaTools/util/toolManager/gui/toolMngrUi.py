import os
from functools import partial
from _ui import toolManagerUI
from coreSys import pFile, env
from PyQt4 import QtGui, QtCore
from mayaCore.cmds import pUtil
import toolMngrWgts, toolMngrCmds


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
    __iconPath__ = pFile.conformPath(os.path.join(env.iconsPath, 'png'))

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
        self._setupMenu()
        #--- Refresh ---#
        self.buildTree()

    def _setupMenu(self):
        """
        Setup toolManager menu
        """
        #--- Log Level ---#
        for level in self.log.levels:
            menuItem = self.m_logLevel.addAction(level)
            menuItem.setCheckable(True)
            menuItem.triggered.connect(partial(self.on_miLogLevel, level))
        self.on_miLogLevel(self.log.level)

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
            catItem = self.new_treeItem('category', category)
            self.tw_tools.addTopLevelItem(catItem)
            self.tw_tools.setItemWidget(catItem, 0, catItem._widget)
            #--- Add Tool ---#
            for tool in sorted(self.toolsDict[category].keys()):
                toolItem = self.new_treeItem('tool', tool, tmFile=self.toolsDict[category][tool])
                catItem.addChild(toolItem)
                self.tw_tools.setItemWidget(toolItem, 0, toolItem._widget)
        #--- Refresh ---#
        self.tw_tools.collapseAll()

    def new_treeItem(self, itemType, itemName, tmFile=None):
        """
        Create 'Tool' tree item

        :param itemType: 'Category' or 'tool'
        :type itemType: str
        :param itemName: Tool name
        :type itemName: str
        :param tmFile: __tm__.py file fullPath
        :type tmFile: str
        :return: Tool item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemType = itemType
        newItem.itemName = itemName
        newItem._widget = toolMngrWgts.TreeNode(self, newItem, tmFile=tmFile)
        return newItem

    def on_miLogLevel(self, logLevel):
        """
        Command launched when 'Log Level' QMenuItem is triggered

        Set ui and core log level
        :param logLevel : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
        :type logLevel: str
        """
        #--- Uncheck All ---#
        for menuItem in self.m_logLevel.children():
            menuItem.setChecked(False)
        #--- Check Given LogLvl ---#
        for menuItem in self.m_logLevel.children():
            if str(menuItem.text()) == logLevel:
                menuItem.setChecked(True)
                break
        #--- Set Log Level ---#
        self.log.level = logLevel



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
