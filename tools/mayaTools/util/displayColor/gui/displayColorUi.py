from PyQt4 import QtGui
from coreSys import pFile
from mayaCore.cmds import pUtil
from _ui import displayColorUI
import displayColorWgts


class DisplayColor(QtGui.QMainWindow, displayColorUI.Ui_mw_displayColor):
    """
    DisplayColor class: Override display color

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :param parent: Maya main window
    :type parent: QtCore.QObject
    """

    def __init__(self, logLvl='info', parent=None):
        self.log = pFile.Logger(title=self.__class__.__name__, level=logLvl)
        self.log.info("########## Launching %s Ui ##########" % self.__class__.__name__, newLinesBefore=1)
        super(DisplayColor, self).__init__(parent)
        self._setupUi()

    def _setupUi(self):
        """
        Setup ToolManager ui
        """
        self.setupUi(self)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setMargin(0)
        self._initWidgets()
        self.pb_default.clicked.connect(self.on_defaultColor)
        self.pb_override.clicked.connect(self.on_overrideColor)

    def _initWidgets(self):
        """
        Init tool widgets
        """
        self.tw_tree = displayColorWgts.ColorTree(self)
        self.vl_tree.addWidget(self.tw_tree)

    @staticmethod
    def on_defaultColor():
        """
        Command launched when 'Default' QPushButton is clicked

        Restore selected objects color
        """
        pUtil.defaultDisplayColor()

    def on_overrideColor(self):
        """
        Command launched when 'Override' QPushButton is clicked

        Override selected objects color
        """
        cIndex = self.tw_tree.selectedColorIndex
        pUtil.overrideDisplayColor(cIndex)


def mayaLaunch(logLvl='detail', parent=None):
    """
    Launch OverrideColor

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :param parent: Maya main window
    :type parent: QtCore.QObject
    :return: Launched window, Dock layout
    :rtype: OverrideColor, mc.dockControl
    """
    global window
    window, dock = pUtil.launchQtWindow('DisplayColor', 'mw_displayColor', DisplayColor,
                                        toolKwargs=dict(logLvl=logLvl, parent=parent))
    window.show()
    return window, dock
