import requests
import eel
import os
import sys
import json
import subprocess
import ctypes
import time
import sys
import math

server = "INSERT_DEFAULT_SERVER_HERE"
port = "8080"
clientver = "1.1.0" #Required as the server will block out of date clients

app_port = 17755
minToTimeout = 10 #Number of minutes to check status before timing out

run_program = True

def errorNotice(message): #Logs error then shows message with error before exiting program.
	log("ERROR: " + message)
	ctypes.windll.user32.MessageBoxExW(0, message, "Error", 0x0 | 0x10)
	sys.exit(42)

def log(message): # Logging function
	log_folder = "./logs"
	if not os.path.exists(log_folder):
		os.mkdir(log_folder)
	program_logs = log_folder + "/new-computer-setup.log"
	try:
		if not os.path.exists(program_logs):
			open(program_logs, "w+").write("")
		with open(program_logs, "a+") as f:
			f.write("(" + str(round(time.time() * 1000)) + ") " + message + "\n")
			print(message)
	except Exception as e: #Uses %temp%\adsclient.log if the log file cannot be created or used
		open(os.environ.get("temp") + "\\adsclient.log", "a+").write("(" + str(round(time.time() * 1000)) + ") " + "ADS Client: Unable to save to log file \"" + program_logs + "\" due to the following error: " + str(e) + "\n")
		ctypes.windll.user32.MessageBoxExW(0, "Unable to save logs, please check log path. Please check %temp%\\adsclient.log for additional information.", "Error", 0x0 | 0x10)
		sys.exit(42)

try: #Check if ADS client is already running by pinging the application port on localhost
	r = requests.get("http://localhost:" + str(app_port) + "/")
	if r.text:
		run_program = False
		message = "New Computer Setup is already running, please close open instance before starting new one."
		log(message)
		errorNotice(message)
except:
	pass

def indexSetup(): #Setup default index file by reading the template file and making appropriate changes before saving
	err = None

	with open("./web/template/template_index.html", "r") as f:
		index = f.read()

	#Replaces text in index with the current client version and max install time
	index = index.replace("REPLACE_WITH_VERSION_NUM", "Version " + clientver)
	index = index.replace("MAX_TIME_TO_INSTALL", str(math.ceil(minToTimeout)))

	try:
		r = requests.get("http://" + server + ":" + port, params={"get":"softwareInfo", "user":os.environ.get("username"), "client":clientver}) #Retrieve stack information from ADS server
		if r.status_code == 200:
			log("Recieved the following software information from server: " + r.text.strip().replace("\n","").replace("    ","").replace("\t",""))
		else:
			if r.text != "":
				output = "Failed connecting to server with message: \"" + r.text + "\"."
			else:
				output = "Failed connecting to server with status code \"" + str(r.status_code) + "\"."
			log(output)
			err = output
	except Exception as e:
		err = str(e)
	
	if not err: #Adds software stacks to index
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
		if "does not meet the server's minimum required version" in err: #Checks if error is a client version issue
			message = "Your client is out of date! An update is required before continuing."
		else:
			message = "Unable to connect to the application deployment server, check log file for additional information."
		run_program = False
		log("ERROR: " + message + " Error information: server=" + server + ";port=" + port +";error=" + err)
		errorNotice(message)

	with open("./web/index.html", "w+") as f:
		f.write(index)

def checkStatus(asset, user): #Checks status page of ADS server to see if it has completed running
	try:
		r = requests.get("http://" + server + ":" + port + "/status", params={"get":asset, "user":os.environ.get("username")})
		log("Server returned the following status code for \"" + asset + "\": " + str(r.status_code))
		if not r.status_code == 102: #A return code of 102 means it's still running
			return r.text
		else:
			return None
	except:
		return "Unable to connect to status page, check log file for additional information."
	

#Start program
indexSetup()
try:
	eel.init("web")
except Exception as e:
	message = "Error: " + str(e)
	log(message)
	run_program = False
	errorNotice(message)

@eel.expose
def runInstall(asset, stack, user):

	log("Running install: asset=" + asset + "; user=" + user + "; stack=" + stack)

	r = requests.post(
		"http://" + server + ":" + port,
		data={"asset":asset, "stack":stack, "user":user, "requser":os.environ.get("username")},
		timeout=60.0 #Waits a minute to timeout
		)

	if r.status_code == 202: #Status code 202 means the server has accepted and begun the installation
		res = None

		checkInterval = 3 #Number of seconds to wait between status checks
		totalChecks = int(60 / checkInterval * minToTimeout)

		for i in range(totalChecks): #Makes requests to the status server the number of times requested in the global variable "minToTimeout" with the interval set above in "checkInterval"
			x = i + 1
			eel.sleep(checkInterval)
			log("Checking status of \"" + asset + "\" (Check " + str(x) + "/" + str(totalChecks) + ")")
			res = checkStatus(asset, user)
			if res:
				break

		if res:
			output = res
		else:
			output = "ERROR: No response from server after " + str(minToTimeout) + " minutes, check ADS server logs for more information."
		
		log("Status of \"" + asset + " returned the following: " + output)

		return output
	else:
		output = "ERROR: " + r.text
		log(output)
		return output

if run_program: #run_program is set to True if there are no errors in the index and program setup, if this is True then start the eel app
	try:
		eel.start("index.html",size=(800,800),port=app_port)
	except Exception as e:
		errorNotice("Unable to start program due to the following error: " + str(e))