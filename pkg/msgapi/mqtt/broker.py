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

    ofname = os.path.join(const.LOGS_DIR,const.MQTT_BROKER+'.log') 
    cffile = os.path.join(const.CFG_FILEDIR, const.MQTT_BROKER+'.conf')
    atfile = os.path.join(const.CFG_FILEDIR, const.MQTT_BROKER+'.auth')

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
    def begin():
        if(not os.path.isfile( BrokerThread.cffile )):
            #recreate config file
            from pkg.msgapi.mqtt.models import MQTT_Broker_Configuration
            MQTT_Broker_Configuration.update_config()
        if(not os.path.isfile( BrokerThread.atfile )):
            from pkg.msgapi.models import Msgapi_User
            Msgapi_User.update_auth("MQTTv0")
        ephemereal = BrokerThread()
        ephemereal.start()

    @staticmethod
    def terminate():
        if(BrokerThread.broker_started()):
            getpid = Popen(['pgrep',const.MQTT_BROKER],stdout=PIPE)
            pid = getpid.stdout.readline()[:-1] #ignore the last character
            term = Popen(['kill','-s','SIGTERM',pid])
            term.wait()

    @staticmethod
    def restart():
        BrokerThread.terminate()
        BrokerThread.begin()

    def run(self):
        time.sleep(3) #wait for previous broker to fully stop first
        if(BrokerThread.broker_started()):
            print("[ER]",__name__," : ","Warning. MQTT broker already running, Skipping start")
            srvlog["sys"].warning("Unable to start broker. {} already up!".format(
                const.MQTT_BROKER))
            return
        else:
            print("[IF]",__name__," : ","MQTT Broker Config/Log Files",\
                    self.cffile,self.ofname)
        try:
            mqbroker = Popen([const.MQTT_BROKER,'-c',self.cffile,'-v'])
            mqbroker.wait()
        except FileNotFoundError:
            print("[ER]",__name__," : ","Unable to locate {} or it's config file on system path. PATH set or installed ?".format(const.MQTT_BROKER))
            srvlog["sys"].error("Broker/ConfigFile not found on system path.")
        except Exception as e:
            print("[ER]",__name__," : ","Unknown exception has occurred",str(e))
            srvlog["sys"].error("Exception has occurred on MQTT BrokerThread:"+str(e))
        finally:
            BrokerThread.terminate()
            print("[IF]",__name__," : ","BrokerThread stopped.")
            srvlog["sys"].info("MQTT BrokerThread stopped.")
            
