#--------------------------------------------------
# socketio.py
# basic file that handles socket io use-cases
# introduced 8/1/2019
#--------------------------------------------------

from flask import Blueprint
from flask_socketio import Namespace
from flask_socketio import send, emit

from flask import render_template, redirect, url_for
import datetime

from pkg.system.servlog import srvlog
import pkg.const as const
import pkg.resource.rdef as res
import json

bp = Blueprint('sock_sysutil', __name__, url_prefix='') #flask sock bp

def livelog(logstring,logtype='logins'):

	from pkg.source import out as socketio # use carefully to prevent circular imports

	try:
		#live logins - update7
		socketio.emit('livelog_cast',
		{'logtype':logtype,
		'logstring':logstring},
		namespace='/sysutil')
		# emit may also contain namespaces to emit to other classes
	except Exception as e:
		print("Exception has occurred".str(e))
		srvlog["oper"].info("Exception ocurred in live logging :"+str(e))

#----------------------------------------------------------------------------------------
# ROUTES
#----------------------------------------------------------------------------------------

@bp.route('/sysclock',methods=['GET','POST'])
def sysclock():
	return render_template('flask_sockio/sysclock.html')

#SystemUtilNamespace is a socket.io class that handles system utility realtime
#data, currently implemented methods is the on_sync_time that allows a realtime
#clock on the server - 8/1/2019 ToraNova
#TODO: implement mapping system
class SystemUtilNamespace(Namespace):
	def on_connect(self):
		print("sysutil on_connect")

	def on_disconnect(self):
		print("sysutil on_disconnect")

	def on_handle_message(self,message):
		print('received message: '+ message)

	def on_handle_json(self,json):
		print('received json: '+ str(json))

	def on_sync_time(self,json):
		#print("callback:",json['data'])
		dTString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		emit('recv_sync', {"datetime":dTString})

	# system interface methods
	# non context aware
	# live logins - update7
