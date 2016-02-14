import os
from coreQt import pQt
from PyQt4 import QtGui
from coreSys import pMath
from coreQt.widgets import basicTreeUi
from foundation.gui._ui import ts_groupsDialUI


class Groups(basicTreeUi.BasicTree):
    """
    Groups Class: Contains UserGroups settings, child of ToolSettings

    :param pWidget: Parent widget
    :type pWidget: dialogs.ToolSettings
    """

    def __init__(self, pWidget):
        self.pWidget = pWidget
        self.log = self.pWidget.log
        self.mainUi = self.pWidget.parent()
        self.fdn = self.pWidget.fdn
        self.userGrps = self.fdn.userGrps
        self.users = self.fdn.users
        super(Groups, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        super(Groups, self)._initWidget()
        self.userGrps.buildFromSettings()

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
        if not self.users._user.grade == 0:
            self.pb_del.setEnabled(False)

    def _setupWidget(self):
        """
        Setup Groups widget
        """
        super(Groups, self)._setupWidget()
        self.l_title.setText('Groups')
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
            if not self.users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected group (Disabled for your grade)")
        else:
            super(Groups, self).rf_toolTips()

    def buildTree(self):
        """
        Build Groups tree widget
        """
        super(Groups, self).buildTree()
        self.log.detail("---> Groups tree")
        if self.userGrps._groups:
            grpItems = []
            for grpObj in self.userGrps._groups:
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
        self.dial_groups = GroupsDialog(dialogMode='add', parent=self)
        self.dial_groups.exec_()

    def on_editItem1(self):
        """
        Command launched when 'Edit' QPushButton is clicked

        Launch Group editing dialog
        """
        super(Groups, self).on_editItem1()
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            self.dial_groups = GroupsDialog(dialogMode='edit', selItem=selItems[0], parent=self)
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
                    if not ind in grpDict.keys():
                        grpDict[ind] = dict()
                    for k, v in treeDict[n].iteritems():
                        grpDict[ind][k] = v
                    ind += 1
            else:
                self.log.warning("!!! ERROR: Group 'code' value not valide, skipp %s !!!" % treeDict[n]['grpCode'])
        #--- Store and refresh ---#
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])
        self.userGrps.buildFromDict(grpDict)
        self.pWidget.rf_editedItemStyle()
        self.buildTree()

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save data
        """
        super(Groups, self).on_save()
        self.userGrps.writeSettingsFile()

    def on_cancel(self):
        """
        Command launched when 'Cancel' QPushButton is clicked

        Restore datas from itemObject
        """
        super(Groups, self).on_cancel()
        self.pWidget.rf_editedItemStyle()


class GroupsDialog(QtGui.QDialog, ts_groupsDialUI.Ui_dial_groups):
    """
    Groups Dialog: UserGroups edition, child of Groups

    :param dialogMode: 'add' or 'edit'
    :type dialogMode: str
    :param selItem: Selected group item
    :type selItem: newItem
    :param parent: Parent Ui
    :type parent: Groups
    """

    def __init__(self, dialogMode='add', selItem=None, parent=None):
        self.dialogMode = dialogMode
        self.selItem = selItem
        self.log = parent.log
        self.log.title = 'TS_groups'
        super(GroupsDialog, self).__init__(parent)
        self.pWidget = parent
        self.mainUi = self.pWidget.mainUi
        self.userGrps = self.pWidget.userGrps
        self._setupUi()

    def _setupUi(self):
        """
        Setup QtGui Groups dialog
        """
        self.log.detail("#----- Setup GroupsDialog Ui -----#")
        self.setupUi(self)
        #--- Mode ---#
        if self.dialogMode == 'add':
            self.le_userGrpCode.setEnabled(True)
        else:
            self.le_userGrpCode.setEnabled(False)
        #--- Grade ---#
        for n in range(max(self.userGrps.grades) + 1):
            self.cb_grade.addItem(str(n))
        #--- Color ---#
        self.pb_userGrpStyle.clicked.connect(self.on_color)
        self.sb_styleR.editingFinished.connect(self.on_rgb)
        self.sb_styleG.editingFinished.connect(self.on_rgb)
        self.sb_styleB.editingFinished.connect(self.on_rgb)
        #--- Edit ---#
        self.pb_save.setIcon(self.pWidget.iconApply)
        self.pb_save.clicked.connect(self.on_save)
        self.pb_cancel.setIcon(self.pWidget.iconCancel)
        self.pb_cancel.clicked.connect(self.close)
        #--- Refresh ---#
        self.rf_dialog()
        self.rf_toolTips()

    def rf_dialog(self):
        """
        Refresh dialog values
        """
        if self.selItem is not None:
            self.le_userGrpCode.setText(str(self.selItem.itemObj.grpCode))
            self.le_userGrpName.setText(str(self.selItem.itemObj.grpName))
            self.cb_grade.setCurrentIndex(self.selItem.itemObj.grpGrade)
            self.pb_userGrpStyle.setStyleSheet("background-color: rgb(%s, %s, %s)" % (self.selItem.itemObj.grpColor[0],
                                                                                      self.selItem.itemObj.grpColor[1],
                                                                                      self.selItem.itemObj.grpColor[2]))
            self.sb_styleR.setValue(self.selItem.itemObj.grpColor[0])
            self.sb_styleG.setValue(self.selItem.itemObj.grpColor[1])
            self.sb_styleB.setValue(self.selItem.itemObj.grpColor[2])
        else:
            self.pb_userGrpStyle.setStyleSheet("background-color: rgb(0, 0, 0)")
            self.sb_styleR.setValue(0)
            self.sb_styleG.setValue(0)
            self.sb_styleB.setValue(0)

    def rf_toolTips(self):
        """
        Refresh dialog toolTips
        """
        if self.mainUi.showToolTips:
            self.le_userGrpCode.setToolTip("Group code ('ADMIN', 'DEV', ...)")
            self.le_userGrpName.setToolTip("Group name")
            self.cb_grade.setToolTip("Group grade index (min=0, max=9")
            self.sb_styleR.setToolTip("Red color value (0, 255)")
            self.sb_styleG.setToolTip("Green color value (0, 255)")
            self.sb_styleB.setToolTip("Blue color value (0, 255)")
            self.pb_userGrpStyle.setToolTip("Click to pick a color")
        else:
            wList = [self.sb_styleR, self.sb_styleG, self.sb_styleB, self.pb_userGrpStyle]
            for widget in wList:
                widget.setToolTip('')

    def on_color(self):
        """
        Command launched when 'Color' QPushButton is clicked

        Launch color dialog
        """
        # noinspection PyArgumentList
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            rgba = color.getRgb()
            self.sb_styleR.setValue(rgba[0])
            self.sb_styleG.setValue(rgba[1])
            self.sb_styleB.setValue(rgba[2])
            self.on_rgb()

    def on_rgb(self):
        """
        Command launched when 'RGB' QSpinBoxes are edited

        Edit and refresh color
        """
        grpColor = (self.sb_styleR.value(), self.sb_styleG.value(), self.sb_styleB.value())
        self.pb_userGrpStyle.setStyleSheet("background-color: rgb(%s, %s, %s)" % (grpColor[0],
                                                                                  grpColor[1],
                                                                                  grpColor[2]))

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save group datas
        """
        #--- Get Datas ---#
        excludes = ['', ' ', 'None', None]
        grpCode = str(self.le_userGrpCode.text())
        grpName = str(self.le_userGrpName.text())
        grpGrade = int(self.cb_grade.currentText())
        grpColor = (self.sb_styleR.value(), self.sb_styleG.value(), self.sb_styleB.value())
        #--- Check Datas ---#
        if grpCode in excludes or grpName in excludes:
            message = "!!! 'code' or 'name' invalid: %s -- %s !!!" % (grpCode, grpName)
            pQt.errorDialog(message, self)
            raise AttributeError(message)
        #--- Check New Code ---#
        if self.dialogMode == 'add':
            grpData = self.pWidget.getData()
            for n in grpData.keys():
                if grpCode == grpData[n]['grpCode']:
                    message = "!!! %s already exists !!!" % grpCode
                    pQt.errorDialog(message, self)
                    raise AttributeError(message)
        data = dict(grpCode=grpCode, grpName=grpName, grpGrade=grpGrade, grpColor=grpColor)
        #--- Added Goup ---#
        if self.dialogMode == 'add':
            self.log.detail("Adding new group: %s" % grpCode)
            itemObj = self.userGrps.newGroup(**data)
            self.selItem = self.pWidget.new_treeItem(itemObj)
            self.pWidget.tw_tree.addTopLevelItem(self.selItem)
            self.pWidget.tw_tree.clearSelection()
            self.pWidget.tw_tree.setItemSelected(self.selItem, True)
            #--- Store Edition ---#
            if not self.selItem in self.pWidget.__editedItems__['added']:
                self.pWidget.__editedItems__['added'].append(self.selItem)
        #--- Edited Group ---#
        elif self.dialogMode == 'edit':
            self.log.detail("Editing user: %s" % grpCode)
            self.pWidget.ud_treeItem(self.selItem, **data)
            if not self.selItem in self.pWidget.__editedItems__['edited']:
                if not self.selItem in self.pWidget.__editedItems__['added']:
                    self.pWidget.__editedItems__['edited'].append(self.selItem)
        #--- Quit ---#
        self.pWidget.rf_treeColumns()
        self.pWidget.rf_itemStyle()
        self.close()
