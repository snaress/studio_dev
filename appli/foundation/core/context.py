import os
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


class Entity(common.Child):
    """
    Entity Class: Contains entity data, child of Context

    :param parentObject: Storage object
    :type parentObject: Context
    """

    __attrPrefix__ = 'entity'

    def __init__(self, parentObject=None):
        super(Entity, self).__init__(parentObject=parentObject)
        self._project = self._fdn._project
        #--- Data ---#
        self.entityMainType = None
        self.entitySubType = None
        self.entityCode = None
        self.entityName = None
        self.entityThumb = None
        self.entityStatus = None
        self.entityExtraAttrs = dict()

    @property
    def entityType(self):
        """
        Get Entity type

        :return: Entity type
        :rtype: str
        """
        if self._parent is not None:
            return self._parent.contextName

    @property
    def entityLabel(self):
        """
        Get Entity label

        :return: Entity label
        :rtype: str
        """
        if self.entityName is not None:
            return '%s%s' % (self.entityName[0].upper(), self.entityName[1:])

    @property
    def entityPath(self):
        """
        Get entity path

        :return: Entity path
        :rtype: str
        """
        if self.entityMainType is not None and self.entitySubType is not None and self.entityName is not None:
            return pFile.conformPath(os.path.join(self._project.projectPath, self._parent.contextFolder,
                                                  self.entityMainType, self.entitySubType, self.entityName))

    @property
    def entityFile(self):
        """
        Get entity file full path

        :return: Entity file
        :rtype: str
        """
        if self.entityPath is not None:
            return pFile.conformPath(os.path.join(self.entityPath, '%s.py' % self.entityName))

    def writeFile(self):
        """
        Write entity file
        """
        self.log.debug("#---- Write Entity File: %s ----#" % self.entityName)
        #--- Check Path ---#
        self.log.detail("Check entity path ...")
        pFile.createPath(self.entityPath, recursive=True, root=self._project.projectPath, log=self.log)
        #--- Write File ---#
        self.log.detail("Write entity file ...")
        try:
            pFile.writeDictFile(self.entityFile, self.getData())
            self.log.debug("---> User file successfully written: %s" % self.entityFile)
        except:
            raise IOError("!!! Can not write user file: %s !!!" % self.entityName)


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
        self.entities = []
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

    @property
    def entityNames(self):
        """
        Get all entity names

        :return: Entity names
        :rtype: list
        """
        names = []
        for entity in self.entities:
            names.append(entity.entityName)
        return names

    @property
    def entityCodes(self):
        """
        Get all entity codes

        :return: Entity codes
        :rtype: list
        """
        codes = []
        for entity in self.entities:
            codes.append(entity.entityCode)
        return codes

    def getData(self):
        """
        get class representation as dict

        :return: Class data
        :rtype: dict
        """
        childsData = super(Context, self).getData()
        data = dict(contextName=self.contextName, childs=childsData)
        return data

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

    def getEntitiesData(self):
        """
        Get entities data

        :return: Entities data
        :rtype: list
        """
        data = []
        for entity in self.entities:
            data.append(entity.getData())
        return data

    def getEntities(self, entityMainType, entitySubType=None):
        """
        Get entities considering given types

        :param entityMainType: Entity main type
        :type entityMainType: str
        :param entitySubType: Entity sub type
        :type entitySubType: str
        :return: Entities
        :rtype: list
        """
        entities = []
        for entity in self.entities:
            if entity.entityMainType == entityMainType:
                if entitySubType is None:
                    entities.append(entity)
                else:
                    if entity.entitySubType == entitySubType:
                        entities.append(entity)
        return entities

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

    def update(self, **kwargs):
        """
        Update childs list

        :param kwargs: Context entities data
        :type kwargs: dict
        """
        self.log.detail("Updating context %r ..." % self.contextName)
        if kwargs.get('childs') is not None:
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

    def newEntity(self, create=False,  **kwargs):
        """
        Create new entity

        :param create: Enable entity file creation
        :type create: bool
        :param kwargs: Entity data (key must starts with 'entity')
        :type kwargs: dict
        :return: Entity object
        :rtype: Entity
        """
        entityChild = Entity(parentObject=self)
        entityChild.update(**kwargs)
        #--- Create Entity File ---#
        if create:
            if os.path.exists(entityChild.entityFile):
                raise IOError("!!! Entity File already exists: %s !!!" % entityChild.entityFile)
            entityChild.writeFile()
        #--- Result ---#
        return entityChild

    def addEntity(self, entityObject):
        """
        Add entity object to storage

        :param entityObject: Entity object
        :type entityObject: Entity
        """
        #--- Check Entity ---#
        if entityObject.entityCode in self.entityCodes or entityObject.entityName in self.entityNames:
            raise AttributeError("!!! Entity %r (%r) already exists !!!" % (entityObject.entityName,
                                                                            entityObject.entityCode))
        #--- Add Entity Object ---#
        self.entities.append(entityObject)
