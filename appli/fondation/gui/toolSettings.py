from coreQt import pQt
from PyQt4 import QtGui
from dialogs import userGroups
from coreQt.dialogs import settingsUi


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
        #--- Refresh ---#
        for widget in [self.wg_groups]:
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
                                          1: {'users': {'widget': None,
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
