from coreQt import pQt
from coreSys import pFile
from functools import partial
from PyQt4 import QtGui, QtCore
from mayaCore.cmds import pUtil, pShading
from _ui import displayColorUI


class DisplayColor(QtGui.QMainWindow, displayColorUI.Ui_mw_displayColor):
    """
    DisplayColor class: Override display color

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :param parent: Maya main window
    :type parent: QtCore.QObject
    """

    def __init__(self, logLvl='info', parent=None):
        self.log = pFile.Logger(title=self.__class__.__name__, level=logLvl)
        self.log.info("########## Launching %s Ui ##########" % self.__class__.__name__, newLinesBefore=1)
        super(DisplayColor, self).__init__(parent)
        self._setupUi()

    def _setupUi(self):
        """
        Setup ToolManager ui
        """
        self.setupUi(self)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setMargin(0)
        self._initWidgets()
        self.pb_default.clicked.connect(self.on_defaultColor)
        self.pb_override.clicked.connect(self.on_overrideColor)

    def _initWidgets(self):
        """
        Init tool widgets
        """
        self.tw_tree = ColorTree(self)
        self.vl_tree.addWidget(self.tw_tree)

    @property
    def overrideMode(self):
        """
        Get override mode

        :return: Wire state, shader state
        :rtype: bool, bool
        """
        return self.cb_wire.isChecked(), self.cb_shader.isChecked()

    def on_defaultColor(self):
        """
        Command launched when 'Default' QPushButton is clicked

        Restore selected objects color
        """
        wire, shader = self.overrideMode
        if wire:
            pUtil.defaultDisplayColor()
        if shader:
            pShading.defaultShader()

    def on_overrideColor(self):
        """
        Command launched when 'Override' QPushButton is clicked

        Override selected objects color
        """
        cIndex = self.tw_tree.selectedColorIndex
        wire, shader = self.overrideMode
        if wire:
            pUtil.overrideDisplayColor(cIndex)
        if shader:
            pShading.overrideShader(cIndex)


class ColorTree(QtGui.QTreeWidget):
    """
    ColorTree class: Display color indexes

    :param mainUi: DisplayColor main ui
    :type mainUi: DisplayColor
    :param parent: Parent Qt ui
    :type parent: QtGui.QWidget
    """

    rows = 2
    maxColors = 32
    cellSize = 20

    def __init__(self, mainUi, parent=None):
        super(ColorTree, self).__init__(parent)
        self.mainUi = mainUi
        self.setupWidget()

    def setupWidget(self):
        """
        Setup tree widget
        """
        self.setHeaderHidden(True)
        self.setIndentation(0)
        self.setColumnCount(self.maxColors / self.rows)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.header().setDefaultSectionSize(self.cellSize)
        self.header().setMinimumSectionSize(self.cellSize)
        self.header().setStretchLastSection(False)
        self.buildTree()

    @property
    def selectedColorIndex(self):
        for item in pQt.getAllItems(self):
            for widget in item._widgets:
                if widget.isChecked():
                    return widget.index

    # noinspection PyUnresolvedReferences
    def buildTree(self):
        """
        Build tree widget
        """
        for r in range(self.rows):
            newItem = self.new_item(r)
            self.addTopLevelItem(newItem)
            for n, w in enumerate(newItem._widgets):
                self.setItemWidget(newItem, n, newItem._widgets[n])

    def new_item(self, line):
        """
        New tree widget item

        :param line: Tree current line
        :type line: int
        :return: New tree widget item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem._widgets = []
        for i in range(self.maxColors / self.rows):
            index = i + ((self.maxColors / self.rows) * line)
            newItem._widgets.append(self.new_button(i, index, newItem))
        return newItem

    # noinspection PyUnresolvedReferences
    def new_button(self, i, index, pItem):
        """
        New colorIndex button

        :param i: Column index
        :type i: int
        :param index: Color index
        :type index: int
        :param pItem: Parent item
        :type pItem: QtGui.QTreeWidgetItem
        :return: New color index button
        :rtype: QtGui.QPushButton
        """
        newButton = QtGui.QPushButton()
        newButton.setText(str(index))
        newButton.setCheckable(True)
        newButton.setAutoExclusive(True)
        newButton.column = i
        newButton.index = index
        newButton.pItem = pItem
        if index > 0:
            color = pUtil.getColorFromIndex(index)
            newButton.color = color
            newButton.setStyleSheet("background-color: rgb(%s, %s, %s)" % (color[0]*255, color[1]*255, color[2]*255))
        newButton.clicked.connect(partial(self.on_button, newButton))
        return newButton

    def on_button(self, QPushButton):
        """
        Command launched when given QPushButton is clicked

        Add border line to selected color index
        :param QPushButton: Color index button
        :type QPushButton: QtGui.QPushButton
        """
        self.clearSelection()
        for item in pQt.getAllItems(self):
            for n in range(self.columnCount()):
                item.setBackgroundColor(n, QtGui.QColor(0, 0, 0))
        QPushButton.pItem.setBackgroundColor(QPushButton.column, QtGui.QColor(255, 0, 0))


def mayaLaunch(logLvl='detail', parent=None):
    """
    Launch OverrideColor

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    :param parent: Maya main window
    :type parent: QtCore.QObject
    :return: Launched window, Dock layout
    :rtype: OverrideColor, mc.dockControl
    """
    global window
    window, dock = pUtil.launchQtWindow('DisplayColor', 'mw_displayColor', DisplayColor,
                                        toolKwargs=dict(logLvl=logLvl, parent=parent))
    window.show()
    return window, dock
