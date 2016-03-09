import os
import common
from coreSys import pFile


class Entity(common.Child):
    """
    Entity Class: Contains entity data, child of Context

    :param parentObject: Storage object
    :type parentObject: Entities
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

    def updateFromFile(self):
        if self.entityFile is not None:
            if os.path.exists(self.entityFile):
                entityData = pFile.readDictFile(self.entityFile)
                self.update(**entityData)

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


class Entities(common.Storage):
    """
    Entities Class: Contains entities data, child of CtxtChild

    :param projectObject: Project object
    :type projectObject: Project
    :param contextObject: Context object
    :type contextObject: Context
    """

    def __init__(self, projectObject, contextObject):
        #--- Global ---#
        self._fdn = projectObject._fdn
        self._project = projectObject
        self._context = contextObject
        #--- Data ---#
        #--- Update ---#
        super(Entities, self).__init__(self._fdn)

    @property
    def entityNames(self):
        """
        Get all entity names

        :return: Entity names
        :rtype: list
        """
        names = []
        for entity in self.childs:
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
        for entity in self.childs:
            codes.append(entity.entityCode)
        return codes

    # def buildEntities(self, *args):
    #     self.entities = []
    #     for entityInfo in args:
    #         params = entityInfo.split('/')
    #         newEntity = self.newEntity(entityMainType=params[0], entitySubType=params[1], entityName=params[2])
    #         newEntity.updateFromFile()
    #         self.addEntity(newEntity)
    #
    # def newEntity(self, create=False, **kwargs):
    #     """
    #     Create new entity
    #
    #     :param create: Enable entity file creation
    #     :type create: bool
    #     :param kwargs: Entity data (key must starts with 'entity')
    #     :type kwargs: dict
    #     :return: Entity object
    #     :rtype: Entity
    #     """
    #     entityChild = Entity(parentObject=self)
    #     entityChild.update(**kwargs)
    #     #--- Create Entity File ---#
    #     if create:
    #         if os.path.exists(entityChild.entityFile):
    #             raise IOError("!!! Entity File already exists: %s !!!" % entityChild.entityFile)
    #         entityChild.writeFile()
    #     #--- Result ---#
    #     return entityChild
    #
    # def addEntity(self, entityObject, create=False):
    #     """
    #     Add entity object to storage
    #
    #     :param entityObject: Entity object
    #     :type entityObject: Entity
    #     :param create: Enable entity file creation
    #     :type create: bool
    #     """
    #     #--- Check Entity ---#
    #     if entityObject.entityCode in self.entityCodes or entityObject.entityName in self.entityNames:
    #         raise AttributeError("!!! Entity %r (%r) already exists !!!" % (entityObject.entityName,
    #                                                                         entityObject.entityCode))
    #     #--- Add Entity Object ---#
    #     self.entities.append(entityObject)
    #     if create:
    #         self._project.writeProject()
    #