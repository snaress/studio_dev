import common


class CtxtEntity(common.Child):
    """
    CtxtEntity Class: Contains entity context data, child of Context

    :param parentObject: Storage object
    :type parentObject: Context
    """

    __attrPrefix__ = 'ctxt'

    def __init__(self, parentObject=None):
        super(CtxtEntity, self).__init__(parentObject=parentObject)
        #--- Data ---#
        self.ctxtType = None
        self.ctxtCode = None
        self.ctxtLabel = None
        self.ctxtFolder = None


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

    def update(self, **kwargs):
        if kwargs.get('childs') is not None:
            for child in kwargs['childs']:
                print child

    def newChild(self, **kwargs):
        """
        Create new context entity

        :param kwargs: Context entity data (key must starts with 'grp')
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
        #--- Check Context entity code ---#
        #--- Add Context entity Object ---#
        super(Context, self).addChild(childObject)
