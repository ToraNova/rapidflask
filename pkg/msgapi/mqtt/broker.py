#--------------------------------------------------
# broker.py
# this file allows the web application effectively
# control
# introduced 19/05/2019 (u8)
#--------------------------------------------------

# TODO: Please read
# http://www.steves-internet-guide.com/mosquitto-logging/
import os, threading, time
from subprocess import Popen, PIPE
from collections import deque

import pkg.const as const
from pkg.system.servlog import srvlog

class ReaderThread( threading.Thread ):
    # MAJOR ! TODO: Clean up zombie tail processes
    # once socket io dc, the tail process is still running,
    # find a way to kill it
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.io_ready = threading.Event() #not used
        self.runflag = False

    def run(self):
        # start a tail -f on the ofname file on brokerThread
        from pkg.msgapi.mqtt.rqtt import brokerlogs
        tproc = Popen(['tail','-f',BrokerThread.ofname],stdout=PIPE)
        self.runflag = True
        self.msgq = deque()
        while self.runflag:

            rin = tproc.stdout.readline()
            self.io_ready.set()
            if(len(rin) <= 0):
                tproc.kill()
                self.runflag = False
            else:
                brokerlogs( (rin[:-1]).decode('utf-8') )
        self.io_ready.clear()
        tproc.kill()
        print("Stopped")

    def kill(self):
        self.runflag = False


class BrokerThread( threading.Thread ):

    ofname = os.path.join(const.LOGS_DIR,'mosquitto.log.tmp') 
    plname = os.path.join(const.LOGS_DIR,'mosquitto.log') #persistent log
    cffile = os.path.join(const.CFG_FILEDIR, 'mosquitto.conf')
    atfile = os.path.join(const.CFG_FILEDIR, 'mosquitto.auth')

    def __init__(self):
        threading.Thread.__init__(self)

    @staticmethod
    def broker_started():
        #ps = Popen(['ps','aux'],\
        #        stdout=PIPE)
        #vgrep = Popen(['grep','-v','grep'],\
        #        stdin=ps.stdout, stdout=PIPE)
        #grep = Popen(['grep','mosquitto$'],
        #        stdin=vgrep.stdout,stdout=PIPE)
        pg = Popen(['pgrep','mosquitto$'],stdout=PIPE)
        try:
            out,err = pg.communicate(timeout=5)
            if(len(out) <=0):
                return False #broker probably not running
            else:
                return True #broker probably running
        except Exception as e:
            print("Exception as occurred:",str(e))
            return False

    @staticmethod
    def begin():

        broker_enable = const.BROKER_ENABLE

        if(not broker_enable):
            print("[ER]",__name__," : ","MQTT Broker disabled in rapidconfig")
            return 1
        if(not os.path.isfile( BrokerThread.cffile )):
            #recreate config file
            from pkg.msgapi.mqtt.models import MQTT_Broker_Configuration
            MQTT_Broker_Configuration.update_config()
        if(not os.path.isfile( BrokerThread.atfile )):
            from pkg.msgapi.models import Msgapi_User
            Msgapi_User.update_auth("MQTTv0")
        if(not os.path.isfile( BrokerThread.plname )):
            tp = open(BrokerThread.plname,'w')
            tp.write("Mosquitto Broker Persisten Logfile")
            tp.close()
        ephemereal = BrokerThread()
        ephemereal.start()
        return 0

    @staticmethod
    def terminate():
        if(BrokerThread.broker_started()):
            getpid = Popen(['pgrep','mosquitto$'],stdout=PIPE)
            pid = getpid.stdout.readline()[:-1] #ignore the last character
            if(len(pid) <=0):
                pass # do nothing
            else:
                term = Popen(['kill','-s','SIGTERM',pid])
                term.wait()

    @staticmethod
    def restart():
        BrokerThread.terminate()
        BrokerThread.begin()

    def run(self):
        time.sleep(1.33)
        if(BrokerThread.broker_started()):
            print("[ER]",__name__," : ","Warning. MQTT broker already running, Skipping start")
            srvlog["sys"].warning("Unable to start broker. mosquitto already up!")
            return
        else:
            print("[IF]",__name__," : ","MQTT Broker Config/Log Files",\
                    self.cffile,self.ofname)
            srvlog["sys"].info("MQTT BrokerThread started. "+self.cffile)
        try:
            if( os.path.isfile( self.ofname ) ):
                os.remove( self.ofname ) #refresh logs
            mqbroker = Popen(['mosquitto','-c',self.cffile,'-v'])
            mqbroker.wait()
            with open( self.plname, 'a') as catfile:
                with open( self.ofname ) as tmpfile:
                    for line in tmpfile:
                        catfile.write(line)
            print("[IF]",__name__," : ","BrokerThread stopped. Concat-ed logs")
            srvlog["sys"].info("MQTT BrokerThread stopped.")
        except FileNotFoundError:
            print("[ER]",__name__," : ","Unable to locate mosquitto or it's config file on system path. PATH set or installed ?")
            srvlog["sys"].error("Broker/ConfigFile not found on system path.")
        except Exception as e:
            print("[ER]",__name__," : ","Unknown exception has occurred",str(e))
            srvlog["sys"].error("Exception has occurred on MQTT BrokerThread:"+str(e))
        finally:
            pass

