import os
import storage
from coreSys import pFile


class Group(storage.Child):
    """
    Group Class: Contains group data, child of Groups

    :param parentObject: Storage object
    :type parentObject: Groups
    """

    __attrPrefix__ = 'grp'

    def __init__(self, parentObject=None):
        super(Group, self).__init__(parentObject=parentObject)
        #--- Data ---#
        self.grpCode = None
        self.grpName = None
        self.grpGrade = 9
        self.grpColor = None


class Groups(storage.Storage):
    """
    Groups Class: Contains groups data, child of Foundation

    :param fdnObject: Fondation object
    :type fdnObject: fondation.Fondation
    """

    def __init__(self, fdnObject):
        #--- Global ---#
        #--- Data ---#
        #--- Update ---#
        super(Groups, self).__init__(fdnObject)

    def _init(self):
        """
        Init Group core object
        """
        super(Groups, self)._init()
        self.log.title = self.__class__.__name__

    def _setup(self):
        """
        Setup Group core object
        """
        super(Groups, self)._setup()
        #--- Check UserGroups File ---#
        self.log.debug("#--- Check Settings File ---#")
        if not os.path.exists(self.settingsFile):
            self.createSettingsFile()
        #--- Build Groups ---#
        self.buildFromSettings()

    @property
    def settingsFile(self):
        """
        Get settings file full path

        :return: Settings file full path
        :rtype: str
        """
        return pFile.conformPath(os.path.join(self._fdn.__settingsPath__, 'userGroups.py'))

    @property
    def defaultChilds(self):
        """
        Get default user groups

        :return: User groups param
        :rtype: dict
        """
        #--- Init Default Groups ---#
        grps = [{'grpCode': 'ADMIN', 'grpColor': (255, 0, 0),   'grpGrade': 0, 'grpName': 'Administrator'},
                {'grpCode': 'HDEV',  'grpColor': (220, 35, 0),  'grpGrade': 1, 'grpName': 'Head Of Development'},
                {'grpCode': 'DEV',   'grpColor': (180, 70, 0),  'grpGrade': 2, 'grpName': 'Development'},
                {'grpCode': 'HSPV',  'grpColor': (145, 110, 0), 'grpGrade': 2, 'grpName': 'Head Supervisor'},
                {'grpCode': 'SPV',   'grpColor': (110, 145, 0), 'grpGrade': 3, 'grpName': 'Supervisor'},
                {'grpCode': 'HTD',   'grpColor': (70, 180, 0),  'grpGrade': 3, 'grpName': 'Head Technical Director'},
                {'grpCode': 'TD',    'grpColor': (35, 220, 0),  'grpGrade': 4, 'grpName': 'Technical Director'},
                {'grpCode': 'SGRP',  'grpColor': (0, 255, 0.0), 'grpGrade': 5, 'grpName': 'Senior Graphist'},
                {'grpCode': 'LGRP',  'grpColor': (0, 225, 30),  'grpGrade': 5, 'grpName': 'Lead Graphist'},
                {'grpCode': 'GRP',   'grpColor': (0, 190, 65),  'grpGrade': 6, 'grpName': 'Graphist'},
                {'grpCode': 'HPRD',  'grpColor': (0, 160, 95),  'grpGrade': 6, 'grpName': 'Head Production'},
                {'grpCode': 'PRD',   'grpColor': (0, 127, 127), 'grpGrade': 7, 'grpName': 'Production'},
                {'grpCode': 'APRD',  'grpColor': (0, 95, 160),  'grpGrade': 8, 'grpName': 'Production Assistant'},
                {'grpCode': 'VST',   'grpColor': (0, 0, 255),   'grpGrade': 9, 'grpName': 'Visitor'}]
        #--- Build Grp Dict ---#
        grpDict = dict()
        for n, grpData in enumerate(grps):
            grpDict[n] = grpData
        #--- Result ---#
        return grpDict

    @property
    def codes(self):
        """
        Get codes list

        :return: Groups code list
        :rtype: list
        """
        return self.getValues('grpCode')

    @property
    def grades(self):
        """
        Get all userGroups grades

        :return: User groups grade
        :rtype: list
        """
        gradeList = []
        for grpObj in self.childs:
            if not grpObj.grpGrade in gradeList:
                gradeList.append(grpObj.grpGrade)
        return gradeList

    def newChild(self, **kwargs):
        """
        Create new group

        :param kwargs: Group data (key must starts with 'grp')
        :type kwargs: dict
        :return: Group object
        :rtype: Group
        """
        grpObj = Group(parentObject=self)
        grpObj.update(**kwargs)
        return grpObj

    def addChild(self, childObject):
        """
        Add Group object to storage

        :param childObject: Group object
        :type childObject: Group
        """
        #--- Check Group Name ---#
        if childObject.grpCode in self.getValues('grpCode'):
            raise AttributeError("!!! Group code %r already exists !!!" % childObject.grpCode)
        #--- Add Group Object ---#
        super(Groups, self).addChild(childObject)

    def buildFromSettings(self):
        """
        Populate _groups from settings file
        """
        self.log.detail("Build userGroups from settings ...")
        grpDict = pFile.readDictFile(self.settingsFile)
        self.buildChilds(grpDict)

    def createSettingsFile(self):
        """
        Create default settings file
        """
        try:
            pFile.writeDictFile(self.settingsFile, self.defaultChilds)
            self.log.debug("---> UserGroups file successfully written: %s" % self.settingsFile)
        except:
            raise IOError("!!! Can not write userGroups file: %s !!!" % os.path.basename(self.settingsFile))

    def writeSettingsFile(self):
        """
        Write groups to settings file
        """
        self.log.debug("#--- Write Groups File ---#")
        try:
            pFile.writeDictFile(self.settingsFile, self.getData())
            self.log.debug("---> Groups file successfully written: %s" % self.settingsFile)
        except:
            raise IOError("!!! Can not write Groups file: %s !!!" % self.settingsFile)
