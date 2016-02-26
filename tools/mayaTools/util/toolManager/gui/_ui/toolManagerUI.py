# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\util\toolManager\gui\_src\toolManager.ui'
#
# Created: Thu Feb 25 21:55:07 2016
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
        self.tw_tools.setIndentation(0)
        self.tw_tools.setObjectName(_fromUtf8("tw_tools"))
        self.tw_tools.headerItem().setText(0, _fromUtf8("1"))
        self.tw_tools.header().setVisible(False)
        self.gridLayout.addWidget(self.tw_tools, 0, 0, 1, 1)
        mw_toolManager.setCentralWidget(self.centralwidget)
        self.m_menuBar = QtGui.QMenuBar(mw_toolManager)
        self.m_menuBar.setGeometry(QtCore.QRect(0, 0, 423, 21))
        self.m_menuBar.setObjectName(_fromUtf8("m_menuBar"))
        self.m_menu = QtGui.QMenu(self.m_menuBar)
        self.m_menu.setObjectName(_fromUtf8("m_menu"))
        self.m_logLevel = QtGui.QMenu(self.m_menu)
        self.m_logLevel.setObjectName(_fromUtf8("m_logLevel"))
        mw_toolManager.setMenuBar(self.m_menuBar)
        self.actionEmpty = QtGui.QAction(mw_toolManager)
        self.actionEmpty.setObjectName(_fromUtf8("actionEmpty"))
        self.m_menu.addAction(self.m_logLevel.menuAction())
        self.m_menuBar.addAction(self.m_menu.menuAction())

        self.retranslateUi(mw_toolManager)
        QtCore.QMetaObject.connectSlotsByName(mw_toolManager)

    def retranslateUi(self, mw_toolManager):
        mw_toolManager.setWindowTitle(_translate("mw_toolManager", "Tool Manager", None))
        self.m_menu.setTitle(_translate("mw_toolManager", "Menu", None))
        self.m_logLevel.setTitle(_translate("mw_toolManager", "Log Level", None))
        self.actionEmpty.setText(_translate("mw_toolManager", "empty", None))

