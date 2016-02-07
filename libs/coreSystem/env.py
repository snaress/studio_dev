import os


#===== ENV VAR =====#
appsPath = os.path.normpath("F:/apps")


#===== SYSTEM =====#
cmdExe = 'C:/Windows/System32/cmd.exe'
python27 = 'C:/Python27/python.exe'
pyUic = "C:/Python27/Lib/site-packages/PyQt4/pyuic4.bat"
pyCharm = '"C:/Program Files (x86)/JetBrains/PyCharm Community Edition 3.4.1/bin/pycharm.exe "'


#===== MAYA =====#
mayaPath = os.path.join(appsPath, "Autodesk", "Maya2014")
maya = os.path.join(mayaPath, "bin", "maya.exe")
mayaPy = os.path.join(mayaPath, "bin", "mayapy.exe")
mayaBatch = os.path.join(mayaPath, "bin", "mayabatch.exe")
mayaRender = os.path.join(mayaPath, "bin", "Render.exe")


#===== NUKE =====#
nuke5 = os.path.join(appsPath, "Nuke5.0v2", "nuke5.0.exe")
nuke9 = os.path.join(appsPath, "Nuke9.0v1", "nuke9.0.exe")
nuke = nuke9
