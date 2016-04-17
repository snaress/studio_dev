from PyQt4 import QtGui
from foundation_old.gui._ui import wg_entityInfoUI, wi_entityInfoUI


class EntityInfo(QtGui.QWidget, wg_entityInfoUI.Ui_wg_tabInfo):
    """
    EntityInfo class: Contains foundation entities data

    :param mainUi: Parent main ui
    :type mainUi: foundation.gui.FoundationUi
    """

    def __init__(self, mainUi):
        super(EntityInfo, self).__init__()
        self.mainUi = mainUi
        self.mainTree = self.mainUi.wg_mainTree
        self.log = self.mainUi.log
        self._fdn = self.mainUi._fdn
        #--- Setup ---#
        self._setupWidget()

    def _setupWidget(self):
        """
        Setup widget Ui
        """
        self.setupUi(self)
        #--- Init ---#
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)

    def refresh(self):
        """
        Refresh widget
        """
        self.buildTree()

    def buildTree(self):
        """
        Build entity tree
        """
        self.tw_entities.clear()
        selItems = self.mainTree.currentSelection
        if selItems:
            entities = []
            itemObj = selItems[0].itemObj
            #--- Get Entities ---#
            if itemObj.__class__.__name__ == 'Entity':
                entities = itemObj._parent.entities
            elif itemObj.__class__.__name__ == 'CtxtEntity':
                if itemObj.contextType == 'subType':
                    entities = itemObj.entities
                else:
                    entities = itemObj.getChildrenEntities(keepParentEntities=True)
            #--- Populate Tree ---#
            for entity in entities:
                newItem = self.new_entityItem(entity)
                self.tw_entities.addTopLevelItem(newItem)
                self.tw_entities.setItemWidget(newItem, 0, newItem.itemWidget)

    def new_entityItem(self, entityObj):
        """
        Create entity item

        :param entityObj: Entity object
        :type entityObj: Entity
        :return: Entity item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemObj = entityObj
        newItem.itemWidget = EntityNode(self, newItem)
        return newItem


class EntityNode(QtGui.QWidget, wi_entityInfoUI.Ui_wi_entityInfo):
    """
    EntityNode class: Contains entity info

    :param pWidget: Parent  ui
    :type pWidget: EntityInfo
    :param pItem: Parent item
    :type pItem: EntityInfo.new_entityItem
    """

    def __init__(self, pWidget, pItem):
        super(EntityNode, self).__init__()
        self.pWidget = pWidget
        self.pItem = pItem
        self.mainUi = self.pWidget.mainUi
        self.entityObj = self.pItem.itemObj
        self.log = self.mainUi.log
        self._fdn = self.mainUi._fdn
        #--- Setup ---#
        self._setupWidget()

    def _setupWidget(self):
        """
        Setup widget Ui
        """
        self.setupUi(self)
        #--- Init ---#
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        #--- Refresh ---#
        self.refresh()

    def refresh(self):
        """
        refresh node
        """
        self.l_mainTypeValue.setText(self.entityObj.entityMainType)
        self.l_subTypeValue.setText(self.entityObj.entitySubType)
        self.l_nameValue.setText(self.entityObj.entityName)
        self.l_codeValue.setText(self.entityObj.entityCode)
