# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\libs\coreQt\dialogs\_src\wg_promptLine.ui'
#
# Created: Sat Feb 27 17:31:01 2016
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

class Ui_wg_promptLine(object):
    def setupUi(self, wg_promptLine):
        wg_promptLine.setObjectName(_fromUtf8("wg_promptLine"))
        wg_promptLine.resize(490, 28)
        self.gridLayout = QtGui.QGridLayout(wg_promptLine)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(wg_promptLine)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        self.hl_prompt = QtGui.QHBoxLayout()
        self.hl_prompt.setObjectName(_fromUtf8("hl_prompt"))
        self.l_prompt = QtGui.QLabel(wg_promptLine)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_prompt.sizePolicy().hasHeightForWidth())
        self.l_prompt.setSizePolicy(sizePolicy)
        self.l_prompt.setMinimumSize(QtCore.QSize(100, 0))
        self.l_prompt.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.l_prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.l_prompt.setObjectName(_fromUtf8("l_prompt"))
        self.hl_prompt.addWidget(self.l_prompt)
        self.le_prompt = QtGui.QLineEdit(wg_promptLine)
        self.le_prompt.setMouseTracking(False)
        self.le_prompt.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.le_prompt.setFrame(True)
        self.le_prompt.setEchoMode(QtGui.QLineEdit.Normal)
        self.le_prompt.setObjectName(_fromUtf8("le_prompt"))
        self.hl_prompt.addWidget(self.le_prompt)
        self.gridLayout.addLayout(self.hl_prompt, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(wg_promptLine)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)

        self.retranslateUi(wg_promptLine)
        QtCore.QMetaObject.connectSlotsByName(wg_promptLine)

    def retranslateUi(self, wg_promptLine):
        wg_promptLine.setWindowTitle(_translate("wg_promptLine", "Prompt Line", None))
        self.l_prompt.setText(_translate("wg_promptLine", "Prompt Label:", None))

