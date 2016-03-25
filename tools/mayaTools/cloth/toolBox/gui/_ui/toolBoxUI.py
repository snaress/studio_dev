# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\tools\mayaTools\cloth\toolBox\gui\_src\toolBox.ui'
#
# Created: Fri Mar 25 02:24:29 2016
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

class Ui_mw_toolBox(object):
    def setupUi(self, mw_toolBox):
        mw_toolBox.setObjectName(_fromUtf8("mw_toolBox"))
        mw_toolBox.setWindowModality(QtCore.Qt.NonModal)
        mw_toolBox.resize(300, 500)
        self.centralwidget = QtGui.QWidget(mw_toolBox)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tab_clothBox = QtGui.QTabWidget(self.centralwidget)
        self.tab_clothBox.setObjectName(_fromUtf8("tab_clothBox"))
        self.tab_mode = QtGui.QWidget()
        self.tab_mode.setObjectName(_fromUtf8("tab_mode"))
        self.vl_mode = QtGui.QVBoxLayout(self.tab_mode)
        self.vl_mode.setSpacing(0)
        self.vl_mode.setMargin(0)
        self.vl_mode.setObjectName(_fromUtf8("vl_mode"))
        self.tab_clothBox.addTab(self.tab_mode, _fromUtf8(""))
        self.tab_Rigg = QtGui.QWidget()
        self.tab_Rigg.setObjectName(_fromUtf8("tab_Rigg"))
        self.vl_setup = QtGui.QVBoxLayout(self.tab_Rigg)
        self.vl_setup.setSpacing(0)
        self.vl_setup.setMargin(0)
        self.vl_setup.setObjectName(_fromUtf8("vl_setup"))
        self.tab_clothBox.addTab(self.tab_Rigg, _fromUtf8(""))
        self.tab_simu = QtGui.QWidget()
        self.tab_simu.setObjectName(_fromUtf8("tab_simu"))
        self.vl_simu = QtGui.QVBoxLayout(self.tab_simu)
        self.vl_simu.setSpacing(0)
        self.vl_simu.setMargin(0)
        self.vl_simu.setObjectName(_fromUtf8("vl_simu"))
        self.tab_clothBox.addTab(self.tab_simu, _fromUtf8(""))
        self.gridLayout.addWidget(self.tab_clothBox, 0, 0, 1, 1)
        mw_toolBox.setCentralWidget(self.centralwidget)
        self.mi_help = QtGui.QAction(mw_toolBox)
        self.mi_help.setObjectName(_fromUtf8("mi_help"))

        self.retranslateUi(mw_toolBox)
        self.tab_clothBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mw_toolBox)

    def retranslateUi(self, mw_toolBox):
        mw_toolBox.setWindowTitle(_translate("mw_toolBox", "Cloth Box", None))
        self.tab_clothBox.setTabText(self.tab_clothBox.indexOf(self.tab_mode), _translate("mw_toolBox", "Mode", None))
        self.tab_clothBox.setTabText(self.tab_clothBox.indexOf(self.tab_Rigg), _translate("mw_toolBox", "Rigg", None))
        self.tab_clothBox.setTabText(self.tab_clothBox.indexOf(self.tab_simu), _translate("mw_toolBox", "Simu", None))
        self.mi_help.setText(_translate("mw_toolBox", "Help", None))

