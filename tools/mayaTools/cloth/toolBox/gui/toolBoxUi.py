import toolBoxWgts
from PyQt4 import QtGui
from _ui import toolBoxUI
from coreSys import pFile, env
from mayaCore.cmds import pUtil


class ToolBox(QtGui.QMainWindow, toolBoxUI.Ui_mw_toolBox):
    """
    ToolBox class: Cloth toolBox mainUi. Contains cloth dept cmds and tools

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :param parent: Maya main window
    :type parent: QtCore.QObject
    """

    __iconPath__ = pFile.conformPath(env.iconsPath)

    def __init__(self, logLvl='info', parent=None):
        self.log = pFile.Logger(title=self.__class__.__name__, level=logLvl)
        self.log.info("########## Launching %s Ui ##########" % self.__class__.__name__, newLinesBefore=1)
        super(ToolBox, self).__init__(parent)
        self._setupUi()

    def _setupUi(self):
        """
        Setup main ui
        """
        self.log.debug("Setup %s ui ..." % self.__class__.__name__)
        self.setupUi(self)
        #-- Widgets --#
        self.wgModeBox = toolBoxWgts.ModeBox(self)
        self.vl_mode.addWidget(self.wgModeBox)
        self.wgRiggBox = toolBoxWgts.RiggBox(self)
        self.vl_setup.addWidget(self.wgRiggBox)
        # self.wgSimuBox = toolBoxWgts.SimuBox(self)
        # self.vl_simu.addWidget(self.wgSimuBox)


def mayaLaunch(logLvl='info'):
    """
    Tool launcher for maya

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :return: launched tool
    :rtype: ToolBox
    """
    global window
    try:
        window.close()
    except:
        pass
    window = ToolBox(logLvl=logLvl, parent=pUtil.getMayaMainWindow())
    window.show()
    return window
