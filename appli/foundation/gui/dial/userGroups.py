import os
from coreQt import pQt
from coreSys import pMath
from functools import partial
from PyQt4 import QtGui, QtCore
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
        excludes = ['', ' ', 'None', None]
        result = self.dial_groups.result()
        result['grpGrade'] = int(result['grpGrade'])
        #--- Check Data ---#
        if result['grpCode'] in excludes or result['grpName'] in excludes:
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
        self.pWidget.rf_editedItemStyle()
        self.rf_itemStyle()
        # self.buildTree()

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
            if itemObj.userName in self._project.watchers:
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
        #--- Get Prompts ---#
        prompts = [dict(promptType='line', promptLabel='userName'),
                   dict(promptType='combo', promptLabel='userGroup', promptValue=self._groups.codes,
                        defaultValue=self._groups.codes[-1]),
                   dict(promptType='line', promptLabel='userFirstName'),
                   dict(promptType='line', promptLabel='userLastName')]
        #--- Launch Dialog ---#
        self.dial_user = promptMultiUi.PromptMulti(title="New User", prompts=prompts, parent=self,
                                                   acceptCmd=partial(self.on_dialogAccept, dialogMode='add',
                                                                     selItem=None))
        self.dial_user.exec_()

    def on_editItem1(self):
        """
        Command launched when 'Edit' QPushButton is clicked

        Launch User editing dialog
        """
        super(Users, self).on_editItem1()
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            #--- Get Prompts ---#
            itemObj = selItems[0].itemObj
            prompts = [dict(promptType='line', promptLabel='userName', promptValue=itemObj.userName, readOnly=True),
                       dict(promptType='combo', promptLabel='userGroup', promptValue=self._groups.codes,
                            defaultValue=itemObj.userGroup),
                       dict(promptType='line', promptLabel='userFirstName', promptValue=itemObj.userFirstName),
                       dict(promptType='line', promptLabel='userLastName', promptValue=itemObj.userLastName)]
            #--- Launch Dialog ---#
            self.dial_user = promptMultiUi.PromptMulti(title="Edit User", prompts=prompts, parent=self,
                                                       acceptCmd=partial(self.on_dialogAccept, dialogMode='edit',
                                                                         selItem=selItems[0]))
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
        excludes = ['', ' ', 'None', None]
        result = self.dial_user.result()
        #--- Check Data ---#
        if result['userName'] in excludes:
            message = "!!! 'userName' invalid: %s !!!" % result['userName']
            pQt.errorDialog(message, self)
            raise AttributeError(message)
        #--- Check New User ---#
        if dialogMode == 'add':
            userData = self.getData()
            for n in sorted(userData.keys()):
                if result['userName'] == userData[n]['userName']:
                    message = "!!! %s already exists !!!" % result['userName']
                    pQt.errorDialog(message, self)
                    raise AttributeError(message)
        #--- Added User ---#
        if dialogMode == 'add':
            self.log.detail("Adding new user: %s" % result['userName'])
            userObj = self._users.newChild(userName=result['userName'])
            selItem = self.new_treeItem(userObj)
            self.tw_tree.addTopLevelItem(selItem)
            # noinspection PyUnresolvedReferences
            self.tw_tree.setItemWidget(selItem, 4, selItem.itemWidget)
            self.ud_treeItem(selItem, **result)
            #--- Store Edition ---#
            self.__editedItems__['added'].append(selItem)
            #--- Update Filters ---#
            if not result['userName'][0].upper() in pQt.getComboBoxItems(self.cbb_filter):
                self.cbb_filter.addItem(result['userName'][0].upper())
                self.cbb_filter.setCurrentIndex(self.cbb_filter.findText(result['userName'][0].upper()))
        #--- Edited User ---#
        elif dialogMode == 'edit':
            self.log.detail("Editing user: %s" % result['userName'])
            self.ud_treeItem(selItem, **result)
            if not selItem in self.__editedItems__['edited']:
                if not selItem in self.__editedItems__['added']:
                    self.__editedItems__['edited'].append(selItem)
        #--- Quit ---#
        self.rf_treeColumns()
        self.rf_itemStyle()
        self.dial_user.close()

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
