# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\libs\coreQt\dialogs\_src\dial_prompt.ui'
#
# Created: Sat Feb 27 17:24:07 2016
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

class Ui_dial_prompt(object):
    def setupUi(self, dial_prompt):
        dial_prompt.setObjectName(_fromUtf8("dial_prompt"))
        dial_prompt.resize(397, 121)
        self.gridLayout = QtGui.QGridLayout(dial_prompt)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(dial_prompt)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        self.hl_buttons = QtGui.QHBoxLayout()
        self.hl_buttons.setSpacing(0)
        self.hl_buttons.setObjectName(_fromUtf8("hl_buttons"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_buttons.addItem(spacerItem)
        self.pb_save = QtGui.QPushButton(dial_prompt)
        self.pb_save.setMinimumSize(QtCore.QSize(60, 0))
        self.pb_save.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_save.setAutoDefault(True)
        self.pb_save.setFlat(False)
        self.pb_save.setObjectName(_fromUtf8("pb_save"))
        self.hl_buttons.addWidget(self.pb_save)
        self.pb_cancel = QtGui.QPushButton(dial_prompt)
        self.pb_cancel.setMinimumSize(QtCore.QSize(60, 0))
        self.pb_cancel.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_cancel.setAutoDefault(True)
        self.pb_cancel.setFlat(False)
        self.pb_cancel.setObjectName(_fromUtf8("pb_cancel"))
        self.hl_buttons.addWidget(self.pb_cancel)
        self.gridLayout.addLayout(self.hl_buttons, 5, 0, 1, 1)
        self.l_title = QtGui.QLabel(dial_prompt)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.l_title.setFont(font)
        self.l_title.setAlignment(QtCore.Qt.AlignCenter)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self.gridLayout.addWidget(self.l_title, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(dial_prompt)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.line_3 = QtGui.QFrame(dial_prompt)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 4, 0, 1, 1)
        self.tw_prompts = QtGui.QTreeWidget(dial_prompt)
        self.tw_prompts.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
        self.tw_prompts.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tw_prompts.setIndentation(0)
        self.tw_prompts.setItemsExpandable(False)
        self.tw_prompts.setExpandsOnDoubleClick(False)
        self.tw_prompts.setObjectName(_fromUtf8("tw_prompts"))
        self.tw_prompts.headerItem().setText(0, _fromUtf8("1"))
        self.tw_prompts.header().setVisible(False)
        self.gridLayout.addWidget(self.tw_prompts, 3, 0, 1, 1)

        self.retranslateUi(dial_prompt)
        QtCore.QMetaObject.connectSlotsByName(dial_prompt)

    def retranslateUi(self, dial_prompt):
        dial_prompt.setWindowTitle(_translate("dial_prompt", "Prompt Dialog", None))
        self.pb_save.setText(_translate("dial_prompt", "Save", None))
        self.pb_cancel.setText(_translate("dial_prompt", "Cancel", None))
        self.l_title.setText(_translate("dial_prompt", "Title", None))

