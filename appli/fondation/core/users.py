import os
import shutil
import storage
from coreSys import pFile


class User(storage.Child):
    """
    User Class: Contains user data, child of Users

    :param parentObject: Storage object
    :type parentObject: Users
    """

    __attrPrefix__ = 'user'

    def __init__(self, parentObject=None):
        super(User, self).__init__(parentObject=parentObject)
        #--- data ---#
        self.userName = None
        self.userStatus = True
        self.userGroup = None
        self.userFirstName = None
        self.userLastName = None
        self.userRecentProjects = []
        self.userPinedProjects = []

    @property
    def userPrefix(self):
        """
        Get user prefixe folder

        :return: User prefixe folder
        :rtype: str
        """
        if self.userName is not None:
            return self.userName[0].lower()

    @property
    def userPath(self):
        """
        Get user path

        :return: User path
        :rtype: str
        """
        if self.userName is not None:
            return pFile.conformPath(os.path.join(self._parent.usersPath, self.userPrefix, self.userName))

    @property
    def userFile(self):
        """
        Get user file full path

        :return: User file full path
        :rtype: str
        """
        if self.userName is not None:
            return pFile.conformPath(os.path.join(self.userPath, '%s.py' % self.userName))

    @property
    def grade(self):
        """
        Get user grade

        :return: User grade
        :rtype: int
        """
        if self.userGroup is not None:
            grpObjs = self._parent._groups.getChilds(grpCode=self.userGroup)
            if len(grpObjs) == 1:
                return grpObjs[0].grpGrade

    def setDataFromUserFile(self):
        """
        Set user data from userFile
        """
        data = pFile.readDictFile(self.userFile)
        self.update(**data)

    def addPinedProject(self, project):
        """
        Add given project to pinedProjects

        :param project: Project (name--code)
        :type project: str
        """
        if not project in self.userPinedProjects:
            self.userPinedProjects.append(project)
            self.log.info("%r added to pinProjects" % project)
        else:
            raise ValueError("!!! Project %r already in pinedProjects, Skipp !!!" % project)

    def delPinedProject(self, project):
        """
        Remove given project from pinedProjects

        :param project: Project (name--code)
        :type project: str
        """
        if project in self.userPinedProjects:
            self.userPinedProjects.remove(project)
            self.log.info("%r removed from pinedProjects" % project)
        else:
            raise ValueError("!!! %r not found, Skipp !!!" % project)

    def writeFile(self):
        """
        Write user file
        """
        self.log.debug("#---- Write User File: %s ----#" % self.userName)
        #--- Check Path ---#
        self.log.detail("Check user path ...")
        pFile.createPath(self.userPath, recursive=True, root=self._parent.usersPath, log=self.log)
        #--- Write File ---#
        self.log.detail("Write user file ...")
        try:
            pFile.writeDictFile(self.userFile, self.getData())
            self.log.debug("---> User file successfully written: %s" % self.userFile)
        except:
            raise IOError("!!! Can not write user file: %s !!!" % self.userName)


class Users(storage.Storage):
    """
    Users Class: Contains user data, child of Fondation

    :param fdnObject: Fondation object
    :type fdnObject: fondation.Fondation
    """

    __usersDir__ = "users"
    __archiveDir__ = "_archive"

    def __init__(self, fdnObject):
        #--- Global ---#
        self._groups = fdnObject._groups
        #--- Data ---#
        self._user = None
        #--- Update ---#
        super(Users, self).__init__(fdnObject)

    def _init(self):
        """
        Init Group core object
        """
        super(Users, self)._init()
        self.log.title = self.__class__.__name__

    def _setup(self):
        """
        Setup Group core object
        """
        super(Users, self)._setup()
        #--- Create Tool Paths ---#
        self.log.debug("#---- Check Paths ----#")
        userGrp = self._groups.defaultChilds[len(self._groups.defaultChilds)-1]['grpCode']
        if not os.path.exists(self.usersPath):
            pFile.createPath(self.usersPath, log=self.log)
            userGrp = self._groups.defaultChilds[0]['grpCode']
        #--- Check User ---#
        self.log.debug("#--- Check User ---#")
        self.collecteUsers(userName=self._fdn.__user__)
        #--- Create Current User ---#
        if self._user is None:
            self.log.debug("Create user %r ..." % self._fdn.__user__)
            childObj = self.newChild(userName=self._fdn.__user__, userGroup=userGrp, userStatus=True)
            self.addChild(childObj)
            childObj.writeFile()

    @property
    def usersPath(self):
        """
        Get users path

        :return: Users path
        :rtype: str
        """
        return pFile.conformPath(os.path.join(self._fdn.__rootPath__, self.__usersDir__))

    @property
    def archivePath(self):
        """
        Get archive path

        :return: Archive path
        :rtype: str
        """
        return pFile.conformPath(os.path.join(self.usersPath, self.__archiveDir__))

    @property
    def users(self):
        """
        Get users name list

        :return: Users name list
        :rtype: list
        """
        return self.getValues('userName')

    def getUserPrefixes(self, capital=False):
        """
        Get user prefix list

        :param capital: Return upper form prefix
        :type capital: bool
        :return: User prefix list
        :rtype: list
        """
        prefixList = []
        for userObj in self.childs:
            #--- Get Prefix ---#
            if capital:
                prefix = userObj.userPrefix.upper()
            else:
                prefix = userObj.userPrefix
            #--- Store Prefix ---#
            if not prefix in prefixList:
                prefixList.append(prefix)
        #--- Result ---#
        return sorted(prefixList)

    def collecteUsers(self, userPrefix=None, userName=None, clear=False, checkStatus=False):
        """
        Collecte Users from disk

        :param userPrefix: User prefix folder
        :type userPrefix: str
        :param userName: User name
        :type userName: str
        :param clear: Clear childs contents
        :type clear: bool
        :param checkStatus: Consider userStatus when collecting
        :type checkStatus: bool
        :return: Collected user objects
        :rtype: list
        """
        self.log.debug("Collecting users ...")
        #--- Clear Users ---#
        if clear:
            self.log.detail("Clear users list")
            self.clearChilds()
        #--- Collecte Users ---#
        userObjects = []
        userList = self.parseUsers(userPrefix, userName)
        for user in userList:
            userPath = pFile.conformPath(os.path.join(self.usersPath, user[0].lower(), user))
            if not user.startswith('_') and os.path.isdir(userPath):
                #--- Remove Existing object ---#
                userCheck = self.getChilds(userName=user)
                if userCheck:
                    self.log.debug("Remove user object: %s" % user)
                    if len(userCheck) == 1:
                        self.childs.remove(userCheck[0])
                    else:
                        raise ValueError("!!! Several userObj with same userName value !!!")
                #--- Create User Object ---#
                userObj = self.newChild(userName=user)
                userObj.setDataFromUserFile()
                #--- Check Status ---#
                addUserObj = True
                if checkStatus:
                    addUserObj = userObj.userStatus
                if addUserObj:
                    #--- Store Current User ---#
                    if user == self._fdn.__user__:
                        self._user = userObj
                    #--- Add User Object ---#
                    self.addChild(userObj)
                    userObjects.append(userObj)
                    self.log.detail("---> User Object %r added" % user)
                else:
                    #--- Reject Current User ---#
                    self.log.detail("---> User Object skipped, %r status is False" % user)
        #--- Result ---#
        return userObjects

    def parseUsers(self, userPrefix, userName):
        """
        Parse disk users directory

        :param userPrefix: User prefix folder
        :type userPrefix: str
        :param userName: User name
        :type userName: str
        :return: Users list
        :rtype: list
        """
        self.log.detail("Parse disk ...")
        #--- Get Index List ---#
        if userPrefix is not None:
            prefixList = [userPrefix]
        else:
            if userName is not None:
                prefixList = [userName[0].lower()]
            else:
                prefixList = os.listdir(self.usersPath) or []
        #--- Collecte Index ---#
        userList = []
        for prefix in prefixList:
            prefixPath = pFile.conformPath(os.path.join(self.usersPath, prefix))
            if len(prefix) == 1 and os.path.isdir(prefixPath):
                #--- Get User List ---#
                if userName is not None:
                    userList = [userName]
                else:
                    userList.extend(os.listdir(prefixPath) or [])
        #--- Result ---#
        return userList

    def newChild(self, **kwargs):
        """
        Create new user

        :return: User object
        :rtype: User
        """
        userObj = User(parentObject=self)
        userObj.update(**kwargs)
        return userObj

    def addChild(self, childObject):
        """
        Add User object to storage

        :param childObject: User object
        :type childObject: User
        """
        #--- Check Group Name ---#
        if childObject.userName in self.users:
            raise AttributeError("!!! User name %r already exists !!!" % childObject.userName)
        #--- Add User Object ---#
        super(Users, self).addChild(childObject)

    def delUser(self, userName=None, userObj=None, archive=False):
        """
        Delete given user

        :param userName: User name
        :type userName: str
        :param userObj: User object
        :type userObj: User
        :param archive: Archives datas (clean disk)
        :type archive: bool
        """
        #--- Check User Object ---#
        if userObj is None:
            userObj = self.getChilds(userName=userName)
        if userObj is None:
            raise AttributeError("!!! User not found: %s !!!" % userName)
        #--- Archive User ---#
        if archive:
            self.log.info("Archive user %r" % userObj.userName)
            dateTime = '%s--%s' % (pFile.getDate(), pFile.getTime())
            archivePath = pFile.conformPath(os.path.join(self.archivePath, userObj.userPrefix,
                                                         userObj.userName, dateTime))
            pFile.createPath(archivePath, recursive=True, root=self.usersPath, log=self.log)
            archiveFullPath = pFile.conformPath(os.path.join(archivePath, userObj.userName))
            #--- Create Archive ---#
            if os.path.exists(userObj.userPath):
                try:
                    shutil.copytree(userObj.userPath, archiveFullPath)
                    shutil.rmtree(userObj.userPath)
                    self.log.debug("---> User %r archived in %s" % (userObj.userName, archivePath))
                except:
                    raise IOError("!!! Can not copy tree: %s !!!" % userObj.userPath)
            else:
                raise IOError("!!! User path not found: %s !!!" % userObj.userPath)
        #--- Delete User Object ---#
        if userObj in self.childs:
            self.log.info("Deleting user object %r ..." % userObj.userName)
            self.childs.remove(userObj)
        else:
            self.log.debug("User object %r already deleted. Skipp !!!" % userObj.userName)
        #--- Result ---#
        self.log.info("---> %r deleted." % userObj.userName)
