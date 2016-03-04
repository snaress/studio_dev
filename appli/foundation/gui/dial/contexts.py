from coreQt import pQt
from coreQt.widgets import basicTreeUi
from coreQt.dialogs import promptMultiUi


class Contexts(basicTreeUi.BasicTree):
    """
    Groups Class: Contains UserGroups settings, child of ToolSettings

    :param pWidget: Parent widget
    :type pWidget: dialogs.ToolSettings
    """

    def __init__(self, pWidget):
        self.pWidget = pWidget
        self.mainUi = self.pWidget.parent()
        self._fdn = self.pWidget._fdn
        self._project = self._fdn._project
        self._users = self._fdn._users
        super(Contexts, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        self.log = self.pWidget.log
        super(Contexts, self)._initWidget()
        self._project.buildContextsFromSettings()

    def _setupIcons(self):
        """
        Setup Groups icons
        """
        super(Contexts, self)._setupIcons()
        #--- Edit Grade ---#
        if not self._users._user.grade == 0:
            self.pb_del.setEnabled(False)

    def _setupWidget(self):
        """
        Setup Groups widget
        """
        super(Contexts, self)._setupWidget()
        self.l_title.setText(self.__class__.__name__)
        self.cbb_filter.setVisible(False)
        self.pb_template.setVisible(False)
        self.pb_edit1.setVisible(False)
        self.pb_edit2.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.tw_tree.header().setStretchLastSection(False)
        self.rf_headers('Name', 'Label', 'Folder')
        self.rf_treeColumns()

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        if self.mainUi.showToolTips:
            self.pb_itemUp.setToolTip("Move up selected context")
            self.pb_itemDn.setToolTip("Move down selected context")
            self.pb_template.setToolTip("Open templates")
            self.pb_add.setToolTip("Create new context")
            self.pb_del.setToolTip("Delete selected context")
            self.pb_apply.setToolTip("Apply datas to Foundation object")
            self.pb_cancel.setToolTip("Restore datas from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected context (Disabled for your grade)")
        else:
            super(Contexts, self).rf_toolTips()

    def buildTree(self):
        """
        Build Groups tree widget
        """
        super(Contexts, self).buildTree()
        if self._project.contexts:
            ctxtItems = []
            for ctxtObj in self._project.contexts:
                newItem = self.new_treeItem(ctxtObj)
                ctxtItems.append(newItem)
            self.tw_tree.addTopLevelItems(ctxtItems)
        self.rf_treeColumns()
        self.rf_itemStyle()

    def ud_treeItem(self, item, **kwargs):
        """
        Update item data and settings

        :param item: Group tree item
        :type item: newItem
        :param kwargs: Group item data (key must starts with 'grp')
        :type kwargs: dict
        """
        super(Contexts, self).ud_treeItem(item, **kwargs)
        #--- Edit Item ---#
        item.setText(0, item.itemObj.contextName)
        item.setText(1, item.itemObj.contextLabel)
        item.setText(2, item.itemObj.contextFolder)

    def on_addItem(self):
        """
        Command launched when 'Add' QPushButton is clicked

        Add new group to tree
        """
        super(Contexts, self).on_addItem()
        #--- Get Prompts ---#
        prompts = [dict(promptType='line', promptLabel='contextName'),
                   dict(promptType='line', promptLabel='contextLabel', enable=False),
                   dict(promptType='line', promptLabel='contextFolder', enable=False)]
        #--- Launch Dialog ---#
        self.dial_context = ContextDialog(title="New Context", prompts=prompts, parent=self,
                                          acceptCmd=self.on_dialogAccept)
        self.dial_context.exec_()

    def on_dialogAccept(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save context datas
        """
        #--- Get Datas ---#
        excludes = ['', ' ', 'None', None]
        results = self.dial_context.result()
        ctxtName = results['contextName']
        #--- Check Data ---#
        if ctxtName in excludes :
            message = "!!! 'contextName' invalid: %s !!!" % ctxtName
            pQt.errorDialog(message, self.dial_context)
            raise AttributeError(message)
        #--- Check New Name ---#
        ctxtData = self.getData()
        for n in sorted(ctxtData.keys()):
            if ctxtData[n]['contextName'] == ctxtName:
                message = "!!! %s already exists !!!" % ctxtName
                pQt.errorDialog(message, self.dial_context)
                raise AttributeError(message)
        #--- Added Context ---#
        self.log.detail("Adding new context: %s" % ctxtName)
        itemObj = self._project.newContext(ctxtName)
        newItem = self.new_treeItem(itemObj)
        self.tw_tree.addTopLevelItem(newItem)
        self.tw_tree.clearSelection()
        self.tw_tree.setItemSelected(newItem, True)
        #--- Store Edition ---#
        self.__editedItems__['added'].append(newItem)
        #--- Quit ---#
        self.rf_treeColumns()
        self.rf_itemStyle()
        self.dial_context.close()

    def on_apply(self):
        """
        Command launched when 'Apply' QPushButton is clicked

        Store datas to itemObject
        """
        super(Contexts, self).on_apply()
        #--- Parse Group Tree ---#
        ctxtData = []
        treeDict = self.getData()
        for n in sorted(treeDict.keys()):
            if not treeDict[n]['contextName'] in ['', ' ', 'None', None]:
                item = self.getItemFromAttrValue('contextName', treeDict[n]['contextName'])
                if not item in self.__editedItems__['deleted']:
                    ctxtData.append(dict(contextName=treeDict[n]['contextName'], childs=treeDict[n]['childs']))
            else:
                self.log.warning("!!! Context 'name' value not valide, skipp %s !!!" % treeDict[n]['contextName'])
        #--- Store and refresh ---#
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])
        self._project.buildContexts(*ctxtData)
        self.pWidget.rf_editedItemStyle()
        self.rf_itemStyle()

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save data
        """
        super(Contexts, self).on_save()
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])

    def on_cancel(self):
        """
        Command launched when 'Cancel' QPushButton is clicked

        Restore datas from itemObject
        """
        super(Contexts, self).on_cancel()
        self.pWidget.rf_editedItemStyle()


class ContextDialog(promptMultiUi.PromptMulti):
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
    :param parent: Parent ui or widget
    :type parent: Context
    """

    def __init__(self, title="New Context", prompts=None, acceptCmd=None, parent=None):
        super(ContextDialog, self).__init__(title=title, prompts=prompts, acceptCmd=acceptCmd, parent=parent)

    def _initDialog(self):
        """
        Init dialog window
        """
        super(ContextDialog, self)._initDialog()
        ctxtItemName = self.tw_prompts.topLevelItem(0).itemWidget
        ctxtItemName.le_prompt.textChanged.connect(self.on_lineEdit)

    def on_lineEdit(self):
        """
        Command launched when 'Context Name' QLineEdit text changed

        Edit 'Context Label' and 'Context Folder'
        """
        ctxtItemName = self.tw_prompts.topLevelItem(0).itemWidget
        ctxtItemLabel = self.tw_prompts.topLevelItem(1).itemWidget
        ctxtItemFolder = self.tw_prompts.topLevelItem(2).itemWidget
        result = str(ctxtItemName.le_prompt.text())
        ctxtItemLabel.le_prompt.setText('%s%s' % (result[0].upper(), result[1:]))
        ctxtItemFolder.le_prompt.setText('%ss' % result)


class Entities(basicTreeUi.BasicTree):
    """
    Entities Class: Contains Entities settings, child of ToolSettings

    :param pWidget: Parent widget
    :type pWidget: dialogs.ToolSettings
    """

    def __init__(self, pWidget):
        self.pWidget = pWidget
        self.mainUi = self.pWidget.parent()
        self._fdn = self.pWidget._fdn
        self._project = self._fdn._project
        self._users = self._fdn._users
        super(Entities, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        self.log = self.pWidget.log
        super(Entities, self)._initWidget()
        #--- Edit Grade ---#
        if not self._users._user.grade == 0:
            self.pb_del.setEnabled(False)

    def _setupWidget(self):
        """
        Setup Entities widget
        """
        super(Entities, self)._setupWidget()
        self.l_title.setText(self.__class__.__name__)
        self.cbb_filter.setVisible(False)
        self.pb_template.setVisible(False)
        self.pb_template.setVisible(False)
        self.pb_edit1.setVisible(False)
        self.pb_edit2.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.tw_tree.header().setStretchLastSection(False)
        self.rf_headers('Entity Type', 'Entity SubType')
        self.rf_treeColumns()

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        if self.mainUi.showToolTips:
            self.pb_itemUp.setToolTip("Move up selected Entity")
            self.pb_itemDn.setToolTip("Move down selected Entity")
            self.pb_template.setToolTip("Open templates")
            self.pb_add.setToolTip("Create new Entity")
            self.pb_del.setToolTip("Delete selected Entity")
            self.pb_apply.setToolTip("Apply datas to Foundation object")
            self.pb_cancel.setToolTip("Restore datas from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected Entity (Disabled for your grade)")
        else:
            super(Entities, self).rf_toolTips()
