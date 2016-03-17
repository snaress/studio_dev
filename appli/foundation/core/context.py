import common
from coreSys import pFile


class CtxtEntity(common.Child):
    """
    CtxtEntity Class: Contains entity context data, child of Context

    :param parentObject: Storage object or Child object
    :type parentObject: Context || CtxtEntity
    """

    __attrPrefix__ = 'ctxt'

    def __init__(self, parentObject=None):
        super(CtxtEntity, self).__init__(parentObject=parentObject)
        #--- Data ---#
        self.childs = []
        self.ctxtCode = None
        self.ctxtName = None
        self.ctxtFolder = None

    @property
    def contextName(self):
        """
        Get context name

        :return: Context Name
        :rtype: str
        """
        return self._parent.contextName

    @property
    def contextType(self):
        """
        Get context type

        :return: Context type ('mainType' or 'subType')
        :rtype: str
        """
        if self._parent.__class__.__name__ == 'Context':
            return 'mainType'
        return 'subType'

    @property
    def contextLabel(self):
        """
        Get context entity label

        :return: Context entity label
        :rtype: str
        """
        if self.ctxtName is not None:
            return '%s%s' % (self.ctxtName[0].upper(), self.ctxtName[1:])

    def getData(self):
        """
        get class representation as dict

        :return: Class data
        :rtype: dict
        """
        data = dict(childs=dict())
        for attr in self.attributes:
            data[attr] = getattr(self, attr)
        for n, child in enumerate(self.childs):
            data['childs'][n] = child.getData()
        return data

    def update(self, **kwargs):
        """
        Update class data with given attributes

        :param kwargs: child data (key must start with self.__attrPrefix__)
        :type kwargs: dict
        """
        for k, v in kwargs.iteritems():
            if k in self.attributes:
                setattr(self, k, v)
            elif k == 'childs':
                for n in sorted(kwargs['childs']):
                    newChild = self.newChild(**kwargs['childs'][n])
                    self.addChild(newChild)
            else:
                self.log.warning("!!! Unrecognized attribute: %s. Skipp !!!" % k)

    def newChild(self, **kwargs):
        """
        Create new context entity

        :param kwargs: Context entity data (key must starts with 'ctxt')
        :type kwargs: dict
        :return: Context entity object
        :rtype: CtxtEntity
        """
        childObj = CtxtEntity(parentObject=self)
        childObj.update(**kwargs)
        return childObj

    def addChild(self, childObject):
        """
        Add context entity object to storage

        :param childObject: Context entity object
        :type childObject: CtxtEntity
        """
        #--- Check Context entity code ---#
        for child in self.childs:
            for attr in child.attributes:
                if getattr(child, attr) == getattr(childObject, attr):
                    raise AttributeError("!!! Context entity %r already exists !!!" % childObject.ctxtCode)
        #--- Add Context entity Object ---#
        self.childs.append(childObject)


class Context(common.Storage):
    """
    Context Class: Contains context data, child of Project

    :param projectObject: Project object
    :type projectObject: Project
    :param contextName: Context name
    :type contextName: str
    """

    def __init__(self, projectObject, contextName):
        #--- Global ---#
        self._fdn = projectObject._fdn
        self._project = projectObject
        #--- Data ---#
        self.contextName = contextName
        #--- Update ---#
        super(Context, self).__init__(self._fdn)

    def _init(self):
        """
        Init Group core object
        """
        super(Context, self)._init()
        self.log.title = self.__class__.__name__

    @property
    def contextLabel(self):
        """
        Get context label

        :return: Context label
        :rtype: str
        """
        if self.contextName is not None:
            return '%s%s' % (self.contextName[0].upper(), self.contextName[1:])

    @property
    def contextFolder(self):
        """
        Get context folder

        :return: Context folder
        :rtype: str
        """
        if self.contextName is not None:
            return '%ss' % self.contextName

    def getData(self):
        """
        get class representation as dict

        :return: Class data
        :rtype: dict
        """
        childsData = super(Context, self).getData()
        data = dict(contextName=self.contextName, childs=childsData)
        return data

    def getCtxtEntity(self, mainType, subType=None):
        """
        Get context entity object

        :param mainType: Entity main type
        :type mainType: str
        :param subType: Entity sub type
        :type subType: str
        :return: Context entity object
        :rtype: CtxtEntity
        """
        for child in self.childs:
            if child.ctxtCode == mainType:
                if subType is None:
                    return child
                for subChild in child.childs:
                    if subChild.ctxtCode == subType:
                        return subChild

    def getCtxtEntityNames(self, mainType=None):
        """
        Get Context entity names

        :param mainType: Context entity main type label (to get subTypes)
        :type mainType: str
        :return: Context entity names
        :rtype: list
        """
        ctxtEntities = []
        for child in self.childs:
            if mainType is None:
                ctxtEntities.append(child.ctxtName)
            else:
                if child.contextLabel == mainType:
                    for subChild in child.childs:
                        ctxtEntities.append(subChild.ctxtName)
        return ctxtEntities

    def getCtxtEntityLabels(self, mainType=None):
        """
        Get Context entity labels

        :param mainType: Context entity main type label (to get subTypes)
        :type mainType: str
        :return: Context entity labels
        :rtype: list
        """
        ctxtEntities = []
        for child in self.childs:
            if mainType is None:
                ctxtEntities.append(child.contextLabel)
            else:
                if child.contextLabel == mainType:
                    for subChild in child.childs:
                        ctxtEntities.append(subChild.contextLabel)
        return ctxtEntities

    def buildFromSettings(self):
        """
        Populate _childs from settings file
        """
        projectDict = pFile.readDictFile(self._project.projectFile)
        ctxtDict = dict()
        for ctxt in projectDict['contexts']:
            if ctxt['contextName'] == self.contextName:
                ctxtDict = ctxt
        self.update(**ctxtDict)

    def update(self, clearChilds=True, **kwargs):
        """
        Update childs list

        :param clearChilds: Clear childs storage
        :type clearChilds: bool
        :param kwargs: Context entities data
        :type kwargs: dict
        """
        self.log.detail("Updating context %r ..." % self.contextName)
        if kwargs.get('childs') is not None:
            if clearChilds:
                self.clearChilds()
            for n in sorted(kwargs['childs']):
                newChild = self.newChild(**kwargs['childs'][n])
                self.addChild(newChild)

    def newChild(self, **kwargs):
        """
        Create new context entity

        :param kwargs: Context entity data (key must starts with 'ctxt')
        :type kwargs: dict
        :return: Context entity object
        :rtype: CtxtEntity
        """
        ctxtChild = CtxtEntity(parentObject=self)
        ctxtChild.update(**kwargs)
        return ctxtChild

    def addChild(self, childObject):
        """
        Add context entity object to storage

        :param childObject: Context entity object
        :type childObject: CtxtEntity
        """
        #--- Check Context Entity ---#
        for child in self.childs:
            for attr in child.attributes:
                if getattr(child, attr) == getattr(childObject, attr):
                    raise AttributeError("!!! Context entity %r already exists !!!" % childObject.ctxtCode)
        #--- Add Context entity Object ---#
        super(Context, self).addChild(childObject)

    def delChild(self, mainTypeCode, subTypeCode=None):
        """
        Delete context entity object from storage

        :param mainTypeCode: Context entity code
        :type mainTypeCode: str
        :param subTypeCode: Parent context entity code
        :type subTypeCode: str
        """
        entityMainType = self.getCtxtEntity(mainTypeCode)
        if entityMainType is not None:
            if subTypeCode is None:
                self.log.debug("Removing context entity %r" % entityMainType.ctxtName)
                self.childs.remove(entityMainType)
            else:
                entitySubType = self.getCtxtEntity(mainTypeCode, subType=subTypeCode)
                if entitySubType is not None:
                    self.log.debug("Removing context entity %r" % entitySubType.ctxtName)
                    entityMainType.childs.remove(entitySubType)
