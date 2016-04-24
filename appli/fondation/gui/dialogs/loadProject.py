import os
from coreQt import pQt
from coreSys import pFile
from PyQt4 import QtGui, QtCore
from fondation.gui._ui import loadProjectUI


class LoadProject(QtGui.QDialog, loadProjectUI.Ui_Dialog):
    """
    LoadProject Dialog: Project load, child of FondationUi

    :param mainUi: Parent Ui
    :type mainUi: fondationUi.FondationUi
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
