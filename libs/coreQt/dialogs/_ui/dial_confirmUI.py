# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\libs\coreQt\dialogs\_src\dial_confirm.ui'
#
# Created: Sat Feb 13 16:17:11 2016
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

class Ui_dial_confirm(object):
    def setupUi(self, dial_confirm):
        dial_confirm.setObjectName(_fromUtf8("dial_confirm"))
        dial_confirm.resize(430, 78)
        self.gridLayout = QtGui.QGridLayout(dial_confirm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(dial_confirm)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        self.l_message = QtGui.QLabel(dial_confirm)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.l_message.setFont(font)
        self.l_message.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.l_message.setAlignment(QtCore.Qt.AlignCenter)
        self.l_message.setObjectName(_fromUtf8("l_message"))
        self.gridLayout.addWidget(self.l_message, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(dial_confirm)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.hl_buttons = QtGui.QHBoxLayout()
        self.hl_buttons.setObjectName(_fromUtf8("hl_buttons"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_buttons.addItem(spacerItem)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_buttons.addItem(spacerItem1)
        self.gridLayout.addLayout(self.hl_buttons, 3, 0, 1, 1)

        self.retranslateUi(dial_confirm)
        QtCore.QMetaObject.connectSlotsByName(dial_confirm)

    def retranslateUi(self, dial_confirm):
        dial_confirm.setWindowTitle(_translate("dial_confirm", "Dialog", None))
        self.l_message.setText(_translate("dial_confirm", "Message", None))

