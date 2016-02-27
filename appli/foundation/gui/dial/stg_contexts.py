import os
from PyQt4 import QtGui
from coreQt.widgets import basicTreeUi
from foundation.gui._ui import ts_contextDialUI


class Contexts(basicTreeUi.BasicTree):
    """
    Groups Class: Contains UserGroups settings, child of ToolSettings

    :param pWidget: Parent widget
    :type pWidget: dialogs.ToolSettings
    """

    def __init__(self, pWidget):
        self.pWidget = pWidget
        self.mainUi = self.pWidget.parent()
        self._fdn = self.pWidget._fdn
        self._project = self._fdn._project
        self._users = self._fdn._users
        super(Contexts, self).__init__(pWidget)

    def _initWidget(self):
        """
        Init widget core
        """
        self.log = self.pWidget.log
        super(Contexts, self)._initWidget()

    def _setupIcons(self):
        """
        Setup Groups icons
        """
        super(Contexts, self)._setupIcons()
        #--- Init Icons ---#
        self.iconPush = QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'pinBlue.png'))
        #--- Add Icons ---#
        self.pb_edit1.setIcon(self.iconPush)
        #--- Edit Label ---#
        self.pb_edit1.setText("Push")
        #--- Edit Grade ---#
        if not self._users._user.grade == 0:
            self.pb_del.setEnabled(False)

    def _setupWidget(self):
        """
        Setup Groups widget
        """
        super(Contexts, self)._setupWidget()
        self.l_title.setText(self.__class__.__name__)
        self.cbb_filter.setVisible(False)
        self.pb_edit2.setVisible(False)
        self.qf_treeEdit_R.setVisible(False)
        self.rf_headers('Name', 'Label', 'Folder')
        self.rf_treeColumns()

    def rf_toolTips(self):
        """
        Refresh widgets toolTips
        """
        if self.mainUi.showToolTips:
            self.pb_itemUp.setToolTip("Move up selected group")
            self.pb_itemDn.setToolTip("Move down selected group")
            self.pb_template.setToolTip("Open templates")
            self.pb_add.setToolTip("Create new context")
            self.pb_del.setToolTip("Delete selected context")
            self.pb_edit1.setToolTip("Push selected context as template")
            self.pb_apply.setToolTip("Apply datas to Foundation object")
            self.pb_cancel.setToolTip("Restore datas from Foundation object")
            #--- Edit Grade ---#
            if not self._users._user.grade == 0:
                self.pb_del.setToolTip("Delete selected context (Disabled for your grade)")
        else:
            super(Contexts, self).rf_toolTips()


class ContextsDialog(QtGui.QDialog, ts_contextDialUI.Ui_dial_context):
    """
    Contexts Dialog: Conexts edition, child of Contexts

    :param dialogMode: 'add' or 'edit'
    :type dialogMode: str
    :param selItem: Selected context item
    :type selItem: newItem
    :param parent: Parent Ui
    :type parent: Contexts
    """

    def __init__(self, dialogMode='add', selItem=None, parent=None):
        self.dialogMode = dialogMode
        self.selItem = selItem
        super(ContextsDialog, self).__init__(parent)
        self.pWidget = parent
        self.mainUi = self.pWidget.mainUi
        self._project = self.pWidget._project
        self._setupUi()

    def _setupUi(self):
        """
        Setup QtGui Groups dialog
        """
        self.log = self.pWidget.log
        self.log.title = self.__class__.__name__
        self.log.detail("#----- Setup %s Ui -----#" % self.__class__.__name__)
        self.setupUi(self)