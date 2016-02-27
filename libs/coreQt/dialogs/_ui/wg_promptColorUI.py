# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\libs\coreQt\dialogs\_src\wg_promptColor.ui'
#
# Created: Sat Feb 27 22:31:52 2016
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

class Ui_wg_promptColor(object):
    def setupUi(self, wg_promptColor):
        wg_promptColor.setObjectName(_fromUtf8("wg_promptColor"))
        wg_promptColor.resize(485, 28)
        wg_promptColor.setMinimumSize(QtCore.QSize(100, 0))
        self.gridLayout = QtGui.QGridLayout(wg_promptColor)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(wg_promptColor)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        self.line_2 = QtGui.QFrame(wg_promptColor)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.hl_prompt = QtGui.QHBoxLayout()
        self.hl_prompt.setObjectName(_fromUtf8("hl_prompt"))
        self.l_prompt = QtGui.QLabel(wg_promptColor)
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
        self.l_red = QtGui.QLabel(wg_promptColor)
        self.l_red.setObjectName(_fromUtf8("l_red"))
        self.hl_prompt.addWidget(self.l_red)
        self.sb_colorRed = QtGui.QSpinBox(wg_promptColor)
        self.sb_colorRed.setMinimumSize(QtCore.QSize(30, 0))
        self.sb_colorRed.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_colorRed.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sb_colorRed.setPrefix(_fromUtf8(""))
        self.sb_colorRed.setMaximum(255)
        self.sb_colorRed.setObjectName(_fromUtf8("sb_colorRed"))
        self.hl_prompt.addWidget(self.sb_colorRed)
        spacerItem = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hl_prompt.addItem(spacerItem)
        self.l_green = QtGui.QLabel(wg_promptColor)
        self.l_green.setObjectName(_fromUtf8("l_green"))
        self.hl_prompt.addWidget(self.l_green)
        self.sb_colorGreen = QtGui.QSpinBox(wg_promptColor)
        self.sb_colorGreen.setMinimumSize(QtCore.QSize(30, 0))
        self.sb_colorGreen.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_colorGreen.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sb_colorGreen.setMaximum(255)
        self.sb_colorGreen.setObjectName(_fromUtf8("sb_colorGreen"))
        self.hl_prompt.addWidget(self.sb_colorGreen)
        spacerItem1 = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hl_prompt.addItem(spacerItem1)
        self.l_blue = QtGui.QLabel(wg_promptColor)
        self.l_blue.setObjectName(_fromUtf8("l_blue"))
        self.hl_prompt.addWidget(self.l_blue)
        self.sb_colorBlue = QtGui.QSpinBox(wg_promptColor)
        self.sb_colorBlue.setMinimumSize(QtCore.QSize(30, 0))
        self.sb_colorBlue.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_colorBlue.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.sb_colorBlue.setMaximum(255)
        self.sb_colorBlue.setObjectName(_fromUtf8("sb_colorBlue"))
        self.hl_prompt.addWidget(self.sb_colorBlue)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hl_prompt.addItem(spacerItem2)
        self.pb_color = QtGui.QPushButton(wg_promptColor)
        self.pb_color.setMaximumSize(QtCore.QSize(20, 20))
        self.pb_color.setText(_fromUtf8(""))
        self.pb_color.setAutoDefault(False)
        self.pb_color.setFlat(False)
        self.pb_color.setObjectName(_fromUtf8("pb_color"))
        self.hl_prompt.addWidget(self.pb_color)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_prompt.addItem(spacerItem3)
        self.gridLayout.addLayout(self.hl_prompt, 1, 0, 1, 1)

        self.retranslateUi(wg_promptColor)
        QtCore.QMetaObject.connectSlotsByName(wg_promptColor)

    def retranslateUi(self, wg_promptColor):
        wg_promptColor.setWindowTitle(_translate("wg_promptColor", "Prompt Color", None))
        self.l_prompt.setText(_translate("wg_promptColor", "Prompt Label:", None))
        self.l_red.setText(_translate("wg_promptColor", "R = ", None))
        self.l_green.setText(_translate("wg_promptColor", "G = ", None))
        self.l_blue.setText(_translate("wg_promptColor", "B = ", None))

