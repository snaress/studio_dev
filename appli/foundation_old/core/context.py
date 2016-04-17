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
    def contextPath(self):
        """
        Get context path

        :return: Context path
        :rtype: str
        """
        return self._parent.contextPath

    @property
    def entityPath(self):
        """
        Get entity path

        :return: Entity path
        :rtype: str
        """
        if self.contextPath is not None and self.entityName is not None:
            return pFile.conformPath(os.path.join(self.contextPath, self.entityName))

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
        self.entities = []
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
    def contextObj(self):
        """
        Get Context object

        :return: Context object
        :rtype: Context
        """
        return self._parent.contextObj

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

    @property
    def contextPath(self):
        """
        Get context entity path

        :return: Context entity path
        :rtype: str
        """
        if self._parent.contextPath is not None and self.ctxtFolder is not None:
            return pFile.conformPath(os.path.join(self._parent.contextPath, self.ctxtFolder))

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

    def getChildrenEntities(self, keepParentEntities=False):
        """
        Get entities recursively

        :param keepParentEntities: Keep parent entities in result
        :type keepParentEntities: bool
        :return: Child entities
        :rtype: list
        """
        entities = []
        if keepParentEntities:
            entities.extend(self.entities)
        for child in self.childs:
            entities.extend(child.entities)
        return entities

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

    def buildEntities(self):
        """
        Build all entities from disk
        """
        self.entities = []
        if self.contextPath is not None:
            if os.path.exists(self.contextPath):
                contents = os.listdir(self.contextPath) or []
                for fld in contents:
                    if not fld.startswith('_') and not fld.startswith('.'):
                        path = pFile.conformPath(os.path.join(self.contextPath, fld))
                        entityFile = pFile.conformPath(os.path.join(path, '%s.py' % fld))
                        if os.path.exists(entityFile):
                            self.log.detail(">>> Build entity from file %s ..." % entityFile)
                            data = pFile.readDictFile(entityFile)
                            self.addEntity(self.newEntity(**data))

    def newEntity(self, **kwargs):
        """
        Create new entity

        :param kwargs: Entity data (key must starts with 'entity')
        :type kwargs: dict
        :return: Entity object
        :rtype: Entity
        """
        entityObj = Entity(parentObject=self)
        entityObj.update(**kwargs)
        return entityObj

    def addEntity(self, entityObject):
        """
        Add entity object to storage

        :param entityObject: Entity object
        :type entityObject: Entity
        """
        #--- Check Entity ---#
        if (entityObject.entityCode in self.contextObj.entityCodes
            or entityObject.entityName in self.contextObj.entityNames):
            raise AttributeError("!!! Entity %r (%r) already exists !!!" % (entityObject.entityName,
                                                                            entityObject.entityCode))
        #--- Create Entity File ---#
        if not os.path.exists(entityObject.entityFile):
            entityObject.writeFile()
        #--- Result ---#
        self.entities.append(entityObject)
        self.log.detail("Entity %s successfully added." % entityObject.entityName)


class CtxtPipe(common.Child):
    """
    CtxtStep Class: Contains pipeLine steps and tasks, child of Context

    :param parentObject: Storage object or Child object
    :type parentObject: Context || CtxtEntity
    """

    __attrPrefix__ = 'pipe'

    def __init__(self, parentObject=None):
        super(CtxtPipe, self).__init__(parentObject=parentObject)
        #--- Data ---#
        self.childs = []
        self.pipeType = None
        self.pipeName = None
        self.pipeCode = None

    def newChild(self, **kwargs):
        #--- Check New Pipe Data ---#
        for taskObj in self.childs:
            if kwargs.get('pipeName') == taskObj.pipeName or kwargs.get('pipeCode') == taskObj.pipeCode:
                raise AttributeError("!!! Context pipe %s--%s already exists !!!" % (taskObj.pipeName,
                                                                                     taskObj.pipeCode))
        #--- Create Context Pipe Object ---#
        pipeObj = CtxtPipe(parentObject=self)
        pipeObj.update(**kwargs)
        return pipeObj



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
        self.contextPipe = []
        #--- Update ---#
        super(Context, self).__init__(self._fdn)

    def _init(self):
        """
        Init Group core object
        """
        super(Context, self)._init()
        self.log.title = self.__class__.__name__

    @property
    def contextObj(self):
        """
        Get Context object

        :return: Context object
        :rtype: Context
        """
        return self

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
    def contextPath(self):
        """
        Get context path

        :return: Context path
        :rtype: str
        """
        if self.contextFolder is not None:
            return pFile.conformPath(os.path.join(self._project.projectPath, self.contextFolder))

    @property
    def allContextEntities(self):
        """
        Get all context entites

        :return: Context entities
        :rtype: list
        """
        ctxtEntities = []
        for mainTypeObj in self.childs:
            ctxtEntities.append(mainTypeObj)
            for subTypeObj in mainTypeObj.childs:
                ctxtEntities.append(subTypeObj)
        return ctxtEntities

    @property
    def entityNames(self):
        """
        Get entitys names

        :return: Entity names
        :rtype: list
        """
        names = []
        for ctxtEntityObj in self.allContextEntities:
            names.extend(ctxtEntityObj.entityNames)
        return names

    @property
    def entityCodes(self):
        """
        Get entitys codes

        :return: Entity codes
        :rtype: list
        """
        codes = []
        for ctxtEntityObj in self.allContextEntities:
            codes.extend(ctxtEntityObj.entityCodes)
        return codes

    def getData(self):
        """
        get class representation as dict

        :return: Class data
        :rtype: dict
        """
        childsData = super(Context, self).getData()
        pipeData = dict()
        data = dict(contextName=self.contextName, contextPipe=pipeData, childs=childsData)
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
            if child.ctxtName == mainType:
                if subType is None:
                    return child
                for subChild in child.childs:
                    if subChild.ctxtName == subType:
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
                if child.ctxtName == mainType:
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

    def getCtxtPipe(self, stepName, taskName=None):
        """
        Get context pipe object

        :param stepName: Context step name
        :type stepName: str
        :param taskName: Context task name
        :type taskName: str
        :return: Context pipe object
        :rtype: CtxtPipe
        """
        for stepObj in self.contextPipe:
            if stepObj.pipeName == stepName:
                if taskName is None:
                    return stepObj
                for taskObj in stepObj.childs:
                    if taskObj.pipeName == taskName:
                        return taskObj

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

    def newPipeChild(self, **kwargs):
        """
        Create context pipe object

        :param kwargs: Context pipe data (key must star with ('pipe')
        :type kwargs: dict
        :return: Context pipe object
        :rtype: CtxtPipe
        """
        if kwargs.get('pipeType') == 'step':
            #--- Check New Pipe Data ---#
            for stepObj in self.contextPipe:
                if kwargs.get('pipeName') == stepObj.pipeName or kwargs.get('pipeCode') == stepObj.pipeCode:
                    raise AttributeError("!!! Context pipe %s--%s already exists !!!" % (stepObj.pipeName,
                                                                                         stepObj.pipeCode))
            #--- Create Context Pipe Object ---#
            pipeObj = CtxtPipe(parentObject=self)
            pipeObj.update(**kwargs)
            return pipeObj

    def delPipeChild(self, stepName, taskName=None):
        """
        Delete context pipe object from storage

        :param stepName: Context pipe name
        :type stepName: str
        :param taskName: Parent context pipe name
        :type taskName: str
        """
        stepObj = self.getCtxtPipe(stepName)
        if stepObj is not None:
            if taskName is None:
                self.log.debug("Removing step %r" % stepObj.pipeName)
                self.contextPipe.remove(stepObj)
            else:
                taskObj = self.getCtxtPipe(stepName, taskName=taskName)
                if taskObj is not None:
                    self.log.debug("Removing task %r" % taskObj.pipeName)
                    stepObj.childs.remove(taskObj)

    def buildEntities(self):
        """
        Build entities from disk
        """
        self.log.detail("Build %s entities ..." % self.contextName)
        for ctxtEntityObj in self.allContextEntities:
            ctxtEntityObj.buildEntities()

    def newEntity(self, **kwargs):
        """
        Create new entity

        :param kwargs: Entity data (key must starts with 'entity')
                       Requires: 'entityMainType', 'entitySubType', 'entityCode' and 'entityName'
        :type kwargs: dict
        :return: Entity object
        :rtype: Entity
        """
        #--- Get Params ---#
        mainType = kwargs.get('entityMainType')
        subType = kwargs.get('entitySubType')
        entityName = kwargs.get('entityName')
        entityCode = kwargs.get('entityCode')
        #--- Check Data ---#
        if (mainType in self._fdn.typoExclusion or subType in self._fdn.typoExclusion or
            entityName in self._fdn.typoExclusion or entityCode in self._fdn.typoExclusion):
            raise AttributeError("!!! Entity invalid: %s -- %s -- %s -- %s !!!" % (mainType, subType,
                                                                                   entityName, entityCode))
        #--- Check Context Entity ---#
        if not mainType in self.getCtxtEntityNames() or not subType in self.getCtxtEntityNames(mainType=mainType):
            raise AttributeError("Context entity not found: %s--%s" % (mainType, subType))
        #--- Create Entity Object ---#
        ctxtEntityObj = self.getCtxtEntity(mainType, subType)
        entityObj = ctxtEntityObj.newEntity(**kwargs)
        #--- Result ---#
        return entityObj

    def addEntity(self, entityObject):
        """
        Add given new entity to storage

        :param entityObject: Entity object
        :type entityObject: Entity
        """
        self.log.debug("Adding Entity %s" % entityObject.entityName)
        entityObject._parent.addEntity(entityObject)
