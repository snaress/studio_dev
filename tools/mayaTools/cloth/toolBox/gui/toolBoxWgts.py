import os
import toolBoxCmds
from PyQt4 import QtGui
from _ui import wgModeBoxUI, wgRiggBoxUI


class ModeBox(QtGui.QWidget, wgModeBoxUI.Ui_wg_modeBox):
    """
    Widget ModeBox, child of mainUi. Contains all modeling tools

    :param mainUi: Cloth toolBox mainUi
    :type mainUi: toolBoxUi.ToolBox()
    """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.log = self.mainUi.log
        self.log.debug("---> Init Mode Tools ...")
        self.iconPath = self.mainUi.__iconPath__
        super(ModeBox, self).__init__()
        self._setupWidget()

    # noinspection PyUnresolvedReferences
    def _setupWidget(self):
        """
        Setup widget
        """
        self.setupUi(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        #--- Icons ---#
        self.pb_displayColorUi.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'tool', 'displayColor.png')))
        self.pb_duplicateSelected.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'maya', 'duplicateSelected.png')))
        self.pb_duplicateGeom.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'maya', 'duplicateGeom.png')))
        self.pb_decoupeMesh.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'maya', 'decoupe.png')))
        self.pb_symmetrizePose.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'maya', 'symmetry.png')))
        self.pb_createOutMesh.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'maya', 'outMeshCreate.png')))
        self.pb_connectOutMesh.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'maya', 'outMeshConnect.png')))
        self.pb_updateOutMesh.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'maya', 'outMeshUpdate.png')))
        #--- Connect ---#
        self.pb_displayColorUi.clicked.connect(self.on_displayColorUi)
        self.pb_duplicateSelected.clicked.connect(self.on_duplicateSelected)
        self.pb_duplicateGeom.clicked.connect(self.on_duplicateGeom)
        self.pb_decoupeMesh.clicked.connect(self.on_decoupeMesh)
        self.pb_symmetrizePose.clicked.connect(self.on_symmetrizePose)
        self.pb_createOutMesh.clicked.connect(self.on_createOutMesh)
        self.pb_connectOutMesh.clicked.connect(self.on_connectOutMesh)
        self.pb_updateOutMesh.clicked.connect(self.on_updateOutMesh)

    @staticmethod
    def on_displayColorUi():
        """
        Command launched when 'Display Color Ui' QPushButton is clicked

        Launch tool DisplayColor
        """
        toolBoxCmds.launchDisplayColorUi()

    @staticmethod
    def on_duplicateSelected():
        """
        Command launched when 'Duplicate Selected' QPushButton is clicked

        Duplicate selected mesh
        """
        toolBoxCmds.duplicateSelected()

    @staticmethod
    def on_duplicateGeom():
        """
        Command launched when 'Duplicate Geom' QPushButton is clicked

        Duplicate selected mesh via outMesh / inMesh
        """
        toolBoxCmds.duplicateGeom()

    @staticmethod
    def on_decoupeMesh():
        """
        Command launched when 'Decoupe Mesh' QPushButton is clicked

        Extract selected faces
        """
        toolBoxCmds.decoupeMesh()

    @staticmethod
    def on_symmetrizePose():
        """
        Command launched when 'Symmetrize Pose' QPushButton is clicked

        Symmetrize selected pose
        """
        toolBoxCmds.symmetrizePose()

    @staticmethod
    def on_createOutMesh():
        """
        Command launched when 'Create OutMesh' QPushButton is clicked

        Create outMesh from selected objects
        """
        toolBoxCmds.createOutMesh()

    @staticmethod
    def on_connectOutMesh():
        """
        Command launched when 'Connect OutMesh' QPushButton is clicked

        Connect srcMesh.worldMesh to outMesh.inMesh
        """
        toolBoxCmds.connectOutMesh()

    @staticmethod
    def on_updateOutMesh():
        """
        Command launched when 'Update OutMesh' QPushButton is clicked

        Update given outMesh, then remove connection
        """
        toolBoxCmds.updateOutMesh()


class RiggBox(QtGui.QWidget, wgRiggBoxUI.Ui_wg_riggBox):
    """
    Widget ModeBox, child of mainUi. Contains all modeling tools

    :param mainUi: Cloth toolBox mainUi
    :type mainUi: toolBoxUi.ToolBox()
    """

    def __init__(self, mainUi):
        self.mainUi = mainUi
        self.log = self.mainUi.log
        self.log.debug("---> Init Rigg Tools ...")
        self.iconPath = self.mainUi.__iconPath__
        super(RiggBox, self).__init__()
        self._setupWidget()

    # noinspection PyUnresolvedReferences
    def _setupWidget(self):
        """
        Setup widget
        """
        self.setupUi(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        #--- Icons ---#
        self.pb_riggerUi.setIcon(QtGui.QIcon(os.path.join(self.iconPath, 'tool', 'riggerCloth.png')))
        #--- Connect ---#
        self.pb_riggerUi.clicked.connect(self.on_riggerUi)

    @staticmethod
    def on_riggerUi():
        """
        Command launched when 'Rigger Ui' QPushButton is clicked

        Launch tool Rigger
        """
        toolBoxCmds.launchRiggerUi()
