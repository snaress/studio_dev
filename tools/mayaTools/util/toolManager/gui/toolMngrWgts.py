from PyQt4 import QtGui
from _ui import treeNodeUI


class ToolNode(QtGui.QWidget, treeNodeUI.Ui_wg_treeNode):

    def __init__(self, mainUi, parentItem):
        self.mainUi = mainUi
        self.pItem = parentItem
        super(ToolNode, self).__init__()
        self._setupUi()

    def _setupUi(self):
        self.setupUi(self)
