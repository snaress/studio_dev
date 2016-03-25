import sys
from coreSys import pFile


tool = None
log = pFile.Logger(title=sys.argv[0], level=sys.argv[1])


########## Compile Ui ##########
#--- Tool ---#
from mayaTools.util.displayColor import gui
gui.compileUi()


########## Init Requires ##########
requires = [dict(libs=['coreSys.pFile',
                       'coreQt.pQt']),
            dict(mayaCore=['mayaCore.cmds.pUtil']),
            dict(toolUi=['mayaTools.util.displayColor.gui._ui.displayColorUI']),
            dict(toolGui=['mayaTools.util.displayColor.gui.displayColorWgts',
                          'mayaTools.util.displayColor.gui.displayColorUi'])]


########## Reload Requires ##########
for require in requires:
    for cat, values in require.iteritems():

        #--- Get Category ---#
        log.debug("#--- Reload %s ---#" % cat)

        #--- Reload Module ---#
        for module in values:
            _module = __import__(str(module), globals(), locals(), -1)
            result = reload(_module)
            tool = _module
            log.detail(str(result).split(' from ')[0])
            log.detail(' from   %s' % (str(result).split(' from ')[-1]))

        #--- Separator ---#
        log.detail(' ')


########## Launch Tool ##########
if tool is not None:
    tool.mayaLaunch(logLvl=log.level, parent=sys.argv[2])
