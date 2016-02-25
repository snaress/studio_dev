import os
from PyQt4 import QtGui, QtCore
from coreSys import pFile
from _ui import treeNodeUI


class TreeNode(QtGui.QWidget, treeNodeUI.Ui_wg_treeNode):
    """
    TreeNode class: ToolManager tree item widget

    :param mainUi: ToolManager main ui
    :type mainUi: ToolManager
    :param parentItem: Parent tree item
    :type parentItem: ToolManager.new_treeItem
    :param tmFile: ToolManager file (__tm__.py)
    :type tmFile: str
    """

    def __init__(self, mainUi, parentItem, tmFile=None):
        self.mainUi = mainUi
        self.pItem = parentItem
        self.log = self.mainUi.log
        super(TreeNode, self).__init__()
        self.tmFile = tmFile
        self._setupUi()

    def _setupUi(self):
        """
        Setup TreeNode widget
        """
        self.setupUi(self)
        #--- Fonts ---#
        self.categoryFont = QtGui.QFont()
        self.categoryFont.setBold(True)
        self.categoryFont.setUnderline(True)
        self.categoryFont.setPixelSize(14)
        #--- Label ---#
        self.l_toolName.setText(self.pItem.itemName)
        #--- Setup ---#
        if self.pItem.itemType == 'category':
            self.l_toolName.setFont(self.categoryFont)
            self.pb_tool.setVisible(False)
            self.qf_info.setVisible(False)
        else:
            iconSize = 24
            self.pb_tool.setMaximumSize(iconSize, iconSize)
            if self.toolIcon is not None:
                self.pb_tool.setIcon(QtGui.QIcon(self.toolIcon))
                self.pb_tool.setIconSize(QtCore.QSize(iconSize, iconSize))
        #--- Connect ---#
        self.pb_tool.clicked.connect(self.on_tool)

    @property
    def toolIcon(self):
        """
        Get icon file full path

        :return: Icon file
        :rtype: str
        """
        if self.tmFile is not None:
            iconFile = pFile.conformPath(os.path.join(os.path.dirname(self.tmFile), '__ico__.png'))
            if os.path.exists(iconFile):
                return iconFile

    def on_tool(self):
        """
        Command launched when 'Tool' QPushbutton is clicked

        Launch selected tool
        """
        if self.tmFile is not None:
            self.log.info("Launch tool")
