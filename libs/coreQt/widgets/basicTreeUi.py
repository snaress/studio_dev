import os, pprint
from coreQt import pQt
from PyQt4 import QtGui
from coreQt import widgets
from coreSys import env
from functools import partial

# widgets.compileUi('wg_basicTree.ui')
from _ui import wg_basicTreeUI


class BasicTree(QtGui.QWidget, wg_basicTreeUI.Ui_wg_basicTree):
    """
    BasicTree common Class: Category tree widget

    :param parent: Parent Ui
    :type parent: QtGui
    """

    __iconPath__ = env.iconsPath
    __edited__ = False
    __editedItems__ = dict(added=[], edited=[], deleted=[])

    def __init__(self, parent=None):
        super(BasicTree, self).__init__(parent)
        #--- Icons ---#
        self.iconUp = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'arrowUpBlue.png'))
        self.iconDn = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'arrowDnBlue.png'))
        self.iconTpl = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'template.png'))
        self.iconAdd = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'add.png'))
        self.iconDel = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'del.png'))
        self.iconEdit = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'edit.png'))
        self.iconClear = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'clear.png'))
        self.iconApply = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'apply.png'))
        self.iconCancel = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'cancel.png'))
        #--- Setup ---#
        self._setupWidget()

    def _initWidget(self):
        """
        Init widget
        """
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])

    def _setupIcons(self):
        """
        Setup widget icons
        """
        self.pb_itemUp.setIcon(self.iconUp)
        self.pb_itemDn.setIcon(self.iconDn)
        self.pb_template.setIcon(self.iconTpl)
        self.pb_add.setIcon(self.iconAdd)
        self.pb_del.setIcon(self.iconDel)
        self.pb_edit1.setIcon(self.iconEdit)
        self.pb_edit2.setIcon(self.iconEdit)
        self.pb_apply.setIcon(self.iconApply)
        self.pb_cancel.setIcon(self.iconCancel)

    def _setupConnections(self):
        """
        Setup widget connections
        """
        self.pb_itemUp.clicked.connect(partial(self.on_moveItem, 'up'))
        self.pb_itemDn.clicked.connect(partial(self.on_moveItem, 'down'))
        self.cbb_filter.currentIndexChanged.connect(self.on_filter)
        self.pb_add.clicked.connect(self.on_addItem)
        self.pb_del.clicked.connect(self.on_delItem)
        self.pb_edit1.clicked.connect(self.on_editItem1)
        self.pb_edit2.clicked.connect(self.on_editItem2)
        self.pb_apply.clicked.connect(self.on_apply)
        self.pb_cancel.clicked.connect(self.on_cancel)

    def _setupWidget(self):
        """
        Setup widget ui
        """
        self.setupUi(self)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.tw_tree.setIndentation(0)
        self.tw_tree.setAlternatingRowColors(True)
        self._initWidget()
        self._setupIcons()
        self._setupConnections()
        self.rf_headers()
        self.rf_toolTips()

    @property
    def treeTitle(self):
        """
        Get tree title

        :return: Tree title
        :rtype: str
        """
        return str(self.l_title.text())

    def getData(self, asString=False):
        """
        Get tree datas

        :param asString: Return string instead of dict
        :type asString: bool
        :return: Tree datas
        :rtype: dict
        """
        data = dict()
        for n, item in enumerate(pQt.getTopItems(self.tw_tree)):
            data[n] = item.itemObj.getData()
            data[n]['childs'] = dict()
            for c in range(item.childCount()):
                data[n]['childs'][c] = item.child(c).itemObj.getData()
        if asString:
            return pprint.pformat(data)
        return data

    def getItemFromAttrValue(self, attr, value):
        """
        Get tree item considering given attribute and value

        :param attr: Item attribute name
        :type attr: str
        :param value: Item attribute value
        :type value: str
        :return: Tree item
        :rtype: QtGui.QtreeWidgetItem
        """
        for item in pQt.getAllItems(self.tw_tree):
            if hasattr(item.itemObj, attr):
                if getattr(item.itemObj, attr) == value:
                    return item

    def rf_headers(self, *args):
        """
        Refresh widget tree headers

        :param args: header labels
        :type args: list
        """
        newHeader = QtGui.QTreeWidgetItem()
        if not args:
            self.tw_tree.setColumnCount(1)
            newHeader.setText(0, 'None')
        else:
            self.tw_tree.setColumnCount(len(args))
            for n, label in enumerate(args):
                newHeader.setText(n, label)
        self.tw_tree.setHeaderItem(newHeader)

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        wList = [self.pb_itemUp, self.pb_itemDn, self.pb_template, self.cbb_filter, self.pb_add, self.pb_del,
                 self.pb_edit1, self.pb_edit2, self.pb_apply, self.pb_cancel]
        for widget in wList:
            widget.setToolTip('')

    def rf_treeColumns(self):
        """
        Refresh tree column size
        """
        for n in range(self.tw_tree.columnCount()):
            self.tw_tree.resizeColumnToContents(n)

    def rf_itemStyle(self):
        """
        refresh tree item style
        """
        for item in pQt.getAllItems(self.tw_tree) or []:
            #--- Get Color ---#
            if item in self.__editedItems__['added']:
                color = (0, 255, 0)
            elif item in self.__editedItems__['edited']:
                color = (50, 150, 255)
            elif item in self.__editedItems__['deleted']:
                color = (255, 0, 0)
            else:
                color = (200, 200, 200)
            #--- Set Color ---#
            for n in range(self.tw_tree.columnCount()):
                item.setTextColor(n, QtGui.QColor(color[0], color[1], color[2]))

    def buildFilters(self):
        """
        Build comboBox items
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Build filters ...")
        self.cbb_filter.clear()

    def buildTree(self):
        """
        Build tree widget
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Build tree ...")
        self.tw_tree.clear()

    def new_treeItem(self, itemObj):
        """
        Create or update tree item widget

        :param itemObj: Core object
        :type itemObj: Group | User
        :return: New tree item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemObj = itemObj
        self.ud_treeItem(newItem)
        for n in range(self.tw_tree.columnCount()):
            newItem.setTextAlignment(n, 5)
        return newItem

    @staticmethod
    def ud_treeItem(item, **kwargs):
        """
        Update item datas and settings

        :param item: Tree item
        :type item: newItem
        :param kwargs: Item datas
        :type kwargs: dict
        """
        #--- Clean Dict ---#
        for key in kwargs.keys():
            if key.startswith('item'):
                kwargs.pop(key)
        #--- Update ---#
        item.itemObj.update(**kwargs)

    def on_moveItem(self, side):
        """
        Command launched when 'Up' or 'Down' QPushButton is clicked

        Move selected item
        :param side: 'up' or 'down'
        :type side: str
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Move Item': %s <<<" % side)
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            movedItem = None
            #--- Get Current Index ---#
            if selItems[0].parent() is None:
                parent = None
                index = self.tw_tree.indexOfTopLevelItem(selItems[0])
            else:
                parent = selItems[0].parent()
                index = parent.indexOfChild(selItems[0])
            #--- Move Up ---#
            if side == 'up':
                if index > 0:
                    if parent is None:
                        movedItem = self.tw_tree.takeTopLevelItem(self.tw_tree.indexOfTopLevelItem(selItems[0]))
                        self.tw_tree.insertTopLevelItem((index - 1), movedItem)
                    else:
                        movedItem = parent.takeChild(parent.indexOfChild(selItems[0]))
                        parent.insertChild((index - 1), movedItem)
            #--- Move Down ---#
            else:
                if index < (self.tw_tree.topLevelItemCount()):
                    if parent is None:
                        movedItem = self.tw_tree.takeTopLevelItem(self.tw_tree.indexOfTopLevelItem(selItems[0]))
                        self.tw_tree.insertTopLevelItem((index + 1), movedItem)
                    else:
                        movedItem = parent.takeChild(parent.indexOfChild(selItems[0]))
                        parent.insertChild((index + 1), movedItem)
            #--- Select Moved Item ---#
            if movedItem is not None:
                self.tw_tree.clearSelection()
                for item in pQt.getAllItems(self.tw_tree):
                    if item == movedItem:
                        self.tw_tree.setItemSelected(movedItem, True)

    def on_filter(self):
        """
        Command launched when 'Filter' QComboBox item is clicked

        Update tree display
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Filter' ...")

    def on_addItem(self):
        """
        Command launched when 'Add' QPushButton is clicked

        Add new item to tree
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Add' ...")

    def on_delItem(self):
        """
        Command launched when 'Del' QPushButton is clicked

        Delete selected item from tree
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Del' ...")
        selItems = self.tw_tree.selectedItems() or []
        if selItems:
            if not selItems[0] in self.__editedItems__['deleted']:
                self.__editedItems__['deleted'].append(selItems[0])
                if selItems[0] in self.__editedItems__['added']:
                    self.__editedItems__['added'].remove(selItems[0])
                if selItems[0] in self.__editedItems__['edited']:
                    self.__editedItems__['edited'].remove(selItems[0])
        self.rf_itemStyle()

    def on_editItem1(self):
        """
        Command launched when 'Edit1' QPushButton is clicked

        Launch editing dialog
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Edit Item 1' ...")

    def on_editItem2(self):
        """
        Command launched when 'Edit2' QPushButton is clicked

        Launch editing dialog
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Edit Item 2' ...")

    def on_apply(self):
        """
        Command launched when 'Apply' QPushButton is clicked

        Store datas to itemObject
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Apply' ...")
        self.__edited__ = True

    def on_save(self):
        """
        Command launched when 'Save' QPushButton is clicked

        Save data
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Save %s' ..." % self.treeTitle)

    def on_cancel(self):
        """
        Command launched when 'Cancel' QPushButton is clicked

        Restore datas from itemObject
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Cancel' ...")
        self._initWidget()
        self.buildTree()
        self.__edited__ = False

    def on_discard(self):
        """
        Command launched when 'Discard' QPushButton is clicked

        Discard edited data
        """
        if hasattr(self, 'log'):
            self.log.detail(">>> Launch 'Discard %s' ..." % self.treeTitle)
        self.__editedItems__ = dict(added=[], edited=[], deleted=[])
        self._initWidget()
