import pprint
from coreQt import pQt
from PyQt4 import QtGui
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
            self.pb_apply.setToolTip("Apply data to Foundation object")
            self.pb_cancel.setToolTip("Restore data from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected context (Disabled for your grade)")
        else:
            super(Contexts, self).rf_toolTips()

    def getData(self, asString=False):
        """
        Get tree datas

        :param asString: Return string instead of dict
        :type asString: bool
        :return: Tree datas
        :rtype: dict
        """
        data = dict()
        for n, item in enumerate(pQt.getTopItems(self.tw_tree)):
            data[n] = item.itemObj.getData()
        if asString:
            return pprint.pformat(data)
        return data

    def buildTree(self):
        """
        Build Context tree widget
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

        :param item: Context tree item
        :type item: newItem
        :param kwargs: Context item data
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
        result = self.dial_context.result()
        self._checkDialogResult(result)
        #--- Added Context ---#
        self.log.detail("Adding new context: %s" % result['contextName'])
        itemObj = self._project.newContext(result['contextName'])
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

    def _checkDialogResult(self, result):
        """
        Check Dialog results

        :param result: Dialog results
        :type result: dict
        """
        #--- Check Data ---#
        if result['contextName'] in self._fdn.typoExclusion :
            pQt.errorDialog("!!! 'contextName' invalid: %s !!!" % result['contextName'],
                            self.dial_context, raiseError=True)
        #--- Check New Name ---#
        ctxtData = self.getData()
        for n in sorted(ctxtData.keys()):
            if ctxtData[n]['contextName'] == result['contextName']:
                pQt.errorDialog("!!! %s already exists !!!" % result['contextName'],
                                self.dial_context, raiseError=True)

    def on_apply(self):
        """
        Command launched when 'Apply' QPushButton is clicked

        Store datas to itemObject
        """
        super(Contexts, self).on_apply()
        #--- Parse Context Tree ---#
        ctxtData = []
        treeDict = self.getData()
        for n in sorted(treeDict.keys()):
            if not treeDict[n]['contextName'] in ['', ' ', 'None', None]:
                item = self.getItemFromAttrValue('contextName', treeDict[n]['contextName'])
                if not item in self.__editedItems__['deleted']:
                    ctxtData.insert(n, dict(contextName=treeDict[n]['contextName'], childs=treeDict[n]['childs']))
                else:
                    self._project.delContext(treeDict[n]['contextName'])
            else:
                self.log.warning("!!! Context 'name' value not valide, skipp %s !!!" % treeDict[n]['contextName'])
        #--- Store and refresh ---#
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])
        self._project.buildContexts(*ctxtData)
        self.buildTree()
        self.pWidget.rf_editedItemStyle()

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
    :param contextObject: Context object
    :type contextObject: Context
    """

    def __init__(self, pWidget, contextObject):
        self.pWidget = pWidget
        self.mainUi = self.pWidget.parent()
        self._fdn = self.pWidget._fdn
        self._project = self._fdn._project
        self._context = contextObject
        self._users = self._fdn._users
        super(Entities, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        self.log = self.pWidget.log
        super(Entities, self)._initWidget()
        self._context.buildFromSettings()

    def _setupIcons(self):
        """
        Setup Entity icons
        """
        self.log = self.pWidget.log
        super(Entities, self)._setupIcons()
        #--- Edit Label ---#
        self.pb_edit1.setText('Clear')
        self.pb_edit1.setIcon(self.iconClear)
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
        self.pb_edit2.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.tw_tree.setIndentation(12)
        self.tw_tree.header().setStretchLastSection(False)
        self.rf_headers('Entity Type', 'Entity SubType')
        self.rf_treeColumns()

    def getItemFromCtxtCode(self, ctxtCode, parentCode=None):
        """
        Get item from given CtxtCode

        :param ctxtCode: Context entity code
        :type ctxtCode: str
        :param parentCode: Parent context entity code
        :type parentCode: str
        :return: CtxtEntity item
        :rtype: QtGui.QTreeWidgetItem
        """
        for item in pQt.getAllItems(self.tw_tree):
            if parentCode is None:
                if item.itemObj.ctxtCode == ctxtCode and item.itemObj.contextType == 'mainType':
                    return item
            else:
                if item.itemObj.ctxtCode == ctxtCode and item.itemObj.contextType == 'subType':
                    if item.parent().itemObj.ctxtCode == parentCode:
                        return item

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
            self.pb_edit1.setToolTip("Clear selection")
            self.pb_apply.setToolTip("Apply data to Foundation object")
            self.pb_cancel.setToolTip("Restore data from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected Entity (Disabled for your grade)")
        else:
            super(Entities, self).rf_toolTips()

    def buildTree(self):
        """
        Build Context entities tree widget
        """
        super(Entities, self).buildTree()
        if self._context.childs:
            for ctxtObj in self._context.childs:
                newMainItem = self.new_treeItem(ctxtObj)
                self.ud_treeItem(newMainItem, itemType='mainType')
                self.tw_tree.addTopLevelItem(newMainItem)
                if ctxtObj.childs:
                    for childObj in ctxtObj.childs:
                        newSubItem =  self.new_treeItem(childObj)
                        self.ud_treeItem(newSubItem, itemType='subType')
                        newMainItem.addChild(newSubItem)
        self.rf_treeColumns()
        self.rf_itemStyle()
        self.tw_tree.expandAll()

    def new_treeItem(self, itemObj):
        """
        Create or update tree item widget

        :param itemObj: Core object
        :type itemObj: Group | User
        :return: New tree item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemObj = itemObj
        self.ud_treeItem(newItem)
        for n in range(self.tw_tree.columnCount()):
            newItem.setTextAlignment(n, 5)
        return newItem

    def ud_treeItem(self, item, **kwargs):
        """
        Update item data and settings

        :param item: Entities tree item
        :type item: newItem
        :param kwargs: Context entity item data (key must starts with 'ctxt')
        :type kwargs: dict
        """
        super(Entities, self).ud_treeItem(item, **kwargs)
        #--- Get Type ---#
        selItems = self.tw_tree.selectedItems() or []
        if kwargs.get('itemType') is None:
            if not selItems:
                item.itemType = 'mainType'
            else:
                item.itemType = 'subType'
        else:
            item.itemType = kwargs['itemType']
        #--- Get Tool Tips ---#
        toolTip = ["Type   = %s" % item.itemType,
                   "Code   = %s" % item.itemObj.ctxtCode,
                   "Name   = %s" % item.itemObj.ctxtName,
                   "Label  = %s" % item.itemObj.contextLabel,
                   "Folder = %s" % item.itemObj.ctxtFolder]
        #--- Clear Item ---#
        for n in range(2):
            item.setText(n, '')
            item.setToolTip(n, '')
        #--- Edit Item ---#
        if item.itemType == 'mainType':
            item.setText(0, item.itemObj.contextLabel)
            item.setToolTip(0, '\n'.join(toolTip))
        else:
            item.setText(1, item.itemObj.contextLabel)
            item.setToolTip(1, '\n'.join(toolTip))

    def on_addItem(self):
        """
        Command launched when 'Add' QPushButton is clicked

        Add new group to tree
        """
        super(Entities, self).on_addItem()
        #--- Get Prompts ---#
        prompts = [dict(promptType='line', promptLabel='ctxtCode'),
                   dict(promptType='line', promptLabel='ctxtName'),
                   dict(promptType='line', promptLabel='ctxtFolder')]
        #--- Launch Dialog ---#
        self.dial_CtxtEntity = promptMultiUi.PromptMulti(title="New Entity", prompts=prompts, parent=self,
                                                         acceptCmd=self.on_dialogAccept)
        self.dial_CtxtEntity.exec_()

    def on_dialogAccept(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save context datas
        """
        #--- Get Datas ---#
        result = self.dial_CtxtEntity.result()
        self._checkDialogResult(result)
        #--- Get Selected item ---#
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            if selItems[0].itemType == 'subType':
                selItems = [selItems[0].parent()]
        #--- Add Context Entity ---#
        self.log.detail("Adding new Context Entity: %s" % result['ctxtCode'])
        itemObj = self._context.newChild(ctxtCode=result['ctxtCode'], ctxtName=result['ctxtName'],
                                         ctxtFolder=result['ctxtFolder'])
        newItem = self.new_treeItem(itemObj)
        if not selItems:
            self.tw_tree.addTopLevelItem(newItem)
        else:
            selItems[0].addChild(newItem)
        #--- Store Edition ---#
        self.__editedItems__['added'].append(newItem)
        #--- Quit ---#
        self.rf_treeColumns()
        self.rf_itemStyle()
        self.dial_CtxtEntity.close()

    def _checkDialogResult(self, result):
        """
        Check Dialog results

        :param result: Dialog results
        :type result: dict
        """
        #--- Check Data ---#
        if (result['ctxtCode'] in self._fdn.typoExclusion or result['ctxtName'] in self._fdn.typoExclusion
            or result['ctxtFolder'] in self._fdn.typoExclusion):
            pQt.errorDialog("!!! Entity invalid: %s -- %s -- %s !!!" % (result['ctxtCode'], result['ctxtName'],
                                                                        result['ctxtFolder']),
                            self.dial_CtxtEntity, raiseError=True)
        #--- Check New Entity ---#
        treeDict = self.getData()
        selItems = self.tw_tree.selectedItems() or []
        for n in sorted(treeDict.keys()):
            message = None
            #--- Check Main Type ---#
            if not selItems:
                if treeDict[n]['ctxtCode'] == result['ctxtCode']:
                    message = "!!! EntityCode %r already exists !!!" % result['ctxtCode']
                elif treeDict[n]['ctxtName'] == result['ctxtName']:
                    message = "!!! EntityName %r already exists !!!" % result['ctxtName']
                elif treeDict[n]['ctxtFolder'] == result['ctxtFolder']:
                    message = "!!! EntityFolder %r already exists !!!" % result['ctxtFolder']
            #--- Check Sub Type ---#
            else:
                if treeDict[n]['ctxtCode'] == selItems[0].itemObj.ctxtCode:
                    for m in sorted(treeDict[n]['childs'].keys()):
                        if treeDict[n]['childs'][m]['ctxtCode'] == result['ctxtCode']:
                            message = "!!! EntityCode %r already exists !!!" % result['ctxtCode']
                        elif treeDict[n]['childs'][m]['ctxtName'] == result['ctxtName']:
                            message = "!!! EntityName %r already exists !!!" % result['ctxtName']
                        elif treeDict[n]['childs'][m]['ctxtFolder'] == result['ctxtFolder']:
                            message = "!!! EntityFolder %r already exists !!!" % result['ctxtFolder']
            #--- Result ---#
            if message is not None:
                pQt.errorDialog(message, self.dial_CtxtEntity, raiseError=True)

    def on_editItem1(self):
        """
        Command launched when 'Edit1' QPushButton is clicked

        Clear selection
        """
        super(Entities, self).on_editItem1()
        self.tw_tree.clearSelection()

    def on_apply(self):
        """
        Command launched when 'Apply' QPushButton is clicked

        Store datas to itemObject
        """
        super(Entities, self).on_apply()
        #--- Remove Deleted Items ---#
        for item in self.__editedItems__['deleted']:
            if item.itemObj.contextType == 'mainType':
                self._context.delChild(item.itemObj.ctxtCode)
                self.tw_tree.takeTopLevelItem(self.tw_tree.indexOfTopLevelItem(item))
            else:
                self._context.delChild(item.itemObj._parent.ctxtCode, item.itemObj.ctxtCode)
                item.parent().removeChild(item)
        #--- Parse Entities Tree ---#
        ind = 0
        ctxtData = dict(childs=dict())
        treeDict = self.getData()
        for n in sorted(treeDict.keys()):
            item = self.getItemFromAttrValue('ctxtCode', treeDict[n]['ctxtCode'])
            if not item in self.__editedItems__['deleted']:
                ctxtData['childs'][ind] = treeDict[n]
                ind += 1
        #--- Store and refresh ---#
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])
        self.pWidget.rf_editedItemStyle()
        self._context.update(**ctxtData)
        self.rf_itemStyle()

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save data
        """
        super(Entities, self).on_save()
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])

    def on_cancel(self):
        """
        Command launched when 'Cancel' QPushButton is clicked

        Restore datas from itemObject
        """
        super(Entities, self).on_cancel()
        self.pWidget.rf_editedItemStyle()


class Tasks(basicTreeUi.BasicTree):
    """
    Entities Class: Contains Entities settings, child of ToolSettings

    :param pWidget: Parent widget
    :type pWidget: dialogs.ToolSettings
    :param contextObject: Context object
    :type contextObject: Context
    """

    def __init__(self, pWidget, contextObject):
        self.pWidget = pWidget
        self.mainUi = self.pWidget.parent()
        self._fdn = self.pWidget._fdn
        self._users = self._fdn._users
        self._context = contextObject
        super(Tasks, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        self.log = self.pWidget.log
        super(Tasks, self)._initWidget()

    def _setupIcons(self):
        """
        Setup Task icons
        """
        self.log = self.pWidget.log
        super(Tasks, self)._setupIcons()
        #--- Edit Label ---#
        self.pb_edit1.setText('Clear')
        self.pb_edit1.setIcon(self.iconClear)
        #--- Edit Grade ---#
        if not self._users._user.grade == 0:
            self.pb_del.setEnabled(False)

    def _setupWidget(self):
        """
        Setup Entities widget
        """
        super(Tasks, self)._setupWidget()
        self.l_title.setText(self.__class__.__name__)
        self.cbb_filter.setVisible(False)
        self.pb_template.setVisible(False)
        self.pb_template.setVisible(False)
        self.pb_edit2.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.tw_tree.setIndentation(12)
        self.tw_tree.header().setStretchLastSection(False)
        self.rf_headers('%s Step' % self._context.contextLabel, '%s Task' % self._context.contextLabel)
        self.rf_treeColumns()

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        if self.mainUi.showToolTips:
            self.pb_itemUp.setToolTip("Move up selected Step/Task")
            self.pb_itemDn.setToolTip("Move down selected Step/Task")
            self.pb_template.setToolTip("Open templates")
            self.pb_add.setToolTip("Create new Step/Task")
            self.pb_del.setToolTip("Delete selected Step/Task")
            self.pb_edit1.setToolTip("Clear selection")
            self.pb_apply.setToolTip("Apply data to Foundation object")
            self.pb_cancel.setToolTip("Restore data from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected Step/Task (Disabled for your grade)")
        else:
            super(Tasks, self).rf_toolTips()

    def buildTree(self):
        """
        Build Context entities tree widget
        """
        super(Tasks, self).buildTree()

    def new_treeItem(self, itemObj):
        """
        Create or update tree item widget

        :param itemObj: Core object
        :type itemObj: Group | User
        :return: New tree item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemObj = itemObj
        self.ud_treeItem(newItem)
        for n in range(self.tw_tree.columnCount()):
            newItem.setTextAlignment(n, 5)
        return newItem

    def ud_treeItem(self, item, **kwargs):
        """
        Update item data and settings

        :param item: Entities tree item
        :type item: newItem
        :param kwargs: Context entity item data (key must starts with 'ctxt')
        :type kwargs: dict
        """
        super(Tasks, self).ud_treeItem(item, **kwargs)
        #--- Get Type ---#
        selItems = self.tw_tree.selectedItems() or []
        if kwargs.get('itemType') is None:
            if not selItems:
                item.itemType = 'step'
            else:
                item.itemType = 'task'
        else:
            item.itemType = kwargs['itemType']
        #--- Get Tool Tips ---#
        toolTip = ["Type   = %s" % item.itemType,
                   "Code   = %s" % item.itemObj.pipeCode,
                   "Name   = %s" % item.itemObj.pipeName]
        #--- Clear Item ---#
        for n in range(2):
            item.setText(n, '')
            item.setToolTip(n, '')
        #--- Edit Item ---#
        if item.itemType == 'step':
            item.setText(0, item.itemObj.pipeName)
            item.setToolTip(0, '\n'.join(toolTip))
        else:
            item.setText(1, item.itemObj.pipeName)
            item.setToolTip(1, '\n'.join(toolTip))

    def on_addItem(self):
        """
        Command launched when 'Add' QPushButton is clicked

        Add new group to tree
        """
        super(Tasks, self).on_addItem()
        #--- Get Prompts ---#
        prompts = [dict(promptType='line', promptLabel='pipeCode'),
                   dict(promptType='line', promptLabel='pipeName')]
        #--- Launch Dialog ---#
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            title = "New Task"
        else:
            title = "New Step"
        self.dial_pipeLine = promptMultiUi.PromptMulti(title=title, prompts=prompts, parent=self,
                                                       acceptCmd=self.on_dialogAccept)
        self.dial_pipeLine.exec_()

    def on_dialogAccept(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save context datas
        """
        #--- Check Datas ---#
        result = self.dial_pipeLine.result()
        self._checkDialogResult(result)
        #--- Get Datas ---#
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            result['pipeType'] = 'task'
            if selItems[0].itemObj.pipeType == 'task':
                selItems = [selItems[0].parent()]
            itemObj = selItems[0].itemObj.newChild(**result)
        else:
            result['pipeType'] = 'step'
            itemObj = self._context.newPipeChild(**result)
        #--- Add Task ---#
        self.log.detail("Adding new %s: %s" % (result['pipeType'], result['pipeName']))
        newItem = self.new_treeItem(itemObj)
        if not selItems:
            self.tw_tree.addTopLevelItem(newItem)
        else:
            selItems[0].addChild(newItem)
        #--- Store Edition ---#
        self.__editedItems__['added'].append(newItem)
        #--- Quit ---#
        self.rf_treeColumns()
        self.rf_itemStyle()
        self.dial_pipeLine.close()

    def _checkDialogResult(self, result):
        """
        Check Dialog results

        :param result: Dialog results
        :type result: dict
        """
        #--- Check Data ---#
        if result['pipeCode'] in self._fdn.typoExclusion or result['pipeName'] in self._fdn.typoExclusion:
            pQt.errorDialog("!!! Pipe invalid: %s -- %s !!!" % (result['pipeCode'], result['pipeName']),
                            self.dial_CtxtEntity, raiseError=True)
        #--- Check New Pipe ---#
        treeDict = self.getData()
        selItems = self.tw_tree.selectedIndexes() or []
        pprint.pprint(treeDict)
        if treeDict.keys():
            for n, stepDict in sorted(treeDict.iteritems()):
                print stepDict['pipeName'],
                if stepDict['pipeName'] == result['pipeName'] or stepDict['pipeCode'] == result['pipeCode']:
                    pQt.errorDialog("!!! Step already exists: %s -- %s !!!" % (result['pipeName'],
                                                                               result['pipeCode']),
                                    self.dial_pipeLine, raiseError=True)
                if selItems:
                    for c, taskDict in sorted(stepDict['childs']):
                        if taskDict['pipeName'] == result['pipeName'] or taskDict['pipeCode'] == result['pipeCode']:
                            pQt.errorDialog("!!! Task already exists: %s -- %s !!!" % (result['pipeName'],
                                                                                       result['pipeCode']),
                                            self.dial_pipeLine, raiseError=True)

    def on_editItem1(self):
        """
        Command launched when 'Edit1' QPushButton is clicked

        Clear selection
        """
        super(Tasks, self).on_editItem1()
        self.tw_tree.clearSelection()

    def on_apply(self):
        """
        Command launched when 'Apply' QPushButton is clicked

        Store datas to itemObject
        """
        super(Tasks, self).on_apply()
        #--- Remove Deleted Items ---#
        for item in self.__editedItems__['deleted']:
            if item.itemObj.pipeType == 'step':
                self._context.delPipeChild(item.itemObj.pipeName)
                self.tw_tree.takeTopLevelItem(self.tw_tree.indexOfTopLevelItem(item))
            else:
                self._context.delPipeChild(item.parent().itemObj.pipeName, taskName=item.itemObj.pipeName)
                item.parent().removeChild(item)
        #--- Parse Entities Tree ---#
        ind = 0
        pipeData = dict(childs=dict())
        treeDict = self.getData()