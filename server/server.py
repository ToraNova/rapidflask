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

from pkg.database.fsqlite import init_db
from pkg.database.fsqlite import db_session

import os.path
import configparser
import logging
import pkg.const as const

if __name__ == '__main__':

    ##################################################################
    # Performs config parsing
    ##################################################################
    rcf = configparser.RawConfigParser()
    rcf.read("rapid.conf")
    main_host = rcf.get('conn','hostaddr')
    try:
        main_port = int(rcf.get('conn','port'))
    except Exception as e:
        print("[ER]",__name__," : ","Exception occured while parsing port number.")
        print(str(e))
        srvlog["sys"].error("Parsing port exception "+str(e))
    main_debug = True if rcf.get('flags','debug')=='1' else False
    main_reload = True if rcf.get('flags','reload')=='1' else False
    ##################################################################

    # print and log out configuration details
    print("[IF]",__name__," : ","Hosting RapidFlask on",main_host,str(main_port))
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
            init_db()#initialization
        else:
            print("[IF]",__name__," : ","Database already initialized...skipping")
            pass
    except  Exception as e:
        print("[ER]",__name__," : ","Exception occured while trying to create database")
        print (str(e))
        srvlog['sys'].error("Database creation exception :"+str(e))
    ##################################################################

    from pkg.source import out_nonsock, out
    mainsrv_sock = out
    mainsrv = out_nonsock
    srvlog["sys"].info("system start") #logging

    if(not main_debug):
        # Restrict werkzeug logs to only errors
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    try:
        #mainsrv.run(debug=app_debug,host=main_host, port=main_port, use_reloader = True) #flask run
        mainsrv_sock.run(mainsrv,debug= main_debug,host=main_host, port=main_port, use_reloader = main_reload)
    except Exception as e:
        print("Exception error",str(e))
        srvlog["sys"].error("exception error")
        srvlog["sys"].error(str(e))
    finally:
        print("[IF]",__name__," Server terminated.")
        srvlog["sys"].info("system halt") #logging
