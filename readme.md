# Application Deployment Client

This program is meant to work in conjunction with the Application Deployment Server found in the requirements section. This program will work with the server to retrieve all software stacks and install the requested stack on any supported machine.

## Requirements
This software was created with and requires Python 3.6+ as well as a Chromium browser as the frontend is supported by Eel which uses the Chromium browser. This client also requires the Application Deployment Server for use which can found found on the following page:

>[https://github.com/RylanTaylor/Application-Deployment-Server](https://github.com/RylanTaylor/Application-Deployment-Server)

## Installation

Download the latest release on GitHub and after doing so edit "app.py" changing the two variable "server" and "port" to point toward the hosted Application Deployment Server api. After doing so, run the following commands in the downloaded folder:

```bash
pip install -r requirements.txt
python3 app.py
```

## Usage
Upon running the application, put the computer name in the "Computer Host Name" field to point the installation server to that machine. The "Owner's Username" field is used for logging purposes only and is not a required field, leave blank if needed. Select a software stack to install on the machine then click "Submit" to begin the installation. After the installation has completed an alert will be shown with the status.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is provided under the MIT license, please refer to the "LICENSE" file for additional information.
