import os
from coreQt import pQt
from PyQt4 import QtGui
from functools import partial
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
        self.buildContextMenu()
        self.buildContexts()
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

    def buildContextMenu(self):
        """
        Build 'New Entity' mainUi menu
        """
        self.mainUi.m_newEntity.clear()
        for context in self._project.contexts:
            menuItem = self.mainUi.m_newEntity.addAction(context.contextLabel)
            menuItem.triggered.connect(partial(self.on_newEntity, context.contextName))

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
                for subEntity in mainEntity.childs:
                    newSubEntity = self.new_ctxtEntityItem(subEntity)
                    newMainItem.addChild(newSubEntity)

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
        :rtype: CtxtEntity
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.setFont(0, self.ctxtFont)
        newItem.setText(0, ctxtObj.contextLabel)
        newItem.setIcon(0, self.iconFolder)
        return newItem

    def on_newEntity(self, contextName):
        """
        Command launched when 'Add New Entity' QMenuItem is triggered

        Launch new entity dialog
        :param contextName: New entity context
        :type contextName: str
        """
        #--- Get Main Types ---#
        ctxtObj = self._project.getContext(contextName)
        mainTypes = ctxtObj.getCtxtEntityLabels()
        #--- Get Prompts ---#
        prompts = [dict(promptType='combo', promptLabel='entityMainType', promptValue=mainTypes),
                   dict(promptType='combo', promptLabel='entitySubType', promptValue=[]),
                   dict(promptType='line', promptLabel='entityCode', promptValue=''),
                   dict(promptType='line', promptLabel='entityName', promptValue='')]
        #--- Launch Dialog ---#
        self.dial_newEntity = NewEntityDialog(title="New Entity", prompts=prompts,
                                              acceptCmd=partial(self._newEntity, ctxtObj),
                                              ctxtObj=ctxtObj, parent=self)
        self.dial_newEntity.exec_()

    def _newEntity(self, ctxtObj):
        """
        Create entity when dialog is accepted

        :param ctxtObj: Context object
        :type ctxtObj: Context
        """
        self.log.info("Creating new entity ...")
        results = self.dial_newEntity.result()
        self._checkDialogResult(results, ctxtObj)
        newEntity = ctxtObj.newEntity(create=True,entityMainType=results['entityMainType'],
                                      entitySubType=results['entitySubType'], entityCode=results['entityCode'],
                                      entityName=results['entityName'])
        ctxtObj.addEntity(newEntity)

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
            message = "!!! Entity invalid: %s -- %s -- %s -- %s !!!" % (result['entityMainType'], result['entitySubType'],
                                                                        result['entityCode'], result['entityName'])
            pQt.errorDialog(message, self.dial_newEntity)
            raise AttributeError(message)
        #--- Check New Entity ---#
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
