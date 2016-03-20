# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\util\displayColor\gui\_src\displayColor.ui'
#
# Created: Sun Mar 20 22:07:14 2016
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

class Ui_mw_displayColor(object):
    def setupUi(self, mw_displayColor):
        mw_displayColor.setObjectName(_fromUtf8("mw_displayColor"))
        mw_displayColor.resize(324, 75)
        mw_displayColor.setMinimumSize(QtCore.QSize(324, 75))
        mw_displayColor.setMaximumSize(QtCore.QSize(324, 75))
        self.centralwidget = QtGui.QWidget(mw_displayColor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hl_buttons = QtGui.QHBoxLayout()
        self.hl_buttons.setSpacing(0)
        self.hl_buttons.setObjectName(_fromUtf8("hl_buttons"))
        self.pb_default = QtGui.QPushButton(self.centralwidget)
        self.pb_default.setObjectName(_fromUtf8("pb_default"))
        self.hl_buttons.addWidget(self.pb_default)
        self.pb_override = QtGui.QPushButton(self.centralwidget)
        self.pb_override.setObjectName(_fromUtf8("pb_override"))
        self.hl_buttons.addWidget(self.pb_override)
        self.gridLayout.addLayout(self.hl_buttons, 3, 0, 1, 1)
        self.vf_tree = QtGui.QFrame(self.centralwidget)
        self.vf_tree.setObjectName(_fromUtf8("vf_tree"))
        self.vl_tree = QtGui.QVBoxLayout(self.vf_tree)
        self.vl_tree.setSpacing(0)
        self.vl_tree.setMargin(0)
        self.vl_tree.setObjectName(_fromUtf8("vl_tree"))
        self.gridLayout.addWidget(self.vf_tree, 1, 0, 1, 1)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        mw_displayColor.setCentralWidget(self.centralwidget)

        self.retranslateUi(mw_displayColor)
        QtCore.QMetaObject.connectSlotsByName(mw_displayColor)

    def retranslateUi(self, mw_displayColor):
        mw_displayColor.setWindowTitle(_translate("mw_displayColor", "Display Color", None))
        self.pb_default.setText(_translate("mw_displayColor", "Default", None))
        self.pb_override.setText(_translate("mw_displayColor", "Override", None))

