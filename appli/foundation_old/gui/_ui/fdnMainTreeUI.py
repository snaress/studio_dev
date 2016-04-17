# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\appli\foundation\gui\_src\fdnMainTree.ui'
#
# Created: Sun Mar 06 02:17:16 2016
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

class Ui_wg_fdnMainTree(object):
    def setupUi(self, wg_fdnMainTree):
        wg_fdnMainTree.setObjectName(_fromUtf8("wg_fdnMainTree"))
        wg_fdnMainTree.resize(315, 581)
        self.gridLayout = QtGui.QGridLayout(wg_fdnMainTree)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tw_tree = QtGui.QTreeWidget(wg_fdnMainTree)
        self.tw_tree.setAlternatingRowColors(False)
        self.tw_tree.setObjectName(_fromUtf8("tw_tree"))
        self.tw_tree.headerItem().setText(0, _fromUtf8("1"))
        self.tw_tree.header().setVisible(False)
        self.gridLayout.addWidget(self.tw_tree, 3, 0, 1, 1)
        self.line = QtGui.QFrame(wg_fdnMainTree)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.line_2 = QtGui.QFrame(wg_fdnMainTree)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 1)
        self.line_3 = QtGui.QFrame(wg_fdnMainTree)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 4, 0, 1, 1)
        self.qf_filters = QtGui.QFrame(wg_fdnMainTree)
        self.qf_filters.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qf_filters.setObjectName(_fromUtf8("qf_filters"))
        self.hl_filters = QtGui.QHBoxLayout(self.qf_filters)
        self.hl_filters.setSpacing(4)
        self.hl_filters.setMargin(0)
        self.hl_filters.setObjectName(_fromUtf8("hl_filters"))
        self.pb_filters = QtGui.QPushButton(self.qf_filters)
        self.pb_filters.setMaximumSize(QtCore.QSize(60, 20))
        self.pb_filters.setObjectName(_fromUtf8("pb_filters"))
        self.hl_filters.addWidget(self.pb_filters)
        spacerItem = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.hl_filters.addItem(spacerItem)
        self.qf_contexts = QtGui.QFrame(self.qf_filters)
        self.qf_contexts.setObjectName(_fromUtf8("qf_contexts"))
        self.hl_contexts = QtGui.QHBoxLayout(self.qf_contexts)
        self.hl_contexts.setSpacing(12)
        self.hl_contexts.setMargin(0)
        self.hl_contexts.setObjectName(_fromUtf8("hl_contexts"))
        self.hl_filters.addWidget(self.qf_contexts)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_filters.addItem(spacerItem1)
        self.gridLayout.addWidget(self.qf_filters, 1, 0, 1, 1)
        self.qf_search = QtGui.QFrame(wg_fdnMainTree)
        self.qf_search.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qf_search.setObjectName(_fromUtf8("qf_search"))
        self.hl_search = QtGui.QHBoxLayout(self.qf_search)
        self.hl_search.setSpacing(0)
        self.hl_search.setMargin(0)
        self.hl_search.setObjectName(_fromUtf8("hl_search"))
        self.le_search = QtGui.QLineEdit(self.qf_search)
        self.le_search.setMaximumSize(QtCore.QSize(16777215, 20))
        self.le_search.setFrame(False)
        self.le_search.setObjectName(_fromUtf8("le_search"))
        self.hl_search.addWidget(self.le_search)
        self.pb_clear = QtGui.QPushButton(self.qf_search)
        self.pb_clear.setMinimumSize(QtCore.QSize(0, 0))
        self.pb_clear.setMaximumSize(QtCore.QSize(40, 20))
        self.pb_clear.setObjectName(_fromUtf8("pb_clear"))
        self.hl_search.addWidget(self.pb_clear)
        self.gridLayout.addWidget(self.qf_search, 5, 0, 1, 1)

        self.retranslateUi(wg_fdnMainTree)
        QtCore.QMetaObject.connectSlotsByName(wg_fdnMainTree)

    def retranslateUi(self, wg_fdnMainTree):
        wg_fdnMainTree.setWindowTitle(_translate("wg_fdnMainTree", "Main Tree", None))
        self.pb_filters.setText(_translate("wg_fdnMainTree", "Filters", None))
        self.pb_clear.setText(_translate("wg_fdnMainTree", "X", None))

