import os
from coreQt import pQt
from PyQt4 import QtGui
from coreSystem import pMath
from coreQt.widgets import treeWidgets


class Groups(treeWidgets.BasicTree):
    """
    Groups Class: Contains UserGroups settings, child of ToolSettings

    :param pWidget: Parent widget
    :type pWidget: dialogs.ToolSettings
    """

    def __init__(self, pWidget):
        self.pWidget = pWidget
        self.log = self.pWidget.log
        self.mainUi = self.pWidget.parent()
        self.fdn = self.pWidget.fdn
        self.userGrps = self.fdn.userGrps
        self.users = self.fdn.users
        super(Groups, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        super(Groups, self)._initWidget()
        self.userGrps.buildFromSettings()

    def _setupIcons(self):
        """
        Setup Groups icons
        """
        super(Groups, self)._setupIcons()
        #-- Init Icons --#
        self.iconStyle = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'style.png'))
        #-- Add Icons --#
        self.pb_edit2.setIcon(self.iconStyle)
        #-- Edit Label --#
        self.pb_edit1.setText("Edit")
        self.pb_edit2.setText("Style")
        #-- Edit Grade --#
        if not self.users._user.grade == 0:
            self.pb_del.setEnabled(False)

    def _setupWidget(self):
        """
        Setup Groups widget
        """
        super(Groups, self)._setupWidget()
        self.l_title.setText('Groups')
        self.pb_template.setVisible(False)
        self.cbb_filter.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.tw_tree.header().setStretchLastSection(False)
        self.rf_headers('Code', 'Name', 'Grade', 'Style')
        self.rf_treeColumns()

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        if self.mainUi.showToolTips:
            self.pb_itemUp.setToolTip("Move up selected group")
            self.pb_itemDn.setToolTip("Move down selected group")
            self.pb_add.setToolTip("Create new user group")
            self.pb_del.setToolTip("Delete selected group")
            self.pb_edit1.setToolTip("Edit selected group")
            self.pb_edit2.setToolTip("Update style auto")
            self.pb_apply.setToolTip("Apply datas to Foundation object")
            self.pb_cancel.setToolTip("Restore datas from Foundation object")
            #-- Edit Grade --#
            if not self.users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected group (Disabled for your grade)")
        else:
            super(Groups, self).rf_toolTips()

    def buildTree(self):
        """
        Build Groups tree widget
        """
        super(Groups, self).buildTree()
        self.log.detail("---> Groups tree")
        if self.userGrps._groups:
            grpItems = []
            for grpObj in self.userGrps._groups:
                newItem = self.new_treeItem(grpObj)
                grpItems.append(newItem)
            self.tw_tree.addTopLevelItems(grpItems)
        self.rf_treeColumns()
        self.rf_itemStyle()

    def ud_treeItem(self, item, **kwargs):
        """
        Update item data and settings

        :param item: Group tree item
        :type item: newItem
        :param kwargs: Group item data (key must starts with 'grp')
        :type kwargs: dict
        """
        super(Groups, self).ud_treeItem(item, **kwargs)
        #-- Edit Item --#
        item.setText(0, item.itemObj.grpCode)
        item.setText(1, item.itemObj.grpName)
        item.setText(2, str(item.itemObj.grpGrade))
        item.setBackgroundColor((self.tw_tree.columnCount() - 1), QtGui.QColor(item.itemObj.grpColor[0],
                                                                               item.itemObj.grpColor[1],
                                                                               item.itemObj.grpColor[2]))

    def on_editItem2(self):
        """
        Command launched when 'Style' QPushButton is clicked

        Auto assign color to all items
        """
        super(Groups, self).on_editItem2()
        N = len(pQt.getTopItems(self.tw_tree))
        for n, item in enumerate(pQt.getTopItems(self.tw_tree)):
            if n == 0:
                rgb = (255, 0, 0)
            elif n == (len(pQt.getTopItems(self.tw_tree)) - 1):
                rgb = (0, 0, 255)
            elif n < (N / 2):
                rgb = (pMath.linear(0, (N / 2), 255, 0, n), pMath.linear(0, (N / 2), 0, 255, n), 0)
            else:
                rgb = (0, pMath.linear((N / 2), N, 255, 0, n), pMath.linear((N / 2), N, 0, 255, n))
            self.ud_treeItem(item, grpColor=rgb)
            if (not item in self.__editedItems__['added'] and not item in self.__editedItems__['edited'] and
                not item in self.__editedItems__['deleted']):
                self.__editedItems__['edited'].append(item)
        self.rf_itemStyle()

    def on_cancel(self):
        """
        Command launched when 'Cancel' QPushButton is clicked

        Restore datas from itemObject
        """
        super(Groups, self).on_cancel()
        self.pWidget.rf_editedItemStyle()
