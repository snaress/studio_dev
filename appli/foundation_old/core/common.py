import pprint


class Child(object):
    """
    Child Class: Contains node data, child of Storage

    :param parentObject: Storage object
    :type parentObject: Storage
    """

    __attrPrefix__ = 'None'

    def __init__(self, parentObject=None):
        self._parent = parentObject
        self._fdn = self._parent._fdn
        self.log = self._parent.log

    @property
    def attributes(self):
        """
        List class attributes

        :return: Attributes
        :rtype: list
        """
        attrs = []
        for attr in self.__dict__.keys():
            if attr.startswith(self.__attrPrefix__):
                attrs.append(attr)
        return attrs

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
        Update class data with given attributes

        :param kwargs: child data (key must start with self.__attrPrefix__)
        :type kwargs: dict
        """
        for k, v in kwargs.iteritems():
            if k in self.attributes:
                setattr(self, k, v)
            else:
                self.log.warning("!!! Unrecognized attribute: %s. Skipp !!!" % k)

    def __str__(self):
        """
        get class representation as str

        :return: Class data
        :rtype: str
        """
        return pprint.pformat(self.getData())


class Storage(object):
    """
    Storage Class: Contains data storage, child of Foundation

    :param fdnObject: Foundation object
    :type fdnObject: foundation.Foundation
    """

    def __init__(self, fdnObject):
        self._fdn = fdnObject
        #--- Datas ---#
        self.childs = []
        #--- Update ---#
        self._init()
        self._setup()

    def _init(self):
        """
        Init Storage core object
        """
        self.log = self._fdn.log
        self.log.title = self.__class__.__name__

    def _setup(self):
        """
        Setup Storage core object
        """
        self.log.info("#===== Setup %s Core =====#" % self.__class__.__name__, newLinesBefore=1)

    def getData(self):
        """
        get class representation as dict

        :return: Class data
        :rtype: dict
        """
        data = dict()
        for n, grpObj in enumerate(self.childs):
            data[n] = grpObj.getData()
        return data

    def getValues(self, attrName):
        """
        Get value from given attribute on all childs

        :param attrName: Attribute name
        :type attrName: str
        :return: Values
        :rtype: list
        """
        values = []
        for child in self.childs:
            if hasattr(child, attrName):
                values.append(getattr(child, attrName))
            else:
                self.log.warning("Attribute %r not found" % attrName)
        return values

    def getChilds(self, **kwargs):
        """
        Get childs object matching with given attribute value

        :param kwargs: Data to match (key should start with self.__attrPrefix__)
        :type kwargs: dict
        :return: Childs matching with data
        :rtype: list
        """
        childs = []
        for child in self.childs:
            addChild = True
            #--- Check Attributes ---#
            for k, v in kwargs.iteritems():
                if hasattr(child, k):
                    if not getattr(child, k) == v:
                        addChild = False
                else:
                    addChild = False
            #--- Store Child ---#
            if addChild:
                childs.append(child)
        #--- Result ---#
        return childs

    def newChild(self, **kwargs):
        """
        Create new group

        :param kwargs: Child data (key must starts with self.__attrPrefix__)
        :type kwargs: dict
        :return: Group object
        :rtype: Group
        """
        grpObj = Child(parentObject=self)
        grpObj.update(**kwargs)
        return grpObj

    def addChild(self, childObject):
        """
        Add Child object to storage

        :param childObject: Child object
        :type childObject: Child
        """
        self.childs.append(childObject)

    def clearChilds(self):
        """
        Clear childs contents
        """
        self.childs = []

    def buildChilds(self, storageData):
        """
        Populate childs from given dict

        :param storageData: Storage dict
        :type storageData: dict
        """
        self.log.detail("Build childs from storageData ...")
        self.clearChilds()
        for n in sorted(storageData.keys()):
            self.addChild(self.newChild(**storageData[n]))

    def __str__(self):
        """
        get class representation as str

        :return: Class data
        :rtype: str
        """
        return pprint.pformat(self.getData())
