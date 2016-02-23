import os
from coreQt import pQt
from coreSys import pMath
from functools import partial
from PyQt4 import QtGui, QtCore
from coreQt.widgets import basicTreeUi
from foundation.gui._ui import ts_groupsDialUI, ts_usersDialUI


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
                    for k, v in treeDict[n].iteritems():
                        if not k == 'childs':
                            if not ind in grpDict.keys():
                                grpDict[ind] = dict()
                            grpDict[ind][k] = v
                    ind += 1
            else:
                self.log.warning("!!! ERROR: Group 'code' value not valide, skipp %s !!!" % treeDict[n]['grpCode'])
        #--- Store and refresh ---#
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])
        self._groups.buildChilds(grpDict)
        self.pWidget.rf_editedItemStyle()
        self.buildTree()

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
        super(GroupsDialog, self).__init__(parent)
        self.pWidget = parent
        self.mainUi = self.pWidget.mainUi
        self._groups = self.pWidget._groups
        self._setupUi()

    def _setupUi(self):
        """
        Setup QtGui Groups dialog
        """
        self.log = self.pWidget.log
        self.log.title = self.__class__.__name__
        self.log.detail("#----- Setup %s Ui -----#" % self.__class__.__name__)
        self.setupUi(self)
        #--- Mode ---#
        if self.dialogMode == 'add':
            self.le_userGrpCode.setEnabled(True)
        else:
            self.le_userGrpCode.setEnabled(False)
        #--- Grade ---#
        for n in range(max(self._groups.grades) + 1):
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
            itemObj = self._groups.newChild(**data)
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


class Users(basicTreeUi.BasicTree):
    """
    Users Class: Contains User settings, child of ToolSettings, ProjectSettings

    :param pWidget: Parent widget
    :type pWidget: ToolSettings | ProjectSettings
    :param settingsMode: 'tool' or 'project'
    :type settingsMode: str
    """

    __usersCollected__ = False

    def __init__(self, pWidget, settingsMode='tool'):
        self.pWidget = pWidget
        self.settingsMode = settingsMode
        self.mainUi = self.pWidget.parent()
        self._fdn = self.pWidget._fdn
        self._groups = self._fdn._groups
        self._users = self._fdn._users
        self._project = self._fdn._project
        super(Users, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        self.log = self.pWidget.log
        super(Users, self)._initWidget()
        if self.settingsMode == 'tool':
            self._users.collecteUsers(clear=True)
        else:
            self._users.collecteUsers(clear=True, checkStatus=True)

    def _setupWidget(self):
        """
        Setup Users widget
        """
        super(Users, self)._setupWidget()
        self.l_title.setText('Users')
        self.qf_moveItem.setVisible(False)
        self.pb_template.setVisible(False)
        self.pb_edit2.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.tw_tree.setSortingEnabled(True)
        self.tw_tree.header().setStretchLastSection(False)
        if self.settingsMode == 'tool':
            self.rf_headers('User Name', 'Group', 'First Name', 'Last Name', 'Status')
        elif self.settingsMode == 'project':
            self.pb_add.setVisible(False)
            self.pb_del.setVisible(False)
            self.pb_edit1.setVisible(False)
            self.rf_headers('User Name', 'Group', 'First Name', 'Last Name', 'Watch')
        self.rf_treeColumns()

    def _setupIcons(self):
        """
        Setup Users icons
        """
        super(Users, self)._setupIcons()
        #--- Tool Settings ---#
        if self.settingsMode == 'tool':
            #--- Init Icons ---#
            self.iconActive = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'enable.png'))
            self.iconInactive = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'disable.png'))
            #--- Edit Label ---#
            self.buildFilters()
            self.pb_edit1.setText("Edit")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setEnabled(False)
        #--- Project Settings ---#
        elif self.settingsMode == 'project':
            #--- Init Icons ---#
            self.iconActive = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'pinGreen.png'))
            self.iconInactive = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'pinRed.png'))
            #--- Edit Label ---#
            self.buildFilters()

    @staticmethod
    def getStatus(userItem):
        """
        Get user status state

        :param userItem: User tree item
        :type userItem: QtGui.QTreeWidgetItem
        :return: User status
        :rtype: bool
        """
        # noinspection PyUnresolvedReferences
        return userItem.itemWidget.isChecked()

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        if self.mainUi.showToolTips:
            self.cbb_filter.setToolTip("User index filter")
            self.pb_add.setToolTip("Create new user")
            self.pb_del.setToolTip("Delete selected user")
            self.pb_edit1.setToolTip("Edit selected user")
            self.pb_apply.setToolTip("Apply datas to Foundation object")
            self.pb_cancel.setToolTip("Restore datas from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected user (Disabled for your grade)")
        else:
            super(Users, self).rf_toolTips()

    def rf_statusState(self, itemWidget):
        """
        Refresh watch button icon

        :param itemWidget: User item button
        :type itemWidget: QtGui.QPushButton
        """
        if itemWidget.isChecked():
            itemWidget.setIcon(self.iconActive)
        else:
            itemWidget.setIcon(self.iconInactive)

    def buildFilters(self):
        """
        Build comboBox filters
        """
        super(Users, self).buildFilters()
        self.cbb_filter.addItems(['All', 'Added', 'Edited', 'Deleted', 'Changed'])
        self.cbb_filter.addItems(self._users.getUserPrefixes(capital=True))
        self.cbb_filter.insertSeparator(5)
        self.cbb_filter.setEditable(True)
        self.cbb_filter.lineEdit().setReadOnly(True)
        self.cbb_filter.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        for n in range(self.cbb_filter.count()):
            self.cbb_filter.setItemData(n, QtCore.Qt.AlignCenter, QtCore.Qt.TextAlignmentRole)

    def buildTree(self):
        """
        Build Users tree widget
        """
        super(Users, self).buildTree()
        #--- Collecte Users ---#
        if not self.__usersCollected__:
            if self.settingsMode == 'tool':
                self._users.collecteUsers(clear=True)
            elif self.settingsMode == 'project':
                self._users.collecteUsers(clear=True, checkStatus=True)
            self.__usersCollected__ = True
        #--- Populate Tree ---#
        if self._users.childs:
            for userObj in self._users.childs:
                newItem = self.new_treeItem(userObj)
                self.tw_tree.addTopLevelItem(newItem)
                # noinspection PyUnresolvedReferences
                self.tw_tree.setItemWidget(newItem, 4, newItem.itemWidget)
        #--- Refresh ---#
        self.rf_treeColumns()
        self.rf_itemStyle()
        self.tw_tree.sortItems(0, QtCore.Qt.AscendingOrder)

    def new_treeItem(self, itemObj):
        """
        Create or update tree item widget

        :param itemObj: User core object
        :type itemObj: User
        :return: New user item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemObj = itemObj
        if self.settingsMode == 'tool':
            newItem.itemWidget = self.new_itemButton(itemObj.userStatus)
        elif self.settingsMode == 'project':
            if itemObj.userName in self._project.projectWatchers:
                newItem.itemWidget = self.new_itemButton(True)
            else:
                newItem.itemWidget = self.new_itemButton(False)
        # noinspection PyUnresolvedReferences
        newItem.itemWidget.clicked.connect(partial(self.on_status, newItem))
        self.ud_treeItem(newItem)
        for n in range(self.tw_tree.columnCount()):
            newItem.setTextAlignment(n, 5)
        return newItem

    def ud_treeItem(self, item, **kwargs):
        """
        Update item datas and settings

        :param item: Group tree item
        :type item: newItem
        :param kwargs: Group item datas (key must starts with 'user')
        :type kwargs: dict
        """
        super(Users, self).ud_treeItem(item, **kwargs)
        #--- Edit Item ---#
        item.setText(0, str(item.itemObj.userName))
        item.setText(1, str(item.itemObj.userGroup))
        item.setText(2, str(item.itemObj.userFirstName))
        item.setText(3, str(item.itemObj.userLastName))

    def new_itemButton(self, state):
        """
        Create tree item button

        :param state: Check state
        :type state: bool
        :return: Tree item button
        :rtype: QtGui.QPushButton
        """
        newButton = QtGui.QPushButton()
        newButton.setText('')
        newButton.setCheckable(True)
        newButton.setChecked(state)
        newButton.setIconSize(QtCore.QSize(18, 18))
        newButton.setMaximumSize(40, 20)
        self.rf_statusState(newButton)
        return newButton

    def on_filter(self):
        """
        Command launched when 'Filter' QComboBox item is clicked

        Update use tree display
        """
        super(Users, self).on_filter()
        filter = str(self.cbb_filter.currentText())
        for item in pQt.getAllItems(self.tw_tree):
            #--- Prefix ---#
            if len(filter) == 1:
                if item.itemObj.userPrefix == filter.lower():
                    item.setHidden(False)
                else:
                    item.setHidden(True)
            #--- All ---#
            elif filter == 'All':
                item.setHidden(False)
            #--- Added, Edited, Deleted ---#
            elif filter in ['Added', 'Edited', 'Deleted']:
                if item in self.__editedItems__[filter.lower()]:
                    item.setHidden(False)
                else:
                    item.setHidden(True)
            #--- Changed ---#
            elif filter == 'Changed':
                if (item in self.__editedItems__['added'] or item in self.__editedItems__['edited']
                    or item in self.__editedItems__['deleted']):
                    item.setHidden(False)
                else:
                    item.setHidden(True)

    def on_addItem(self):
        """
        Command launched when 'Add' QPushButton is clicked

        Create new user
        """
        super(Users, self).on_addItem()
        self.dial_user = UsersDialog(dialogMode='add', parent=self)
        self.dial_user.exec_()

    def on_editItem1(self):
        """
        Command launched when 'Edit' QPushButton is clicked

        Launch User editing dialog
        """
        super(Users, self).on_editItem1()
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            self.dial_user = UsersDialog(dialogMode='edit', selItem=selItems[0], parent=self)
            self.dial_user.exec_()
        else:
            message = "!!! Select at least one user item !!!"
            pQt.errorDialog(message, self)

    def on_status(self, item):
        """
        Command launched when 'Status' QPushButton is clicked

        Tag user as active or inactive
        :param item: User tree item
        :type item: QtGui.QTreeWidgetItem
        """
        #--- Store Edition ---#
        if (not item in self.__editedItems__['edited'] and not item in self.__editedItems__['added']
            and not item in self.__editedItems__['deleted']):
            self.__editedItems__['edited'].append(item)
        #--- Refresh Item Style ---#
        # noinspection PyUnresolvedReferences
        self.rf_statusState(item.itemWidget)
        self.rf_itemStyle()

    def on_apply(self):
        """
        Command launched when 'Apply' QPushButton is clicked

        Store datas to itemObject
        """
        super(Users, self).on_apply()
        #--- Added User ---#
        for item in self.__editedItems__['added']:
            if not item.itemObj.userName in self._users.users:
                self._users.addChild(item.itemObj)
                item.itemObj.userStatus = self.getStatus(item)
        #--- Edited User ---#
        for item in self.__editedItems__['edited']:
            if self.settingsMode == 'tool':
                item.itemObj.userStatus = self.getStatus(item)
            elif self.settingsMode == 'project':
                if self.getStatus(item):
                    self._project.addWatcher(item.itemObj.userName)
                else:
                    self._project.delWatcher(item.itemObj.userName)
        #--- Deleted User ---#
        for item in self.__editedItems__['deleted']:
            if item.itemObj.userName in self._users.users:
                self._users.delUser(userObj=item.itemObj)
        #--- Refresh ---#
        self.pWidget.rf_editedItemStyle()
        self.buildTree()

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save data
        """
        super(Users, self).on_save()
        #--- Tool Settings ---#
        if self.settingsMode == 'tool':
            for item in self.__editedItems__['added']:
                item.itemObj.writeFile()
            for item in self.__editedItems__['edited']:
                item.itemObj.writeFile()
            for item in self.__editedItems__['deleted']:
                self._users.delUser(userObj=item.itemObj, archive=True)
        #--- Project Settings ---#
        elif self.settingsMode == 'project':
            pass
        #--- Reset ---#
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])

    def on_cancel(self):
        """
        Command launched when 'Cancel' QPushButton is clicked

        Restore datas from itemObject
        """
        super(Users, self).on_cancel()
        self.pWidget.rf_editedItemStyle()

    def on_discard(self):
        """
        Command launched when 'Discard' QPushButton is clicked

        Discard edited data
        """
        super(Users, self).on_discard()
        self.__usersCollected__ = False


class UsersDialog(QtGui.QDialog, ts_usersDialUI.Ui_dial_users):
    """
    Users Dialog: User edition, child of Users

    :param dialogMode: 'add' or 'edit'
    :type dialogMode: str
    :param selItem: Selected user item
    :type selItem: newItem
    :param parent: Parent Ui
    :type parent: Users
    """

    def __init__(self, dialogMode='add', selItem=None, parent=None):
        self.dialogMode = dialogMode
        self.selItem = selItem
        super(UsersDialog, self).__init__(parent)
        self.pWidget = parent
        self.mainUi = self.pWidget.mainUi
        self._groups = self.pWidget._groups
        self._users = self.pWidget._users
        self._setupUi()

    def _setupUi(self):
        """
        Setup QtGui Groups dialog
        """
        self.log = self.pWidget.log
        self.log.title = self.__class__.__name__
        self.log.detail("#----- Setup UsersDialog Ui -----#")
        self.setupUi(self)
        #--- Mode ---#
        if self.dialogMode == 'add':
            self.le_userName.setEnabled(True)
        elif self.dialogMode == 'edit':
            self.le_userName.setEnabled(False)
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
        self.cb_userGroup.addItems(self._groups.codes)
        if self.selItem is not None:
            self.le_userName.setText(str(self.selItem.itemObj.userName))
            self.cb_userGroup.setCurrentIndex(self.cb_userGroup.findText(self.selItem.itemObj.userGroup))
            self.le_userFirstName.setText(str(self.selItem.itemObj.userFirstName))
            self.le_userLastName.setText(str(self.selItem.itemObj.userLastName))
        else:
            self.cb_userGroup.setCurrentIndex(self.cb_userGroup.findText('VST'))

    def rf_toolTips(self):
        """
        Refresh dialog toolTips
        """
        if self.pWidget.mainUi.showToolTips:
            self.le_userName.setToolTip("User login")
            self.cb_userGroup.setToolTip("User group")
            self.le_userFirstName.setToolTip("User first name")
            self.le_userLastName.setToolTip("User last name")
        else:
            wList = [self.le_userName, self.cb_userGroup, self.le_userFirstName, self.le_userLastName]
            for widget in wList:
                widget.setToolTip('')

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save user datas
        """
        #--- Get Datas ---#
        excludes = ['', ' ', 'newUser', 'None', None]
        userName = str(self.le_userName.text())
        userGroup = str(self.cb_userGroup.currentText())
        userFirstName = str(self.le_userFirstName.text())
        userLastName = str(self.le_userLastName.text())
        #--- Check Data ---#
        if userName in excludes:
            message = "!!! 'userName' invalid: %s !!!" % userName
            pQt.errorDialog(message, self)
            raise AttributeError(message)
        #--- Check New User ---#
        if self.dialogMode == 'add':
            userData = self.pWidget.getData()
            for n in sorted(userData.keys()):
                if userName == userData[n]['userName']:
                    message = "!!! %s already exists !!!" % userName
                    pQt.errorDialog(message, self)
                    raise AttributeError(message)
        data = dict(userName=userName, userGroup=userGroup, userFirstName=userFirstName, userLastName=userLastName)
        #--- Added User ---#
        if self.dialogMode == 'add':
            self.log.detail("Adding new user: %s" % userName)
            userObj = self._users.newChild(userName=userName)
            self.selItem = self.pWidget.new_treeItem(userObj)
            self.pWidget.tw_tree.addTopLevelItem(self.selItem)
            # noinspection PyUnresolvedReferences
            self.pWidget.tw_tree.setItemWidget(self.selItem, 4, self.selItem.itemWidget)
            self.pWidget.ud_treeItem(self.selItem, **data)
            #--- Store Edition ---#
            if not self.selItem in self.pWidget.__editedItems__['added']:
                self.pWidget.__editedItems__['added'].append(self.selItem)
            #--- Update Filters ---#
            if not userName[0].upper() in pQt.getComboBoxItems(self.pWidget.cbb_filter):
                self.pWidget.cbb_filter.addItem(userName[0].upper())
                self.pWidget.cbb_filter.setCurrentIndex(self.pWidget.cbb_filter.findText(userName[0].upper()))
        #--- Edited User ---#
        elif self.dialogMode == 'edit':
            self.log.detail("Editing user: %s" % userName)
            self.pWidget.ud_treeItem(self.selItem, **data)
            if not self.selItem in self.pWidget.__editedItems__['edited']:
                if not self.selItem in self.pWidget.__editedItems__['added']:
                    self.pWidget.__editedItems__['edited'].append(self.selItem)
        #--- Quit ---#
        self.pWidget.rf_treeColumns()
        self.pWidget.rf_itemStyle()
        self.close()
