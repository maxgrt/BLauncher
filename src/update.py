#!/usr/bin/python3

import zipfile
import shutil
import os
import sys

banner = """
 ____  _                            _               
|  _ \| |                          | |              
| |_) | |     __ _ _   _ _ __   ___| |__   ___ _ __ 
|  _ <| |    / _` | | | | '_ \ / __| '_ \ / _ \ '__|
| |_) | |___| (_| | |_| | | | | (__| | | |  __/ |   
|____/|______\__,_|\__,_|_| |_|\___|_| |_|\___|_|   
                         upgrader v0.2
"""
print(banner)
print("[i] BLauncher is updating now...")
z = zipfile.ZipFile("update.zip", "r")
print("[i] Extracting files...")
z.extractall()
print("[i] Copying files...")

for i in os.walk("BLauncher-master/src"):
	for x in i[2]:
		if x == "update.py":
			pass
		else:
			shutil.copy(os.path.join("BLauncher-master/src/", x), os.path.dirname(os.path.realpath(__file__)))
			print("[+] Copied: " + x)


print("[i] Deleting unnecessary files...")
#os.remove("update.zip")
shutil.rmtree("BLauncher-master")
print("[i] Sucsess!")

os.system(sys.executable + " main.py")
