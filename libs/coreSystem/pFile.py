import os, math, time


def conformPath(path):
    """
    Comform path separator with '/'

    :param path: Path to conform
    :type path: str
    :return: Conformed path
    :rtype: str
    """
    return path.replace('\\', '/')

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
    #-- Check Args --#
    if isinstance(paths, basestring):
        paths = [paths]
    #-- Create Paths --#
    for path in paths:
        if recursive:
            if root is None:
                mess = "!!! In recursive mode, root can not be None !!!"
                if log is not None:
                    log.critical(mess)
                else:
                    print mess
                raise AttributeError(mess)
            #-- Decompose Folders --#
            folders = path.replace('%s/' % root, '').split('/')
            recPath = root
            for fld in folders:
                recPath = conformPath(os.path.join(recPath, fld))
                makeDir(recPath, log=log)
        else:
            makeDir(path, log=log)

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
