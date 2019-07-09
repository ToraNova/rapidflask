#--------------------------------------------------
# mqtt_control.py
# MQTT_Control is a database model to control subscriptions
# and publications
# introduced in u8
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r
from pkg.system.database import dbms
Base = dbms.msgapi.base

class MQTT_Msg(Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "MQTT_Msgs" #Try to use plurals here (i.e car's')
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    # the string topic of the topic to subscribe to
    topic = r.Column(r.String(r.lim.MAX_MQTT_TOPIC_SIZE), nullable=False)
    tlink = r.Column(r.Integer, nullable=True) #links to one of our subscribed topic
    msg = r.Column(r.String(r.lim.MAX_MQTT_MSGCT_SIZE), nullable=False)
    timev0 = r.Column(r.DateTime, nullable=False) #insertion time
    timed0 = r.Column(r.DateTime, nullable=True) #deletion time (msg to be kept until)
    pflag0 = r.Column(r.Boolean, nullable=False)  #flag to check if the msg has been processed
    pflag1 = r.Column(r.Boolean, nullable=False)  #flag to check if the msg has been processed successfully
    delonproc = r.Column(r.Boolean, nullable=False) #flag to check if this message should be delete on process

    # TODO: DEFINE THE RLIST
    # CHANGED ON U6 : RLISTING NOW MERGED WITH RLINKING : see 'RLINKING _ HOW TO USE:'
    # The following is for r-listing (as of u6, rlinking as well) (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = r.OrderedDict([
    ("Topic","topic"),
    ("Linked (description)","__link__/tlink/MQTT_Subs/id:description"),
    ("Content","msg"),
    ("Received","__time__/%b-%d-%Y %H:%M:%S/timev0"),
    ("Delete on","__time__/%b-%d-%Y %H:%M:%S/timed0"),
    ("Processed?","pflag0"),
    ("Process OK?","pflag1")
    ]) #header,row data

    # RLINKING _ HOW TO USE :
    # using the __link__ keyword, seperate the arguments with /
    # The first argument is the local reference, the field in which we use to refer
    # the second argument is the foreign table
    # the third argument is the foreign table Primary key
    # the fourth argument is the field we want to find from the foreign table
    # NOTICE that the fourth table uses ':' instead of /.
    # Example
    # "RPi id":"__link__/rpi_id/RPi/id:rpi_name"
    # for the display of RPi id, we link to a foreign table that is called RPi
    # we use the rpi_id foreign key on this table, to locate the id on the foreign table
    # then we query for the field rpi_name

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "MQTT Message Stack" #display for r routes

    def get_onrecv(self):
        # get the name of the process used on this msg
        from pkg.msgapi.mqtt.models import MQTT_Sub
        t = MQTT_Sub.query.filter( MQTT_Sub.id == self.tlink ).first()
        if( t is not None ):
            return t.onrecv

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        '''requirements in insert_list
        @param tlink - link to the mqtt sub record
        @param topic - the topic string (incase linking failed)
        @param msg - the msg content'''
        from pkg.msgapi.mqtt.models import MQTT_Sub
        from pkg.system.servlog import srvlog
        import datetime
        from datetime import timedelta
        # find links
        self.tlink = r.checkNull( insert_list, "tlink")
        self.topic = insert_list["topic"]
        self.msg = insert_list["msg"]
        self.timev0 = datetime.datetime.now()
        self.pflag0 = insert_list["pflag0"]
        self.pflag1 = insert_list["pflag1"]
        submaster = MQTT_Sub.query.filter( MQTT_Sub.id == self.tlink ).first()
        if(submaster is not None):
            if( submaster.stordur is None):
                self.timed0 = None #store forever
            else:
                self.timed0 = self.timev0 + timedelta( seconds= submaster.stordur)
            self.delonproc = submaster.delonproc #inherits from the topic master
        else:
            srvlog["oper"].warning("MQTT message added to unknown link topic:"+self.topic+
                    " id="+int(self.tlink))
            self.timed0 = r.lim.DEF_MQTT_MSGST_DURA
            self.delonproc = True

    def default_add_action(self):
        # This will be run when the table is added via r-add
        # may do some imports here i.e (from pkg.database.fsqlite import db_session)
        # TODO add a MQTT restart function here
        pass

    def default_mod_action(self):
        # This will be run when the table is added modified via r-mod
        # may do some imports here i.e (from pkg.database.fsqlite import db_session)
        pass

    def default_del_action(self):
        # This will be run when the table is deleted
        # may do some imports here i.e (from pkg.database.fsqlite import db_session)
        pass
    ######################################################################################################

