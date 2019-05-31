#--------------------------------------------------
# rqtt.py
# this file allows generic mqtt calls to the system
# rqtt is to prevent name collisions 
# RapidFlasks's mqtt system - rqtt
# introduced 19/05/2019 (u8)
#--------------------------------------------------

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
from pkg.msgapi.mqtt.client import RapidClientThread
from pkg.msgapi.mqtt.models import MQTT_Sub, MQTT_Msg,\
                            MQTT_Broker_Configuration
from pkg.msgapi.models import Msgapi_User

# primary blueprint
bp = Blueprint('mqttio', __name__, url_prefix='/api/mqtt')

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

    def on_rqttstart(self):
        # access the main's global rqtt rapidclient
        if( const.LOCAL_RQTT_ENABLE ):
            from __main__ import global_rqttclient
            if( global_rqttclient.runflag ):
                emit('mqttqstat_cast',{'statstring':'localrqtt already running.'})
                return
            lu = Msgapi_User.query.filter( Msgapi.username == 'localuser' ).one()
            if(lu is not None):
                # lu available, load from it
                username = lu.username
                password = lu.plain_password
            else:
                # lu not available, load from config instead
                username = const.LOCAL_RQTT_USERNAME
                password = const.LOCAL_RQTT_PASSWORD

            if(const.BROKER_ENABLE and not const.LOCAL_RQTT_EXTBROKE):
                portn = MQTT_Broker_Configuration.query.filter(
                        MQTT_Broker_Configuration.config_name == "port").one()
                addrn = "127.0.0.1" #localhost loopback

            else:
                portn = const.LOCAL_RQTT_PORT
                addrn = const.LOCAL_RQTT_ADDR
            # reload config
            global_rqttclient.load_config( lu.username, lu.plain_password,\
                    addrn, portn)
            # start the rqtt client
            global_rqttclient.start()
        else:
            emit('mqttqstat_cast',{'statstring':'localrqtt disabled in config.'})

    def on_rqttstop(self):
        # access the main's global rqtt rapidclient
        if( const.LOCAL_RQTT_ENABLE ):
            from __main__ import global_rqttclient
            if( not global_rqttclient.runflag ):
                emit('mqttqstat_cast',{'statstring':'local rqtt already not running.'})
                return
            global_rqttclient.terminate()
        else:
            emit('mqttqstat_cast',{'statstring':'localrqtt disabled in config.'})

    def on_connect(self):
        join_room("mqttctl")
        self.rthread = ReaderThread(self)
        self.rthread.start()
        print("[IF]",__name__," : ","MQTTCTL Socket established.")
        if( BrokerThread.broker_started() ):
            emit('mqttqstat_cast',{'statstring':'mosquitto OK'})
        else:
            emit('mqttqstat_cast',{'statstring':'mosquitto not running'})

    def on_disconnect(self):
        leave_room("mqttctl")
        ReaderThread.sigterm()
        print("[IF]",__name__," : ","MQTTCTL Socket disconnected.")

    def on_start(self):
        if( BrokerThread.broker_started() ):
            emit('mqttqstat_cast',{'statstring':'mosquitto already up!'})
        else:
            rc = BrokerThread.begin()
            emit('mqttqstat_cast',{'statstring':'mosquitto start :'+\
                rc})

    def on_refresh(self):
        ReaderThread.sigterm()
        print("[IF]",__name__," : ","Refreshing ReaderThread")
        self.rthread = ReaderThread(self)
        self.rthread.start()

    def on_stop(self):
        rc = BrokerThread.terminate()
        emit('mqttqstat_cast',{'statstring':'mosquitto stop :'+\
            rc})

