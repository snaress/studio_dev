import os
from PyQt4 import QtGui
from coreSys import env
from coreQt import pQt, dialogs


dialogs.compileUi('dial_settings.ui')
from _ui import dial_settingsUI
class Settings(QtGui.QDialog, dial_settingsUI.Ui_dial_settings):
    """
    Settings dialog Class: Edit settings ui

    :param parent: Parent Ui
    :type parent: QtGui
    """

    __iconPath__ = env.iconsPath

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)
        #--- Icons ---#
        self.iconEnable = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'enable.png'))
        self.iconDisable = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'disable.png'))
        #--- Setup ---#
        self._initSettings()
        self._setupUi()

    def _initSettings(self):
        """
        Init dialog settings
        """
        if hasattr(self, 'log'):
            self.log.detail("#===== Init Settings Dialog =====#", newLinesBefore=1)

    def _initWidgets(self):
        """
        Init dialog widgets
        """
        self.setWindowTitle("Settings Dialog")
        #--- Category Font ---#
        self.categoryFont = QtGui.QFont()
        self.categoryFont.setPointSize(10)
        self.categoryFont.setBold(True)
        #--- Edited SubCategory Font ---#
        self.editedSubCategoryFont = QtGui.QFont()
        self.editedSubCategoryFont.setItalic(True)
        self.editedSubCategoryFont.setBold(True)

    def _setupUi(self):
        """
        Setup dialog Ui
        """
        self.setupUi(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        #--- Icons ---#
        self.pb_save.setIcon(self.iconEnable)
        self.pb_close.setIcon(self.iconDisable)
        #--- Connect ---#
        self.tw_category.clicked.connect(self.on_category)
        self.pb_save.clicked.connect(self.on_save)
        self.pb_close.clicked.connect(self.on_close)
        #--- Update ---#
        self._initWidgets()
        self.buildTree()

    @property
    def category(self):
        """
        Get settings category

        :return: Category data
        :rtype: dict
        """
        return dict()

    def buildTree(self):
        """
        Build category Tree widget
        """
        if hasattr(self, 'log'):
            self.log.detail("Build Category Tree ...")
        self.tw_category.clear()
        categoryDict = self.category
        #--- Build Category ---#
        for n in sorted(categoryDict.keys()):
            cat = categoryDict[n].keys()[0]
            catDict = categoryDict[n][cat]
            catItem = self.new_categoryItem('category', **catDict)
            self.tw_category.addTopLevelItem(catItem)
            #--- Build Sub Category ---#
            for nn in sorted(catDict['subCat'].keys()):
                subCat = catDict['subCat'][nn].keys()[0]
                subCatItem = self.new_categoryItem('subCategory', **catDict['subCat'][nn][subCat])
                catItem.addChild(subCatItem)
        #--- Refresh ---#
        self.tw_category.expandAll()

    def new_categoryItem(self, itemType, **kwargs):
        """
        Create category tree item widget

        :param itemType: 'category' or 'subCategory'
        :type itemType: str
        :param kwargs: Category params ('code', 'label', 'widget')
        :type kwargs: dict
        :return: New category item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        #--- Set Datas ---#
        newItem.itemType = itemType
        newItem.itemCode = kwargs['code']
        newItem.itemLabel = kwargs['label']
        if itemType == 'subCategory':
            newItem.itemWidget = kwargs['widget']
        #--- Edit Item ---#
        newItem.setText(0, newItem.itemLabel)
        if itemType == 'category':
            newItem.setFont(0, self.categoryFont)
        return newItem

    def on_category(self):
        """
        Command launched when 'Category' tree item widget is clicked

        Update category settings
        """
        selItems = self.tw_category.selectedItems() or []
        #--- Update Display ---#
        if not selItems:
            self.qf_settingsWidget.setVisible(False)
        else:
            if selItems[0].itemType == 'category':
                self.qf_settingsWidget.setVisible(False)
            else:
                self.qf_settingsWidget.setVisible(True)
                #--- Reset Visibility (resize bug) ---#
                for item in pQt.getAllItems(self.tw_category):
                    if hasattr(item, 'itemWidget'):
                        if item.itemWidget is not None:
                            item.itemWidget.setVisible(False)
                #--- Edit Visibility ---#
                for item in pQt.getAllItems(self.tw_category):
                    if hasattr(item, 'itemWidget'):
                        if item.itemWidget is not None:
                            if item.itemLabel == selItems[0].itemLabel:
                                item.itemWidget.setVisible(True)

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save settings to disk
        """
        if hasattr(self, 'log'):
            self.log.debug("#--- Save Settings ---#")

    def on_close(self):
        """
        Command launched when 'Close' QPushButton is clicked

        Close settings ui
        """
        if hasattr(self, 'log'):
            self.log.debug("#--- Close Dialog ---#")
