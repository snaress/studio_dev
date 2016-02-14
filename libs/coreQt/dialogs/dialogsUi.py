import os
from PyQt4 import QtGui
from coreSystem import env
from coreQt import pQt, dialogs

dialogs.compileUi()


from _ui import dial_confirmUI
class Confirm(QtGui.QDialog, dial_confirmUI.Ui_dial_confirm):
    """
    Confirm dialog ui class

    :param message: Dialog texte
    :type message: str
    :param buttons: Buttons label list
    :type buttons: list
    :param btnCmds: Buttons commands list
    :type btnCmds: list
    :param cancelBtn: Add cancel button
    :type cancelBtn: bool
    :param parent: Parent ui or widget
    :type parent: QtGui
    """

    def __init__(self, message="Confirm Massage", buttons=list(), btnCmds=list(), cancelBtn=True, parent=None):
        super(Confirm, self).__init__(parent)
        self.message = message
        self.btns = buttons.reverse()
        self.btnCmds = btnCmds.reverse()
        self.cancelBtn = cancelBtn
        #--- Setup ---#
        self.setupUi(self)
        self._initDialog()

    def _initDialog(self):
        """
        Init dialog window
        """
        self.l_message.setText(self.message)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        #--- Cancel Button ---#
        if self.cancelBtn:
            newButton = self.newButton('Cancel', self.close)
            self.hl_buttons.insertWidget(1, newButton)
        #--- Confirm Buttons ---#
        if self.btns is not None:
            for n, btn in enumerate(self.btns):
                newButton = self.newButton(btn, self.btnCmds[n])
                self.hl_buttons.insertWidget(1, newButton)

    @staticmethod
    def newButton(label, btnCmd):
        """
        Create new button

        :param label: Button label
        :type label: str
        :param btnCmd: Button command
        :type btnCmd: function
        :return: New QPushButton
        :rtype: QtGui.QPushButton
        """
        newButton = QtGui.QPushButton()
        newButton.setText(label)
        # noinspection PyUnresolvedReferences
        newButton.clicked.connect(btnCmd)
        return newButton


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
        if self.log is not None:
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
        self.log.debug("#--- Save Settings ---#")

    def on_close(self):
        """
        Command launched when 'Close' QPushButton is clicked

        Close settings ui
        """
        self.log.debug("#--- Close Dialog ---#")




if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    window = Settings()
    window.show()
    sys.exit(app.exec_())
