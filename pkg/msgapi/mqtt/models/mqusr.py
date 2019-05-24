#--------------------------------------------------
# mqusr.py
# MQTT_BROKER_USER is for access control on the mqtt
# broker
# introduced in u8
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r
from shutil import copyfile,
import os
from pkg.system.database import dbms
from pkg.msgapi.mqtt import BrokerThread
Base = dbms.msgapi.base

class MQTT_Broker_User(Base):
    __tablename__ = "MQTT_Broker_User" #Try to use plurals here (i.e car's')
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    username = Column(String(r.lim.MAX_USERNAME_SIZE), unique=True)
    plain_password = Column(String(r.lim.MAX_PASSWORD_SIZE))

    rlist = {
        "Username":"username",
        "Password":"password"
    }
    rlist_priKey = "id"
    rlist_dis = "MQTT Broker Configuration" #display for r routes

    @staticmethod
    def update_auth():
        authfile = os.path.join(r.const.CFG_FILEDIR,const.MQTT_BROKER+'.auth')
        if( os.path.isfile( authfile ):
                os.remove( authfile )
        users = MQTT_Broker_User.query.all()
        with open( authfile, 'w') as afile:
            for u in users:
                afile.write(c.username)
                afile.write(':')
                afile.write(c.plain_password)
        BrokerThread.restart() # restart the broker

    def __init__(self.insert_list):
        self.username = insert_list["username"]
        self.plain_password = insert_list["plain_password"]

    def default_add_action(self):
        # updates the config file
        MQTT_Broker_User.update_auth()

    def default_mod_action(self):
        # updates the config file
        MQTT_Broker_User.update_auth()

    def default_del_action(self):
        # updates the config file
        MQTT_Broker_User.update_auth()

class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_username = r.StringField('MQTT UserName',validators=[ r.Length(max=r.lim.MAX_USERNAME_SIZE) ] )
    rgen_plain_password = r.StringField('MQTT UserPass(Plaintext)',validators=[ r.Length(max=r.lim.MAX_PASSWORD_SIZE) ] )
