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

import pkg.const as const
from pkg.system.servlog import srvlog

class BrokerThread( threading.Thread ):

    def __init__(self):
        threading.Thread.__init__(self)

    @staticmethod
    def broker_started():
        target_process = const.MQTT_BROKER
        ps = Popen(['ps','aux'],\
                stdout=PIPE)
        vgrep = Popen(['grep','-v','grep'],\
                stdin=ps.stdout, stdout=PIPE)
        grep = Popen(['grep',target_process],
                stdin=vgrep.stdout,stdout=PIPE)
        try:
            out,err = grep.communicate(timeout=5)
            if(len(out) <=0):
                return False #broker probably not running
            else:
                return True #broker probably running
        except Exception as e:
            print("Exception as occurred:",str(e))
            return False

    @staticmethod
    def terminate():
        if(BrokerThread.broker_started()):
            getpid = Popen(['pgrep',const.MQTT_BROKER],stdout=PIPE)
            pid = getpid.stdout.readline()[:-1] #ignore the last character
            term = Popen(['kill','-s','SIGTERM',pid])
            term.wait()

    def run(self):
        if( BrokerThread.broker_started() ):
            print("[ER]",__name__," : ","Warning. MQTT broker already running, Skipping start")
            srvlog["sys"].warning("Unable to start broker. Mosquitto already up!")
            return
        try:
            ofname = os.path.join(const.LOGS_DIR,const.MQTT_BROKER+'.log') 
            print("[IF]",__name__," : ","MQTT BrokerThread stdout written to",ofname)
            stdoutfile = open( ofname, 'w')
            mqbroker = Popen([const.MQTT_BROKER],stdout=PIPE)
            while True:
                mbop = mqbroker.stdout.readline()
                if(len(mbop)<=0):
                    break
        except FileNotFoundError:
            print("[ER]",__name__," : ","Unable to locate mosquitto on system path. PATH set or installed ?")
            srvlog["sys"].error("Mosquitto not found on system path.")
        except Exception as e:
            print("[ER]",__name__," : ","Unknown exception has occurred",str(e))
            srvlog["sys"].error("Exception has occurred on MQTT BrokerThread:"+str(e))
        finally:
            stdoutfile.close()
            BrokerThread.terminate()
            print("[IF]",__name__," : ","BrokerThread stopped.")
            srvlog["sys"].info("MQTT BrokerThread stopped.")
            
