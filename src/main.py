#!/usr/bin/python3

import sys
import json
from threading import Thread
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
import random
import string

import langa as lang # language module

# =================== #
#      SETTINGS       #
# =================== #

path = 'game' # folder to install Minecraft
version_code = 2 # do not change this
check_for_updates = True 

# =================== #
#      FUNCTIONS      #
# =================== #

# get versions
if not(os.path.isdir(os.path.join(path, 'versions'))):
	os.mkdir(path)
	os.mkdir(os.path.join(path, 'versions'))

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
	version_code = requests.get("https://raw.githubusercontent.com/maxgrt/BLauncher/master/src/version_code.txt")
	last = int(version_code.content.decode("utf-8"))
	if last > VERSION_C:
		thread1 = Thread(target=downloader, args=("https://github.com/maxgrt/BLauncher/archive/master.zip", "update.zip"))
		thread1.start()
		thread1.join()
		root.destroy()
		py_executable = sys.executable
		os.system(py_executable + " update.py")

def show_settings():
	pass

def setProgress(value, max_value):
	progresspersent = max_value[0] / 100
	progr = value / progresspersent
	progress["value"] = progr
	root.update()

def setMax(max_value, value):
	max_value[0] = value

def run():
	if version.get() in installed_ver or version.get() in all_ver:
		runbtn.configure(state='disabled')
		nick.configure(state='disabled')
		version.configure(state='disabled')
		nickname = nick.get()
		ver = version.get()
		#######
		uuid = 'bhfsdbhf'
		token = 'dfcfghgnjg'
		#######
		with open(os.path.join(path, 'profile.json'), 'w') as pj:
			pj.write(json.dumps({
				'nick': nickname,
				'version': ver,
				'uuid': uuid,
				'accToken': token
				}))
		max_value = [0]
		callback = {
			"setStatus": lambda text: logger(text),
			"setProgress": lambda value: setProgress(value, max_value),
			"setMax": lambda value: setMax(max_value, value)
		}
		minecraft_launcher_lib.install.install_minecraft_version(ver, path, callback)
		
		options = {
			'username': nickname,
			'uuid': uuid,
			'token': token
		}
		command = minecraft_launcher_lib.command.get_minecraft_command(ver, path, options)
		subprocess.Popen(command)
		runbtn.configure(state='normal')
		nick.configure(state='normal')
		version.configure(state='normal')

	else:
		mb.showerror(lang.error, lang.version_is_not_detected)
def runner():
	try:
		run()
	except Exception as e:
		raise e

def mojanglogin():
	login = sd.askstring('BLauncher', lang.ask_mojang_login)
	password = sd.askstring('BLauncher', lang.ask_mojang_password)
	try:
		login_data = minecraft_launcher_lib.account.login_user(login, password)
		with open(os.path.join(path, 'profile.json'), 'w') as pj:
			pj.write(json.dumps({
				'nick': login_data["selectedProfile"]["name"],
				'version': version.get(),
				'uuid': login_data["selectedProfile"]["id"],
				'accToken': login_data["accessToken"]
				}))
	except Exception as e:
		logger(lang.error_during_login)

# =================== #
#       TKINTER       #
# =================== #

root = Tk()
root.title("BLauncher")
root.resizable(False, False)

# MENUBAR
#menubar = Menu(root)
#root.config(menu=menubar)

#file_menu = Menu(menubar)
#file_menu.add_command(label=lang.settings, command=show_settings)
#file_menu.add_command(label=lang.exit, command=exit)
#menubar.add_cascade(label=lang.file, menu=file_menu)

f_top = Frame(root)
f_top.pack()
f_bottom = Frame(root)
f_bottom.pack()

log = Text(f_top, width=50, height=10,state='disabled', font='TkFixedFont')
log.pack()
progress = ttk.Progressbar(f_top, length=100)
progress.pack(fill='x')

# ACCOUNT SECTION
f_account = LabelFrame(f_bottom, text=lang.account)
f_account.pack(side=LEFT)

txt1 = Label(f_account, text=lang.nick)
txt1.pack()
nick = Entry(f_account)
nick.pack()
mlogin = Button(f_account, text=lang.mojang_login, command=mojanglogin)
mlogin.pack(fill='x')

# VERSION SECTION
f_version = LabelFrame(f_bottom, text=lang.version)
f_version.pack(side=LEFT, fill='y')

version = ttk.Combobox(f_version, values=ver_list)
version.pack()

# RUN SECTION
f_run = LabelFrame(f_bottom, text=lang.run)
f_run.pack(side=LEFT, fill='y')

runbtn = Button(f_run, text=lang.run, comman=runner)
runbtn.pack()

# =================== #
#        FINAL        #
# =================== #

# load profile
if os.path.isfile(os.path.join(path, 'profile.json')):
	rp = open(os.path.join(path, 'profile.json'), 'r')
	try:
		profile = json.load(rp)
		nick.insert(0, profile['nick'])
		version.insert(0, profile['version'])
	except Exception as e:
		pass
	

# launcher-profiles.json
jsonstr = """
{
  "authenticationDatabase": {},
  "clientToken": \"""" + "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(16)) + """\",
  "profiles": {
    "comment": "This is workaround to make Forge and OptiFine installers work properly"
  }
}
"""
if not(os.path.isfile(os.path.join(path, 'launcher_profiles.json'))):
	with open(os.path.join(path, 'launcher_profiles.json'), 'w') as lp:
		lp.write(jsonstr)

logger('''
 ____  _      
|  _ \| |     
| |_) | |     
|  _ <| |     
| |_) | |____ 
|____/|______|   v 0.2 by maxgrt
	''')

root.mainloop()
