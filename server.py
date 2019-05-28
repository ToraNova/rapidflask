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
    # Performs config parsing (read from const file u8) const file 
    # performs all this read from the config file
    ##################################################################
    main_host = const.BIND_ADDR
    main_port = const.BIND_PORT
    main_debug = const.EDEBUG
    main_reload = const.RELOAD
    broker_enable = const.BROKER_ENABLE
    broker_autostart = const.BROKER_AUTOSTART
    ssl_enable = const.SSL_ENABLE
    ssl_cert = const.SSL_CERT
    ssl_pkey = const.SSL_PKEY
    ssl_ca = const.SSL_CA
    ##################################################################

    # print and log out configuration details
    print("[IF]",__name__," : ","Hosting {} on".format(const.SERVER_NAME),main_host,str(main_port))
    if(ssl_enable):
        print("[IF]",__name__," : ","Hosting over TLS, HTTPS")
    else:
        print("[IF]",__name__," : ","Warning. Hosting over insecure HTTP")
    print("[IF]",__name__," : ","Debug/Reload :",main_debug,"/",main_reload)
    srvlog["sys"].info(main_host+":"+str(main_port))
    srvlog["sys"].info("debug/reload : "+
            "yes/" if main_debug else "no/"+
            "yes" if main_reload else "no")

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

    if( sys.platform == "linux" or sys.platform == "linux2"):
        if(broker_enable and broker_autostart):
            from pkg.msgapi.mqtt import BrokerThread
            BrokerThread.begin()
        else:
            print("[IF]",__name__," : ","Skipping MQTT broker service on autostart")
    else:
        print("[ER]",__name__," : ","MQTT broker service disabled as platform is not linux")

    if(not main_debug):
        # Restrict werkzeug logs to only errors
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    try:
        #mainsrv.run(debug=app_debug,host=main_host, port=main_port, use_reloader = True) #flask run

        if(ssl_enable):
            srvlog["sys"].info("Starting server over SSL/TLS HTTPS")
            # FLASK HOSTING
            #mainsrv.run( debug = main_debug, host = main_host, port = main_port, use_reloader= main_reload, ssl_context=(ssl_cert,ssl_pkey))

            # FLASK_SOCKETIO HOSTING
            mainsrv_sock.run(mainsrv,debug= main_debug,host=main_host, port=main_port, use_reloader = main_reload, \
                    certfile = ssl_cert, keyfile = ssl_pkey, ca_certs = ssl_ca)
            # TODO: SSL version / cert require ? Check these 2 settings out
        else:
            srvlog["sys"].info("Starting server over HTTP")
            mainsrv_sock.run(mainsrv,debug= main_debug,host=main_host, port=main_port, use_reloader = main_reload)
    except Exception as e:
        print("[ER]",__name__," : ","Exception :",str(e))
        traceback.print_exc()
        srvlog["sys"].error("Exception has occurred:"+str(e))
    finally:
        print("[IF]",__name__," Server terminated.")
        srvlog["sys"].info("system halt") #logging
        BrokerThread.terminate()
