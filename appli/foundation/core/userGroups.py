import os, pprint
from coreSys import pFile


class Group(object):
    """
    Group Class: Contains user group datas, child of UserGroups

    :param userGrpsObj: Foundation UserGroups object
    :type userGrpsObj: UserGroups
    """

    __attrPrefix__ = 'grp'

    def __init__(self, userGrpsObj):
        self.userGrps = userGrpsObj
        self.foundation = self.fdn = self.userGrps.foundation
        self.log = self.userGrps.log
        #--- Datas ---#
        self.grpCode = None
        self.grpName = None
        self.grpGrade = 9
        self.grpColor = None

    @property
    def attributes(self):
        """
        List all attributes

        :return: Attributes
        :rtype: list
        """
        attrs = []
        for attr in self.__dict__.keys():
            if attr.startswith(self.__attrPrefix__):
                attrs.append(attr)
        return attrs

    def getData(self, asString=False):
        """
        Get group data

        :param asString: Return string instead of dict
        :type asString: bool
        :return: Group data
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
        Set group data

        :param kwargs: Group data (key must start with 'grp')
        :type kwargs: dict
        """
        for k, v in kwargs.iteritems():
            if k.startswith(self.__attrPrefix__):
                if k in self.attributes:
                    setattr(self, k, v)
                else:
                    self.log.warning("!!! Unrecognized attribute: %s. Skipp !!!" % k)


class UserGroups(object):
    """
    UserGroups Class: Contains user groups data, child of Foundation

    :param fdnObj: Foundation object
    :type fdnObj: foundation.Foundation
    """

    def __init__(self, fdnObj):
        self.foundation = self.fdn = fdnObj
        self.log = self.fdn.log
        self.log.title = "UserGrps"
        #--- Datas ---#
        self._groups = []
        #--- Update ---#
        self._setup()

    def _setup(self):
        """
        Setup UserGroups core object
        """
        self.log.info("#===== Setup UserGroups Core =====#", newLinesBefore=1)
        #--- Check UserGroups File ---#
        self.log.debug("#--- Check UserGroups File ---#")
        if not os.path.exists(self.settingsFile):
            self.createSettingsFile()
        #--- Build Groups ---#
        self.buildFromSettings()

    @property
    def settingsFile(self):
        """
        Get userGroups file full path

        :return: userGroups file full path
        :rtype: str
        """
        return pFile.conformPath(os.path.join(self.fdn.__settingsPath__, 'userGroups.py'))

    @property
    def defaultGroups(self):
        """
        Get default user groups

        :return: User groups param
        :rtype: dict
        """
        #--- Init Default Groups ---#
        grps = [{'grpCode': 'ADMIN', 'grpColor': (255, 0, 0), 'grpGrade': 0, 'grpName': 'Administrator'},
                {'grpCode': 'HDEV', 'grpColor': (220, 35, 0), 'grpGrade': 1, 'grpName': 'Head Of Development'},
                {'grpCode': 'DEV', 'grpColor': (180, 70, 0), 'grpGrade': 2, 'grpName': 'Development'},
                {'grpCode': 'HSPV', 'grpColor': (145, 110, 0), 'grpGrade': 2, 'grpName': 'Head Supervisor'},
                {'grpCode': 'SPV', 'grpColor': (110, 145, 0), 'grpGrade': 3, 'grpName': 'Supervisor'},
                {'grpCode': 'HTD', 'grpColor': (70, 180, 0), 'grpGrade': 3, 'grpName': 'Head Technical Director'},
                {'grpCode': 'TD', 'grpColor': (35, 220, 0), 'grpGrade': 4, 'grpName': 'Technical Director'},
                {'grpCode': 'SGRP', 'grpColor': (0, 255, 0.0), 'grpGrade': 5, 'grpName': 'Senior Graphist'},
                {'grpCode': 'LGRP', 'grpColor': (0, 225, 30), 'grpGrade': 5, 'grpName': 'Lead Graphist'},
                {'grpCode': 'GRP', 'grpColor': (0, 190, 65), 'grpGrade': 6, 'grpName': 'Graphist'},
                {'grpCode': 'HPRD', 'grpColor': (0, 160, 95), 'grpGrade': 6, 'grpName': 'Head Production'},
                {'grpCode': 'PRD', 'grpColor': (0, 127, 127), 'grpGrade': 7, 'grpName': 'Production'},
                {'grpCode': 'APRD', 'grpColor': (0, 95, 160), 'grpGrade': 8, 'grpName': 'Production Assistant'},
                {'grpCode': 'VST', 'grpColor': (0, 0, 255), 'grpGrade': 9, 'grpName': 'Visitor'}]
        #--- Build Grp Dict ---#
        grpDict = dict()
        for n, grpData in enumerate(grps):
            grpDict[n] = grpData
        #--- Result ---#
        return grpDict

    @property
    def codes(self):
        """
        Get groups code list

        :return: Groups code list
        :rtype: list
        """
        grpList = []
        for grp in self._groups:
            grpList.append(grp.grpCode)
        return grpList

    @property
    def names(self):
        """
        Get groups name list

        :return: Groups name list
        :rtype: list
        """
        grpList = []
        for grp in self._groups:
            grpList.append(grp.grpName)
        return grpList

    @property
    def grades(self):
        """
        Get all userGroups grades

        :return: User groups grade
        :rtype: list
        """
        gradeList = []
        for grp in self._groups:
            if not grp.grpGrade in gradeList:
                gradeList.append(grp.grpGrade)
        return gradeList

    def getData(self, asString=False):
        """
        Get groups data

        :param asString: Return string instead of dict
        :type asString: bool
        :return: Group data
        :rtype: dict | str
        """
        data = dict()
        for n, grpObj in enumerate(self._groups):
            data[n] = grpObj.getData(asString=asString)
        #--- Result ---#
        if asString:
            return pprint.pformat(data)
        return data

    def getObjectFromCode(self, grpCode):
        """
        Get group object from given groupCode

        :param grpCode: Group code
        :type grpCode: str
        :return: Group object
        :rtype: Group
        """
        for grpObj in self._groups:
            if grpObj.grpCode == grpCode:
                return grpObj

    def getObjectFromName(self, groupName):
        """
        Get group object from given groupName

        :param groupName: Group name
        :type groupName: str
        :return: Group object
        :rtype: Group
        """
        for grpObj in self._groups:
            if grpObj.grpName == groupName:
                return grpObj

    def newGroup(self, grpCode, **kwargs):
        """
        Create new group

        :param grpCode: Group code
        :type grpCode: str
        :param kwargs: Group datas (key must starts with 'grp')
        :type kwargs: dict
        :return: Group object
        :rtype: Group
        """
        #--- Check GrpName ---#
        if grpCode in self.codes:
            raise AttributeError("!!! Group code %r already exists !!!" % grpCode)
        #--- Create Group ---#
        grpObj = Group(self)
        if 'grpCode' in kwargs:
            kwargs.pop('grpCode')
        grpObj.setData(grpCode=grpCode, **kwargs)
        #--- Result ---#
        return grpObj

    def buildFromSettings(self):
        """
        Populate _groups from settings
        """
        self.log.detail("Build userGroups from settings ...")
        grpDict = pFile.readDictFile(self.settingsFile)
        self.buildFromDict(grpDict)

    def buildFromDict(self, grpDict):
        """
        Populate _groups from given dict

        :param grpDict: Groups dict
        :type grpDict: dict
        """
        self.log.detail("Build userGroups from grpDict ...")
        self._groups = []
        for n in sorted(grpDict.keys()):
            self._groups.append(self.newGroup(**grpDict[n]))

    def createSettingsFile(self):
        """
        Create default settings file
        """
        try:
            pFile.writeDictFile(self.settingsFile, self.defaultGroups)
            self.log.debug("---> UserGroups file successfully written: %s" % self.settingsFile)
        except:
            raise IOError("!!! Can not write userGroups file: %s !!!" % os.path.basename(self.settingsFile))

    def writeSettingsFile(self):
        """
        Write userGroups to settings file
        """
        self.log.debug("#--- Write UserGroups File ---#")
        try:
            pFile.writeDictFile(self.settingsFile, self.getData())
            self.log.debug("---> UserGroup file successfully written: %s" % self.settingsFile)
        except:
            raise IOError("!!! Can not write userGroups file: %s !!!" % self.settingsFile)
