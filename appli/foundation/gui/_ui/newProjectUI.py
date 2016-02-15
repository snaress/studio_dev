# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\appli\foundation\gui\_src\newProject.ui'
#
# Created: Sun Feb 14 15:23:04 2016
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

class Ui_dial_newProject(object):
    def setupUi(self, dial_newProject):
        dial_newProject.setObjectName(_fromUtf8("dial_newProject"))
        dial_newProject.resize(318, 97)
        self.gridLayout = QtGui.QGridLayout(dial_newProject)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(dial_newProject)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        self.l_newProject = QtGui.QLabel(dial_newProject)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.l_newProject.setFont(font)
        self.l_newProject.setAlignment(QtCore.Qt.AlignCenter)
        self.l_newProject.setObjectName(_fromUtf8("l_newProject"))
        self.gridLayout.addWidget(self.l_newProject, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(dial_newProject)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.line_3 = QtGui.QFrame(dial_newProject)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 6, 0, 1, 1)
        self.hl_buttons = QtGui.QHBoxLayout()
        self.hl_buttons.setSpacing(0)
        self.hl_buttons.setObjectName(_fromUtf8("hl_buttons"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_buttons.addItem(spacerItem)
        self.pb_save = QtGui.QPushButton(dial_newProject)
        self.pb_save.setMinimumSize(QtCore.QSize(60, 0))
        self.pb_save.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_save.setAutoDefault(True)
        self.pb_save.setFlat(False)
        self.pb_save.setObjectName(_fromUtf8("pb_save"))
        self.hl_buttons.addWidget(self.pb_save)
        self.pb_cancel = QtGui.QPushButton(dial_newProject)
        self.pb_cancel.setMinimumSize(QtCore.QSize(60, 0))
        self.pb_cancel.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_cancel.setAutoDefault(True)
        self.pb_cancel.setFlat(False)
        self.pb_cancel.setObjectName(_fromUtf8("pb_cancel"))
        self.hl_buttons.addWidget(self.pb_cancel)
        self.gridLayout.addLayout(self.hl_buttons, 7, 0, 1, 1)
        self.hl_projectCode = QtGui.QHBoxLayout()
        self.hl_projectCode.setContentsMargins(6, -1, 0, -1)
        self.hl_projectCode.setObjectName(_fromUtf8("hl_projectCode"))
        self.l_projectCode = QtGui.QLabel(dial_newProject)
        self.l_projectCode.setMinimumSize(QtCore.QSize(72, 0))
        self.l_projectCode.setMaximumSize(QtCore.QSize(72, 16777215))
        self.l_projectCode.setObjectName(_fromUtf8("l_projectCode"))
        self.hl_projectCode.addWidget(self.l_projectCode)
        self.le_projectCode = QtGui.QLineEdit(dial_newProject)
        self.le_projectCode.setMouseTracking(False)
        self.le_projectCode.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.le_projectCode.setFrame(False)
        self.le_projectCode.setEchoMode(QtGui.QLineEdit.Normal)
        self.le_projectCode.setObjectName(_fromUtf8("le_projectCode"))
        self.hl_projectCode.addWidget(self.le_projectCode)
        self.gridLayout.addLayout(self.hl_projectCode, 5, 0, 1, 1)
        self.hl_projectName = QtGui.QHBoxLayout()
        self.hl_projectName.setContentsMargins(6, -1, 0, -1)
        self.hl_projectName.setObjectName(_fromUtf8("hl_projectName"))
        self.l_projectName = QtGui.QLabel(dial_newProject)
        self.l_projectName.setMinimumSize(QtCore.QSize(72, 0))
        self.l_projectName.setMaximumSize(QtCore.QSize(72, 16777215))
        self.l_projectName.setObjectName(_fromUtf8("l_projectName"))
        self.hl_projectName.addWidget(self.l_projectName)
        self.le_projectName = QtGui.QLineEdit(dial_newProject)
        self.le_projectName.setMouseTracking(False)
        self.le_projectName.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.le_projectName.setFrame(False)
        self.le_projectName.setEchoMode(QtGui.QLineEdit.Normal)
        self.le_projectName.setObjectName(_fromUtf8("le_projectName"))
        self.hl_projectName.addWidget(self.le_projectName)
        self.gridLayout.addLayout(self.hl_projectName, 3, 0, 1, 1)
        self.line_4 = QtGui.QFrame(dial_newProject)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 4, 0, 1, 1)

        self.retranslateUi(dial_newProject)
        QtCore.QMetaObject.connectSlotsByName(dial_newProject)
        dial_newProject.setTabOrder(self.le_projectName, self.le_projectCode)
        dial_newProject.setTabOrder(self.le_projectCode, self.pb_save)
        dial_newProject.setTabOrder(self.pb_save, self.pb_cancel)

    def retranslateUi(self, dial_newProject):
        dial_newProject.setWindowTitle(_translate("dial_newProject", "New Project", None))
        self.l_newProject.setText(_translate("dial_newProject", "New Project", None))
        self.pb_save.setText(_translate("dial_newProject", "Save", None))
        self.pb_cancel.setText(_translate("dial_newProject", "Cancel", None))
        self.l_projectCode.setText(_translate("dial_newProject", "Project Code: ", None))
        self.l_projectName.setText(_translate("dial_newProject", "Project Name: ", None))

