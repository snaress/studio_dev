# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\rnd\workspace\studio_dev\libs\coreQt\widgets\_src\wg_range.ui'
#
# Created: Sun Feb 07 16:40:22 2016
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

class Ui_wg_range(object):
    def setupUi(self, wg_range):
        wg_range.setObjectName(_fromUtf8("wg_range"))
        wg_range.resize(333, 89)
        self.gridLayout = QtGui.QGridLayout(wg_range)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hl_range = QtGui.QHBoxLayout()
        self.hl_range.setContentsMargins(6, -1, 6, -1)
        self.hl_range.setObjectName(_fromUtf8("hl_range"))
        self.l_range = QtGui.QLabel(wg_range)
        self.l_range.setObjectName(_fromUtf8("l_range"))
        self.hl_range.addWidget(self.l_range)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_range.addItem(spacerItem)
        self.l_min = QtGui.QLabel(wg_range)
        self.l_min.setObjectName(_fromUtf8("l_min"))
        self.hl_range.addWidget(self.l_min)
        self.le_min = QtGui.QLineEdit(wg_range)
        self.le_min.setObjectName(_fromUtf8("le_min"))
        self.hl_range.addWidget(self.le_min)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_range.addItem(spacerItem1)
        self.l_max = QtGui.QLabel(wg_range)
        self.l_max.setObjectName(_fromUtf8("l_max"))
        self.hl_range.addWidget(self.l_max)
        self.le_max = QtGui.QLineEdit(wg_range)
        self.le_max.setObjectName(_fromUtf8("le_max"))
        self.hl_range.addWidget(self.le_max)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hl_range.addItem(spacerItem2)
        self.gridLayout.addLayout(self.hl_range, 0, 0, 1, 1)
        self.line = QtGui.QFrame(wg_range)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.hs_min = QtGui.QSlider(wg_range)
        self.hs_min.setMaximum(100)
        self.hs_min.setTracking(True)
        self.hs_min.setOrientation(QtCore.Qt.Horizontal)
        self.hs_min.setInvertedAppearance(False)
        self.hs_min.setTickPosition(QtGui.QSlider.TicksBelow)
        self.hs_min.setObjectName(_fromUtf8("hs_min"))
        self.gridLayout.addWidget(self.hs_min, 2, 0, 1, 1)
        self.qf_ramp = QtGui.QFrame(wg_range)
        self.qf_ramp.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 255, 255), stop:0.25 rgba(0, 255, 0, 255), stop:0.5 rgba(255, 255, 0, 255), stop:0.75 rgba(255, 125, 0, 255), stop:1 rgba(255, 0, 0, 255));"))
        self.qf_ramp.setFrameShape(QtGui.QFrame.StyledPanel)
        self.qf_ramp.setFrameShadow(QtGui.QFrame.Plain)
        self.qf_ramp.setLineWidth(1)
        self.qf_ramp.setObjectName(_fromUtf8("qf_ramp"))
        self.gridLayout.addWidget(self.qf_ramp, 3, 0, 1, 1)
        self.hs_max = QtGui.QSlider(wg_range)
        self.hs_max.setMaximum(100)
        self.hs_max.setProperty("value", 100)
        self.hs_max.setTracking(True)
        self.hs_max.setOrientation(QtCore.Qt.Horizontal)
        self.hs_max.setInvertedAppearance(False)
        self.hs_max.setTickPosition(QtGui.QSlider.TicksAbove)
        self.hs_max.setObjectName(_fromUtf8("hs_max"))
        self.gridLayout.addWidget(self.hs_max, 4, 0, 1, 1)

        self.retranslateUi(wg_range)
        QtCore.QMetaObject.connectSlotsByName(wg_range)

    def retranslateUi(self, wg_range):
        wg_range.setWindowTitle(_translate("wg_range", "Range", None))
        self.l_range.setText(_translate("wg_range", "Range:", None))
        self.l_min.setText(_translate("wg_range", "Min =", None))
        self.l_max.setText(_translate("wg_range", "Max =", None))

