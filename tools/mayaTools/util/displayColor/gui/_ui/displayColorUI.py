# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\util\displayColor\gui\_src\displayColor.ui'
#
# Created: Fri Apr 08 04:30:21 2016
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
        mw_displayColor.resize(324, 73)
        mw_displayColor.setMinimumSize(QtCore.QSize(324, 73))
        mw_displayColor.setMaximumSize(QtCore.QSize(324, 73))
        self.centralwidget = QtGui.QWidget(mw_displayColor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.vf_tree = QtGui.QFrame(self.centralwidget)
        self.vf_tree.setObjectName(_fromUtf8("vf_tree"))
        self.vl_tree = QtGui.QVBoxLayout(self.vf_tree)
        self.vl_tree.setSpacing(0)
        self.vl_tree.setMargin(0)
        self.vl_tree.setObjectName(_fromUtf8("vl_tree"))
        self.gridLayout.addWidget(self.vf_tree, 1, 0, 1, 1)
        self.hl_buttons = QtGui.QHBoxLayout()
        self.hl_buttons.setSpacing(0)
        self.hl_buttons.setObjectName(_fromUtf8("hl_buttons"))
        self.qf_options = QtGui.QFrame(self.centralwidget)
        self.qf_options.setObjectName(_fromUtf8("qf_options"))
        self.hl_options = QtGui.QHBoxLayout(self.qf_options)
        self.hl_options.setSpacing(8)
        self.hl_options.setContentsMargins(6, 0, 0, 0)
        self.hl_options.setObjectName(_fromUtf8("hl_options"))
        self.l_override = QtGui.QLabel(self.qf_options)
        self.l_override.setMinimumSize(QtCore.QSize(0, 0))
        self.l_override.setMaximumSize(QtCore.QSize(60, 16777215))
        self.l_override.setObjectName(_fromUtf8("l_override"))
        self.hl_options.addWidget(self.l_override)
        self.cb_wire = QtGui.QCheckBox(self.qf_options)
        self.cb_wire.setChecked(True)
        self.cb_wire.setObjectName(_fromUtf8("cb_wire"))
        self.hl_options.addWidget(self.cb_wire)
        self.cb_shader = QtGui.QCheckBox(self.qf_options)
        self.cb_shader.setObjectName(_fromUtf8("cb_shader"))
        self.hl_options.addWidget(self.cb_shader)
        self.hl_buttons.addWidget(self.qf_options)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_buttons.addItem(spacerItem)
        self.pb_default = QtGui.QPushButton(self.centralwidget)
        self.pb_default.setMaximumSize(QtCore.QSize(60, 20))
        self.pb_default.setObjectName(_fromUtf8("pb_default"))
        self.hl_buttons.addWidget(self.pb_default)
        self.pb_override = QtGui.QPushButton(self.centralwidget)
        self.pb_override.setMaximumSize(QtCore.QSize(60, 20))
        self.pb_override.setObjectName(_fromUtf8("pb_override"))
        self.hl_buttons.addWidget(self.pb_override)
        self.gridLayout.addLayout(self.hl_buttons, 5, 0, 1, 1)
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
        self.l_override.setText(_translate("mw_displayColor", "Override:", None))
        self.cb_wire.setText(_translate("mw_displayColor", "Wire", None))
        self.cb_shader.setText(_translate("mw_displayColor", "Shader", None))
        self.pb_default.setText(_translate("mw_displayColor", "Default", None))
        self.pb_override.setText(_translate("mw_displayColor", "Override", None))

