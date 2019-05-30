#--------------------------------------------------
# rqtt.py
# this file allows generic mqtt calls to the system
# rqtt is to prevent name collisions 
# RapidFlasks's mqtt system - rqtt
# introduced 19/05/2019 (u8)
#--------------------------------------------------

# requires MQTT
import paho.mqtt.client as mqtt
import time

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

# flask socketio
from flask_socketio import Namespace
from flask_socketio import send, emit
from flask_socketio import join_room, leave_room

#flask logins
from flask_login import login_required
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
from pkg.system.database import dbms
from pkg.system import assertw as a
from pkg.system.servlog import srvlog,logtofile

from pkg.msgapi.mqtt.broker import ReaderThread
from pkg.msgapi.mqtt.broker import BrokerThread

# primary blueprint
bp = Blueprint('mqttio', __name__, url_prefix='/api/mqtt')

#----------------------------------------------------------------------------------------
# External calls
# introduced u7
# The livelog functions allows other functions which are not registered with
# socketio to emit a message.
#----------------------------------------------------------------------------------------
def brokerlogs( logstr ):
    
    from pkg.source import out as socketio # use carefully to prevent circular imports

    try:
        #live logins - update7
        socketio.emit('brokerlogs_cast',
        {'logstring':logstr},
        room="mqttctl",
        namespace='/brokerctl')
        # emit may also contain namespaces to emit to other classes
    except Exception as e:
        print("Exception has occurred",str(e))
        srvlog["sys"].info("Exception ocurred in broker logging :"+str(e))

##############################################################################################
# API pull routings
##############################################################################################
@bp.route('/service')
def servicectl():
    '''a control panel to enable/disable the mosquitto broker and view the logs'''
    return render_template('flask_sockio/mosquittoctl.html',
            socket_io_proto = const.SOCKET_IO_PROTO)

class MQTTCTLNamespace(Namespace):
    '''This class is currently used to display broker logs 
    as like a pseudo terminal on the web application
    MQTTCTL - mqtt broker control namespace'''

    def on_connect(self):
        join_room("mqttctl")
        self.rthread = ReaderThread(self)
        self.rthread.start()
        print("[IF]",__name__," : ","MQTTCTL Socket established.")
        if( BrokerThread.broker_started() ):
            emit('brokerqstat_cast',{'statstring':'mosquitto OK'})
        else:
            emit('brokerqstat_cast',{'statstring':'mosquitto not running'})

    def on_disconnect(self):
        leave_room("mqttctl")
        ReaderThread.sigterm()
        print("[IF]",__name__," : ","MQTTCTL Socket disconnected.")

    def on_start(self):
        if( BrokerThread.broker_started() ):
            emit('brokerqstat_cast',{'statstring':'mosquitto already up!'})
        else:
            rc = BrokerThread.begin()
            emit('brokerqstat_cast',{'statstring':'mosquitto start :'+\
                rc})

    def on_refresh(self):
        ReaderThread.sigterm()
        print("[IF]",__name__," : ","Refreshing ReaderThread")
        self.rthread = ReaderThread(self)
        self.rthread.start()

    def on_stop(self):
        rc = BrokerThread.terminate()
        emit('brokerqstat_cast',{'statstring':'mosquitto stop :'+\
            rc})

