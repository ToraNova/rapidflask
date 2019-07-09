# RapidFlask - Rapid Flask Server General Deployment
RapidFlask is a general purpose flask server that can be used for rapid deployment. It comes with basic user models,
logging and some access control mechanism that are pretty much required in many scenarios. RapidFlask is meant to be
a both front/back end system that allows quick API deployment either with HTTP REST APIs or MQTT protocols. The project uses **Python3.5x**
and supports **SQLITE3** for it's database.

## Requirements (currently on virtualenv)

ArchLinux

	sudo pacman -S python-virtualenv python-pip mosquitto

Ubuntu (Please install mosquitto from source or other means gpgkey etc..)

	sudo apt-get install python3-virtualenv python3-pip


## Used Modules (Installable with pip3)

	pip3 install flask
	pip3 install flask_wtf
	pip3 install flask_login
	pip3 install flask_admin
	pip3 install flask_mail
	pip3 install flask_socketio
	pip3 install flask_babel
	pip3 install sqlalchemy
	pip3 install paho-mqtt
	pip3 install gevent
	pip3 install eventlet

## Running (virtualenv)

setup

	. envsetup

launch

	. bin/activate
	./server.py

stopping

	Ctrl-c on terminal
	deactivate

### Please read the [changelogs](changelogs.txt)

1. Incremental updates are by updates written like uxx where xx is the update number.
2. Currently the project is on __u81__
3. Please replace the certificates in the certs/ directory upon deployment !

### [License](LICENSE)

### Past naming
+ Ported from pyflask - old flask project (u1)
+ Renamed to RapidFlask from minimalflask (u7)

