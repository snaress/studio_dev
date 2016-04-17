from PyQt4 import QtGui
from foundation_old.gui._ui import fdnInfoViewUI
from foundation_old.gui.widgets import entityInfo


class InfoView(QtGui.QWidget, fdnInfoViewUI.Ui_wg_infoView):
    """
    InfoView class: Contains foundation main ui data

    :param mainUi: Parent main ui
    :type mainUi: foundation.gui.FoundationUi
    """

    def __init__(self, mainUi):
        super(InfoView, self).__init__()
        self.mainUi = mainUi
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
        #--- Widgets ---#
        self.wg_entityInfo = entityInfo.EntityInfo(self.mainUi)
        self.gl_entityInfo.addWidget(self.wg_entityInfo)

    def refresh(self):
        """
        Refresh active info tab
        """
        if self.mainUi.currentInfoTab == 'Entity Info':
            self.wg_entityInfo.refresh()
