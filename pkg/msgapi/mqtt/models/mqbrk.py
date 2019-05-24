#--------------------------------------------------
# mqtt_control.py
# MQTT_Control is a database model to control subscriptions
# and publications
# introduced in u8
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r
from shutil import copyfile
import os, configparser
from pkg.system.database import dbms
from pkg.msgapi.mqtt import BrokerThread
Base = dbms.msgapi.base

class MQTT_Broker_Configuration(Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "MQTT_Broker_Configs" #Try to use plurals here (i.e car's')
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)

    config_name = r.Column(r.String(r.lim.MAX_CONFIG_NAME_SIZE),nullable=False)
    config_value = r.Column(r.String(r.lim.MAX_CONFIG_VALU_SIZE), unique=False,nullable=False)

    rlist = {
    "Configuration Name":"config_name",
    "Value":"config_value"
    } #header:row data

    rlist_priKey = "id"
    rlist_dis = "MQTT Broker Configuration" #display for r routes

    def __init__(self,insert_list):
        self.config_name = insert_list["config_name"]
        self.config_value = insert_list["config_value"]

    @staticmethod
    def update_config():
        mbconf_file = os.path.join(r.const.CFG_FILEDIR,const.MQTT_BROKER+'.conf')
        if( os.path.isfile( mbconf_file )):
                os.remove( mbconf_file )
        copyfile( os.path.join(r.const.CFG_FILEDIR,'mosquitto.conf.bak'),
                mbconf_file)
        conf = MQTT_Broker_Configuration.query.all()
        rcf = configparser.RawConfigParser()
        conf_file =os.path.join(const.CFG_FILEDIR,"rapid.conf") 
        rcf.read( conf_file )
        ssl_ca = rcf.get("conn","ssl_ca")
        ssl_cert = rcf.get("conn","ssl_cert")
        ssl_pkey = rcf.get("conn","ssl_pkey")
        with open( mbconf_file, 'wa') as cfile:
            cfile.write("log_dest "+os.path.join(const.LOGS_DIR,MQTT_BROKER+'.log'))
            cfile.write("password_file "+os.path.join(const.CFG_FILEDIR+'.auth'))
            cfile.write("ca_file "+ssl_ca)
            cfile.write("certfile "+ssl_cert)
            cfile.write("keyfile "+ssl_pkey)
            for c in conf:
                if( c.config_name == "log_dest" or c.config_name == "password_file" \
                        or c.config_name == "cafile" or c.config_name == "certfile" \
                        or c.config_name == "keyfile"):
                    #log_dest must not be changed, so does the password_file loc
                    #TLS params should not be edited at all.
                    continue
                cfile.write(c.config_name)
                cfile.write(' ')
                cfile.write(c.config_value)
        BrokerThread.restart() # restart the broker


    def default_add_action(self):
        # updates the config file
        MQTT_Broker_Configuration.update_config()

    def default_mod_action(self):
        # updates the config file
        MQTT_Broker_Configuration.update_config()

    def default_del_action(self):
        # updates the config file
        MQTT_Broker_Configuration.update_config()
    ######################################################################################################

class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_config_name = r.StringField('MQTT Broker Configuration Name',validators=[ r.Length(max=r.lim.MAX_CONFIG_NAME_SIZE) ] )
    rgen_config_value = r.StringField('MQTT Broker Configuration Value',validators=[ r.Length(max=r.lim.MAX_CONFIG_VALU_SIZE) ] )
