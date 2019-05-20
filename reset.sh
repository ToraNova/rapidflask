#!/bin/bash

echo "Reset Database ? (WARN:Irreversible action !)"
read yesno
if [ $yesno = "y" ] || [ $yesno = "yes" ]
then
	rm -fv *.db tokens/init.token
fi

