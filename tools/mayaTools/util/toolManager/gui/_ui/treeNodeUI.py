# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\util\toolManager\gui\_src\treeNode.ui'
#
# Created: Thu Apr 07 02:39:17 2016
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

class Ui_wg_treeNode(object):
    def setupUi(self, wg_treeNode):
        wg_treeNode.setObjectName(_fromUtf8("wg_treeNode"))
        wg_treeNode.resize(267, 28)
        self.gridLayout = QtGui.QGridLayout(wg_treeNode)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line_6 = QtGui.QFrame(wg_treeNode)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.gridLayout.addWidget(self.line_6, 0, 0, 1, 1)
        self.hl_tool = QtGui.QHBoxLayout()
        self.hl_tool.setSpacing(0)
        self.hl_tool.setObjectName(_fromUtf8("hl_tool"))
        self.line_2 = QtGui.QFrame(wg_treeNode)
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.hl_tool.addWidget(self.line_2)
        self.pb_tool = QtGui.QPushButton(wg_treeNode)
        self.pb_tool.setMaximumSize(QtCore.QSize(20, 20))
        self.pb_tool.setText(_fromUtf8(""))
        self.pb_tool.setFlat(True)
        self.pb_tool.setObjectName(_fromUtf8("pb_tool"))
        self.hl_tool.addWidget(self.pb_tool)
        self.line = QtGui.QFrame(wg_treeNode)
        self.line.setMaximumSize(QtCore.QSize(16777215, 20))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.hl_tool.addWidget(self.line)
        self.l_toolName = QtGui.QLabel(wg_treeNode)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_toolName.sizePolicy().hasHeightForWidth())
        self.l_toolName.setSizePolicy(sizePolicy)
        self.l_toolName.setAlignment(QtCore.Qt.AlignCenter)
        self.l_toolName.setObjectName(_fromUtf8("l_toolName"))
        self.hl_tool.addWidget(self.l_toolName)
        self.qf_info = QtGui.QFrame(wg_treeNode)
        self.qf_info.setLineWidth(0)
        self.qf_info.setObjectName(_fromUtf8("qf_info"))
        self.hl_info = QtGui.QHBoxLayout(self.qf_info)
        self.hl_info.setSpacing(0)
        self.hl_info.setMargin(0)
        self.hl_info.setObjectName(_fromUtf8("hl_info"))
        self.line_3 = QtGui.QFrame(self.qf_info)
        self.line_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.hl_info.addWidget(self.line_3)
        self.pb_wiki = QtGui.QPushButton(self.qf_info)
        self.pb_wiki.setMaximumSize(QtCore.QSize(40, 20))
        self.pb_wiki.setFlat(True)
        self.pb_wiki.setObjectName(_fromUtf8("pb_wiki"))
        self.hl_info.addWidget(self.pb_wiki)
        self.line_5 = QtGui.QFrame(self.qf_info)
        self.line_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.hl_info.addWidget(self.line_5)
        self.pb_api = QtGui.QPushButton(self.qf_info)
        self.pb_api.setMaximumSize(QtCore.QSize(40, 20))
        self.pb_api.setFlat(True)
        self.pb_api.setObjectName(_fromUtf8("pb_api"))
        self.hl_info.addWidget(self.pb_api)
        self.hl_tool.addWidget(self.qf_info)
        self.line_4 = QtGui.QFrame(wg_treeNode)
        self.line_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.hl_tool.addWidget(self.line_4)
        self.gridLayout.addLayout(self.hl_tool, 1, 0, 1, 1)
        self.line_7 = QtGui.QFrame(wg_treeNode)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.gridLayout.addWidget(self.line_7, 2, 0, 1, 1)

        self.retranslateUi(wg_treeNode)
        QtCore.QMetaObject.connectSlotsByName(wg_treeNode)

    def retranslateUi(self, wg_treeNode):
        wg_treeNode.setWindowTitle(_translate("wg_treeNode", "Tool Node", None))
        self.l_toolName.setText(_translate("wg_treeNode", "Tool Name", None))
        self.pb_wiki.setText(_translate("wg_treeNode", "Wiki", None))
        self.pb_api.setText(_translate("wg_treeNode", "Api", None))

