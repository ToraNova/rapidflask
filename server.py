#!/usr/bin/python3

#--------------------------------------------------
# server.py
# this is the main file to be executed
# created 8/12/2018
#--------------------------------------------------

# perform monkey patching
from gevent import monkey
monkey.patch_all()

from pkg.system.servlog import srvlog

from pkg.system.database import dbcon

import os, sys, traceback
import ssl
import logging
import pkg.const as const


                
if __name__ == '__main__':

    ##################################################################
    # print and log out configuration details
    ##################################################################
    print("[IF]",__name__," : ","Hosting {} on".format(const.SERVER_NAME),const.BIND_ADDR,str(const.BIND_PORT))
    if(const.SSL_ENABLE):
        print("[IF]",__name__," : ","Hosting over TLS, HTTPS")
    else:
        print("[IF]",__name__," : ","Warning. Hosting over insecure HTTP")
    print("[IF]",__name__," : ","Debug/Reload :",const.EDEBUG,"/",const.RELOAD)
    srvlog["sys"].info(const.BIND_ADDR+":"+str(const.BIND_PORT))
    srvlog["sys"].info("debug/reload : "+("yes/" if const.EDEBUG else "no/")+("yes" if const.RELOAD else "no"))

    ##################################################################
    #First run issues (create database)
    ##################################################################
    try:
        if(not os.path.isdir(os.path.join(const.TOKN_DIR,const.TOKN_SYS))):
            #creates the directory if it does not exist
            os.makedirs(os.path.join(const.TOKN_DIR,const.TOKN_SYS))
        if(not os.path.isfile(os.path.join(const.TOKN_DIR,"init.token"))):
            #database not initialized yet, we delete the db and reinit
            dbcon.init_db(system=True,deploy=True,msgapi=True)#initialization
        else:
            print("[IF]",__name__," : ","Database already initialized...skipping")
            pass
    except  Exception as e:
        print("[ER]",__name__," : ","Exception occured while trying to create database:",str(e))
        traceback.print_exc()
        dbcon.delete_db(system=True,deploy=True,msgapi=True) # deletes the db (and the init token)
        srvlog['sys'].error("Database creation exception :"+str(e))
    ##################################################################

    from pkg.source import out_nonsock, out
    mainsrv_sock = out
    mainsrv = out_nonsock
    srvlog["sys"].info("system start") #logging

    ##################################################################
    # MQTT BROKER START CHECK
    ##################################################################
    if( sys.platform == "linux" or sys.platform == "linux2"):
        if(const.BROKER_ENABLE and const.BROKER_AUTOSTART):
            from pkg.msgapi.mqtt import BrokerThread
            BrokerThread.begin()
        else:
            print("[IF]",__name__," : ","Skipping MQTT broker service on autostart")
    else:
        print("[ER]",__name__," : ","MQTT broker service disabled as platform is not linux")

    if(not const.EDEBUG):
        # Restrict werkzeug logs to only errors
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    try:
    ##################################################################
    # LOCAL RQTT CLIENT START CHECK
    ##################################################################
        if( const.LOCAL_RQTT_ENABLE ):
            # enable the local rqtt threads
            from pkg.msgapi.mqtt.client import RapidClientThread
            global_rqttclient = RapidClientThread() # THIS IS USED GLOBALLY.
            # from __main__ import global_rqttclient to use it
            if( const.LOCAL_RQTT_AUTOSTART ):
                # autostart it
                if( const.LOCAL_RQTT_EXTBROKE ):
                    # connect to external broker (or specified broker based on config)
                    global_rqttclient.load_config( const.LOCAL_RQTT_USERNAME,\
                            const.LOCAL_RQTT_PASSWORD, const.LOCAL_RQTT_ADDR,\
                            const.LOCAL_RQTT_PORT ) 
                elif( const.BROKER_ENABLE ):
                    # local broker enabled, connect to it instead
                    from pkg.msgapi.mqtt.models import MQTT_Broker_Configuration
                    portn = MQTT_Broker_Configuration.query.filter(
                            MQTT_Broker_Configuration.config_name == "port").one()
                    try:
                        iportn = int(portn.config_value)
                    except Exception as e:
                        iportn = 1883
                        print("[EX]",__name__," : ","Exception has occured while parsing port",str(e),portn.config_value)
                    global_rqttclient.load_config( const.LOCAL_RQTT_USERNAME,\
                            const.LOCAL_RQTT_PASSWORD, '127.0.0.1',\
                            iportn)
                # start the broker
                global_rqttclient.start()
        else:
            # rqtt disabled
            global_rqttclient = None

    ##################################################################
    # MAIN SERVER START
    ##################################################################
        if(const.SSL_ENABLE):
            #mainsrv.run(debug=app_debug,host=const.BIND_ADDR, port=const.BIND_PORT, use_reloader = True) #flask run
            srvlog["sys"].info("Starting server over SSL/TLS HTTPS")
            # FLASK HOSTING
            #mainsrv.run( debug = const.EDEBUG, host = const.BIND_ADDR, port = const.BIND_PORT, use_reloader= const.RELOAD, ssl_context=(const.SSL_CERT,const.SSL_SKEY))

            # FLASK_SOCKETIO HOSTING
            mainsrv_sock.run(mainsrv,debug= const.EDEBUG,host=const.BIND_ADDR, port=const.BIND_PORT, use_reloader = const.RELOAD, \
                    certfile = const.SSL_CERT, keyfile = const.SSL_SKEY, ca_certs = const.SSL_CA)
            # TODO: SSL version / cert require ? Check these 2 settings out
        else:
            srvlog["sys"].info("Starting server over HTTP")
            mainsrv_sock.run(mainsrv,debug= const.EDEBUG,host=const.BIND_ADDR, port=const.BIND_PORT, use_reloader = const.RELOAD)
    ##################################################################

    ##################################################################
    # HOUSE KEEPING
    ##################################################################
    except Exception as e:
        print("[ER]",__name__," : ","Exception :",str(e))
        traceback.print_exc()
        srvlog["sys"].error("Exception has occurred:"+str(e))
    finally:
        print("[IF]",__name__," Server terminated.")
        srvlog["sys"].info("system halt") #logging
        BrokerThread.terminate()
