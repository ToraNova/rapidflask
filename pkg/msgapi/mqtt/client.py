#--------------------------------------------------
# rapidclient.py
# the thread that runs the local client to listen in
# on mqtt messages based on the subscription database
# uses the default user 'localuser'
# introduced 31/05/2019 (u8)
#--------------------------------------------------

# requires MQTT
import paho.mqtt.client as mqtt
import time, threading, os
import ssl, traceback

#flask logins
from flask_login import login_required
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
from pkg.system.database import dbms
from pkg.system import assertw as a
from pkg.system.servlog import srvlog
from pkg.iface import sockemit

from pkg.msgapi.mqtt.models import MQTT_Sub, MQTT_Msg,\
                            MQTT_Broker_Configuration

# process table
from pkg.msgapi.proc import proctab

class RapidClientThread( threading.Thread ):
    '''runs a local client and subscribe to the msgsub
    databases's directive. uses the localuser account'''

    def __init__(self):
        threading.Thread.__init__(self)
        self.pub_ready = threading.Event()
        self.pub_done = threading.Event()
        self.reset_client()
        self.lgn_idn="Anonymous"

    def reset_client(self):
        self.client = mqtt.Client() #client creation
        self.client.sublist = []
        self.client.lastmsg = "No last message yet"
        self.client.connrc = 'NA'
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message
        self.client.connflag = False

    def load_config(self, uname, passwd, addr, portn ):
        '''allows uname, passwd and portn to be loaded and
        clears the publish ready flag. please call the
        start method after this'''
        self.uname = uname
        self.passwd = passwd
        self.addr = addr
        self.portn = portn
        self.pub_ready.clear()
        self.pub_done.clear()
        self.runflag = False

    def __sload_config(self):
        '''self loading on new configuration values. this
        function should only be called by the thread obj
        not sure if this is useful for now ?'''
        self.load_config( const.LOCAL_RQTT_USERNAME,\
                const.LOCAL_RQTT_PASSWORD, const.LOCAL_RQTT_ADDR,\
                const.LOCAL_RQTT_PORT )

    def broker_set_config(self, co_ssl_en, co_ano_en):
        '''used externally to set the ssl_en and ano_en
        variables'''
        self.ssl_en = co_ssl_en
        self.ano_en = co_ano_en

    def refresh_subs(self):
        for s in self.client.sublist:
            self.client.unsubscribe( s )
        sublist = MQTT_Sub.query.all()
        client.sublist = []
        for s in sublist:
            res = client.subscribe( s.topic )
            if(res[0] == 0):
                srvlog["oper"].info(\
                        "LOCAL:RapidClient subscribed to topic:"+s.topic)
                sockemit("/mqttctl","mqttqstat_cast",\
                        {'statstring':\
                        "LOCAL:RapidClient subscribed to topic:"+s.topic
                        },
                    eroom='mqttctl')
                client.sublist.append( s.topic )
            else:
                srvlog["oper"].warning(\
                        "LOCAL:RapidClient subscription failed:"+str(res))

    def status(self):
        pass
        #sdict = {
        #    "connected:": self.connflag,
        #    "result code:": self.connrc,
        #    "sublist:": self.

    def pubmsg(self, topic, msg):
        #TODO: returns -1 when self.pub_done.wait(3) enabled
        self.pub_rc = -1 #-1 indicate havent launch yet
        self.pub_done.clear()
        self.pub_topic = topic
        self.pub_msg = msg
        self.pub_ready.set()
        #TODO: why including this slows down the reply process ?
        #self.pub_done.wait(3)
        return 0

    def terminate(self):
        self.pub_topic = None
        self.pub_msg = None
        self.runflag = False
        self.pub_ready.set()

    def rerun(self):
        self.runflag = True

    def run(self):
        self.runflag = True
        while True:
            # Inception-like self contained mega loopz
            # reimport for refreshed config
            self.lgn_idn="Anonymous"
            self.reset_client()
            if( not const.LOCAL_RQTT_EXTBROKE ):
                # Connect to local mosquitto
                if(self.ssl_en in ['True','true',1,'1']):
                    self.client.tls_set(\
                            ca_certs = const.SSL_CA, cert_reqs = ssl.CERT_REQUIRED,\
                            tls_version=ssl.PROTOCOL_TLS)

                if(self.ano_en in ['False','false',0,'0']):
                    self.client.username_pw_set(\
                            username=self.uname, password=self.passwd) #set auth
                    self.lgn_idn=self.uname

            else:
                # External brokers
                if( not const.LOCAL_RQTT_ANON ):
                    self.client.username_pw_set(\
                            username=self.uname, password=self.passwd) #set auth
                    self.lgn_idn=self.uname

            sockemit("/mqttctl","mqttqstat_cast",\
                    {'statstring':"LOCAL:RapidClient starting (ssl:%s, login:%s)" %\
                    (self.ssl_en, self.lgn_idn)},\
                    eroom='mqttctl')

            while self.runflag: #try until stop running
                try:
                    time.sleep(3)
                    self.client.connect(self.addr, self.portn, 60) #connect
                    break
                except Exception as e:
                    print("[EX]",__name__," : ",\
                            "Exception occurred while trying "+\
                            ":to connect to broker",\
                        str(e))
                    srvlog["oper"].error(\
                        "Exception occurred while trying to "+\
                        "connect to broker on {}:{}."\
                        .format(self.addr,self.portn)+str(e))
                    time.sleep(3)

            self.client.loop_start()
            while not self.client.connflag and self.runflag:
                #wait until client is connected
                time.sleep(3)

            while self.runflag:
                self.pub_ready.wait() #block and wait for msg
                if( not self.client.connflag ):
                    while not self.client.connflag and self.runflag:
                        time.sleep(3)
                        sockemit("/mqttctl","mqttqstat_cast",\
                                {'statstring':\
                                "LOCAL:RapidClient connection failed. "+\
                                " retrying"},
                                eroom='mqttctl')
                elif(self.pub_topic is None and self.pub_msg is None):
                    break
                else:
                    #obtain the RC only,
                    #ignores message id (return, message_id)
                    self.pub_rc = self.client.publish(\
                            self.pub_topic, self.pub_msg )[0]
                    #sets the flag to indicate pub is complete
                    self.pub_done.set()
                #clears pub_ready flag to enable block again
                self.pub_ready.clear()

            self.client.sublist = []
            self.client.loop_stop()
            self.client.disconnect()
            sockemit("/mqttctl","mqttqstat_cast",\
                    {'statstring':"LOCAL:RapidClient stopped"},
                    eroom='mqttctl')
            while not self.runflag:
                # wait until run again
                time.sleep(const.THREAD_DORMANT_WTIME)


#defining callback behavior upon message receive
def on_message(client, userdata, msg):
    client.lastmsg = "[{}]:{}".format(msg.topic, msg.payload)
    strpayload = msg.payload.decode('utf-8')
    mtopic = MQTT_Sub.query.filter( MQTT_Sub.topic == msg.topic ).first()
    if( mtopic is None ):
        # Topic is not registered. but how did we receive it ?
        # Error must have occurred
        srvlog["oper"].error(msg.topic+" is not registered but message received.")
        insert = {
                "topic":msg.topic,
                "msg":strpayload,
                "pflag0":False,
                "pflag1":False
                }
        utopm = MQTT_Msg( insert )
    else:
        try:
            # doing this to make processing as instant as possible
            insert = {}
            if(mtopic.instantp and mtopic.onrecv is not None):
                #instantly process
                insert["pflag1"] = proctab[ mtopic.onrecv ](\
                        mtopic.topic, strpayload )
                insert["pflag0"] = True
            else:
                insert["pflag0"] = False
                insert["pflag1"] = False
            insert["tlink"] = mtopic.id
            insert["topic"] = msg.topic
            insert["msg"] = strpayload
            utopm = MQTT_Msg( insert )
            # Topic found. add and link
            srvlog["oper"].info(msg.topic+":"+strpayload+" pushed to mqtt msgstack")
        except Exception as e:
            print(str(e),traceback.format_exc())
    try:
        if utopm.pflag0 and mtopic.delonproc:
            # skip insertion as it is already processed
            # TODO: thinking if we insert it still if process has failed
            pass
            print("[MQ]",__name__," : ","Processed [{}]{}. MSG not pushed (delonproc)".format(\
                    msg.topic,strpayload))
        else:
            # add and commit
            dbms.msgapi.session.add( utopm )
            dbms.msgapi.session.commit()
            print("[MQ]",__name__," : ","Pushed [{}]{} onto MQTT msgstack".format(\
                    msg.topic,strpayload))
    except Exception as e:
        # ROllback any changes
        print("[EX]",__name__," : ","Exception has occurred while pushing to mqtt msgstack",\
                str(e))
        srvlog["oper"].error("Exception has occurred on_message mqtt msgstack :"+str(e))
        dbms.msgapi.session.rollback()


def on_connect(client, userdata, flags, rc):
    srvlog["oper"].info("LOCAL:RapidClient connected with rc:"+str(rc))
    sockemit("/mqttctl","mqttqstat_cast",\
            {'statstring':"LOCAL:RapidClient connected with rc:"+str(rc)},
            eroom='mqttctl')
    if(rc == 0):
        client.connflag = True
        client.connrc = str(rc)
        sublist = MQTT_Sub.query.all()
        client.sublist = []
        for s in sublist:
            res = client.subscribe( s.topic )
            # TODO: check if subscription is successfuly
            srvlog["oper"].info("LOCAL:RapidClient subscribed to topic:"+s.topic)
            client.sublist.append( s.topic )
    elif(rc == 5):
        srvlog["oper"].warning("LOCAL:RapidClient unauthorized connection to broker")

def on_disconnect(client, userdata, rc):
    client.connflag = False
    client.connrc = str(rc)
    client.sublist = [] #remove all subs
    srvlog["oper"].info("LOCAL:RapidClient disconnected rc:"+str(rc))
    sockemit("/mqttctl","mqttqstat_cast",\
            {'statstring':"LOCAL:RapidClient disconnected rc:"+str(c)},
            eroom='mqttctl')
