import os
from coreQt import pQt
from PyQt4 import QtGui
from coreSys import pMath
from functools import partial
from coreQt.widgets import basicTreeUi
from coreQt.dialogs import promptMultiUi


class Groups(basicTreeUi.BasicTree):
    """
    Groups Class: Contains UserGroups settings, child of ToolSettings

    :param pWidget: Parent widget
    :type pWidget: dialogs.ToolSettings
    """

    def __init__(self, pWidget):
        self.pWidget = pWidget
        self.mainUi = self.pWidget.parent()
        self._fdn = self.pWidget._fdn
        self._groups = self._fdn._groups
        self._users = self._fdn._users
        super(Groups, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        self.log = self.pWidget.log
        super(Groups, self)._initWidget()
        self._groups.buildFromSettings()

    def _setupIcons(self):
        """
        Setup Groups icons
        """
        super(Groups, self)._setupIcons()
        #--- Init Icons ---#
        self.iconStyle = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'style.png'))
        #--- Add Icons ---#
        self.pb_edit2.setIcon(self.iconStyle)
        #--- Edit Label ---#
        self.pb_edit1.setText("Edit")
        self.pb_edit2.setText("Style")
        #--- Edit Grade ---#
        if not self._users._user.grade == 0:
            self.pb_del.setEnabled(False)

    def _setupWidget(self):
        """
        Setup Groups widget
        """
        super(Groups, self)._setupWidget()
        self.l_title.setText(self.__class__.__name__)
        self.pb_template.setVisible(False)
        self.cbb_filter.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.tw_tree.header().setStretchLastSection(False)
        self.rf_headers('Code', 'Name', 'Grade', 'Style')
        self.rf_treeColumns()

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        if self.mainUi.showToolTips:
            self.pb_itemUp.setToolTip("Move up selected group")
            self.pb_itemDn.setToolTip("Move down selected group")
            self.pb_add.setToolTip("Create new user group")
            self.pb_del.setToolTip("Delete selected group")
            self.pb_edit1.setToolTip("Edit selected group")
            self.pb_edit2.setToolTip("Update style auto")
            self.pb_apply.setToolTip("Apply datas to Foundation object")
            self.pb_cancel.setToolTip("Restore datas from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected group (Disabled for your grade)")
        else:
            super(Groups, self).rf_toolTips()

    def buildTree(self):
        """
        Build Groups tree widget
        """
        super(Groups, self).buildTree()
        if self._groups.childs:
            grpItems = []
            for grpObj in self._groups.childs:
                newItem = self.new_treeItem(grpObj)
                grpItems.append(newItem)
            self.tw_tree.addTopLevelItems(grpItems)
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
        super(Groups, self).ud_treeItem(item, **kwargs)
        #--- Edit Item ---#
        item.setText(0, item.itemObj.grpCode)
        item.setText(1, item.itemObj.grpName)
        item.setText(2, str(item.itemObj.grpGrade))
        item.setBackgroundColor((self.tw_tree.columnCount() - 1), QtGui.QColor(item.itemObj.grpColor[0],
                                                                               item.itemObj.grpColor[1],
                                                                               item.itemObj.grpColor[2]))

    def on_addItem(self):
        """
        Command launched when 'Add' QPushButton is clicked

        Add new group to tree
        """
        super(Groups, self).on_addItem()
        #--- Get Prompts ---#
        grades = []
        for n in range(max(self._groups.grades) + 1):
            grades.append(str(n))
        prompts = [dict(promptType='line', promptLabel='grpCode'),
                   dict(promptType='line', promptLabel='grpName'),
                   dict(promptType='combo', promptLabel='grpGrade', promptValue=grades, defaultValue='9'),
                   dict(promptType='color', promptLabel='grpColor', promptValue=(0, 0, 0))]
        #--- Launch Dialog ---#
        self.dial_groups = promptMultiUi.PromptMulti(title="New Group", prompts=prompts, parent=self,
                                                     acceptCmd=partial(self.on_dialogAccept, dialogMode='add',
                                                                       selItem=None))
        self.dial_groups.exec_()

    def on_editItem1(self):
        """
        Command launched when 'Edit' QPushButton is clicked

        Launch Group editing dialog
        """
        super(Groups, self).on_editItem1()
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            #--- Get Prompts ---#
            grades = []
            itemObj = selItems[0].itemObj
            for n in range(max(self._groups.grades) + 1):
                grades.append(str(n))
            prompts = [dict(promptType='line', promptLabel='grpCode', promptValue=itemObj.grpCode, readOnly=True),
                       dict(promptType='line', promptLabel='grpName', promptValue=itemObj.grpName),
                       dict(promptType='combo', promptLabel='grpGrade', promptValue=grades,
                            defaultValue=itemObj.grpGrade),
                       dict(promptType='color', promptLabel='grpColor', promptValue=itemObj.grpColor)]
            #--- Launch Dialog ---#
            self.dial_groups = promptMultiUi.PromptMulti(title="Edit Group", prompts=prompts, parent=self,
                                                         acceptCmd=partial(self.on_dialogAccept, dialogMode='edit',
                                                                           selItem=selItems[0]))
            self.dial_groups.exec_()
        else:
            message = "!!! Select at least one group item !!!"
            pQt.errorDialog(message, self)

    def on_editItem2(self):
        """
        Command launched when 'Style' QPushButton is clicked

        Auto assign color to all items
        """
        super(Groups, self).on_editItem2()
        N = len(pQt.getTopItems(self.tw_tree))
        for n, item in enumerate(pQt.getTopItems(self.tw_tree)):
            if n == 0:
                rgb = (255, 0, 0)
            elif n == (len(pQt.getTopItems(self.tw_tree)) - 1):
                rgb = (0, 0, 255)
            elif n < (N / 2):
                rgb = (pMath.linear(0, (N / 2), 255, 0, n), pMath.linear(0, (N / 2), 0, 255, n), 0)
            else:
                rgb = (0, pMath.linear((N / 2), N, 255, 0, n), pMath.linear((N / 2), N, 0, 255, n))
            self.ud_treeItem(item, grpColor=rgb)
            if (not item in self.__editedItems__['added'] and not item in self.__editedItems__['edited'] and
                not item in self.__editedItems__['deleted']):
                self.__editedItems__['edited'].append(item)
        self.rf_itemStyle()

    def on_dialogAccept(self, dialogMode='add', selItem=None):
        """
        Command launched when 'Save' dialog QPushButton is clicked

        Save group datas
        :param dialogMode: 'add' or 'edit'
        :type dialogMode: str
        :param selItem: Selected group item
        :type selItem: QtGui.QTreeWidgetItem
        """
        #--- Get Datas ---#
        result = self.dial_groups.result()
        result['grpGrade'] = int(result['grpGrade'])
        self._checkDialogResult(result, dialogMode)
        #--- Added Goup ---#
        if dialogMode == 'add':
            self.log.detail("Adding new group: %s" % result['grpCode'])
            itemObj = self._groups.newChild(**result)
            newItem = self.new_treeItem(itemObj)
            self.tw_tree.addTopLevelItem(newItem)
            self.tw_tree.clearSelection()
            self.tw_tree.setItemSelected(newItem, True)
            #--- Store Edition ---#
            self.__editedItems__['added'].append(newItem)
        #--- Edited Group ---#
        elif dialogMode == 'edit':
            self.log.detail("Editing user: %s" % result['grpCode'])
            self.ud_treeItem(selItem, **result)
            if not selItem in self.__editedItems__['edited']:
                if not selItem in self.__editedItems__['added']:
                    self.__editedItems__['edited'].append(selItem)
        #--- Quit ---#
        self.rf_treeColumns()
        self.rf_itemStyle()
        self.dial_groups.close()

    def _checkDialogResult(self, result, dialogMode):
        """
        Check Dialog results

        :param result: Dialog results
        :type result: dict
        :param dialogMode: 'add' or 'edit'
        :type dialogMode: str
        """
        #--- Check Data ---#
        if result['grpCode'] in self._fdn.typoExclusion or result['grpName'] in self._fdn.typoExclusion:
            message = "!!! 'code' or 'name' invalid: %s -- %s !!!" % ( result['grpCode'], result['grpName'])
            pQt.errorDialog(message, self)
            raise AttributeError(message)
        #--- Check New Code ---#
        if dialogMode == 'add':
            grpData = self.getData()
            for n in sorted(grpData.keys()):
                if result['grpCode'] == grpData[n]['grpCode']:
                    message = "!!! %s already exists !!!" % result['grpCode']
                    pQt.errorDialog(message, self)
                    raise AttributeError(message)

    def on_apply(self):
        """
        Command launched when 'Apply' QPushButton is clicked

        Store datas to itemObject
        """
        super(Groups, self).on_apply()
        ind = 0
        #--- Parse Group Tree ---#
        grpDict = dict()
        treeDict = self.getData()
        for n in sorted(treeDict.keys()):
            if not treeDict[n]['grpCode'] in ['', ' ', 'None', None]:
                item = self.getItemFromAttrValue('grpCode', treeDict[n]['grpCode'])
                if not item in self.__editedItems__['deleted']:
                    for k, v in treeDict[n].iteritems():
                        if not k == 'childs':
                            if not ind in grpDict.keys():
                                grpDict[ind] = dict()
                            grpDict[ind][k] = v
                    ind += 1
            else:
                self.log.warning("!!! Group 'code' value not valide, skipp %s !!!" % treeDict[n]['grpCode'])
        #--- Store and refresh ---#
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])
        self._groups.buildChilds(grpDict)
        self.buildTree()
        self.pWidget.rf_editedItemStyle()
        self.rf_itemStyle()

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save data
        """
        super(Groups, self).on_save()
        self._groups.writeSettingsFile()

    def on_cancel(self):
        """
        Command launched when 'Cancel' QPushButton is clicked

        Restore datas from itemObject
        """
        super(Groups, self).on_cancel()
        self.pWidget.rf_editedItemStyle()
