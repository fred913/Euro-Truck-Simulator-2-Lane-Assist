import json
import vdf
import os
try:
    import winreg
    STEAM_INSTALL_FOLDER = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Wow6432Node\\Valve\\Steam"), "InstallPath")[0]
except:
    STEAM_INSTALL_FOLDER = r"C:\Program Files (x86)\Steam"

LIBRARY_FOLDER_LOCATION = r"steamapps\libraryfolders.vdf"
SECONDARY_LIBRARY_FOLDER_LOCATION = r"D:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf"
ETS2_PATH_IN_LIBRARY = r"steamapps\common\Euro Truck Simulator 2"
ATS_PATH_IN_LIBRARY = r"steamapps\common\American Truck Simulator"
VERIFY_FILE = "base.scs"

def ReadSteamLibraryFolders():
    libraries = []
    
    if os.path.isfile(os.path.join(STEAM_INSTALL_FOLDER, LIBRARY_FOLDER_LOCATION)):
        file = open(os.path.join(STEAM_INSTALL_FOLDER, LIBRARY_FOLDER_LOCATION), "r")
    else:
        file = open(SECONDARY_LIBRARY_FOLDER_LOCATION, "r")
        
    file = vdf.load(file)   
    for key in file["libraryfolders"]:
        if key.isnumeric():
            libraries.append(file["libraryfolders"][key]["path"])    
    
    return libraries

def FindSCSGames():
    try:
        libraries = ReadSteamLibraryFolders()
    except:
        libraries = [r"C:\Games"]
    foundGames = []
    
    for library in libraries:
        if os.path.isfile(library + "\\" + ETS2_PATH_IN_LIBRARY + "\\" + VERIFY_FILE):
            foundGames.append(library + "\\" + ETS2_PATH_IN_LIBRARY)
        if os.path.isfile(library + "\\" + ATS_PATH_IN_LIBRARY + "\\" + VERIFY_FILE):
            foundGames.append(library + "\\" + ATS_PATH_IN_LIBRARY)
    
    return foundGames
