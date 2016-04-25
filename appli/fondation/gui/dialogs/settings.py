from coreQt import pQt
from PyQt4 import QtGui
import userGroups, users
from coreQt.dialogs import confirmUi, settingsUi


class ToolSettings(settingsUi.Settings):
    """
    ToolSettings Dialog: Contains Fondation tool settings, child of FondationUi

    :param fdnObj: Fondation core object
    :type fdnObj: fondation.core.Fondation
    :param parent: Parent Ui
    :type parent: fondationUi.FondationUi
    """

    def __init__(self, fdnObj, parent=None):
        self._parent = parent
        self._fdn = fdnObj
        self._groups = self._fdn._groups
        self._users = self._fdn._users
        super(ToolSettings, self).__init__(parent=parent)

    def _initSettings(self):
        """
        Init dialog settings
        """
        self.log = self._parent.log
        self.log.title = self.__class__.__name__
        super(ToolSettings, self)._initSettings()
        self._users.collecteUsers(userName=self._fdn.__user__)

    def _initWidgets(self):
        """
        Init dialog widgets
        """
        super(ToolSettings, self)._initWidgets()
        self.setWindowTitle("%s | %s" % (self.log.title, self._fdn.__user__))
        #--- UserGroups ---#
        self.wg_groups = userGroups.Groups(self)
        self.wg_users = users.Users(self, settingsMode='tool')
        #--- Refresh ---#
        for widget in [self.wg_groups, self.wg_users]:
            widget.setVisible(False)
            self.vl_settingsWidget.addWidget(widget)

    @property
    def category(self):
        """
        Get settings category

        :return: Category datas
        :rtype: dict
        """
        return {0: self.userGrpsCategory}

    @property
    def userGrpsCategory(self):
        """
        Get UserGroups category

        :return: UserGroups category
        :rtype: dict
        """
        return {'userGroups': {'code': 'userGroups',
                               'label': 'User Groups',
                               'subCat': {0: {'groups': {'widget': self.wg_groups,
                                                         'code': 'groups',
                                                         'label': 'Groups'}},
                                          1: {'users': {'widget': self.wg_users,
                                                        'code': 'users',
                                                        'label': 'Users'}}}}}

    def getEditedItems(self):
        """
        Get edited subCategory items

        :return: Edited subCategory items
        :rtype: list
        """
        editedItems = []
        for item in pQt.getAllItems(self.tw_category):
            if item.itemType == 'subCategory':
                if item.itemWidget is not None:
                    if item.itemWidget.__edited__:
                        editedItems.append(item)
        return editedItems

    def rf_editedItemStyle(self):
        """
        Refresh catecory style
        """
        for item in pQt.getAllItems(self.tw_category):
            if item.itemType == 'subCategory':
                if item in self.getEditedItems():
                    item.setFont(0, self.editedSubCategoryFont)
                    item.setTextColor(0, QtGui.QColor(100, 150, 255))
                else:
                    item.setFont(0, QtGui.QFont())
                    item.setTextColor(0, QtGui.QColor(220, 220, 220))

    def on_category(self):
        """
        Command launched when 'Category' tree item widget is clicked

        Update category settings
        """
        super(ToolSettings, self).on_category()
        selItems = self.tw_category.selectedItems() or []
        #--- Build Tree ---#
        if selItems:
            if hasattr(selItems[0], 'itemWidget'):
                if selItems[0].itemWidget is not None:
                    if not selItems[0].itemWidget.__edited__:
                        selItems[0].itemWidget._initWidget()
                    selItems[0].itemWidget.buildTree()

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save settings to disk
        """
        super(ToolSettings, self).on_save()
        #--- Parse Edited Items ---#
        for item in self.getEditedItems():
            self.log.detail("---> %s | %s" % (item.parent().itemCode, item.itemCode))
            item.itemWidget.on_save()
            item.itemWidget.__edited__ = False
        #--- Refresh ---#
        self.rf_editedItemStyle()

    def on_close(self):
        """
        Command launched when 'Close' QPushButton is clicked

        Close settings ui
        """
        self.log.debug("#--- Close Dialog ---#")
        editedItems = self.getEditedItems()
        #--- Edited Widget Found ---#
        if editedItems:
            message = ["!!! Warning !!!",
                       "Unsaved category detected:"]
            for item in editedItems:
                message.append("---> %s" % item.itemLabel)
            self.cd_close = confirmUi.Confirm(message='\n'.join(message), buttons=['Save', 'Discard'],
                                              btnCmds=[self._saveSettings, self._discardSettings])
            self.cd_close.setStyleSheet(self.parent().styleSheet())
            self.cd_close.exec_()
        #--- Close Settings ---#
        else:
            self.close()

    def _saveSettings(self):
        """
        Save action confirmed
        """
        self.on_save()
        self.cd_close.close()
        self.close()

    def _discardSettings(self):
        """
        Discard action confirmed
        """
        for item in self.getEditedItems():
            item.itemWidget.on_discard()
        self.cd_close.close()
        self.close()


class ProjectSettings(settingsUi.Settings):
    """
    ProjectSettings Dialog: Contains Fondation project settings, child of FondationUi

    :param fdnObj: Fondation core object
    :type fdnObj: fondation.core.Fondation
    :param parent: Parent Ui
    :type parent: fondationUi.FondationUi
    """

    def __init__(self, fdnObj, parent=None):
        self._parent = parent
        self._fdn = fdnObj
        self._groups = self._fdn._groups
        self._users = self._fdn._users
        self._project = self._fdn._project
        super(ProjectSettings, self).__init__(parent)

    def _initSettings(self):
        """
        Init dialog settings
        """
        self.log = self._parent.log
        self.log.title = self.__class__.__name__
        super(ProjectSettings, self)._initSettings()
        self._users.collecteUsers(userName=self._fdn.__user__)

    def _initWidgets(self):
        """
        Init dialog widgets
        """
        super(ProjectSettings, self)._initWidgets()
        self.setWindowTitle("%s | %s" % (self.log.title, self._fdn.__user__))
        #--- Project ---#
        self.wg_watchers = users.Users(self, settingsMode='project')
        #--- Refresh ---#
        widgets = [self.wg_watchers]
        for widget in widgets:
            widget.setVisible(False)
            self.vl_settingsWidget.addWidget(widget)

    @property
    def category(self):
        """
        Get settings category

        :return: Category datas
        :rtype: dict
        """
        return {0: self.projectCategory}

    @property
    def projectCategory(self):
        """
        Get Project category

        :return: Project category
        :rtype: dict
        """
        return {'project': {'code': 'project',
                            'label': 'Project',
                            'subCat': {0: {'watchers': {'widget': self.wg_watchers,
                                                        'code': 'watchers',
                                                        'label': 'Watchers'}},
                                       1: {'contexts': {'widget': None,
                                                        'code': 'contexts',
                                                        'label': 'Contexts'}}}}}

    def getEditedItems(self):
        """
        Get edited subCategory items

        :return: Edited subCategory items
        :rtype: list
        """
        editedItems = []
        for item in pQt.getAllItems(self.tw_category):
            if item.itemType == 'subCategory':
                if item.itemWidget is not None:
                    if item.itemWidget.__edited__:
                        editedItems.append(item)
        return editedItems

    def rf_editedItemStyle(self):
        """
        Refresh catecory style
        """
        for item in pQt.getAllItems(self.tw_category):
            if item.itemType == 'subCategory':
                if item in self.getEditedItems():
                    item.setFont(0, self.editedSubCategoryFont)
                    item.setTextColor(0, QtGui.QColor(100, 150, 255))
                else:
                    item.setFont(0, QtGui.QFont())
                    item.setTextColor(0, QtGui.QColor(220, 220, 220))

    def on_category(self):
        """
        Command launched when 'Category' tree item widget is clicked

        Update category settings
        """
        super(ProjectSettings, self).on_category()
        selItems = self.tw_category.selectedItems() or []
        #--- Build Tree ---#
        if selItems:
            if hasattr(selItems[0], 'itemWidget'):
                if selItems[0].itemWidget is not None:
                    if not selItems[0].itemWidget.__edited__:
                        selItems[0].itemWidget._initWidget()
                    selItems[0].itemWidget.buildTree()

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save settings to disk
        """
        super(ProjectSettings, self).on_save()
        #--- Parse Edited Items ---#
        for item in self.getEditedItems():
            self.log.detail("---> %s | %s" % (item.parent().itemCode, item.itemCode))
            item.itemWidget.on_save()
            item.itemWidget.__edited__ = False
        #--- Write Project Settings ---#
        self._project.writeProject()
        #--- Refresh ---#
        self.rf_editedItemStyle()

    def on_close(self):
        """
        Command launched when 'Close' QPushButton is clicked

        Close settings ui
        """
        self.log.debug("#--- Close Dialog ---#")
        editedItems = self.getEditedItems()
        #--- Edited Widget Found ---#
        if editedItems:
            message = ["!!! Warning !!!",
                       "Unsaved category detected:"]
            for item in editedItems:
                message.append("---> %s" % item.itemLabel)
            self.cd_close = confirmUi.Confirm(message='\n'.join(message), buttons=['Save', 'Discard'],
                                              btnCmds=[self._saveSettings, self._discardSettings])
            self.cd_close.setStyleSheet(self.parent().styleSheet())
            self.cd_close.exec_()
        #--- Close Settings ---#
        else:
            self.close()

    def _saveSettings(self):
        """
        Save action confirmed
        """
        self.on_save()
        self.cd_close.close()
        self.close()

    def _discardSettings(self):
        """
        Discard action confirmed
        """
        for item in self.getEditedItems():
            item.itemWidget.on_discard()
        self._project.loadProject(self._project.project)
        self.cd_close.close()
        self.close()
