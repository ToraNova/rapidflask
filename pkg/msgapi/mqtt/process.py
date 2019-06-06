#--------------------------------------------------
# process.py 
# process the msgstack, a routine thread
# initial use case is to delete messages
# introduced 31/05/2019 (u8)
#--------------------------------------------------

# Standard import
import time, threading, os
import ssl, traceback

# flask logins
from flask_login import login_required
from flask_login import current_user

# usual imports (copy pasta this)
import pkg.const as const
from pkg.system.database import dbms
from pkg.system import assertw as a
from pkg.system.servlog import srvlog
from pkg.iface import sockemit

from pkg.msgapi.mqtt.models import MQTT_Sub, MQTT_Msg,\
                            MQTT_Broker_Configuration

class MessageProcessThread( threading.Thread ):
    '''performs deletion (and possibly message processing
    periodically in the background'''

    def __init__(self):
        threading.Thread.__init__(self)
        self.pub_ready = threading.Event()

    def terminate(self):
        self.runflag = False

    def rerun(self):
        self.runflag = True

    def run(self):

        while True:
            # Inception-like self contained mega loopz

            while self.runflag: #try until stop running
                try:
                    pass #TODO: do something here (delete message when their time is up
                except Exception as e:
                    print("[EX]",__name__," : ",\
                        "Exception occurred on the processing thread",str(e))
                    srvlog["oper"].error(\
                        "Exception occurred on the processing thread"\
                        +str(e))

            # wait here until flag set again
            while not self.runflag:
                # wait until run again
                time.sleep( const.THREAD_DORMANT_WTIME )

