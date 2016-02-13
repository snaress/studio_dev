import sys
from PyQt4 import QtGui
import widgetsUi


def launchWidget(widgetName):
    """
    Launch given widget class name

    :param widgetName: Widget class name ('Range')
    :type widgetName: str
    """
    #-- Init --"
    app = QtGui.QApplication(sys.argv)
    widget = None
    #-- Range --#
    if widgetName == 'Range':
        widget = widgetsUi.Range()
    #-- Launch Widget --#
    if widget is not None:
        print ">>>> Launching %s" % widgetName
        print widget.__doc__
        widget.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        launchWidget(sys.argv[-1])
    else:
        launchWidget('Range')
