import os
import pFile


#===== ENV VAR =====#
appsPath = pFile.conformPath("F:/apps")
studio = pFile.conformPath("F:/rnd/workspace/studio_dev")
iconsPath = pFile.conformPath(os.path.join(studio, 'libs', '_icons'))


#===== SYSTEM =====#
cmdExe = pFile.conformPath("C:/Windows/System32/cmd.exe")
python27 = pFile.conformPath("C:/Python27/python.exe")
pyUic = pFile.conformPath("C:/Python27/Lib/site-packages/PyQt4/pyuic4.bat")
pyCharm = pFile.conformPath('"C:/Program Files (x86)/JetBrains/PyCharm Community Edition 3.4.1/bin/pycharm.exe "')


#===== MAYA =====#
mayaPath = pFile.conformPath(os.path.join(appsPath, "Autodesk", "Maya2014"))
maya = pFile.conformPath(os.path.join(mayaPath, "bin", "maya.exe"))
mayaPy = pFile.conformPath(os.path.join(mayaPath, "bin", "mayapy.exe"))
mayaBatch = pFile.conformPath(os.path.join(mayaPath, "bin", "mayabatch.exe"))
mayaRender = pFile.conformPath(os.path.join(mayaPath, "bin", "Render.exe"))


#===== NUKE =====#
nuke5 = pFile.conformPath(os.path.join(appsPath, "Nuke5.0v2", "nuke5.0.exe"))
nuke9 = pFile.conformPath(os.path.join(appsPath, "Nuke9.0v1", "nuke9.0.exe"))
nuke = nuke9
