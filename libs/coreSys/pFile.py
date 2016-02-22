import os, math, time, pprint


def conformPath(path):
    """
    Comform path separator with '/'

    :param path: Path to conform
    :type path: str
    :return: Conformed path
    :rtype: str
    """
    return path.replace('\\', '/')

def pathToDict(path, conformed=False):
    """
    Translate directory contents to dict

    :param path: Absolut path
    :type path: str
    :param conformed: Conform path before storing
    :type conformed: bool
    :return: Path contents
    :rtype: dict
    """
    #--- Check Path ---#
    if not os.path.exists(path):
        raise IOError, "!!! ERROR: Path not found!!!\n%s" % path
    #--- Parsing ---#
    pathDict = {'_order': []}
    for root, flds, files in os.walk(path):
        if conformed:
            rootPath = conformPath(root)
        else:
            rootPath = root
        pathDict['_order'].append(rootPath)
        pathDict[rootPath] = {'folders': flds, 'files': files}
    #--- Result ---#
    return pathDict

def makeDir(path, log=None):
    """
    Create Given Path

    :param path: Directory full path
    :type path: str
    :param log: Log object (verbose)
    :type log: Logger
    """
    if not os.path.exists(path):
        try:
            os.mkdir(path)
            if log is not None:
                log.debug("Path Created: %s" % path)
            else:
                print "Path Created: %s" % path
        except:
            mess = "!!! Can not create path: %s !!!" % path
            if log is not None:
                log.critical(mess)
            else:
                print mess
            raise IOError(mess)

def createPath(paths, recursive=False, root=None, log=None):
    """
    Create given path list

    :param paths: Paths to create
    :type paths: str | list
    :param recursive: Create paths recursively considering 'root'
    :type recursive: bool
    :param root: Root path for recursive methode
    :type root: str
    :param log: Log object (verbose)
    :type log: Logger
    """
    #--- Check Args ---#
    if isinstance(paths, basestring):
        paths = [paths]
    #--- Create Paths ---#
    for path in paths:
        if recursive:
            if root is None:
                mess = "!!! In recursive mode, root can not be None !!!"
                if log is not None:
                    log.critical(mess)
                else:
                    print mess
                raise AttributeError(mess)
            #--- Decompose Folders ---#
            folders = path.replace('%s/' % root, '').split('/')
            recPath = root
            for fld in folders:
                recPath = conformPath(os.path.join(recPath, fld))
                makeDir(recPath, log=log)
        else:
            makeDir(path, log=log)

def readFile(filePath):
    """
    Get text from file

    :param filePath: File absolut path
    :type filePath: str
    :return: Text line by line
    :rtype: list
    """
    if not os.path.exists(filePath):
        raise IOError, "!!! Error: Can't read, file doesn't exists !!!"
    fileId = open(filePath, 'r')
    getText = fileId.readlines()
    fileId.close()
    return getText

def readDictFile(filePath):
    """
    Read dict pyFile

    :param filePath: File absolut path
    :type filePath: str
    :return: Translated dictionnary
    :rtype: dict
    """
    fileLines = ''.join(readFile(filePath))
    if not fileLines in ['', ' ']:
        return eval(''.join(fileLines))
    else:
        return dict()

def readPyFile(filePath, keepBuiltin=False):
    """
    Get text from pyFile

    :param filePath: Python file absolut path
    :type filePath: str
    :param keepBuiltin: Keep builtins key
    :type keepBuiltin: bool
    :return: File dict
    :rtype: dict
    """
    if not os.path.exists(filePath):
        raise IOError, "!!! Error: Can't read, file doesn't exists !!!"
    params = {}
    execfile(filePath, params)
    if keepBuiltin:
        return params
    else:
        if '__builtins__' in params.keys():
            params.pop('__builtins__')
            return params

def writeFile(filePath, textToWrite, add=False):
    """
    Create and edit text file. If file already exists, it is overwritten

    :param filePath: File absolut path
    :type filePath: str
    :param textToWrite: Text to edit in file
    :type textToWrite: str | list
    :param add: Add text to existing one in file
    :type add: bool
    """
    oldTxt = ""
    if add:
        oldTxt = ''.join(readFile(filePath))
        if not oldTxt.endswith('\n'):
            oldTxt = "%s\n" % oldTxt
    fileId = open(filePath, 'w')
    if add:
        fileId.write(oldTxt)
    if isinstance(textToWrite, str):
        fileId.write(textToWrite)
    elif isinstance(textToWrite, (list, tuple)):
        fileId.writelines(textToWrite)
    fileId.close()

def writeDictFile(filePath, dictToWrite):
    """
    Create readable text file from given dict

    :param filePath: File absolut path
    :type filePath: str
    :param dictToWrite: Dict to translate and print
    :type dictToWrite: dict
    """
    fileId = open(filePath, 'w')
    fileId.write(pprint.pformat(dictToWrite))
    fileId.close()

# noinspection PyTypeChecker
def fileSizeFormat(_bytes, precision=2):
    """
    Returns a humanized string for a given amount of bytes

    :param _bytes: File size in bytes
    :type _bytes: int
    :param precision: Precision after coma
    :type precision: int
    :return: Humanized string
    :rtype: str
    """
    _bytes = int(_bytes)
    if _bytes is 0:
        return '0 b'
    log = math.floor(math.log(bytes, 1024))
    return "%.*f %s" % (precision, bytes / math.pow(1024, log),
                       ['b', 'kb', 'mb', 'gb', 'tb','pb', 'eb', 'zb', 'yb'][int(log)])

def secondsToStr(seconds):
    """
    Convert number of seconds into humanized string

    :param seconds: Number of seconds
    :type seconds: int
    :return: Humanized string
    :rtype: str
    """
    S = int(seconds)
    hours = S / 3600
    S -= hours * 3600
    minutes = S / 60
    seconds = S - (minutes * 60)
    return "%s:%s:%s" % (hours, minutes, seconds)

def getDate():
    """
    Get current date

    :return: yyyy_mm_dd
    :rtype: str
    """
    return time.strftime("%Y_%m_%d")

def getTime():
    """
    Get current time

    :return: hh_mm_ss
    :rtype: str
    """
    return time.strftime("%H_%M_%S")


class Logger(object):
    """
    Print given message using log levels

    :param title: Log title
    :type title: str
    :param level: Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type level: str
    :param showTime: Add current time in log header
    :type showTime: bool
    """

    def __init__(self, title='LOG', level='info', showTime=False):
        self.levels = ['critical', 'error', 'warning', 'info', 'debug', 'detail']
        self.title = title
        self.level = level
        self.showTime = showTime

    @property
    def lvlIndex(self):
        """
        Get current level index

        :return: Current level index
        :rtype: int
        """
        return self.levels.index(self.level)

    def printLog(self, message, newLinesBefore, newLinesAfter, level):
        """
        Print given message with given level

        :param message: Message to print
        :type message: str
        :param newLinesBefore: New lines to insert befor message
        :type newLinesBefore: int
        :param newLinesAfter: New lines to insert after message
        :type newLinesAfter: int
        :param level: Log level 'critical', 'error', 'warning', 'info', 'debug', 'detail')
        :type level: str
        """
        self._addNewLines(newLinesBefore)
        if self.showTime:
            print "| %s | %s | %s | %s" % (self.title, level, self.currentTime, message)
        else:
            print "| %s | %s | %s" % (self.title, level, message)
        self._addNewLines(newLinesAfter)

    def critical(self, message, newLinesBefore=0, newLinesAfter=0):
        if self.lvlIndex >= 0:
            self.printLog(message, newLinesBefore, newLinesAfter, 'Critical')

    def error(self, message, newLinesBefore=0, newLinesAfter=0):
        if self.lvlIndex >= 1:
            self.printLog(message, newLinesBefore, newLinesAfter, 'Error')

    def warning(self, message, newLinesBefore=0, newLinesAfter=0):
        if self.lvlIndex >= 2:
            self.printLog(message, newLinesBefore, newLinesAfter, 'Warning')

    def info(self, message, newLinesBefore=0, newLinesAfter=0):
        if self.lvlIndex >= 3:
            self.printLog(message, newLinesBefore, newLinesAfter, 'Info')

    def debug(self, message, newLinesBefore=0, newLinesAfter=0):
        if self.lvlIndex >= 4:
            self.printLog(message, newLinesBefore, newLinesAfter, 'Debug')

    def detail(self, message, newLinesBefore=0, newLinesAfter=0):
        if self.lvlIndex >= 5:
            self.printLog(message, newLinesBefore, newLinesAfter, 'Detail')

    @property
    def currentTime(self):
        """
        Get current time

        :return: Current time
        :rtype: str
        """
        return getTime().replace('_', ':')

    @staticmethod
    def _addNewLines(newLines):
        """
        Print new empty lines

        :param newLines: Number of new lines to print
        :type newLines: int
        """
        if newLines > 0:
            if newLines == 1:
                print ""
            else:
                print '\n' * (newLines - 1)
