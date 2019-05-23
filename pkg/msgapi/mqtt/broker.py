#--------------------------------------------------
# broker.py
# this file allows the web application effectively
# control
# introduced 19/05/2019 (u8)
#--------------------------------------------------
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
            print("Warning. MQTT broker already running, Skipping start")
            srvlog["sys"].warning("Unable to start broker. Mosquitto already up!")
            return
        mqbroker = Popen([const.MQTT_BROKER],\
                stdout=PIPE)
        stdoutfile =os.path.join(const.LOGS_DIR,const.MQTT_BROKER+'.log') 
        print("[IF]",__name__," : ","MQTT BrokerThread stdout written to",stdoutfile)
        with open(stdoutfile,'w') as outfile:
            try:
                while True:
                    broker_out = mqbroker.stdout.readline()
                    if( len(broker_out) <= 0):
                        print("Outlen <= 0, Aborting")
                        break
                    outfile.write( broker_out )
                    outfile.write( '\n' )
                    outfile.flush()
            except Exception as e:
                srvlog["sys"].error("Exception has occurred on MQTT BrokerThread. "+str(e))
            finally:
                mqbroker.terminate()
                srvlog["sys"].info("MQTT BrokerThread stopped.")
