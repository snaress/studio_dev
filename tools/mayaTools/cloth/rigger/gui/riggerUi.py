import os
from PyQt4 import QtGui
from _ui import riggerUI
from coreSys import pFile, env
from mayaCore.cmds import pUtil


class Rigger(QtGui.QMainWindow, riggerUI.Ui_mw_rigger):
    """
    Rigger class: Cloth rigger mainUi. Contains cloth setup cmds

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :param parent: Maya main window
    :type parent: QtCore.QObject
    """

    __iconPath__ = pFile.conformPath(env.iconsPath)

    def __init__(self, logLvl='info', parent=None):
        self.log = pFile.Logger(title=self.__class__.__name__, level=logLvl)
        self.log.info("########## Launching %s Ui ##########" % self.__class__.__name__, newLinesBefore=1)
        super(Rigger, self).__init__(parent)
        self.iconCloth = QtGui.QIcon(pFile.conformPath(os.path.join(self.__iconPath__, 'maya', 'nCloth.png')))
        self.iconRigid = QtGui.QIcon(pFile.conformPath(os.path.join(self.__iconPath__, 'maya', 'nRigid.png')))
        self.iconConst = QtGui.QIcon(pFile.conformPath(os.path.join(self.__iconPath__, 'maya', 'nConstraint.png')))
        self._setupUi()

    def _setupUi(self):
        """
        Setup main ui
        """
        self.log.debug("Setup %s ui ..." % self.__class__.__name__)
        self.setupUi(self)
        #--- Wraps ---#
        self.gb_initWraps.clicked.connect(self.rf_initWraps)
        self.pb_hiToDecoupe.setToolTip("Select driver Hi mesh, then slave cutted loS mesh.")
        self.pb_losToDecoupe.setToolTip("Select slave loS mesh component, then slave cutted loS mesh.")
        #--- nCloth ---#
        self.le_clothMesh.wgResult = self.le_clothResult
        self.pb_createCloth.setIcon(self.iconCloth)
        #--- nRigid ---#
        self.le_rigidMesh.wgResult = self.le_rigidResult
        self.pb_createRigid.setIcon(self.iconRigid)
        #--- nConstraint ---#
        self.le_constraint.wgResult = self.le_constResult
        self.pb_storeConst.setIcon(self.iconConst)
        #--- Refresh ---#
        self.rf_initWraps()

    @property
    def clothSolver(self):
        """
        Get current cloth solver

        :return: Cloth solver
        :rtype: str
        """
        return str(self.cb_clothSolver.currentText())

    @property
    def rigidSolver(self):
        """
        Get current rigid solver

        :return: Rigid solver
        :rtype: str
        """
        return str(self.cb_rigidSolver.currentText())

    @property
    def passiveMode(self):
        """
        Get current passive mode

        :return: Passive mode ('collide', 'pushOut', 'passive')
        :rtype: str
        """
        if self.rb_collide.isChecked():
            return "collide"
        elif self.rb_pushOut.isChecked():
            return "pushOut"
        elif self.rb_passive.isChecked():
            return "passive"

    def rf_initWraps(self):
        """
        Refresh 'Init Wraps' QGroupBox visibility
        """
        if self.gb_initWraps.isChecked():
            self.gb_initWraps.setMaximumHeight(55)
        else:
            self.gb_initWraps.setMaximumHeight(15)


def mayaLaunch(logLvl='info'):
    """
    Tool launcher for maya

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :return: launched tool
    :rtype: Rigger
    """
    global window
    try:
        window.close()
    except:
        pass
    window = Rigger(logLvl=logLvl, parent=pUtil.getMayaMainWindow())
    window.show()
    return window
