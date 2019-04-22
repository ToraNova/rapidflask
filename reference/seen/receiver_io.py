#--------------------------------------------------
# receiver_io.py
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

# mb_dpi imports
from mb_dpi import recv

# ReceiverNamespace is a namespace which handles the socket io on the receiving side (RX).
# based on library written by
# Jason Loh mailto : jasonlohjc@gmail.com
# edited by ToraNova mailto: chia_jason96@live.com
class ReceiverNamespace(Namespace):

	main = None

	def on_connect(self):
		print("receiver interface connected")
		self.main=None

	def on_disconnect(self):
		print("receiver interface disconnected")

	def on_setupconn(self,json):
		listen_addr = '0.0.0.0'
		listen_port = int(json.get('conport0'))
		method = json.get('scheme')
		client_certs = 'client.crt'

		if(self.main):
			# terminate the previous running threads
			self.main.killthread()
			self.main.join()
		self.main = recv.MBDPI_receiver(listen_addr,listen_port,method,'/receiver')
		self.main.start() #starts the receiver (never use run here, we need the thread effect)
