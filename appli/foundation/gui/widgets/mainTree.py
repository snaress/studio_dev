import os
from PyQt4 import QtGui
from foundation.gui._ui import fdnMainTreeUI


class MainTree(QtGui.QWidget, fdnMainTreeUI.Ui_wg_fdnMainTree):
    """
    MainTree class: Contains foundation main ui tree

    :param mainUi: Parent main ui
    :type mainUi: foundation.gui.FoundationUi
    """

    def __init__(self, mainUi):
        super(MainTree, self).__init__()
        self.mainUi = mainUi
        self._fdn = self.mainUi._fdn
        self._project = self._fdn._project
        self._setupWidget()
        self._initIcons()

    def _setupWidget(self):
        """
        Setup widget Ui
        """
        self.setupUi(self)
        #--- Init ---#
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.pb_filters.filters = []
        #--- Refresh ---#
        self.buildContexts()

    def _initIcons(self):
        """
        Init widget icons
        """
        self.iconFolder = QtGui.QIcon(os.path.join(self.mainUi.__iconPath__, 'svg', 'listView.svg'))
        self.pb_filters.setIcon(self.iconFolder)

    def _initWidget(self):
        """
        Init widget
        """
        self.buildContexts()
        self.buildTree()

    def currentContext(self):
        """
        Get current context

        :return: Context object
        :rtype: Context
        """
        for cbContext in self.pb_filters.filters:
            if cbContext.isChecked():
                return cbContext.ctxtObj

    def buildContexts(self):
        """
        Build context filters
        """
        self.pb_filters.filters = []
        for n, ctxtObj in enumerate(self._project.contexts):
            if n == 0:
                newCb = self.new_contextCheckBox(ctxtObj, state=True)
            else:
                newCb = self.new_contextCheckBox(ctxtObj, state=False)
            # noinspection PyUnresolvedReferences
            newCb.clicked.connect(self.buildTree)
            self.hl_contexts.addWidget(newCb)
            self.pb_filters.filters.append(newCb)

    def buildTree(self):
        """
        Build tree
        """
        self.tw_tree.clear()
        ctxtObj = self.currentContext()
        for mainEntity in ctxtObj.childs:
            newMainItem = QtGui.QTreeWidgetItem()
            newMainItem.setText(0, mainEntity.ctxtLabel)
            self.tw_tree.addTopLevelItem(newMainItem)
            for subEntity in mainEntity.childs:
                newSubEntity = QtGui.QTreeWidgetItem()
                newSubEntity.setText(0, subEntity.ctxtLabel)
                newMainItem.addChild(newSubEntity)

    def new_contextCheckBox(self, ctxtObj, state=False):
        """
        New 'Context' QCheckBox

        :param ctxtObj: Context tree object
        :type ctxtObj: Context
        :param state: CheckBox state
        :type state: bool
        :return: Context checkBox
        :rtype: Context
        """
        newCb = QtGui.QCheckBox()
        newCb.setText(ctxtObj.contextName)
        newCb.ctxtObj = ctxtObj
        newCb.setChecked(state)
        newCb.setAutoExclusive(True)
        # noinspection PyUnresolvedReferences
        newCb.clicked.connect(self.buildTree)
        return newCb
