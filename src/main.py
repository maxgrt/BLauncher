#!/usr/bin/python3

import minecraft_launcher_lib
import subprocess
from threading import Thread
import requests
import random
import string
import os
import sys
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import lang

VERSION_C = 1
AUTO_UPDATE = True
# settings
path = "game" # path to install

# game versions
if not(os.path.isdir(path + "/versions/")):
    os.mkdir(path)
    os.mkdir(path + "/versions/")

installed_ver = []
all_ver = []
ver_list = []

for i in minecraft_launcher_lib.utils.get_installed_versions(path):
    installed_ver.append(i.get("id"))
for i in minecraft_launcher_lib.utils.get_version_list():
    all_ver.append(i.get("id"))

ver_list.append(lang.installed + ":")
ver_list.extend(installed_ver)
ver_list.append(lang.ready_to_install + ":")
ver_list.extend(all_ver)

# functions
def logger(string):
    log.configure(state="normal")
    log.insert(END, string + "\n")
    log.yview(END)
    log.configure(state="disabled")
    root.update()

def downloader(url, name):
	file = open(name, "wb")
	request = requests.get(url)
	file.write(request.content)
	file.close()

def update_check():
	logger("Checking for updates...")
	version_code = requests.get("https://raw.githubusercontent.com/maxgrt/BLauncher/master/src/version_code.txt")
	last = int(version_code.content.decode("utf-8"))
	if last > VERSION_C:
		logger("Update found! Downloading...")
		thread1 = Thread(target=downloader, args=("https://github.com/maxgrt/BLauncher/archive/master.zip", "update.zip"))
		thread1.start()
		thread1.join()
		#downloader("https://github.com/maxgrt/BLauncher/archive/master.zip", "update.zip")
		logger("Update.zip downloaded.")
		root.destroy()
		py_executable = sys.executable
		os.system(py_executable + " update.py")
	else:
		logger("No updates found")

def setProgress(value, max_value):
    progresspersent = max_value[0] / 100
    progr = value / progresspersent
    progress["value"] = progr
    root.update()

def setMax(max_value, value):
    max_value[0] = value


def run():
    if version.get() in installed_ver or version.get() in all_ver:
        run.configure(state="disabled")
        username.configure(state="disabled")
        uuid.configure(state="disabled")
        access_token.configure(state="disabled")
        mojang_login.configure(state="disabled")
        version.configure(state="disabled")

        with open(path + "/profile.json", "w") as pj:
            pj.write(
                "{ \"nick\": \"" + username.get() + "\", \"uuid\": \"" + uuid.get() + "\", \"accToken\": \"" + access_token.get() + "\", \"version\": \"" + version.get() + "\" }")
        max_value = [0]
        callback = {
             "setStatus": lambda text: logger(text),
             "setProgress": lambda value: setProgress(value, max_value),
             "setMax": lambda value: setMax(max_value, value)
        }
        minecraft_launcher_lib.install.install_minecraft_version(version.get(), path, callback)
        options = {
            "username": username.get(),
            "uuid": uuid.get(),
            "token": access_token.get()
        }
        command = minecraft_launcher_lib.command.get_minecraft_command(version.get(), path, options)
        print(command)
        subprocess.Popen(command)
        run.configure(state="normal")
        username.configure(state="normal")
        uuid.configure(state="normal")
        access_token.configure(state="normal")
        version.configure(state="normal")
        mojang_login.configure(state="normal")
        logger("Sucsess!")
    else:
            mb.showerror(lang.error, lang.version_is_not_detected)

# Mojang login functions
def mlogin():
    def m_log():
        login_data = minecraft_launcher_lib.account.login_user(ml.get, mp.get)
        username.insert(0, login_data["selectedProfile"]["name"])
        uuid.insert(0, login_data["selectedProfile"]["id"])
        access_token.insert(0, login_data["accessToken"])
    root1 = Tk()
    root1.title("BL")
    root1.resizable(False, False)
    mltxt = Label(root1, text=lang.login)
    mltxt.grid(row=0, column=0)
    mptxt = Label(root1, text=lang.password)
    mptxt.grid(row=1, column=0)
    ml = Entry(root1)
    ml.grid(row=0, column=1)
    mp = Entry(root1)
    mp.grid(row=1, column=1)
    lbtn = Button(root1, text=lang.log_in, command=m_log)
    lbtn.grid(row=2, column=0, columnspan=2)


# Tkinter
root = Tk()
root.title("BLauncher")
#root.geometry("500x200") <-- This is bad idea :(
root.resizable(False, False)

# Mojang Login
mojang_login = Button(root, text=lang.mojang_login, command=mlogin)
mojang_login.grid(row=0, column=0, columnspan=2)

# nick
txt1 = Label(root, text=lang.nick)
txt1.grid(row=1, column=0)
username = Entry(root)
username.grid(row=1, column=1)

# UUID
txt2 = Label(root, text=lang.uuid)
txt2.grid(row=2, column=0)
uuid = Entry(root)
uuid.grid(row=2, column=1)

# AccessToken
txt3 = Label(root, text=lang.access_token)
txt3.grid(row=3, column=0)
access_token = Entry(root)
access_token.grid(row=3, column=1)

# version
version = ttk.Combobox(root, values=ver_list)
version.grid(row=4, column=0, columnspan=2)

# progress
progress = ttk.Progressbar(root, length=100)
progress.grid(row=5, column=0, columnspan=2)

# run/install
run = Button(root, text=lang.install_run, command=run)
run.grid(row=6, column=0, columnspan=2)

# log
log = Text(root, height=10, width=41, state="disabled")
log.grid(row=0, column=3, rowspan=7)

# create LauncherProfiles.json
jsonstr = """
{
  "authenticationDatabase": {},
  "clientToken": \"""" + "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(16)) + """\",
  "profiles": {
    "comment": "This is workaround to make Forge and OptiFine installers work properly"
  }
}
"""
if not(os.path.isfile(path + "/launcher_profiles.json")):
    with open(path + "/launcher_profiles.json", "w") as lp:
        lp.write(jsonstr)

# load profile
if os.path.isfile(path + "/profile.json"):
    rp = open(path + "/profile.json", "r")
    profile = json.load(rp)
    username.insert(0, profile['nick'])
    uuid.insert(0, profile['uuid'])
    access_token.insert(0, profile['accToken'])
    version.insert(0, profile['version'])

# log
logger("BLauncher v0.1 by maxgrt")
logger("!!! Minecraft was created by Mojang. All rights belong to their owners. !!!\n")
if AUTO_UPDATE:
	update_check()
root.mainloop()
