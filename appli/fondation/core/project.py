import os, pprint
from coreSys import pFile


class Project(object):
    """
    Project Class: Contains project data, child of Fondation

    :param fdnObject: Fondation object
    :type fdnObject: fondation.Fondation
    """

    def __init__(self, fdnObject):
        #--- Global ---#
        self._fdn = fdnObject
        self._users = self._fdn._users
        #--- Data ---#
        self.project = None
        self.watchers = []
        #--- Update ---#
        self._setup()

    def _setup(self):
        """
        Setup Project core object
        """
        self.log = self._fdn.log
        self.log.title = self.__class__.__name__
        self.log.info("#===== Setup Project Core =====#", newLinesBefore=1)

    @property
    def projects(self):
        """
        Get all projects

        :return: Project list
        :rtype: list
        """
        projectList = []
        for fld in os.listdir(self._fdn.__projectsPath__):
            if '--' in fld:
                fldPath = pFile.conformPath(os.path.join(self._fdn.__projectsPath__, fld))
                if os.path.isdir(fldPath):
                    if os.path.exists(pFile.conformPath(os.path.join(fldPath, '%s.py' % fld))):
                        projectList.append(fld)
        return projectList

    @property
    def projectNames(self):
        """
        Get all project names

        :return: Project names
        :rtype: list
        """
        names = []
        for project in self.projects:
            name = project.split('--')[0]
            if not name in names:
                names.append(name)
        return names

    @property
    def projectCodes(self):
        """
        Get all project codes

        :return: Project codes
        :rtype: list
        """
        codes = []
        for project in self.projects:
            code = project.split('--')[1]
            if not code in codes:
                codes.append(code)
        return codes

    @property
    def projectName(self):
        """
        Get project name

        :return: Project name
        :rtype: str
        """
        if self.project is not None:
            return self.project.split('--')[0]

    @property
    def projectCode(self):
        """
        Get project code

        :return: Project code
        :rtype: str
        """
        if self.project is not None:
            return self.project.split('--')[1]

    @property
    def projectPath(self):
        """
        Get project path

        :return: Project path
        :rtype: str
        """
        if self.project is not None:
            return pFile.conformPath(os.path.join(self._fdn.__projectsPath__, self.project))

    @property
    def projectFile(self):
        """
        Get project file full path

        :return: Project file path
        :rtype: str
        """
        if self.project is not None:
            return pFile.conformPath(os.path.join(self.projectPath, '%s.py' % self.project))

    @property
    def attributes(self):
        """
        List class attributes

        :return: Attributes
        :rtype: list
        """
        return ['project', 'watchers']

    def getData(self):
        """
        get class representation as dict

        :return: Class data
        :rtype: dict
        """
        data = dict()
        for attr in self.attributes:
            data[attr] = getattr(self, attr)
        return data

    def update(self, **kwargs):
        """
        Set project data

        :param kwargs: Project data (key must start with 'project')
        :type kwargs: dict
        """
        self.project = kwargs.get('project')
        for k, v in kwargs.iteritems():
            if k in self.attributes:
                setattr(self, k, v)
            else:
                self.log.debug("!!! Unrecognized attribute: %s. Skip !!!" % k)

    def newProject(self, projectName, projectCode):
        """
        Create new project

        :param projectName: Project name
        :type projectName: str
        :param projectCode: Project code
        :type projectCode: str
        """
        if self._users._user.grade > 2:
            raise AttributeError("Permissin denied, invalide user grade")
        self.log.info("#--- Create New Project ---#")
        self.log.info("Project Name: %s" % projectName)
        self.log.info("Project Code: %s" % projectCode)
        #--- Check New Project ---#
        if '%s--%s' % (projectName, projectCode) in self.projects:
            raise AttributeError("Project already exists: %s--%s" % (projectName, projectCode))
        if projectName in self.projectNames:
            raise AttributeError("Project name already used: %s" % projectName)
        if projectCode in self.projectCodes:
            raise AttributeError("Project code already used: %s" % projectCode)
        #--- Create Project Folder ---#
        newProjectPath = pFile.conformPath(os.path.join(self._fdn.__projectsPath__,
                                                        '%s--%s' % (projectName, projectCode)))
        pFile.createPath([newProjectPath], log=self.log)
        #--- Create Project File ---#
        projFile = pFile.conformPath(os.path.join(newProjectPath, '%s--%s.py' % (projectName, projectCode)))
        projDict = dict(__createdAt__=pFile.getDate(), __createdBy__=self._fdn.__user__,
                        project="%s--%s" % (projectName, projectCode), watchers=[self._fdn.__user__])
        try:
            pFile.writeDictFile(projFile, projDict)
            self.log.debug("---> Project file successfully written: %s" % projFile)
        except:
            raise IOError("!!! Can not write project file: %s !!!" % projFile)

    def loadProject(self, project):
        """
        Load given project

        :param project: Project (name--code)
        :type project: str
        """
        self.log.info("#--- Load Project: %r ---#" % project)
        #--- Check Project ---#
        projectFile = pFile.conformPath(os.path.join(self._fdn.__projectsPath__, project, '%s.py' % project))
        if not os.path.exists(projectFile):
            raise ValueError("!!! Project %r not found !!!" % project)
        #--- Get Project ---#
        try:
            projectDict = pFile.readDictFile(projectFile)
        except:
            raise IOError("!!! Can not load project %r !!!" % project)
        #--- Load Project ---#
        if self._fdn.__user__ in projectDict['watchers']:
            self.update(**projectDict)
            self.log.info("---> Project %r successfully loaded" % project)
        else:
            raise ValueError("User %r is not set as projectUser in %s !" % (self._fdn.__user__, project))

    def reloadProject(self):
        """
        Reload current project
        """
        self.log.info("#--- Relooad Project: %r ---#" % self.project)
        self.loadProject(self.project)

    def writeProject(self):
        """
        Write project file
        """
        self.log.debug("#--- Write Project File: %s ---#" % self.project)
        try:
            pFile.writeDictFile(self.projectFile, self.getData())
            self.log.debug("---> Project file successfully written: %s" % self.projectFile)
        except:
            raise IOError("!!! Can not write projectFile: %s !!!" % self.projectFile)

    def addWatcher(self, userName):
        """
        Add project watcher

        :param userName: User name
        :type userName: str
        """
        if not userName in self.watchers:
            self.watchers.append(userName)
            self.log.detail("User %r added to project %r" % (userName, self.project))

    def delWatcher(self, userName):
        """
        Remove project user (watcher)

        :param userName: User name
        :type userName: str
        """
        if userName in self.watchers:
            self.watchers.remove(userName)
            self.log.detail("User %r removed from project %r" % (userName, self.project))

    def __str__(self):
        """
        get class representation as str

        :return: Class data
        :rtype: str
        """
        return pprint.pformat(self.getData())
