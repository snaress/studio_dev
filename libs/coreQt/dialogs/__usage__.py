import sys
from PyQt4 import QtGui
import dialogsUi


def launchDialog(dialogName):
    """
    Launch given dialog class name

    :param dialogName: Dialog class name ('Settings')
    :type dialogName: str
    """
    #-- Init --"
    app = QtGui.QApplication(sys.argv)
    dialog = None
    #-- Range --#
    if dialogName == 'Settings':
        dialog = dialogsUi.Settings()
    #-- Launch Widget --#
    if dialog is not None:
        print ">>>> Launching %s" % dialogName
        print dialog.__doc__
        dialog.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        launchDialog(sys.argv[-1])
    else:
        launchDialog('Settings')