import sys
from coreQt import pQt
from PyQt4 import QtGui
from foundation import gui
from coreSystem import pFile
from functools import partial


#--- Compile Ui ---#
gui.compileUi()
from _ui import foundationUI
from foundation.core import foundation

class FoundationUi(QtGui.QMainWindow, foundationUI.Ui_mw_foundation):
    """
    FoundationUi Class: Contains foundation mainUi

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    """

    log = pFile.Logger(title="FoundationUi")

    def __init__(self, logLvl='info'):
        self.log.level = logLvl
        self.log.info("########## Launching Foundation Ui ##########", newLinesBefore=1)
        self.fdn = foundation.Foundation(logLvl=self.log.level)
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
        self._initMenu()

    def _initMainUi(self):
        """
        Init main ui window
        """
        self.setWindowTitle("Foundation | %s" % self.fdn.__user__)
        self.resize(1200, 800)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.qf_left.setVisible(False)
        self.qf_datasDn.setVisible(False)

    def _initMenu(self):
        """
        Init main ui menus
        """
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
    def showToolTips(self):
        """
        Get 'Tool Tips' menuItem status

        :return: 'Tool Tips' status
        :rtype: bool
        """
        return self.mi_toolTips.isChecked()

    def on_miLogLevel(self, logLevel):
        """
        Command launched when 'Log Level' QMenuItem is triggered

        Set ui and core log level
        :param logLevel : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
        :type logLevel: str
        """
        self.log.detail(">>> Launch 'Log Level': %s ..." % logLevel)
        #-- Uncheck All --#
        for menuItem in self.m_logLevel.children():
            menuItem.setChecked(False)
        #-- Check Given LogLvl --#
        for menuItem in self.m_logLevel.children():
            if str(menuItem.text()) == logLevel:
                menuItem.setChecked(True)
                break
        #-- Set Log Level --#
        self.log.level = logLevel
        # self.foundation.log.level = logLevel

    def on_miStyle(self, style):
        """
        Command launched when 'Style' QMenuItem is triggered

        :param style: 'default' or 'darkGrey'
        :type style: str
        """
        self.log.detail(">>> Launch 'Style': %s ..." % style)
        #-- Uncheck All --#
        for menuItem in self.m_style.children():
            menuItem.setChecked(False)
        #-- Check Given LogLvl --#
        for menuItem in self.m_style.children():
            if str(menuItem.text()) == style:
                menuItem.setChecked(True)
                break
        #-- Set StyleSheet --#
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
    launch(logLvl='detail')
