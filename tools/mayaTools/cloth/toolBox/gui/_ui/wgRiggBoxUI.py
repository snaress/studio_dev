# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\cloth\toolBox\gui\_src\wgRiggBox.ui'
#
# Created: Thu Apr 07 02:02:45 2016
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

class Ui_wg_riggBox(object):
    def setupUi(self, wg_riggBox):
        wg_riggBox.setObjectName(_fromUtf8("wg_riggBox"))
        wg_riggBox.resize(269, 493)
        self.gridLayout = QtGui.QGridLayout(wg_riggBox)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line_2 = QtGui.QFrame(wg_riggBox)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.gl_modeCmds = QtGui.QGridLayout()
        self.gl_modeCmds.setMargin(2)
        self.gl_modeCmds.setSpacing(2)
        self.gl_modeCmds.setObjectName(_fromUtf8("gl_modeCmds"))
        self.pb_riggerUi = QtGui.QPushButton(wg_riggBox)
        self.pb_riggerUi.setIconSize(QtCore.QSize(24, 24))
        self.pb_riggerUi.setFlat(False)
        self.pb_riggerUi.setObjectName(_fromUtf8("pb_riggerUi"))
        self.gl_modeCmds.addWidget(self.pb_riggerUi, 0, 0, 1, 1)
        self.pb_duplicateGeom = QtGui.QPushButton(wg_riggBox)
        self.pb_duplicateGeom.setEnabled(False)
        self.pb_duplicateGeom.setIconSize(QtCore.QSize(24, 24))
        self.pb_duplicateGeom.setFlat(False)
        self.pb_duplicateGeom.setObjectName(_fromUtf8("pb_duplicateGeom"))
        self.gl_modeCmds.addWidget(self.pb_duplicateGeom, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gl_modeCmds, 1, 0, 1, 1)
        self.line = QtGui.QFrame(wg_riggBox)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)

        self.retranslateUi(wg_riggBox)
        QtCore.QMetaObject.connectSlotsByName(wg_riggBox)

    def retranslateUi(self, wg_riggBox):
        wg_riggBox.setWindowTitle(_translate("wg_riggBox", "Rigging Box", None))
        self.pb_riggerUi.setText(_translate("wg_riggBox", "Rigger UI", None))
        self.pb_duplicateGeom.setText(_translate("wg_riggBox", "Empty", None))

