import os
from coreSystem import pFile


class Foundation(object):
    """
    Foundation Class: Contains foundation datas, main core object

    :param logLvl : Log level ('critical', 'error', 'warning', 'info', 'debug', 'detail')
    :type logLvl: str
    """

    log = pFile.Logger(title="Foundation")
    __user__ = os.environ['USERNAME']

    def __init__(self, logLvl='info'):
        self.log.level = logLvl
        self.log.info("########## Launching Foundation ##########", newLinesBefore=1)