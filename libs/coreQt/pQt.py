import os
from PyQt4 import QtGui
from coreSys import env


#========================================== COMPILE UI ===========================================#

class CompileUi(object):
    """
    CompileUi Class: Convert given ui file or path to python file into dstUi path or file

    :param pyUic: pyuic.bat absolut path (default: coreSystem.env.pyUic)
    :type pyUic: str
    """

    def __init__(self, pyUic=None):
        self.srcDir = None
        self.dstDir = None
        self.srcFile = None
        self.dstFile = None
        self.pyUic = pyUic
        if self.pyUic is None:
            self.pyUic = env.pyUic

    def compileDir(self, srcDir=None, dstDir=None):
        """
        Compile given source directory considering given destination

        :param srcDir: Source ui path
        :type srcDir: str
        :param dstDir: Destination ui path (If None, use srcDir as destination)
        :type dstDir: str
        """
        print "#----- Compile UI Directory -----#"
        #--- Check Data ---#
        self.srcDir = srcDir
        self.dstDir = dstDir
        self._checkDir()
        print "SRC Path: %s\nDST Path: %s" % (self.srcDir, self.dstDir)
        #--- Convert ---#
        files = os.listdir(self.srcDir) or []
        for f in files:
            if f.endswith('.ui'):
                uiFile = os.path.join(self.srcDir, f)
                pyFile = os.path.join(self.dstDir, f.replace('.ui', 'UI.py'))
                if self._checkDate(uiFile, pyFile) in ['create', 'update']:
                    self.convert(uiFile, pyFile)

    def compileFile(self, srcFile=None, dstFile=None):
        """
        Compile given source file considering given destination file

        :param srcFile: Source ui file absolut path
        :type srcFile: str
        :param dstFile: Destination ui file absolut path
        :type dstFile: str
        """
        print "#----- Compile UI File -----#"
        #--- Check Data ---#
        self.srcFile = srcFile
        self.dstFile = dstFile
        self._checkFile()
        print "SRC File: %s\nDST File: %s" % (self.srcFile, self.dstFile)
        #--- Convert ---#
        if self.srcFile.endswith('.ui'):
            uiFile = self.srcFile
            if not self.dstFile.endswith('UI.py'):
                pyFile = self.dstFile.replace('.py', 'UI.py')
            else:
                pyFile = self.dstFile
            if self._checkDate(uiFile, pyFile) in ['create', 'update']:
                self.convert(uiFile, pyFile)

    def convert(self, uiFile, pyFile):
        """
        Convert uiFile into pyFile

        :param uiFile: uiFile absolut path
        :type uiFile: str
        :param pyFile: pyFile absolut path
        :type pyFile: str
        """
        try:
            os.system("%s %s > %s" % (self.pyUic, uiFile, pyFile))
        except:
            raise IOError("!!! ERROR: Can not convert %s !!!" % pyFile)

    def _checkDir(self):
        """
        Check given ui pathes
        """
        #--- Check Source Directory ---#
        if self.srcDir is None:
            raise AttributeError("!!! ERROR: 'srcDir' can not be None !!!")
        if not os.path.exists(self.srcDir):
            raise IOError("!!! ERROR: 'srcDir' not found: %s !!!" % self.srcDir)
        #--- Check Destination Directory ---#
        if self.dstDir is None:
            self.dstDir = self.srcDir
        if not os.path.exists(self.dstDir):
            raise IOError("!!! ERROR: 'dstDir' not found: %s !!!" % self.dstDir)

    def _checkFile(self):
        """
        Check given ui files
        """
        #--- Check Source File ---#
        if self.srcFile is None:
            raise AttributeError("!!! ERROR: 'srcFile' can not be None !!!")
        if not os.path.isabs(self.srcFile):
            raise IOError("!!! ERROR: 'srcFile' should be absolute path: %s !!!" % self.srcFile)
        if not self.srcFile.endswith('.ui'):
            raise IOError("!!! ERROR: 'srcFile' should ends with '.ui': %s !!!" % self.srcFile)
        if not os.path.exists(self.srcFile):
            raise IOError("!!! ERROR: 'srcFile' not found: %s !!!" % self.srcFile)
        #--- Check Destination File ---#
        if self.dstFile is None:
            self.dstFile = os.path.join(os.path.dirname(self.srcFile), os.path.basename(self.dstFile))
        if not os.path.isabs(self.dstFile):
            raise IOError("!!! ERROR: 'dstFile' should be absolute path: %s !!!" % self.dstFile)
        if not self.dstFile.endswith('.py'):
            raise IOError("!!! ERROR: 'srcFile' should ends with '.py': %s !!!" % self.srcFile)
        if not os.path.exists(os.path.dirname(self.dstFile)):
            raise IOError("!!! ERROR: 'dstFile' directory not found: %s !!!" % os.path.dirname(self.dstFile))

    @staticmethod
    def _checkDate(uiFile, pyFile):
        """
        Compare uiFile and pyFile modif date

        :param uiFile: uiFile absolut path
        :type uiFile: str
        :param pyFile: pyFile absolut path
        :type pyFile: str
        :return: 'create', 'update', 'ok'
        :rtype: str
        """
        if pyFile is None:
            print "%s \t ---> \t CREATE" % os.path.basename(pyFile)
            return 'create'
        else:
            if not os.path.exists(pyFile):
                print "%s \t ---> \t CREATE" % os.path.basename(pyFile)
                return 'create'
            else:
                uiDate = os.path.getmtime(uiFile)
                pyDate = os.path.getmtime(pyFile)
                if uiDate > pyDate:
                    print "%s \t ---> \t UPDATE" % os.path.basename(pyFile)
                    return 'update'
                else:
                    print "%s \t ---> \t OK" % os.path.basename(pyFile)
                    return 'ok'

#========================================== TREE WIDGET ==========================================#

def getAllItems(QTreeWidget):
    """
    Get all QTreeWidgetItem of given QTreeWidget

    :param QTreeWidget: QTreeWidget object
    :type QTreeWidget: QtGui.QTreeWidget
    :return: All QTreeWidgetItem list
    :rtype: list
    """
    items = []
    allItems = QtGui.QTreeWidgetItemIterator(QTreeWidget, QtGui.QTreeWidgetItemIterator.All) or None

    if allItems is not None:
        while allItems.value():
            item = allItems.value()
            items.append(item)
            allItems += 1

    return items

def getTopItems(QTreeWidget):
    """
    Get all topLevelItems of given QTreeWidget

    :param QTreeWidget: QTreeWidget object
    :type QTreeWidget: QtGui.QTreeWidget
    :return: All topLevelItem list
    :rtype: list
    """
    items = []
    nTop = QTreeWidget.topLevelItemCount()

    for n in range(nTop):
        items.append(QTreeWidget.topLevelItem(n))

    return items

def getAllChildren(QTreeWidgetItem, depth=-1):
    """
    Get all children of given QTreeWidgetItem

    :param QTreeWidgetItem: Recusion start QTreeWidgetItem
    :type QTreeWidgetItem: QtGui.QTreeWidgetItem
    :param depth: Number of recursion (-1 = infinite)
    :type depth: int
    :return: QTreeWigdetItem list
    :rtype: list
    """
    items = []

    def recurse(currentItem, depth):
        items.append(currentItem)
        if depth != 0:
            for n in range(currentItem.childCount()):
                recurse(currentItem.child(n), depth-1)

    recurse(QTreeWidgetItem, depth)
    return items

def getAllParent(QTreeWidgetItem, depth=-1):
    """
    Get all parent of given QTreeWidgetItem

    :param QTreeWidgetItem: Recusion start QTreeWidgetItem
    :type QTreeWidgetItem: QtGui.QTreeWidgetItem
    :param depth: Number of recursion (-1 = infinite)
    :type depth: int
    :return: QTreeWigdetItem list
    :rtype: list
    """
    items = []

    def recurse(currentItem, depth):
        items.append(currentItem)
        if depth != 0:
            if currentItem.parent() is not None:
                recurse(currentItem.parent(), depth-1)

    recurse(QTreeWidgetItem, depth)
    return items

#=========================================== COMBO BOX ===========================================#

def getComboBoxItems(QComboBox):
    """
    Get all given conboBox items

    :param QComboBox: QComboBox
    :type QComboBox: QtGui.QComboBox
    :return: Items text list
    :rtype: list
    """
    items = []
    for n in range(QComboBox.count()):
        items.append(str(QComboBox.itemText(n)))
    return items

#============================================ DIALOGS ============================================#

def errorDialog(message, parent, raiseError=False):
    """
    Launch default error dialog
    
    :param message: Message to print
    :type message: str | list
    :param parent: Parent ui
    :type parent: QtGui.QMainWindow | QtGui.QWidget
    :param raiseError: Raise error state
    :type raiseError: bool
    """
    errorDial = QtGui.QErrorMessage(parent)
    if isinstance(message, list):
        errorDial.showMessage('\n'.join(message))
    else:
        errorDial.showMessage(message)
    if raiseError:
        raise AttributeError(message)

def fileDialog(fdMode='open', fdFileMode='AnyFile', fdRoot=None, fdRoots=None, fdFilters=None, fdCmd=None):
    """
    FileDialog popup
    
    :param fdMode: setAcceptMode 'open' or 'save'
    :type fdMode: str
    :param fdFileMode: setFileMode 'AnyFile', 'ExistingFile', 'Directory', 'DirectoryOnly'
    :type fdFileMode: str
    :param fdRoot: Start root path
    :type fdRoot: str
    :param fdRoots: List of recent files (list[str(QUrl)])
    :type fdRoots: list
    :param fdFilters: List of extensions
    :type fdFilters: list
    :param fdCmd: Command for accepted execution
    :type fdCmd: function
    :return: QFileDialog widget object
    :rtype: QtGui.QFileDialog
    """
    fd = QtGui.QFileDialog()
    #--- FileDialog AcceptedMode ---#
    if fdMode == 'open':
        fd.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
    elif fdMode == 'save':
        fd.setAcceptMode(QtGui.QFileDialog.AcceptSave)
    #--- FileDialog FileMode ---#
    if fdFileMode == 'AnyFile':
        fd.setFileMode(QtGui.QFileDialog.AnyFile)
    elif fdFileMode == 'ExistingFile':
        fd.setFileMode(QtGui.QFileDialog.ExistingFile)
    elif fdFileMode == 'Directory':
        fd.setFileMode(QtGui.QFileDialog.Directory)
    elif fdFileMode == 'DirectoryOnly':
        fd.setFileMode(QtGui.QFileDialog.DirectoryOnly)
    #--- FileDialog Params ---#
    if fdRoot is not None:
        fd.setDirectory(fdRoot)
    if fdRoots is not None:
        fd.setSidebarUrls(fdRoots)
    if fdFilters is not None:
        fd.setFilters(fdFilters)
    if fdCmd is not None:
        # noinspection PyUnresolvedReferences
        fd.accepted.connect(fdCmd)
    #--- Result ---#
    return fd

#========================================== STYLE SHEET ==========================================#

class Style(object):
    """
    Style Class: Contains ui styleSheets
    """

    def __init__(self):
        self.col = "color"
        self.bgCol = "background-color"
        self.aBgCol = "alternate-background-color"

    @property
    def styles(self):
        """
        Get avalaible styles

        :return: StyleSheets
        :rtype: list
        """
        return ['default', 'darkGrey']

    @property
    def default(self):
        """
        Default Ui styleSheet

        :return: Style sheet
        :rtype: str
        """
        return ""

    @property
    def darkGrey(self):
        """
        Dark Grey Ui styleSheet

        :return: Style sheet
        :rtype: str
        """
        #--- Values ---#
        color_1 = "rgb(200, 200, 200)"
        bgColor_1 = "rgb(50, 50, 50)"
        bgColor_2 = "rgb(40, 40, 40)"
        bgColor_3 = "rgb(65, 65, 65)"
        #--- Style Sheet ---#
        style = ["QWidget {%s: %s; %s: %s; %s: %s;}" % (self.bgCol, bgColor_1,
                                                        self.aBgCol, bgColor_2,
                                                        self.col, color_1),
                 "QPushButton:hover, QLineEdit:hover, QTabBar::tab:hover {%s: %s}" % (self.bgCol, bgColor_3),
                 "QMenuBar::item {%s: %s; %s: %s;}" % (self.bgCol, bgColor_1,
                                                       self.col, color_1),
                 "QMenuBar::item:selected, QMenu::item:selected {%s: %s}" % (self.bgCol, bgColor_3),
                 "QHeaderView::section {%s: %s;}" % (self.bgCol, bgColor_1),
                 "QProgressBar {border: %s;}" % bgColor_1,
                 "QLineEdit {%s: %s}" % (self.bgCol, bgColor_2),
                 "QTabBar::tab {%s: %s;}" % (self.bgCol, bgColor_2),
                 "QTabBar::tab:selected {%s: %s;}" % (self.bgCol, bgColor_1)]
        #--- Result ---#
        return ''.join(style)

    def getStyle(self, style):
        """
        Get styleSheet from given style

        :param style: StyleSheet name (must be in self.styles)
        :type style: str
        :return: StyleSheet
        :rtype: str
        """
        if style in self.styles:
            if style == 'default':
                return self.default
            elif style == 'darkGrey':
                return self.darkGrey
