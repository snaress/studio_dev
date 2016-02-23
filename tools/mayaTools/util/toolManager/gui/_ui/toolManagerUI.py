# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\util\toolManager\gui\_src\toolManager.ui'
#
# Created: Tue Feb 23 03:28:44 2016
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

class Ui_mw_toolManager(object):
    def setupUi(self, mw_toolManager):
        mw_toolManager.setObjectName(_fromUtf8("mw_toolManager"))
        mw_toolManager.resize(423, 600)
        self.centralwidget = QtGui.QWidget(mw_toolManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tw_tools = QtGui.QTreeWidget(self.centralwidget)
        self.tw_tools.setAlternatingRowColors(True)
        self.tw_tools.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tw_tools.setObjectName(_fromUtf8("tw_tools"))
        self.tw_tools.headerItem().setText(0, _fromUtf8("1"))
        self.tw_tools.header().setVisible(False)
        self.gridLayout.addWidget(self.tw_tools, 0, 0, 1, 1)
        mw_toolManager.setCentralWidget(self.centralwidget)

        self.retranslateUi(mw_toolManager)
        QtCore.QMetaObject.connectSlotsByName(mw_toolManager)

    def retranslateUi(self, mw_toolManager):
        mw_toolManager.setWindowTitle(_translate("mw_toolManager", "Tool Manager", None))

