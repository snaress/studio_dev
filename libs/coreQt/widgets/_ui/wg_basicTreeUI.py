# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\libs\coreQt\widgets\_src\wg_basicTree.ui'
#
# Created: Sun Feb 14 03:04:29 2016
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

class Ui_wg_basicTree(object):
    def setupUi(self, wg_basicTree):
        wg_basicTree.setObjectName(_fromUtf8("wg_basicTree"))
        wg_basicTree.resize(510, 382)
        self.gridLayout = QtGui.QGridLayout(wg_basicTree)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.qf_apply = QtGui.QFrame(wg_basicTree)
        self.qf_apply.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qf_apply.setObjectName(_fromUtf8("qf_apply"))
        self.hl_apply = QtGui.QHBoxLayout(self.qf_apply)
        self.hl_apply.setSpacing(0)
        self.hl_apply.setMargin(0)
        self.hl_apply.setObjectName(_fromUtf8("hl_apply"))
        self.pb_apply = QtGui.QPushButton(self.qf_apply)
        self.pb_apply.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pb_apply.setIconSize(QtCore.QSize(16, 16))
        self.pb_apply.setAutoDefault(False)
        self.pb_apply.setFlat(False)
        self.pb_apply.setObjectName(_fromUtf8("pb_apply"))
        self.hl_apply.addWidget(self.pb_apply)
        self.pb_cancel = QtGui.QPushButton(self.qf_apply)
        self.pb_cancel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pb_cancel.setIconSize(QtCore.QSize(16, 16))
        self.pb_cancel.setAutoDefault(False)
        self.pb_cancel.setFlat(False)
        self.pb_cancel.setObjectName(_fromUtf8("pb_cancel"))
        self.hl_apply.addWidget(self.pb_cancel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_apply.addItem(spacerItem)
        self.gridLayout.addWidget(self.qf_apply, 5, 0, 1, 1)
        self.line = QtGui.QFrame(wg_basicTree)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)
        self.hl_tree = QtGui.QHBoxLayout()
        self.hl_tree.setSpacing(0)
        self.hl_tree.setObjectName(_fromUtf8("hl_tree"))
        self.qf_treeEdit_L = QtGui.QFrame(wg_basicTree)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qf_treeEdit_L.sizePolicy().hasHeightForWidth())
        self.qf_treeEdit_L.setSizePolicy(sizePolicy)
        self.qf_treeEdit_L.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qf_treeEdit_L.setObjectName(_fromUtf8("qf_treeEdit_L"))
        self.vl_treeEdit_L = QtGui.QVBoxLayout(self.qf_treeEdit_L)
        self.vl_treeEdit_L.setSpacing(0)
        self.vl_treeEdit_L.setContentsMargins(0, 25, 0, 0)
        self.vl_treeEdit_L.setObjectName(_fromUtf8("vl_treeEdit_L"))
        self.line_11 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_11.setFrameShape(QtGui.QFrame.HLine)
        self.line_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_11.setObjectName(_fromUtf8("line_11"))
        self.vl_treeEdit_L.addWidget(self.line_11)
        self.qf_moveItem = QtGui.QFrame(self.qf_treeEdit_L)
        self.qf_moveItem.setFrameShape(QtGui.QFrame.NoFrame)
        self.qf_moveItem.setLineWidth(0)
        self.qf_moveItem.setObjectName(_fromUtf8("qf_moveItem"))
        self.hl_moveItem = QtGui.QHBoxLayout(self.qf_moveItem)
        self.hl_moveItem.setSpacing(0)
        self.hl_moveItem.setMargin(0)
        self.hl_moveItem.setObjectName(_fromUtf8("hl_moveItem"))
        self.pb_itemUp = QtGui.QPushButton(self.qf_moveItem)
        self.pb_itemUp.setMinimumSize(QtCore.QSize(24, 24))
        self.pb_itemUp.setMaximumSize(QtCore.QSize(24, 24))
        self.pb_itemUp.setText(_fromUtf8(""))
        self.pb_itemUp.setIconSize(QtCore.QSize(16, 16))
        self.pb_itemUp.setAutoDefault(False)
        self.pb_itemUp.setFlat(False)
        self.pb_itemUp.setObjectName(_fromUtf8("pb_itemUp"))
        self.hl_moveItem.addWidget(self.pb_itemUp)
        self.pb_itemDn = QtGui.QPushButton(self.qf_moveItem)
        self.pb_itemDn.setMinimumSize(QtCore.QSize(24, 24))
        self.pb_itemDn.setMaximumSize(QtCore.QSize(24, 24))
        self.pb_itemDn.setText(_fromUtf8(""))
        self.pb_itemDn.setIconSize(QtCore.QSize(16, 16))
        self.pb_itemDn.setAutoDefault(False)
        self.pb_itemDn.setFlat(False)
        self.pb_itemDn.setObjectName(_fromUtf8("pb_itemDn"))
        self.hl_moveItem.addWidget(self.pb_itemDn)
        self.vl_treeEdit_L.addWidget(self.qf_moveItem)
        self.line_8 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_8.setFrameShape(QtGui.QFrame.HLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.vl_treeEdit_L.addWidget(self.line_8)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vl_treeEdit_L.addItem(spacerItem1)
        self.line_13 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_13.setFrameShape(QtGui.QFrame.HLine)
        self.line_13.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_13.setObjectName(_fromUtf8("line_13"))
        self.vl_treeEdit_L.addWidget(self.line_13)
        self.pb_template = QtGui.QPushButton(self.qf_treeEdit_L)
        self.pb_template.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_template.setObjectName(_fromUtf8("pb_template"))
        self.vl_treeEdit_L.addWidget(self.pb_template)
        self.cbb_filter = QtGui.QComboBox(self.qf_treeEdit_L)
        self.cbb_filter.setMaximumSize(QtCore.QSize(60, 16777215))
        self.cbb_filter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbb_filter.setMaxVisibleItems(12)
        self.cbb_filter.setFrame(False)
        self.cbb_filter.setObjectName(_fromUtf8("cbb_filter"))
        self.vl_treeEdit_L.addWidget(self.cbb_filter)
        self.line_14 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_14.setFrameShape(QtGui.QFrame.HLine)
        self.line_14.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_14.setObjectName(_fromUtf8("line_14"))
        self.vl_treeEdit_L.addWidget(self.line_14)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vl_treeEdit_L.addItem(spacerItem2)
        self.line_7 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.vl_treeEdit_L.addWidget(self.line_7)
        self.pb_add = QtGui.QPushButton(self.qf_treeEdit_L)
        self.pb_add.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_add.setToolTip(_fromUtf8(""))
        self.pb_add.setIconSize(QtCore.QSize(16, 16))
        self.pb_add.setAutoDefault(False)
        self.pb_add.setFlat(False)
        self.pb_add.setObjectName(_fromUtf8("pb_add"))
        self.vl_treeEdit_L.addWidget(self.pb_add)
        self.pb_del = QtGui.QPushButton(self.qf_treeEdit_L)
        self.pb_del.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_del.setToolTip(_fromUtf8(""))
        self.pb_del.setIconSize(QtCore.QSize(16, 16))
        self.pb_del.setAutoDefault(False)
        self.pb_del.setFlat(False)
        self.pb_del.setObjectName(_fromUtf8("pb_del"))
        self.vl_treeEdit_L.addWidget(self.pb_del)
        self.line_9 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_9.setFrameShape(QtGui.QFrame.HLine)
        self.line_9.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_9.setObjectName(_fromUtf8("line_9"))
        self.vl_treeEdit_L.addWidget(self.line_9)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vl_treeEdit_L.addItem(spacerItem3)
        self.line_10 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_10.setFrameShape(QtGui.QFrame.HLine)
        self.line_10.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_10.setObjectName(_fromUtf8("line_10"))
        self.vl_treeEdit_L.addWidget(self.line_10)
        self.pb_edit1 = QtGui.QPushButton(self.qf_treeEdit_L)
        self.pb_edit1.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_edit1.setToolTip(_fromUtf8(""))
        self.pb_edit1.setIconSize(QtCore.QSize(16, 16))
        self.pb_edit1.setAutoDefault(False)
        self.pb_edit1.setFlat(False)
        self.pb_edit1.setObjectName(_fromUtf8("pb_edit1"))
        self.vl_treeEdit_L.addWidget(self.pb_edit1)
        self.pb_edit2 = QtGui.QPushButton(self.qf_treeEdit_L)
        self.pb_edit2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pb_edit2.setToolTip(_fromUtf8(""))
        self.pb_edit2.setIconSize(QtCore.QSize(16, 16))
        self.pb_edit2.setAutoDefault(False)
        self.pb_edit2.setFlat(False)
        self.pb_edit2.setObjectName(_fromUtf8("pb_edit2"))
        self.vl_treeEdit_L.addWidget(self.pb_edit2)
        self.line_12 = QtGui.QFrame(self.qf_treeEdit_L)
        self.line_12.setFrameShape(QtGui.QFrame.HLine)
        self.line_12.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_12.setObjectName(_fromUtf8("line_12"))
        self.vl_treeEdit_L.addWidget(self.line_12)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vl_treeEdit_L.addItem(spacerItem4)
        self.hl_tree.addWidget(self.qf_treeEdit_L)
        self.line_5 = QtGui.QFrame(wg_basicTree)
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.hl_tree.addWidget(self.line_5)
        self.tw_tree = QtGui.QTreeWidget(wg_basicTree)
        self.tw_tree.setObjectName(_fromUtf8("tw_tree"))
        self.tw_tree.headerItem().setText(0, _fromUtf8("1"))
        self.hl_tree.addWidget(self.tw_tree)
        self.line_6 = QtGui.QFrame(wg_basicTree)
        self.line_6.setFrameShape(QtGui.QFrame.VLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.hl_tree.addWidget(self.line_6)
        self.qf_treeEdit_R = QtGui.QFrame(wg_basicTree)
        self.qf_treeEdit_R.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qf_treeEdit_R.setObjectName(_fromUtf8("qf_treeEdit_R"))
        self.vl_treeEdit_R = QtGui.QVBoxLayout(self.qf_treeEdit_R)
        self.vl_treeEdit_R.setContentsMargins(0, 25, 0, 0)
        self.vl_treeEdit_R.setObjectName(_fromUtf8("vl_treeEdit_R"))
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vl_treeEdit_R.addItem(spacerItem5)
        self.hl_tree.addWidget(self.qf_treeEdit_R)
        self.gridLayout.addLayout(self.hl_tree, 3, 0, 1, 1)
        self.l_title = QtGui.QLabel(wg_basicTree)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.l_title.setFont(font)
        self.l_title.setAlignment(QtCore.Qt.AlignCenter)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self.gridLayout.addWidget(self.l_title, 1, 0, 1, 1)
        self.line_2 = QtGui.QFrame(wg_basicTree)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 1)
        self.line_3 = QtGui.QFrame(wg_basicTree)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 0, 0, 1, 1)
        self.line_4 = QtGui.QFrame(wg_basicTree)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 6, 0, 1, 1)

        self.retranslateUi(wg_basicTree)
        QtCore.QMetaObject.connectSlotsByName(wg_basicTree)
        wg_basicTree.setTabOrder(self.tw_tree, self.pb_itemUp)
        wg_basicTree.setTabOrder(self.pb_itemUp, self.pb_itemDn)
        wg_basicTree.setTabOrder(self.pb_itemDn, self.pb_add)
        wg_basicTree.setTabOrder(self.pb_add, self.pb_del)
        wg_basicTree.setTabOrder(self.pb_del, self.pb_edit1)
        wg_basicTree.setTabOrder(self.pb_edit1, self.pb_edit2)
        wg_basicTree.setTabOrder(self.pb_edit2, self.pb_apply)
        wg_basicTree.setTabOrder(self.pb_apply, self.pb_cancel)

    def retranslateUi(self, wg_basicTree):
        wg_basicTree.setWindowTitle(_translate("wg_basicTree", "Basic Tree", None))
        self.pb_apply.setText(_translate("wg_basicTree", "Apply", None))
        self.pb_cancel.setText(_translate("wg_basicTree", "Cancel", None))
        self.pb_template.setText(_translate("wg_basicTree", "Tpl", None))
        self.pb_add.setText(_translate("wg_basicTree", "Add", None))
        self.pb_del.setText(_translate("wg_basicTree", "Del", None))
        self.pb_edit1.setText(_translate("wg_basicTree", "Edit_1", None))
        self.pb_edit2.setText(_translate("wg_basicTree", "Edit_2", None))
        self.l_title.setText(_translate("wg_basicTree", "Title", None))

