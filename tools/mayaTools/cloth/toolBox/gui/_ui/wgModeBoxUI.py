# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\cloth\toolBox\gui\_src\wgModeBox.ui'
#
# Created: Sat Apr 09 05:52:03 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_wg_modeBox(object):
    def setupUi(self, wg_modeBox):
        wg_modeBox.setObjectName(_fromUtf8("wg_modeBox"))
        wg_modeBox.resize(269, 493)
        self.gridLayout = QtGui.QGridLayout(wg_modeBox)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gl_modeCmds = QtGui.QGridLayout()
        self.gl_modeCmds.setMargin(2)
        self.gl_modeCmds.setSpacing(2)
        self.gl_modeCmds.setObjectName(_fromUtf8("gl_modeCmds"))
        self.pb_createOutMesh = QtGui.QPushButton(wg_modeBox)
        self.pb_createOutMesh.setEnabled(True)
        self.pb_createOutMesh.setIconSize(QtCore.QSize(24, 24))
        self.pb_createOutMesh.setFlat(False)
        self.pb_createOutMesh.setObjectName(_fromUtf8("pb_createOutMesh"))
        self.gl_modeCmds.addWidget(self.pb_createOutMesh, 3, 1, 1, 1)
        self.pb_symmetrizePose = QtGui.QPushButton(wg_modeBox)
        self.pb_symmetrizePose.setEnabled(True)
        self.pb_symmetrizePose.setIconSize(QtCore.QSize(24, 24))
        self.pb_symmetrizePose.setFlat(False)
        self.pb_symmetrizePose.setObjectName(_fromUtf8("pb_symmetrizePose"))
        self.gl_modeCmds.addWidget(self.pb_symmetrizePose, 3, 0, 1, 1)
        self.pb_updateOutMesh = QtGui.QPushButton(wg_modeBox)
        self.pb_updateOutMesh.setIconSize(QtCore.QSize(24, 24))
        self.pb_updateOutMesh.setFlat(False)
        self.pb_updateOutMesh.setObjectName(_fromUtf8("pb_updateOutMesh"))
        self.gl_modeCmds.addWidget(self.pb_updateOutMesh, 4, 1, 1, 1)
        self.pb_duplicateSelected = QtGui.QPushButton(wg_modeBox)
        self.pb_duplicateSelected.setIconSize(QtCore.QSize(24, 24))
        self.pb_duplicateSelected.setFlat(False)
        self.pb_duplicateSelected.setObjectName(_fromUtf8("pb_duplicateSelected"))
        self.gl_modeCmds.addWidget(self.pb_duplicateSelected, 0, 0, 1, 1)
        self.pb_duplicateGeom = QtGui.QPushButton(wg_modeBox)
        self.pb_duplicateGeom.setEnabled(True)
        self.pb_duplicateGeom.setIconSize(QtCore.QSize(24, 24))
        self.pb_duplicateGeom.setFlat(False)
        self.pb_duplicateGeom.setObjectName(_fromUtf8("pb_duplicateGeom"))
        self.gl_modeCmds.addWidget(self.pb_duplicateGeom, 0, 1, 1, 1)
        self.pb_connectOutMesh = QtGui.QPushButton(wg_modeBox)
        self.pb_connectOutMesh.setIconSize(QtCore.QSize(24, 24))
        self.pb_connectOutMesh.setFlat(False)
        self.pb_connectOutMesh.setObjectName(_fromUtf8("pb_connectOutMesh"))
        self.gl_modeCmds.addWidget(self.pb_connectOutMesh, 4, 0, 1, 1)
        self.pb_decoupeMesh = QtGui.QPushButton(wg_modeBox)
        self.pb_decoupeMesh.setIconSize(QtCore.QSize(24, 24))
        self.pb_decoupeMesh.setFlat(False)
        self.pb_decoupeMesh.setObjectName(_fromUtf8("pb_decoupeMesh"))
        self.gl_modeCmds.addWidget(self.pb_decoupeMesh, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gl_modeCmds, 3, 0, 1, 1)
        self.line = QtGui.QFrame(wg_modeBox)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.line_2 = QtGui.QFrame(wg_modeBox)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.gl_modeTools = QtGui.QGridLayout()
        self.gl_modeTools.setMargin(2)
        self.gl_modeTools.setSpacing(2)
        self.gl_modeTools.setObjectName(_fromUtf8("gl_modeTools"))
        self.pb_displayColorUi = QtGui.QPushButton(wg_modeBox)
        self.pb_displayColorUi.setIconSize(QtCore.QSize(24, 24))
        self.pb_displayColorUi.setFlat(False)
        self.pb_displayColorUi.setObjectName(_fromUtf8("pb_displayColorUi"))
        self.gl_modeTools.addWidget(self.pb_displayColorUi, 0, 0, 1, 1)
        self.pb_empty = QtGui.QPushButton(wg_modeBox)
        self.pb_empty.setEnabled(False)
        self.pb_empty.setIconSize(QtCore.QSize(24, 24))
        self.pb_empty.setFlat(False)
        self.pb_empty.setObjectName(_fromUtf8("pb_empty"))
        self.gl_modeTools.addWidget(self.pb_empty, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gl_modeTools, 1, 0, 1, 1)
        self.line_3 = QtGui.QFrame(wg_modeBox)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 0, 0, 1, 1)

        self.retranslateUi(wg_modeBox)
        QtCore.QMetaObject.connectSlotsByName(wg_modeBox)

    def retranslateUi(self, wg_modeBox):
        wg_modeBox.setWindowTitle(_translate("wg_modeBox", "Modeling Box", None))
        self.pb_createOutMesh.setText(_translate("wg_modeBox", "Create OutMesh", None))
        self.pb_symmetrizePose.setText(_translate("wg_modeBox", "Symmetrize Pose", None))
        self.pb_updateOutMesh.setText(_translate("wg_modeBox", "Update OutMesh", None))
        self.pb_duplicateSelected.setText(_translate("wg_modeBox", "Duplicate Selected", None))
        self.pb_duplicateGeom.setText(_translate("wg_modeBox", "Duplicate Geom", None))
        self.pb_connectOutMesh.setText(_translate("wg_modeBox", "Connect OutMesh", None))
        self.pb_decoupeMesh.setText(_translate("wg_modeBox", "Decoupe Mesh", None))
        self.pb_displayColorUi.setText(_translate("wg_modeBox", "Display Color UI", None))
        self.pb_empty.setText(_translate("wg_modeBox", "Empty", None))

