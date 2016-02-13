from PyQt4 import QtGui
from coreQt import widgets
from functools import partial


widgets.compileUi('wg_range.ui')
from _ui import wg_rangeUI


class Range(QtGui.QWidget, wg_rangeUI.Ui_wg_range):
    """
    Range Class: Range selector Widget
    Usage: widget = Range(rangeMin=0, rangeMax=1000, normalized=True, rampData=None, parent=None)

    :param rangeMin: Minimum range value
    :type rangeMin: int
    :param rangeMax: Maximum range value
    :type rangeMax: int
    :param normalized: Normalize range value
    :type normalized: bool
    :param rampData: Ramp range data (rampDict={'0': 'rgba(0, 0, 0, 255)',
                                                '0.5': 'rgba(0, 255, 0, 255)',
                                                '1': 'rgba(255, 255, 255, 255)'}
    :type rampData: dict
    :param parent: Parent widget
    :type parent: QtGui.QMainWindow | QtGui.QWidget
    """

    def __init__(self, rangeMin=0, rangeMax=1000, normalized=True, rampData=None, parent=None):
        super(Range, self).__init__(parent)
        self._rangeMin = rangeMin
        self._rangeMax = rangeMax
        self.normalized = normalized
        self.rampData = rampData
        self._setupWidget()

    def _setupWidget(self):
        """
        Setup range widget
        """
        self.setupUi(self)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setMargin(0)
        #--- Edit Value ---#
        if self.normalized:
            self.le_min.setText(str(float(self._rangeMin) / self._rangeMax))
            self.le_max.setText(str(float(self._rangeMax) / self._rangeMax))
        else:
            self.le_min.setText(str(self._rangeMin))
            self.le_max.setText(str(self._rangeMax))
        #--- Edit Range ---#
        self._initRamp()
        self.hs_min.setMinimum(self._rangeMin)
        self.hs_min.setMaximum(self._rangeMax - 1)
        self.hs_max.setMinimum(self._rangeMin + 1)
        self.hs_max.setMaximum(self._rangeMax)
        self.hs_min.setValue(self._rangeMin)
        self.hs_max.setValue(self._rangeMax)
        #--- Connect ---#
        self.le_min.editingFinished.connect(partial(self.on_value, rangeMode='min'))
        self.le_max.editingFinished.connect(partial(self.on_value, rangeMode='max'))
        self.hs_min.valueChanged.connect(partial(self.on_slider, rangeMode='min'))
        self.hs_max.valueChanged.connect(partial(self.on_slider, rangeMode='max'))

    def _initRamp(self):
        """
        Init ramp colors

        rampDict = {'0': 'rgba(0, 0, 0, 255)',
                    '0.5': 'rgba(0, 255, 0, 255)',
                    '1': 'rgba(255, 255, 255, 255)'}
        """
        if self.rampData is not None:
            rampColor = 'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0'
            for k, v in sorted(self.rampData.iteritems()):
                rampColor += ', stop:%s %s' % (k, v)
            rampColor += ');'
            self.qf_ramp.setStyleSheet(rampColor)

    @property
    def valueMin(self):
        """
        Get min value

        :return: Min value
        :rtype: float
        """
        return float(str(self.le_min.text()))

    @property
    def valueMax(self):
        """
        Get max value

        :return: Max value
        :rtype: float
        """
        return float(str(self.le_max.text()))

    @property
    def rangeMin(self):
        """
        Get min range value

        :return: Min value
        :rtype: float | int
        """
        value = self.hs_min.value()
        if self.normalized:
            value = float(value) / self._rangeMax
        return value

    @property
    def rangeMax(self):
        """
        Get max range value

        :return: Max value
        :rtype: float | int
        """
        value = self.hs_max.value()
        if self.normalized:
            value = float(value) / self._rangeMax
        return value

    def on_value(self, rangeMode='min'):
        """
        Command launched when 'Value' QLineEdit is edited.

        :param rangeMode: 'min' or 'max'
        :type rangeMode: str
        """
        if rangeMode == 'min':
            if self.normalized:
                self.hs_min.setValue(int(self.valueMin * self._rangeMax))
            else:
                self.hs_min.setValue(int(self.valueMin))
        elif rangeMode == 'max':
            if self.normalized:
                self.hs_max.setValue(int(self.valueMax * self._rangeMax))
            else:
                self.hs_max.setValue(int(self.valueMax))

    def on_slider(self, rangeMode='min'):
        """
        Command launched when 'Range' QSlider is moved.

        :param rangeMode: 'min' or 'max'
        :type rangeMode: str
        """
        if rangeMode == 'min':
            self.le_min.setText(str(self.rangeMin))
            if self.rangeMin >= self.rangeMax:
                self.hs_max.setValue(self.hs_min.value() + 1)
        elif rangeMode == 'max':
            self.le_max.setText(str(self.rangeMax))
            if self.rangeMax <= self.rangeMin:
                self.hs_min.setValue(self.hs_max.value() - 1)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    window = Range()
    window.show()
    sys.exit(app.exec_())