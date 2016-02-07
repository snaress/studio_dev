import os
from coreQt import procQt as pQt


#===== PACKAGE VAR =====#
toolPath = os.path.normpath(os.path.dirname(__file__))
toolName = toolPath.split(os.sep)[-1]
toolPack = __package__


#===== COMPILE UI =====#
print '%s %s %s' % ('#'*30, toolName.capitalize() ,'#'*30)
print 'Tool Path : ', toolPath
print 'Tool Package : ', toolPack
print '#%s#' % ('-'*(60+len(toolName)))
def compileUi(uiFiles):
    if isinstance(uiFiles, basestring):
        uiFiles = [uiFiles]
    for f in uiFiles:
        pQt.CompileUi().compileFile(srcFile=os.path.join(toolPath, '_src', f),
                                    dstFile=os.path.join(toolPath, '_ui', f.replace('.ui', '.py')))
print '%s\n' % ('#'*(62+len(toolName)))
