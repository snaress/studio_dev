import os, pprint, shutil
from coreSys import pFile


class User(object):
    """
    User Class: Contains user data, child of UserGroups

    :param userName: User name
    :type userName: str
    :param usersObj: Foundation Users object
    :type usersObj: Users
    """

    __attrPrefix__ = 'user'

    def __init__(self, userName, usersObj):
        self.users = usersObj
        self.foundation = self.fdn = self.users.foundation
        self.log = self.users.log
        #--- data ---#
        self.userName = userName
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
        return self.userName[0].lower()

    @property
    def userPath(self):
        """
        Get user path

        :return: User path
        :rtype: str
        """
        return pFile.conformPath(os.path.join(self.users.usersPath, self.userPrefix, self.userName))

    @property
    def userFile(self):
        """
        Get user file full path

        :return: User file full path
        :rtype: str
        """
        return pFile.conformPath(os.path.join(self.userPath, '%s.py' % self.userName))

    @property
    def attributes(self):
        """
        List all attributes

        :return: Attributes
        :rtype: list
        """
        attrs = []
        for attr in self.__dict__.keys():
            if attr.startswith(self.__attrPrefix__) and not attr == 'users':
                attrs.append(attr)
        return attrs

    @property
    def grade(self):
        """
        Get user grade

        :return: User grade
        :rtype: int
        """
        if self.userGroup is not None:
            grpObj = self.users.userGrps.getObjectFromCode(self.userGroup)
            if grpObj is not None:
                return grpObj.grpGrade

    def getData(self, asString=False):
        """
        Get user data

        :param asString: Return string instead of dict
        :type asString: bool
        :return: User data
        :rtype: dict | str
        """
        data = dict()
        for attr in self.attributes:
            data[attr] = getattr(self, attr)
        #--- Result ---#
        if asString:
            return pprint.pformat(data)
        return data

    def setData(self, **kwargs):
        """
        Set user data

        :param kwargs: User data (key must start with 'user')
        :type kwargs: dict
        """
        for k, v in kwargs.iteritems():
            if k.startswith(self.__attrPrefix__):
                if k in self.attributes:
                    setattr(self, k, v)
                else:
                    self.log.warning("!!! Unrecognized attribute: %s. Skipp !!!" % k)

    def setDataFromUserFile(self):
        """
        Set user data from userFile
        """
        data = pFile.readDictFile(self.userFile)
        self.setData(**data)

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
        pFile.createPath(self.userPath, recursive=True, root=self.users.usersPath, log=self.log)
        #--- Write File ---#
        self.log.detail("Write user file ...")
        try:
            pFile.writeDictFile(self.userFile, self.getData())
            self.log.debug("---> User file successfully written: %s" % self.userFile)
        except:
            raise IOError("!!! Can not write userFile: %s !!!" % self.userName)


class Users(object):
    """
    Users Class: Contains users data, child of Foundation

    :param fdnObj: Foundation object
    :type fdnObj: foundation.Foundation
    """

    __usersDir__ = "users"
    __archiveDir__ = "_archive"

    def __init__(self, fdnObj):
        self.foundation = self.fdn = fdnObj
        self.userGrps = self.fdn.userGrps
        self.log = self.fdn.log
        self.log.title = "Users"
        #--- data ---#
        self._user = None
        self._users = []
        #--- Update ---#
        self._setup()

    def _setup(self):
        """
        Setup Users core object
        """
        self.log.info("#===== Setup Users Core =====#", newLinesBefore=1)
        #--- Create Tool Paths ---#
        self.log.debug("#---- Check Paths ----#")
        if not os.path.exists(self.usersPath):
            pFile.createPath(self.usersPath, log=self.log)
            self.newUser(install=True)
        #-- Check User --#
        self.log.debug("#--- Check User ---#")
        self.collecteUsers(userName=self.fdn.__user__)
    
    @property
    def usersPath(self):
        """
        Get users path

        :return: Users path
        :rtype: str
        """
        return pFile.conformPath(os.path.join(self.fdn.__rootPath__, self.__usersDir__))

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
        userList = []
        for user in self._users:
            userList.append(user.userName)
        return sorted(userList)
    
    def getUserPrefixes(self, capital=False):
        """
        Get user prefix list

        :param capital: Return upper form prefix
        :type capital: bool
        :return: User prefix list
        :rtype: list
        """
        prefixList = []
        for userObj in self._users:
            if not userObj.userPrefix in prefixList:
                if capital:
                    prefixList.append(userObj.userPrefix.upper())
                else:
                    prefixList.append(userObj.userPrefix)
        return sorted(prefixList)
    
    def getUserObjFromName(self, userName):
        """
        Get user object from given userName

        :param userName: User name
        :type userName: str
        :return: User object
        :rtype: User
        """
        for userObj in self._users:
            if userObj.userName == userName:
                return userObj
    
    def collecteUsers(self, userPrefix=None, userName=None, clearUsers=False):
        """
        Collecte Users from disk

        :param userPrefix: User prefix folder
        :type userPrefix: str
        :param userName: User name
        :type userName: str
        :param clearUsers: Clear '_users' attribute
        :type clearUsers: bool
        :return: Collected user objects
        :rtype: list
        """
        self.log.debug("Collecting users ...")
        #--- Clear Users ---#
        if clearUsers:
            self.log.detail("Clear users list")
            self._users = []
        #--- Collecte Users ---#
        userObjects = []
        userList = self.parseUsers(userPrefix, userName)
        for user in userList:
            userPath = pFile.conformPath(os.path.join(self.usersPath, user[0].lower(), user))
            if not user.startswith('_') and os.path.isdir(userPath):
                #--- Remove Existing object ---#
                userCheck = self.getUserObjFromName(user)
                if userCheck is not None:
                    self.log.debug("Remove user object: %s" % user)
                    self._users.remove(userCheck)
                #--- Add User Object ---#
                userObj = User(user, self)
                userObj.setDataFromUserFile()
                if user == self.fdn.__user__:
                    self._user = userObj
                self._users.append(userObj)
                userObjects.append(userObj)
                self.log.detail("---> User Object %r added" % user)
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
    
    def newUser(self, userName=None, install=False):
        """
        Create new user

        :param userName: New user name
        :type userName: str
        :param install: Install mode
        :type install: bool
        :return: User object
        :rtype: User
        """
        #--- Get UserName ---#
        if userName is None:
            userName = self.fdn.__user__
        self.log.info("Create New User %r ..." % userName)
        #--- Check UserName ---#
        if userName in self.users:
            raise AttributeError("!!! UserName %r already exists !!!" % userName)
        #--- Add User Object ---#
        userObj = User(userName, self)
        if install:
            self.log.detail("Install mode, %s ---> '%s'" % (userName, self.userGrps.defaultGroups[0]['grpCode']))
            userObj.setData(userGroup=self.userGrps.defaultGroups[0]['grpCode'], userStatus=True)
            userObj.writeFile()
        return userObj
    
    def deleteUser(self, userName=None, userObj=None, archive=False):
        """
        Delete given user

        :param userName: User name
        :type userName: str
        :param userObj: User object
        :type userObj: User
        :param archive: Archives datas (clean disk)
        :type archive: bool
        """
        if userObj is None:
            userObj = self.getUserObjFromName(userName)
        #--- Check User Object ---#
        if userObj is None:
            raise AttributeError("!!! User not found: %s !!!" % userName)
        #--- Archive User ---#
        if archive:
            self.log.info("Archive user %r" % userObj.userName)
            dateTime = '%s--%s' % (pFile.getDate(), pFile.getTime())
            archivePath = pFile.conformPath(os.path.join(self.archivePath, userObj.userPrefix, userObj.userName,
                                                         dateTime))
            pFile.createPath(archivePath, recursive=True, root=self.usersPath, log=self.log)
            archiveFullPath = pFile.conformPath(os.path.join(archivePath, userObj.userName))
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
        if userObj in self._users:
            self.log.info("Deleting user object %r ..." % userObj.userName)
            self._users.remove(userObj)
        else:
            self.log.debug("User object %r already deleted. Skipp !!!" % userObj.userName)
        self.log.info("---> %r deleted." % userObj.userName)
