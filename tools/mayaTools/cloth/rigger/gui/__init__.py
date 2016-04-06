import os
from coreQt import pQt


#===== PACKAGE VAR =====#
toolPath = os.path.normpath(os.path.dirname(__file__))
toolName = toolPath.split(os.sep)[-1]
toolPack = __package__


#===== COMPILE UI =====#
def compileUi():
    """
    Compile ui path
    """
    #--- Log ---#
    print '%s %s %s' % ('#'*30, toolName.capitalize() ,'#'*30)
    print 'Tool Path : ', toolPath
    print 'Tool Package : ', toolPack
    print '#%s#' % ('-'*(60+len(toolName)))
    #--- Compile Ui ---#
    pQt.CompileUi().compileDir(srcDir=os.path.join(toolPath, '_src'),
                               dstDir=os.path.join(toolPath, '_ui'))
    print '%s\n' % ('#'*(62+len(toolName)))

compileUi()
