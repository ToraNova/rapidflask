#--------------------------------------------------
# middlebox_io dpi based interface logic
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

from mb_dpi.rule_generator import EncRules, SaveParams, SaveKeys, KeyGen, PMGen
from mb_dpi.middlebox import TheServer, TheTLSServer
from threading import Thread

# MiddleboxNamespace is a namespace which handles the socket io on the middlebox.
# based on library written by
# Jason Loh mailto : jasonlohjc@gmail.com
# edited by ToraNova mailto: chia_jason96@live.com
class MiddleboxNamespace(Namespace):

	def on_connect(self):
		print("middlebox interface connected")

	def on_disconnect(self):
		print("middlebox interface disconnected")

	def on_setupconn(self,json):
		port0=int(json.get('conport0'))
		port1=int(json.get('conport1'))

		server = TheServer('', port0)
		server2 = TheTLSServer('', port0+1)
		try:
			server_thread = Thread(target= server.main_loop, args =( ))
			server2_thread = Thread(target= server2.main_loop, args =( ))
			server_thread.start()
			server2_thread.start()
			emit("status_change",{"status":"threads started"})
		except KeyboardInterrupt:
			emit("status_change",{"status":"threads error"})

	def on_rulegen(self):
		print("RG is generating system parameters....")
		[params, g] = PMGen(512, 160)
		print (params)

		print("RG is generating RG and MB keypairs....")
		[pk_rg, sk_rg] = KeyGen(params, g)
		[pk_mb, sk_mb] = KeyGen(params, g)
		print("G: " + str(g))
		print("PK_RG: " + str(pk_rg))
		print("SK_RG: " + str(sk_rg))
		print("PK_MB: " + str(pk_mb))
		print("SK_MB: " + str(sk_mb))
		print("RG is generating encrypted rules....")
		EncRules(params, g, sk_rg, sk_mb, pk_mb)
		print("RG is generating signature for encrypted rules....")
		SaveParams(params, g)
		SaveKeys(g, pk_mb, sk_mb, pk_rg, sk_rg)
