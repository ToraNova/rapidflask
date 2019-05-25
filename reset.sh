#!/bin/bash

echo "Reset Database ? (WARN:Irreversible action !)"
read yesno
if [ $yesno = "y" ] || [ $yesno = "yes" ]
then
	rm -fv *.db tokens/init.token
	rm -fv configs/mosquitto.conf
	rm -fv configs/mosquitto.auth
	rm -fv logs/*.log
fi

