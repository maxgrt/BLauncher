#!/usr/bin/python3

import zipfile
import shutil
import os
import sys

print("BLauncher is updating now...")
z = zipfile.ZipFile("update.zip", "r")
print("Extracting files...")
z.extractall()
print("Copying files...")
shutil.copyfile("BLauncher-master/src/main.py", "main.py")
shutil.copyfile("BLauncher-master/src/lang.py", "lang.py")
print("Deleting unnecessary files...")
os.remove("update.zip")
shutil.rmtree("BLauncher-master")
print("Sucsess!")

os.system(sys.executable + " main.py")
