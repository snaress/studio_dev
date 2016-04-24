import os
from coreSys import pFile
import userGroups, users, project


class Fondation(object):
    """
    Fondation Class: Contains foundation datas, main core object

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    """

    __user__ = os.environ['USERNAME']
    __rootPath__ = "E:/fondation"
    __projectsPath__ = pFile.conformPath(os.path.join(__rootPath__, "projects"))
    __settingsPath__ = pFile.conformPath(os.path.join(__rootPath__, "settings"))

    def __init__(self, logLvl='info'):
        self._setup(logLvl)
        self._groups = userGroups.Groups(self)
        self._users = users.Users(self)
        self._project = project.Project(self)

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

    @property
    def contextTypes(self):
        """
        Get context types

        :return: Context types
        :rtype: list
        """
        return ['asset', 'shot']

    @property
    def typoExclusion(self):
        """
        Typo results that must not be found

        :return: Typo exclusion
        :rtype: list
        """
        return ['', ' ', 'None', None]


if __name__ == '__main__':
    fdn = Fondation(logLvl='detail')