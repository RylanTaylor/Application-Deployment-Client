import requests
import eel
import os
import sys
import json
import sys
import subprocess
import ctypes
import time
from pathlib import Path

default_server = "INSERT_DEFAULT_SERVER_HERE"
default_port = "177055"

run_program = True

try:
	
	#Suite variables

	suite_files = os.environ.get("localappdata") + "\\ads-client\\"
	suite_programs = suite_files + "programs\\" 
	suite_settings = suite_files + "settings\\"
	suite_logs = suite_files + "logs\\"

	suite_general_settings = suite_settings + "settings.json"

	program_location = suite_programs + "application-deployment-client\\"
	program_settings = suite_settings + "application-deployment-client.json"
	program_logs = suite_logs + "application-deployment-client.log"

	Path(suite_programs).mkdir(parents=True, exist_ok=True)
	Path(suite_settings).mkdir(parents=True, exist_ok=True)
	Path(suite_logs).mkdir(parents=True, exist_ok=True)
	Path(program_location).mkdir(parents=True, exist_ok=True)

	#Functions

	def log(message): # Logging function
		if not os.path.exists(program_logs):
			open(program_logs, "w+").write("")
		with open(program_logs, "a+") as f:
			f.write("(" + str(round(time.time() * 1000)) + ") " + message + "\n")

	def get_user(): # Get user, check default suite credentials but default to computer credentials if all else fails
		if os.path.exists(suite_general_settings):
			with open(suite_general_settings) as f:
				return json.loads(f.read())["Credentials"]["Username"]
		else:
			return os.environ.get("username")


	if not os.path.exists(program_settings): #Check if server settings are present, save default settings if not
		with open(program_settings, "w+", encoding="utf-8") as f:
			server_info = {"Server" : default_server, "Port" : default_port}

			f.write(json.dumps(server_info, indent=4))


	server = None
	port = None

	with open(program_settings, "r") as f: #Get server information
		settings = json.loads(f.read())
		
		server = settings["Server"]
		port = settings["Port"]

	def indexSetup(): #Setup default index file
		cont = False
		err = None

		with open("./web/template/template_index.html", "r") as f:
			index = f.read()

		try:
			set_ver = "Version " + open("./ver.txt", "r", encoding="utf-8").read()
		except:
			set_ver = ""

		index = index.replace("REPLACE_WITH_VERSION_NUM", set_ver)

		try:
			r = requests.get("http://" + server + ":" + port, params={"get":"softwareInfo", "user":get_user()})
			if r.status_code == 200:
				log("Recieved software information from server.")
				cont = True
			else:
				output = "Server status code returned \"" + r.status_code + "\"."
				log(output)
				err = output
		except Exception as e:
			log(err)
			err = str(e)
		
		if cont:
			softwareStacks = r.json()

			dataString = ""
			for item in softwareStacks["Software Stacks"]:
				if item != "Defaults":
					dataString += "<option value=\"" + item + "\" "
					if item == "Standard":
						dataString += "selected"
					dataString += ">" + item + "</option>\n"
			
			index = index.replace("REPLACE_WITH_STACK_INFO", dataString)
		else:
			index = "<center><h1>Unable to connect to Application Deployment Server, please contact your administrator.</h1><br />Error information:<br /><textarea style=\"width:40%;height:5%\">server=" + server + ";port=" + port +";error=" + err + "</textarea></center>"
		with open("./web/index.html", "w+") as f:
				f.write(index)

	if run_program: #Start program
		indexSetup()
		eel.init("./web")

	@eel.expose
	def runPing(asset):
		return 0

	@eel.expose
	def runInstall(asset, stack, user):

		log("Running install: asset=" + asset + "; user=" + user + "; stack=" + stack)

		r = requests.post(
			"http://" + server + ":" + port,
			data={"asset":asset, "stack":stack, "user":user, "requser":get_user()},
			timeout=None #Waits forever to timeout
			)

		if r.status_code == 200:
			output = "All programs successfully installed on " + asset + "!"
			log(output)
			return output
		else:
			output = "ERROR: " + r.text
			log(output)
			return output

	def close_callback_func(one,two):
		sys.exit(0)

	if run_program:
		try:
			eel.start("index.html",size=(800,800),close_callback=close_callback_func,port=17755)
		except (SystemExit, MemoryError, KeyboardInterrupt):
			pass
except Exception as e:
	ctypes.windll.user32.MessageBoxW(0, "Error: " + str(e), "Error", 1)
	log("Error: " + str(e))