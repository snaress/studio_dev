import os
from coreSys import pFile
import userGroups


class Foundation(object):
    """
    Foundation Class: Contains foundation datas, main core object

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    """

    __user__ = os.environ['USERNAME']
    __rootPath__ = "E:/foundation"
    __projectsPath__ = pFile.conformPath(os.path.join(__rootPath__, "projects"))
    __settingsPath__ = pFile.conformPath(os.path.join(__rootPath__, "settings"))

    def __init__(self, logLvl='info'):
        self._setup(logLvl)
        self._groups = userGroups.Groups(self)
        self._users = userGroups.Users(self)

    def _setup(self, logLvl):
        """
        Setup Foundation core object
        """
        #--- Init Log ---#
        self.log = pFile.Logger(title=self.__class__.__name__, level=logLvl)
        self.log.info("########## %s ##########" % self.__class__.__name__, newLinesBefore=1)
        #--- Create Tool Paths ---#
        self.log.debug("#--- Check Paths ---#")
        paths = [self.__rootPath__, self.__projectsPath__, self.__settingsPath__]
        pFile.createPath(paths, log=self.log)


if __name__ == '__main__':
    fdn = Foundation(logLvl='detail')
    print fdn._users
    # child = fdn._groups.newChild()
    # child.update(grpCode='test')
    # print child.__str__()
    # print child.__dict__