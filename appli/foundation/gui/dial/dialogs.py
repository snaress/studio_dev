import os
import stg_userGroups, stg_contexts
from coreQt import pQt
from coreSys import pFile
from PyQt4 import QtGui, QtCore
from coreQt.dialogs import confirmUi, settingsUi
from foundation.gui._ui import newProjectUI, loadProjectUI


class NewProject(QtGui.QDialog, newProjectUI.Ui_dial_newProject):
    """
    NewProject Dialog: Project creation, child of FoundationUi

    :param mainUi: Parent Ui
    :type mainUi: ..foundationUi.Foundation
    """

    def __init__(self, mainUi):
        super(NewProject, self).__init__(mainUi)
        self.mainUi = mainUi
        #--- Core ---#
        self.log = self.mainUi.log
        self._fdn = self.mainUi._fdn
        self._project = self._fdn._project
        #--- Icons ---#
        self.iconSave = QtGui.QIcon(pFile.conformPath(os.path.join(self.mainUi.__iconPath__, 'png', 'apply.png')))
        self.iconCancel = QtGui.QIcon(pFile.conformPath(os.path.join(self.mainUi.__iconPath__, 'png', 'cancel.png')))
        #--- Setup ---#
        self._setupDial()

    def _setupDial(self):
        """
        Setup NewProject dialog
        """
        self.setupUi(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        #--- Icons ---#
        self.pb_save.setIcon(self.iconSave)
        self.pb_cancel.setIcon(self.iconCancel)
        #--- Connect ---#
        self.pb_save.clicked.connect(self.on_save)
        self.pb_cancel.clicked.connect(self.close)

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Create New Project
        """
        self.log.detail(">>> Save New Project Dialog")
        projectName = str(self.le_projectName.text())
        projectCode = str(self.le_projectCode.text())
        #--- Check Values ---#
        exclusions = ['', ' ', 'None', None]
        if projectName in exclusions or projectCode in exclusions:
            pQt.errorDialog("Project Name or Project Code invalide: %s--%s" % (projectName, projectCode), self)
        else:
            #--- Create Project ---#
            self._project.newProject(projectName, projectCode)
            self.close()


class LoadProject(QtGui.QDialog, loadProjectUI.Ui_Dialog):
    """
    LoadProject Dialog: Project load, child of FoundationUi

    :param mainUi: Parent Ui
    :type mainUi: ..foundationUi.Foundation
    """

    def __init__(self, mainUi):
        super(LoadProject, self).__init__(mainUi)
        self.mainUi = mainUi
        #--- Core ---#
        self.log = self.mainUi.log
        self._fdn = self.mainUi._fdn
        self._users = self._fdn._users
        self._groups = self._fdn._groups
        self._project = self._fdn._project
        #--- Icons ---#
        self.iconStore = QtGui.QIcon(pFile.conformPath(os.path.join(self.mainUi.__iconPath__, 'png', 'pinGreen.png')))
        self.iconRemove = QtGui.QIcon(pFile.conformPath(os.path.join(self.mainUi.__iconPath__, 'png', 'del.png')))
        self.iconRefresh = QtGui.QIcon(pFile.conformPath(os.path.join(self.mainUi.__iconPath__, 'png', 'refresh.png')))
        self.iconLoad = QtGui.QIcon(pFile.conformPath(os.path.join(self.mainUi.__iconPath__, 'png', 'apply.png')))
        self.iconCancel = QtGui.QIcon(pFile.conformPath(os.path.join(self.mainUi.__iconPath__, 'png', 'cancel.png')))
        #--- Setup ---#
        self._setupDial()

    def _setupDial(self):
        """
        Setup LoadProject dialog
        """
        self.setupUi(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.tw_allProjects.setHeaderHidden(False)
        self.tw_myProjects.setHeaderHidden(False)
        #--- Icons ---#
        self.pb_store.setIcon(self.iconStore)
        self.pb_remove.setIcon(self.iconRemove)
        self.pb_refresh.setIcon(self.iconRefresh)
        self.pb_load.setIcon(self.iconLoad)
        self.pb_cancel.setIcon(self.iconCancel)
        #--- Connect ---#
        self.pb_store.clicked.connect(self.on_storeProject)
        self.pb_remove.clicked.connect(self.on_removeProject)
        self.pb_refresh.clicked.connect(self.on_refresh)
        self.pb_load.clicked.connect(self.on_load)
        self.pb_cancel.clicked.connect(self.close)
        #--- Refresh ---#
        self.buildTree('allProjects')
        self.buildTree('myProjects')

    @property
    def pinedProjects(self):
        """
        Get pined projects from 'My Projects' tree

        :return: Pined projects
        :rtype: list
        """
        projects = []
        for item in pQt.getAllItems(self.tw_myProjects) or []:
            projects.append(item.project)
        return projects

    @staticmethod
    def rf_treeColumns(twTree):
        """
        Refresh tree column size

        :param twTree: Tree to refresh
        :type twTree: QtGui.QTreeWidget
        """
        for n in range(twTree.columnCount()):
            twTree.resizeColumnToContents(n)

    def buildTree(self, treeName):
        """
        Refresh 'Projects' tree

        :param treeName: Tree widget name ('allProjects' or 'myProjects')
        :type treeName: str
        """
        #--- Get Projects ---#
        if treeName == 'allProjects':
            self.log.detail("Build 'All Projects' tree ...")
            projects = self._project.projects
            treeWidget = self.tw_allProjects
        else:
            self.log.detail("Build 'My Projects' tree ...")
            projects = self._users._user.userPinedProjects
            treeWidget = self.tw_myProjects
        #--- Populate Tree ---#
        treeWidget.clear()
        for project in projects:
            projectFile = pFile.conformPath(os.path.join(self._fdn.__projectsPath__, project, '%s.py' % project))
            data = pFile.readDictFile(projectFile)
            newItem = self.new_projectItem(project, data, treeWidget)
            treeWidget.addTopLevelItem(newItem)
        #--- Refresh ---#
        self.rf_treeColumns(treeWidget)
        treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)

    def new_projectItem(self, project, data, twTree):
        """
        Create new project item

        :param project: Project (name--code)
        :type project: str
        :param data: Project Datas
        :type data: dict
        :param twTree: Tree to refresh
        :type twTree: QtGui.QTreeWidget
        :return: Project tree item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        #--- Set Item ---#
        newItem.projectName = project.split('--')[0]
        newItem.projectCode = project.split('--')[1]
        newItem.project = project
        newItem.projectData = data
        newItem.setText(0, newItem.projectName)
        newItem.setText(1, newItem.projectCode)
        #--- Font ---#
        newFont = QtGui.QFont()
        newFont.setItalic(True)
        for n in range(twTree.columnCount()):
            newItem.setTextAlignment(n, 5)
            if not self._fdn.__user__ in data['watchers']:
                newItem.setFont(n, newFont)
                newItem.setTextColor(n, QtGui.QColor(125, 125, 125))
        #--- Result ---#
        return newItem

    def on_storeProject(self):
        """
        Command launched when 'Store Project' QPushButton is clicked

        Store project in 'My Projects'
        """
        self.log.detail(">>> Launch 'Store Project' ...")
        selItems = self.tw_allProjects.selectedItems() or []
        if selItems:
            #--- Check Project ---#
            if selItems[0].project in self.pinedProjects:
                pQt.errorDialog("!!! Project %r already in pinedProjects, Skipp !!!" % selItems[0].project, self)
            else:
                #--- Add Poject ---#
                self._users._user.addPinedProject(selItems[0].project)
                self._users._user.writeFile()
        #--- Refresh ---#
        self.buildTree('myProjects')

    def on_removeProject(self):
        """
        Command launched when 'Remove Project' QPushButton is clicked

        Remove project from 'My Projects'
        """
        self.log.detail(">>> Launch 'remove Project' ...")
        selItems = self.tw_myProjects.selectedItems() or []
        if selItems:
            #--- Check Project ---#
            if selItems[0].project not in self.pinedProjects:
                pQt.errorDialog("!!! Project %r not found, Skipp !!!" % selItems[0].project, self)
            else:
                #--- Remove Poject ---#
                self._users._user.delPinedProject(selItems[0].project)
                self._users._user.writeFile()
        #--- Refresh ---#
        self.buildTree('myProjects')

    def on_refresh(self):
        """
        Command launched when 'Refresh' QPushButton is clicked

        Refresh project list
        """
        self.log.detail(">>> Launch 'Refresh' ...")
        self.buildTree('myProjects')

    def on_load(self):
        """
        Command launched when 'Load' QPushButton is clicked

        Load selected project
        """
        self.log.detail(">>> Launch 'Load Project' ...")
        #--- Get Selected Project ---#
        if self.tabWidget.currentIndex() == 0:
            selItems = self.tw_allProjects.selectedItems() or []
        else:
            selItems = self.tw_myProjects.selectedItems() or []
        #--- Load Project ---#
        if selItems:
            userName = self._fdn.__user__
            if not self._fdn.__user__ in selItems[0].projectData['watchers']:
                pQt.errorDialog("User %r is not set as projectUser in %s !" % (userName, selItems[0].project), self)
            else:
                self.mainUi.loadProject(project=selItems[0].project)
                self.close()


class ToolSettings(settingsUi.Settings):
    """
    ToolSettings Dialog: Contains Foundation tool settings, child of FoundationUi

    :param fdnObj: Foundation core object
    :type fdnObj: foundation.core.Foundation
    :param parent: Parent Ui
    :type parent: foundationUi.FoundationUi
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
        self.wg_groups = stg_userGroups.Groups(self)
        self.wg_users = stg_userGroups.Users(self, settingsMode='tool')
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
    ProjectSettings Dialog: Contains Foundation project settings, child of FoundationUi

    :param fdnObj: Foundation core object
    :type fdnObj: foundation.core.Foundation
    :param parent: Parent Ui
    :type parent: foundationUi.FoundationUi
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
        self.wg_watchers = stg_userGroups.Users(self, settingsMode='project')
        self.wg_contexts = stg_contexts.Contexts(self)
        #--- Refresh ---#
        for widget in [self.wg_watchers, self.wg_contexts]:
            widget.setVisible(False)
            self.vl_settingsWidget.addWidget(widget)

    @property
    def category(self):
        """
        Get settings category

        :return: Category datas
        :rtype: dict
        """
        return {0: self.projectCategory,
                1: self.entitiesCategory}

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
                                       1: {'contexts': {'widget': self.wg_contexts,
                                                        'code': 'contexts',
                                                        'label': 'Contexts'}}}}}

    @property
    def entitiesCategory(self):
        """
        Get Entities category

        :return: Entities category
        :rtype: dict
        """
        return {'entities': {'code': 'entities',
                             'label': 'Entities',
                             'subCat': {0: {'assets': {'widget': None,
                                                       'code': 'assets',
                                                       'label': 'Assets'}},
                                        1: {'shots': {'widget': None,
                                                      'code': 'shots',
                                                      'label': 'Shots'}}}}}

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
