from PyQt4 import QtGui
from coreQt import dialogs


dialogs.compileUi('dial_confirm.ui')
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



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    window = Confirm()
    window.show()
    sys.exit(app.exec_())
