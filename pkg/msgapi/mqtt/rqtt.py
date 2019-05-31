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
        lu = Msgapi_User.query.filter( Msgapi.username == 'localuser' ).only()
        if(lu is not None):
            portn = MQTT_Broker_Configuration.query.filter(
                    MQTT_Broker_Configuration.config_name == "port").only()
            try:
                iportn = int( portn.config_value )
                cthread = RapidClientThread( lu.username, lu.plain_password, iportn)
                cthread.start()
            except Exception as e:
                print("[EX]",__name__," : ","Port number error on mosquitto broker configs",portn)
                emit('brokerqstat_cast',{'statstring':'mosquitto broker port error!'+\
                        portn.config_value})
        else:
            print("[ER]",__name__," : ","localuser for MQTT RapidClient does not exist!")
            srvlog["oper"].error("localuser for MQTT RapidClient does not exist!")
            emit('brokerqstat_cast',{'statstring':'localuser does not exist!'})

    def on_rqttstop(self):
        pass



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

