import sip
from PyQt4 import QtCore
try:
    import maya.OpenMayaUI as mOpen
except:
    pass


def getMayaMainWindow():
    """
    Get maya main window

    :return: Maya main window
    :rtype: QtCore.QObject
    """
    return sip.wrapinstance(long(mOpen.MQtUtil.mainWindow()), QtCore.QObject)
