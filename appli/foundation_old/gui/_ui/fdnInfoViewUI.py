# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\appli\foundation\gui\_src\fdnInfoView.ui'
#
# Created: Sun Apr 10 12:02:31 2016
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

class Ui_wg_infoView(object):
    def setupUi(self, wg_infoView):
        wg_infoView.setObjectName(_fromUtf8("wg_infoView"))
        wg_infoView.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(wg_infoView)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tab_infoView = QtGui.QTabWidget(wg_infoView)
        self.tab_infoView.setObjectName(_fromUtf8("tab_infoView"))
        self.ti_entityInfo = QtGui.QWidget()
        self.ti_entityInfo.setObjectName(_fromUtf8("ti_entityInfo"))
        self.gl_entityInfo = QtGui.QGridLayout(self.ti_entityInfo)
        self.gl_entityInfo.setMargin(0)
        self.gl_entityInfo.setSpacing(0)
        self.gl_entityInfo.setObjectName(_fromUtf8("gl_entityInfo"))
        self.tab_infoView.addTab(self.ti_entityInfo, _fromUtf8(""))
        self.ti_overView = QtGui.QWidget()
        self.ti_overView.setObjectName(_fromUtf8("ti_overView"))
        self.gl_overView = QtGui.QGridLayout(self.ti_overView)
        self.gl_overView.setMargin(0)
        self.gl_overView.setSpacing(0)
        self.gl_overView.setObjectName(_fromUtf8("gl_overView"))
        self.tab_infoView.addTab(self.ti_overView, _fromUtf8(""))
        self.ti_lineTest = QtGui.QWidget()
        self.ti_lineTest.setObjectName(_fromUtf8("ti_lineTest"))
        self.gl_lineTest = QtGui.QGridLayout(self.ti_lineTest)
        self.gl_lineTest.setMargin(0)
        self.gl_lineTest.setSpacing(0)
        self.gl_lineTest.setObjectName(_fromUtf8("gl_lineTest"))
        self.tab_infoView.addTab(self.ti_lineTest, _fromUtf8(""))
        self.gridLayout.addWidget(self.tab_infoView, 0, 0, 1, 1)

        self.retranslateUi(wg_infoView)
        self.tab_infoView.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(wg_infoView)

    def retranslateUi(self, wg_infoView):
        wg_infoView.setWindowTitle(_translate("wg_infoView", "Info View", None))
        self.tab_infoView.setTabText(self.tab_infoView.indexOf(self.ti_entityInfo), _translate("wg_infoView", "Entity Info", None))
        self.tab_infoView.setTabText(self.tab_infoView.indexOf(self.ti_overView), _translate("wg_infoView", "OverView", None))
        self.tab_infoView.setTabText(self.tab_infoView.indexOf(self.ti_lineTest), _translate("wg_infoView", "LineTest", None))

