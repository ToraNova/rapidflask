#--------------------------------------------------
# mqtt.py (ZFENCE system)
# defines MQTT callbacks that works together with the server
# THIS FILE IS HEAVILY CUSTOMISED. NOT PART OF THE MINIMAL SERVER
# BUT IT COULD SERVE AS A REFERENCE
# introduced 2/25/2019 (u6)
#--------------------------------------------------

import paho.mqtt.client as mqtt #MQTT
import threading,time

from pkg.database import fsqlite as sq #extra for any db commits
from pkg.resource.zfence import rpi
from pkg.resource.zfence import gsensor_alert,radar_alert
from pkg.resource.zfence import segcam

class Threaded_MQTT(threading.Thread):

    def pkgprint(self,str):
        print("{}[ZMAST]".format(datetime.datetime.now()),str)

    def __init__(self,verbose=False):
        threading.Thread.__init__(self)
        self.c = mqtt.Client()
        self.c.on_connect = self.on_connect
        self.c.on_message = self.on_message
        self.sublist = []
        self.verboseprint = self.pkgprint if verbose else lambda *a, **k: None

    def on_connect(client, userdata, flags, rc):
        #subscribe to all RPi in the database
        self.resub()
        verboseprint("Connected and subscribed to "+len(self.sublist)+ " hosts")
        self.c.subscribe('zfence/wire') #
        self.c.subscribe('zfence/gz') #alert subscriptions

    def on_message(client, userdata, msg):
        #process topic
        subtopic = msg.topic.split('/')[1]
        if(subtopic == 'rep'):
            pass
        elif(subtopic == 'gz'):
            #
            pass
        elif(subtopic == 'wire'):
            #wirecut event
            pass


    # HOUSEKEEPING FUNCTIONS

    def unsub(self):
        for s in sublist: #unsubscribe all
            self.c.unsubscribe(s)

    def subdb(self):
        seghost_list = rpi.RPi.query.all()
        for host in seghost_list:
            subtopic = 'zfence/rep/'+host.id #subscribe to all the host's reply channel
            self.sublist.append(subtopic)
            self.c.subscribe(subtopic)

    def resub(self):
        #resubscribe to all known hosts in the database
        self.unsuball() #unsub all
        self.subdb() #resub all db hosts
