import sys
from coreQt import pQt
from PyQt4 import QtGui
from foundation_old import gui
from functools import partial
from coreSys import pFile, env
from coreQt.dialogs import promptMultiUi

#--- Compile Ui ---#
gui.compileUi()
from dial import dialogs
from _ui import foundationUI
from widgets import mainTree, infoView
from foundation_old.core import foundation


class FoundationUi(QtGui.QMainWindow, foundationUI.Ui_mw_foundation):
    """
    FoundationUi Class: Contains foundation mainUi

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    """

    log = pFile.Logger(title="FoundationUi")
    __iconPath__ = env.iconsPath

    def __init__(self, logLvl='info'):
        self.log.level = logLvl
        self.log.info("########## Launching Foundation Ui ##########", newLinesBefore=1)
        self._fdn = foundation.Foundation(logLvl=self.log.level)
        super(FoundationUi, self).__init__()
        self._setupUi()

    def _setupUi(self):
        """
        Setup main Ui
        """
        self.log.debug("#===== Setup Foundation Ui =====#", newLinesBefore=1)
        self.setupUi(self)
        #--- MenuItem Fonts ---#
        self.enableFont = QtGui.QFont()
        self.disableFont = QtGui.QFont()
        self.disableFont.setItalic(True)
        #--- Refresh ---#
        self._initMainUi()
        self._initWidgets()
        self._initMenu()
        self.rf_menuVisibility()

    def _initMainUi(self):
        """
        Init main ui window
        """
        self.setWindowTitle("Foundation | %s" % self._fdn.__user__)
        self.resize(1200, 800)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.qf_left.setVisible(False)
        self.qf_dataDn.setVisible(False)

    def _initWidgets(self):
        """
        Init main ui widgets
        """
        self.wg_mainTree = mainTree.MainTree(self)
        self.vl_treeDn.addWidget(self.wg_mainTree)
        self.wg_infoView = infoView.InfoView(self)
        self.vl_data.addWidget(self.wg_infoView)

    def _initMenu(self):
        """
        Init main ui menus
        """
        #--- Menu Project ---#
        self.mi_newProject.setShortcut("Ctrl+Shift+N")
        self.mi_newProject.triggered.connect(self.on_miNewProject)
        self.mi_loadProject.setShortcut("Ctrl+Shift+L")
        self.mi_loadProject.triggered.connect(self.on_miLoadProject)
        self.mi_refresh.setShortcut("F5")
        self.mi_refresh.triggered.connect(partial(self.on_miRefresh, selItem=None))
        #--- Menu Settings ---#
        self.mi_toolSettings.setShortcut("Ctrl+Shift+T")
        self.mi_toolSettings.triggered.connect(self.on_miToolSettings)
        self.mi_projectSettings.setShortcut("Ctrl+Shift+P")
        self.mi_projectSettings.triggered.connect(self.on_miProjectSettings)
        #--- Menu Help ---#
        #- Log Level
        for level in self.log.levels:
            menuItem = self.m_logLevel.addAction(level)
            menuItem.setCheckable(True)
            menuItem.triggered.connect(partial(self.on_miLogLevel, level))
        self.on_miLogLevel(self.log.level)
        #- Style
        for style in pQt.Style().styles:
            menuItem = self.m_style.addAction(style)
            menuItem.setCheckable(True)
            menuItem.triggered.connect(partial(self.on_miStyle, style))
        self.on_miStyle('darkGrey')

    @property
    def typoExclusion(self):
        """
        Typo results that must not be found

        :return: Typo exclusion
        :rtype: list
        """
        return self._fdn.typoExclusion

    @property
    def showToolTips(self):
        """
        Get 'Tool Tips' menuItem status

        :return: 'Tool Tips' status
        :rtype: bool
        """
        return self.mi_toolTips.isChecked()

    @property
    def currentStyle(self):
        """
        Get current ui style

        :return: Current style
        :rtype: str
        """
        style = 'default'
        for menuItem in self.m_style.children():
            if menuItem.isChecked():
                style = str(menuItem.text())
        return style

    @property
    def currentInfoTab(self):
        """
        Get info view active tab

        :return: Active tab
        :rtype: str
        """
        return self.wg_infoView.tab_infoView.tabText(self.wg_infoView.tab_infoView.currentIndex())

    def rf_menuVisibility(self):
        """
        Refresh menuItem visibility considering user grade
        """
        #-- Project Settings --#
        if self._fdn._project.project is None:
            self._editMenuVisibility(self.mi_projectSettings, state=False)
        else:
            self._editMenuVisibility(self.mi_projectSettings, state=True)
        #-- Grade 1 --#
        for menuItem in [self.mi_toolSettings]:
            self._editMenuVisibility(menuItem, grade=1)
        #-- Grade 2 --#
        for menuItem in [self.mi_newProject]:
            self._editMenuVisibility(menuItem, grade=2)
        #-- Grade 4 --#
        for menuItem in [self.mi_projectSettings]:
            if self._fdn._project.project is not None:
                self._editMenuVisibility(menuItem, grade=4)

    def _editMenuVisibility(self, menuItem, grade=None, state=None):
        """
        Edit menu item visibility

        :param menuItem: Menu item to edit
        :type menuItem: QMenuAction
        :param grade: Max allowed grade
        :type grade: int
        :param state: Visibility state
        :type state: bool
        """
        #-- Get State And Font --#
        if state is not None:
            if state:
                _font = self.enableFont
            else:
                _font = self.disableFont
        else:
            if self._fdn._users._user.grade <= grade:
                _font = self.enableFont
                state = True
            else:
                _font = self.disableFont
                state = False
        #-- Edit Menu Item --#
        menuItem.setFont(_font)
        menuItem.setEnabled(state)

    def loadProject(self, project=None):
        """
        Load given project. If project is None, load current core project

        :param project: Project (name--code)
        :type project: str
        """
        if project is not None:
            self._fdn._project.loadProject(project)
        self.setWindowTitle("Foundation | %s | %s" % (self._fdn._project.project, self._fdn.__user__))
        self.rf_menuVisibility()
        self.qf_left.setVisible(True)
        #--- Main Tree ---#
        self.wg_mainTree._initWidget()

    def on_miNewProject(self):
        """
        Command launched when 'New Project' QMenuItem is triggered

        Launch NewProject dialog
        """
        self.log.detail(">>> Launch 'New Project' ...")
        #--- Get Prompts ---#
        prompts = [dict(promptType='line', promptLabel='projectName'),
                   dict(promptType='line', promptLabel='projectCode')]
        #--- Launch Dialog ---#
        self.dial_newProject = promptMultiUi.PromptMulti(title="New Project", prompts=prompts, parent=self,
                                                         acceptCmd=self.on_dialNewProject)
        self.dial_newProject.exec_()

    def on_dialNewProject(self):
        """
        Command launched when 'Save' dialog QPushButton is clicked

        Save newProject
        """
        self.log.detail(">>> Save 'New Project' ...")
        result = self.dial_newProject.result()
        projectName = result.get('projectName')
        projectCode = result.get('projectCode')
        #--- Check Values ---#
        if projectName in self.typoExclusion or projectCode in self.typoExclusion:
            pQt.errorDialog("Project Name or Project Code invalide: %s--%s" % (projectName, projectCode), self)
        else:
            #--- Create Project ---#
            self._fdn._project.newProject(projectName, projectCode)
            self.dial_newProject.close()

    def on_miLoadProject(self):
        """
        Command launched when 'Load Project' QMenuItem is triggered

        Launch LoadProject dialog
        """
        self.log.detail(">>> Launch 'Load Project' ...")
        dial_loadProject = dialogs.LoadProject(self)
        dial_loadProject.exec_()

    def on_miRefresh(self, selItem=None):
        """
        Command launched when 'Refresh' QMenuItem is clicked

        Refresh ui
        """
        self.wg_mainTree._initWidget()
        self.wg_infoView.refresh()

    def on_miToolSettings(self):
        """
        Command launched when 'Tool Settings' QMenuItem is triggered

        Launch toolSettings dialog
        """
        self.log.detail(">>> Launch 'Tool Settings' ...")
        dial_ts = dialogs.ToolSettings(self._fdn, parent=self)
        dial_ts.exec_()

    def on_miProjectSettings(self):
        """
        Command launched when 'Project Settings' QMenuItem is triggered

        Launch projectSettings dialog
        """
        self.log.detail(">>> Launch 'Project Settings' ...")
        dial_ps = dialogs.ProjectSettings(self._fdn, parent=self)
        dial_ps.exec_()

    def on_miLogLevel(self, logLevel):
        """
        Command launched when 'Log Level' QMenuItem is triggered

        Set ui and core log level
        :param logLevel : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
        :type logLevel: str
        """
        self.log.detail(">>> Launch 'Log Level': %s ..." % logLevel)
        #--- Uncheck All ---#
        for menuItem in self.m_logLevel.children():
            menuItem.setChecked(False)
        #--- Check Given LogLvl ---#
        for menuItem in self.m_logLevel.children():
            if str(menuItem.text()) == logLevel:
                menuItem.setChecked(True)
                break
        #--- Set Log Level ---#
        self.log.level = logLevel
        self._fdn.log.level = logLevel
        self._fdn._groups.log.level = logLevel
        self._fdn._users.log.level = logLevel
        self._fdn._project.log.level = logLevel
        for ctxtObj in self._fdn._project.contexts:
            ctxtObj.log.level = logLevel

    def on_miStyle(self, style):
        """
        Command launched when 'Style' QMenuItem is triggered

        :param style: 'default' or 'darkGrey'
        :type style: str
        """
        self.log.detail(">>> Launch 'Style': %s ..." % style)
        #--- Uncheck All ---#
        for menuItem in self.m_style.children():
            menuItem.setChecked(False)
        #--- Check Given LogLvl ---#
        for menuItem in self.m_style.children():
            if str(menuItem.text()) == style:
                menuItem.setChecked(True)
                break
        #--- Set StyleSheet ---#
        self.setStyleSheet(pQt.Style().getStyle(style))



def launch(project=None, logLvl='info'):
    """
    Foundation launcher

    :param project: Project name (projectName--projectCode)
    :type project: str
    :param logLvl: Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    """
    app = QtGui.QApplication(sys.argv)
    window = FoundationUi(logLvl=logLvl)
    window.show()
    if project is not None:
        window.loadProject(project=project)
    sys.exit(app.exec_())



if __name__ == '__main__':
    # launch(logLvl='detail')
    launch(project='animTest--ANT', logLvl='detail')
