#--------------------------------------------------
# sender_io.py
# basic file that handles socket io use-cases
# introduced 8/1/2019
#--------------------------------------------------

from flask import Blueprint
from flask_socketio import Namespace, emit
from flask import render_template, redirect, url_for
import datetime

import pkg.const as const
import pkg.resource.rdef as res
import json

#mb_dpi use
from mb_dpi import send


# SenderNamespace is a namespace which handles the socket io on the sender (tx).
# based on library written by
# Jason Loh mailto : jasonlohjc@gmail.com
# edited by ToraNova mailto: chia_jason96@live.com

# edits 2nd april :
# remove method send via the setup phase, now each machine takes the scheme from the ui
#

class SenderNamespace(Namespace):

	def on_connect(self):
		print("sender interface connected")
		self.main=None

	def on_disconnect(self):
		print("sender interface disconnected")

	def on_transmit(self,json):
		if(self.main):
			msg_string = json.get('msg_string')
			self.main.pushmsg(msg_string)
		else:
			emit('status_message',{'status':"Please establish connection first !"})

	def on_setupconn(self,json):
		mbox_addr = json.get('mbipaddr')
		recv_addr = json.get('rxipaddr')
		method = json.get('scheme')
		target_port = int(json.get('conport0'))
		middle_port = int(json.get('conport1'))
		print("attempting to setup conn")
		if(self.main):
			# terminate the previous running threads
			self.main.killthread()
			self.main.join()
		self.main = send.MBDPI_transmitter(recv_addr,mbox_addr,target_port,middle_port,method,'/sender')
		self.main.start() #starts the receiver (never use run here, we need the thread effect)
