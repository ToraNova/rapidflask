#!/bin/bash

echo "Reset Database ? (WARN:Irreversible action !)"
read yesno
if [ -z $yesno ]
then
	exit 0
else
	if [ $yesno = "y" ] || [ $yesno = "yes" ]
	then
		echo "Resetting server"
		rm -fv *.db tokens/init.token
		rm -fv configs/mosquitto.conf
		rm -fv configs/mosquitto.auth
		rm -fv logs/*.log logs/*.tmp
	fi
fi

