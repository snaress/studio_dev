# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\appli\foundation\gui\_src\wg_entityInfo.ui'
#
# Created: Sun Apr 10 14:06:34 2016
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

class Ui_wg_tabInfo(object):
    def setupUi(self, wg_tabInfo):
        wg_tabInfo.setObjectName(_fromUtf8("wg_tabInfo"))
        wg_tabInfo.resize(484, 300)
        self.gridLayout = QtGui.QGridLayout(wg_tabInfo)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tw_entities = QtGui.QTreeWidget(wg_tabInfo)
        self.tw_entities.setMinimumSize(QtCore.QSize(350, 0))
        self.tw_entities.setMaximumSize(QtCore.QSize(350, 16777215))
        self.tw_entities.setAlternatingRowColors(False)
        self.tw_entities.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tw_entities.setIndentation(0)
        self.tw_entities.setItemsExpandable(False)
        self.tw_entities.setExpandsOnDoubleClick(False)
        self.tw_entities.setObjectName(_fromUtf8("tw_entities"))
        self.tw_entities.headerItem().setText(0, _fromUtf8("1"))
        self.tw_entities.header().setVisible(False)
        self.gridLayout.addWidget(self.tw_entities, 0, 0, 1, 1)
        self.qf_data = QtGui.QFrame(wg_tabInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qf_data.sizePolicy().hasHeightForWidth())
        self.qf_data.setSizePolicy(sizePolicy)
        self.qf_data.setObjectName(_fromUtf8("qf_data"))
        self.verticalLayout = QtGui.QVBoxLayout(self.qf_data)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout.addWidget(self.qf_data, 0, 1, 1, 1)

        self.retranslateUi(wg_tabInfo)
        QtCore.QMetaObject.connectSlotsByName(wg_tabInfo)

    def retranslateUi(self, wg_tabInfo):
        wg_tabInfo.setWindowTitle(_translate("wg_tabInfo", "Entity Info", None))

