# Rylan's Application Deployment Client

This program is meant to work in conjunction with Rylan's Application Deployment Server. This program will work with the server to retrieve all software stacks and install the requested stack on the machine requested.

## Requirements
This software was created with and requires Python 3.6+ as well as a Chromium browser as the frontend is supported by Eel which uses the Chromium browser for the front end. This client also requires Rylan's Application Deployment server for use which can found found on the following page:

>[https://github.com/RylanTaylor/Application-Deployment-Server](https://github.com/RylanTaylor/Application-Deployment-Server)

## Installation

Download the latest release on GitHub and after doing so edit "app.py" changing the two variable "default_server" and "default_port" to point toward the hosted Rylan's Application Deployment Server server. After doing so, run the following commands in the downloaded folder:

```bash
pip install -r requirements.txt
python3 app.py
```
By changing the variables in "Suite variables" and adding "ver.txt" this can also be used in conjunction with Rylan Software Suite:

>[https://github.com/RylanTaylor/Software-Suite-Updater](https://github.com/RylanTaylor/Software-Suite-Updater)

## Usage
Upon running the application, put the computer name in the "Computer Host Name" field to point the installation server to that machine. The "Owner's Username" field is included in the client but is not used by default in the Application Deployment server. Set this field to Null by default if this is not necessary and remove the entry from "./web/template/template_index.html".

 
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is provided under the MIT license, please refer to the "LICENSE" file for additional information.
