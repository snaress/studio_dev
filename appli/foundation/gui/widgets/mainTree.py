import os
from coreQt import pQt
from functools import partial
from PyQt4 import QtGui, QtCore
from coreQt.dialogs import promptMultiUi
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
        self.log = self.mainUi.log
        self._fdn = self.mainUi._fdn
        self._project = self._fdn._project
        #--- Icons ---#
        self.iconFilter = QtGui.QIcon(os.path.join(self.mainUi.__iconPath__, 'svg', 'listView.svg'))
        self.iconFolder = QtGui.QIcon(os.path.join(self.mainUi.__iconPath__, 'svg', 'folder.svg'))
        self.iconAsset = QtGui.QIcon(os.path.join(self.mainUi.__iconPath__, 'katana', 'actor.png'))
        #--- Setup ---#
        self._setupWidget()
        self._setupFonts()

    def _setupWidget(self):
        """
        Setup widget Ui
        """
        self.setupUi(self)
        #--- Init ---#
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.pb_filters.filters = []
        self.pb_filters.setIcon(self.iconFilter)
        #--- Connect ---#
        self.tw_tree.itemClicked.connect(self.on_treeItem)
        #--- Refresh ---#
        self.buildContexts()

    def _setupFonts(self):
        """
        Setup widget fonts
        """
        #--- CtxtEntity Font ---#
        self.ctxtFont = QtGui.QFont()
        self.ctxtFont.setBold(True)
        self.ctxtFont.setPixelSize(12)

    def _initWidget(self):
        """
        Init widget
        """
        self.buildContextMenu(self.mainUi.m_newEntity, autoUpdate=False)
        self.buildContexts()
        self.buildPopupMenu()
        self.buildTree()

    @property
    def currentContext(self):
        """
        Get current context

        :return: Context object
        :rtype: Context
        """
        for cbContext in self.pb_filters.filters:
            if cbContext.isChecked():
                return cbContext.ctxtObj

    @property
    def currentSelection(self):
        """
        Get Selected items

        :return: Selected items
        :rtype: list
        """
        return self.tw_tree.selectedItems() or []

    def buildContextMenu(self, QMenu, autoUpdate=False):
        """
        Build 'New Entity' mainUi menu

        :param QMenu: Menu object
        :type QMenu: QtGui.QMenu
        :param autoUpdate: Enable dialog QComboBox update
        :type autoUpdate: bool
        """
        QMenu.clear()
        for context in self._project.contexts:
            menuItem = QMenu.addAction(context.contextLabel)
            menuItem.triggered.connect(partial(self.on_newEntity, context.contextName, autoUpdate=autoUpdate))

    def buildPopupMenu(self):
        """
        Build main tree popup menu
        """
        self.m_popMenu = QtGui.QMenu()
        self.m_popMenu.setStyleSheet(pQt.Style().getStyle(self.mainUi.currentStyle))
        self.mi_refresh = self.m_popMenu.addAction('Refresh')
        self.m_newEntity = self.m_popMenu.addMenu('New Entity')
        self.buildContextMenu(self.m_newEntity, autoUpdate=True)
        self.tw_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tw_tree.connect(self.tw_tree,
                             QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                             self.on_popupMenu)

    def buildContexts(self):
        """
        Build context filters
        """
        #--- Clear ---#
        for ctxtFilter in self.pb_filters.filters:
            self.hl_contexts.removeWidget(ctxtFilter)
        self.pb_filters.filters = []
        #--- Build ---#
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
        if self.currentContext is not None:
            contextObj = self.currentContext
            for mainEntity in contextObj.childs:
                newMainItem = self.new_ctxtEntityItem(mainEntity)
                self.tw_tree.addTopLevelItem(newMainItem)
                self.buildEntities(newMainItem)
                for subEntity in mainEntity.childs:
                    newSubItem = self.new_ctxtEntityItem(subEntity)
                    newMainItem.addChild(newSubItem)
                    self.buildEntities(newSubItem)

    def buildEntities(self, ctxtEntityItem):
        """
        Build entities

        :param ctxtEntityItem: Context entity item
        :type ctxtEntityItem: QtGui.QTreeWidgetItem
        """
        # noinspection PyUnresolvedReferences
        for entityObj in ctxtEntityItem.itemObj.entities:
            newEntityItem = self.new_entityItem(entityObj)
            ctxtEntityItem.addChild(newEntityItem)

    def new_contextCheckBox(self, contexttObj, state=False):
        """
        New 'Context' QCheckBox

        :param contexttObj: Context tree object
        :type contexttObj: Context
        :param state: CheckBox state
        :type state: bool
        :return: Context checkBox
        :rtype: Context
        """
        newCb = QtGui.QCheckBox()
        newCb.setText(contexttObj.contextLabel)
        newCb.ctxtObj = contexttObj
        newCb.setChecked(state)
        newCb.setAutoExclusive(True)
        # noinspection PyUnresolvedReferences
        newCb.clicked.connect(self.buildTree)
        return newCb

    def new_ctxtEntityItem(self, ctxtObj):
        """
        New 'Context Entity' QTreeWidgetItem

        :param ctxtObj: Context entity object
        :type ctxtObj: CtxtEntity
        :return: Context entity item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setFont(0, self.ctxtFont)
        newItem.setText(0, ctxtObj.contextLabel)
        newItem.setIcon(0, self.iconFolder)
        newItem.itemObj = ctxtObj
        newItem.itemType = 'ctxtEntity'
        return newItem

    def new_entityItem(self, entityObj):
        """
        New 'Entity' QTreeWidgetItem

        :param entityObj: Entity object
        :type entityObj: Entity
        :return: Entity item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setText(0, entityObj.entityName)
        newItem.setIcon(0, self.iconAsset)
        newItem.itemObj = entityObj
        newItem.itemType = 'entity'
        return newItem

    def on_treeItem(self):
        """
        Command launched when QTreeWidgetItem is clicked

        Refresh info view
        """
        self.mainUi.wg_infoView.refresh()

    def on_popupMenu(self):
        """
        Command launched when QTreeWidget is right clicked

        Launch popup menu
        """
        # noinspection PyArgumentList
        self.m_popMenu.popup(QtGui.QCursor.pos())
        self.m_popMenu.exec_()

    def on_newEntity(self, contextName, autoUpdate=False):
        """
        Command launched when 'Add New Entity' QMenuItem is triggered

        Launch new entity dialog
        :param contextName: New entity context
        :type contextName: str
        :param autoUpdate: Enable dialog QComboBox update
        :type autoUpdate: bool
        """
        #--- Get Main Types ---#
        ctxtObj = self._project.getContext(contextName)
        mainTypes = ctxtObj.getCtxtEntityLabels()
        #--- Get Prompts ---#
        prompts = [dict(promptType='combo', promptLabel='entityMainType', promptValue=mainTypes),
                   dict(promptType='combo', promptLabel='entitySubType', promptValue=[]),
                   dict(promptType='line', promptLabel='entityCode', promptValue=''),
                   dict(promptType='line', promptLabel='entityName', promptValue='')]
        #--- Init Dialog ---#
        self.dial_newEntity = NewEntityDialog(title="New Entity", prompts=prompts,
                                              acceptCmd=partial(self._newEntity, ctxtObj),
                                              ctxtObj=ctxtObj, parent=self)
        #--- Auto Update ---#
        if autoUpdate:
            currentSel = self.currentSelection
            if currentSel:
                #--- Get Context Entity Params ---#
                itemObj = currentSel[0].itemObj
                wgMainType = self.dial_newEntity.tw_prompts.topLevelItem(0).itemWidget
                wgSubType = self.dial_newEntity.tw_prompts.topLevelItem(1).itemWidget
                if itemObj.__class__.__name__ == 'Entity':
                    mainType = '%s%s' % (itemObj.entityMainType[0].upper(), itemObj.entityMainType[1:])
                    subType = '%s%s' % (itemObj.entitySubType[0].upper(), itemObj.entitySubType[1:])
                else:
                    if itemObj.contextType == 'subType':
                        mainType = itemObj._parent.contextLabel
                        subType = itemObj.contextLabel
                    else:
                        mainType = itemObj.contextLabel
                        subType = None
                #--- Update Dialog ---#
                wgMainType.cb_prompt.setCurrentIndex(wgMainType.cb_prompt.findText(mainType))
                self.dial_newEntity.on_mainType()
                if subType is not None:
                    wgSubType.cb_prompt.setCurrentIndex(wgSubType.cb_prompt.findText(subType))
        #--- Launch Dialog ---#
        self.dial_newEntity.exec_()

    def _newEntity(self, ctxtObj):
        """
        Create entity when dialog is accepted

        :param ctxtObj: Context object
        :type ctxtObj: Context
        """
        self.log.info("Creating new entity ...")
        #--- Check Result ---#
        results = self.dial_newEntity.result()
        self._checkDialogResult(results, ctxtObj)
        #--- Create Entity ---#
        newEntity = ctxtObj.newEntity(create=True,
                                      entityMainType='%s%s' % (results['entityMainType'][0].lower(),
                                                               results['entityMainType'][1:]),
                                      entitySubType='%s%s' % (results['entitySubType'][0].lower(),
                                                              results['entitySubType'][1:]),
                                      entityCode=results['entityCode'], entityName=results['entityName'])
        ctxtObj.addEntity(newEntity)
        #--- Quit ---#
        self.dial_newEntity.close()
        self.buildTree()

    def _checkDialogResult(self, result, ctxtObj):
        """
        Check Dialog results

        :param result: Dialog results
        :type result: dict
        """
        #--- Check Data ---#
        excludes = ['', ' ', 'None', None]
        if (result['entityMainType'] in excludes or result['entitySubType'] in excludes
            or result['entityCode'] in excludes or result['entityName'] in excludes):
            message = "!!! Entity invalid: %s--%s--%s--%s !!!" % (result['entityMainType'], result['entitySubType'],
                                                                  result['entityCode'], result['entityName'])
            pQt.errorDialog(message, self.dial_newEntity)
            raise AttributeError(message)
        #--- Check New Entity ---#
        print ctxtObj.entityCodes
        if result['entityCode'] in ctxtObj.entityCodes or result['entityName'] in ctxtObj.entityNames:
            message = "!!! Entity %r (%r) already exists !!!" % (result['entityName'], result['entityCode'])
            pQt.errorDialog(message, self.dial_newEntity)
            raise AttributeError(message)


class NewEntityDialog(promptMultiUi.PromptMulti):
    """
    Prompt dialog ui class

    :param title: Dialog title
    :type title: str
    :param prompts: Prompts dict list
                    [dict(promptType='line', promptLabel='name', promptValue='test'),
                     dict(promptType='color', promptLabel='style', promptValue=(175, 80, 120)),
                     dict(promptType='combo', promptLabel='lists', promptValue=['item1', 'item2', 'item3'])]
    :type prompts: list
    :param acceptCmd: Command to launch when 'Save' QPushButton is clicked
    :type acceptCmd: method || function
    :param ctxtObj: Context object
    :type ctxtObj: Context
    :param parent: Parent ui or widget
    :type parent: QtGui.QWidget
    """

    def __init__(self, title='Prompt Dialog', prompts=[], acceptCmd=None, ctxtObj=None, parent=None):
        self.ctxtObj = ctxtObj
        super(NewEntityDialog, self).__init__(title=title, prompts=prompts, acceptCmd=acceptCmd, parent=parent)

    def _initDialog(self):
        """
        Init dialog window
        """
        super(NewEntityDialog, self)._initDialog()
        entityMainType = self.tw_prompts.topLevelItem(0).itemWidget
        entityMainType.cb_prompt.currentIndexChanged.connect(self.on_mainType)
        self.on_mainType()

    def on_mainType(self):
        """
        Command launched when 'Entity Main Type' QComboBox is clicked

        Build 'Entity Sub Type' QComboBox
        """
        entityMainType = self.tw_prompts.topLevelItem(0).itemWidget
        entitySubType = self.tw_prompts.topLevelItem(1).itemWidget
        entitySubType.cb_prompt.clear()
        subTypes = self.ctxtObj.getCtxtEntityLabels(mainType=entityMainType.result())
        entitySubType.cb_prompt.addItems(subTypes)
