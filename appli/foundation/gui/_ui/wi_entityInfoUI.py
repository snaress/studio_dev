# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\appli\foundation\gui\_src\wi_entityInfo.ui'
#
# Created: Mon Apr 11 01:55:25 2016
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

class Ui_wi_entityInfo(object):
    def setupUi(self, wi_entityInfo):
        wi_entityInfo.setObjectName(_fromUtf8("wi_entityInfo"))
        wi_entityInfo.resize(387, 106)
        self.gridLayout = QtGui.QGridLayout(wi_entityInfo)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line_3 = QtGui.QFrame(wi_entityInfo)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 1, 1, 1, 1)
        self.pb_ima = QtGui.QPushButton(wi_entityInfo)
        self.pb_ima.setMinimumSize(QtCore.QSize(150, 100))
        self.pb_ima.setMaximumSize(QtCore.QSize(150, 100))
        self.pb_ima.setText(_fromUtf8(""))
        self.pb_ima.setFlat(True)
        self.pb_ima.setObjectName(_fromUtf8("pb_ima"))
        self.gridLayout.addWidget(self.pb_ima, 1, 0, 1, 1)
        self.line = QtGui.QFrame(wi_entityInfo)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 0, 0, 1, 3)
        self.line_2 = QtGui.QFrame(wi_entityInfo)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 3)
        self.vl_data = QtGui.QVBoxLayout()
        self.vl_data.setSpacing(0)
        self.vl_data.setMargin(0)
        self.vl_data.setObjectName(_fromUtf8("vl_data"))
        self.line_4 = QtGui.QFrame(wi_entityInfo)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.vl_data.addWidget(self.line_4)
        self.hl_name = QtGui.QHBoxLayout()
        self.hl_name.setObjectName(_fromUtf8("hl_name"))
        self.l_name = QtGui.QLabel(wi_entityInfo)
        self.l_name.setMaximumSize(QtCore.QSize(70, 16777215))
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self.hl_name.addWidget(self.l_name)
        self.l_nameValue = QtGui.QLabel(wi_entityInfo)
        self.l_nameValue.setText(_fromUtf8(""))
        self.l_nameValue.setObjectName(_fromUtf8("l_nameValue"))
        self.hl_name.addWidget(self.l_nameValue)
        self.vl_data.addLayout(self.hl_name)
        self.line_7 = QtGui.QFrame(wi_entityInfo)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.vl_data.addWidget(self.line_7)
        self.hl_code = QtGui.QHBoxLayout()
        self.hl_code.setObjectName(_fromUtf8("hl_code"))
        self.l_code = QtGui.QLabel(wi_entityInfo)
        self.l_code.setMaximumSize(QtCore.QSize(70, 16777215))
        self.l_code.setObjectName(_fromUtf8("l_code"))
        self.hl_code.addWidget(self.l_code)
        self.l_codeValue = QtGui.QLabel(wi_entityInfo)
        self.l_codeValue.setText(_fromUtf8(""))
        self.l_codeValue.setObjectName(_fromUtf8("l_codeValue"))
        self.hl_code.addWidget(self.l_codeValue)
        self.vl_data.addLayout(self.hl_code)
        self.line_6 = QtGui.QFrame(wi_entityInfo)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.vl_data.addWidget(self.line_6)
        self.hl_mainType = QtGui.QHBoxLayout()
        self.hl_mainType.setObjectName(_fromUtf8("hl_mainType"))
        self.l_mainType = QtGui.QLabel(wi_entityInfo)
        self.l_mainType.setMaximumSize(QtCore.QSize(70, 16777215))
        self.l_mainType.setObjectName(_fromUtf8("l_mainType"))
        self.hl_mainType.addWidget(self.l_mainType)
        self.l_mainTypeValue = QtGui.QLabel(wi_entityInfo)
        self.l_mainTypeValue.setText(_fromUtf8(""))
        self.l_mainTypeValue.setObjectName(_fromUtf8("l_mainTypeValue"))
        self.hl_mainType.addWidget(self.l_mainTypeValue)
        self.vl_data.addLayout(self.hl_mainType)
        self.line_5 = QtGui.QFrame(wi_entityInfo)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.vl_data.addWidget(self.line_5)
        self.hl_subType = QtGui.QHBoxLayout()
        self.hl_subType.setObjectName(_fromUtf8("hl_subType"))
        self.l_subType = QtGui.QLabel(wi_entityInfo)
        self.l_subType.setMaximumSize(QtCore.QSize(70, 16777215))
        self.l_subType.setObjectName(_fromUtf8("l_subType"))
        self.hl_subType.addWidget(self.l_subType)
        self.l_subTypeValue = QtGui.QLabel(wi_entityInfo)
        self.l_subTypeValue.setText(_fromUtf8(""))
        self.l_subTypeValue.setObjectName(_fromUtf8("l_subTypeValue"))
        self.hl_subType.addWidget(self.l_subTypeValue)
        self.vl_data.addLayout(self.hl_subType)
        self.line_8 = QtGui.QFrame(wi_entityInfo)
        self.line_8.setFrameShape(QtGui.QFrame.HLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.vl_data.addWidget(self.line_8)
        self.gridLayout.addLayout(self.vl_data, 1, 2, 1, 1)

        self.retranslateUi(wi_entityInfo)
        QtCore.QMetaObject.connectSlotsByName(wi_entityInfo)

    def retranslateUi(self, wi_entityInfo):
        wi_entityInfo.setWindowTitle(_translate("wi_entityInfo", "Form", None))
        self.l_name.setText(_translate("wi_entityInfo", "Name :", None))
        self.l_code.setText(_translate("wi_entityInfo", "Code :", None))
        self.l_mainType.setText(_translate("wi_entityInfo", "Main Type :", None))
        self.l_subType.setText(_translate("wi_entityInfo", "Sub Type :", None))

