#--------------------------------------------------
# mqusr.py
# MQTT_BROKER_USER is for access control on the mqtt
# broker
# introduced in u8
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r
from shutil import copyfile
import os
from subprocess import Popen
from pkg.system.database import dbms
from pkg.msgapi.mqtt import BrokerThread
Base = dbms.msgapi.base

apitypes = [
        ('MQTTv0','Mosquitto (MQTTv0)'),
        ('HTTPv0','HTTP Pull/Push')
        ]

class Msgapi_User(Base):
    __tablename__ = "Msgapi_Users" #Try to use plurals here (i.e car's')
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    username = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), unique=True)
    plain_password = r.Column(r.String(r.lim.MAX_PASSWORD_SIZE))
    # TODO: figure out a way to secure this more
    # justification for plain_password storage here. the reason is
    # to allow the administrator to easily obtain the password from
    # the database 
    usertype = r.Column(r.String(r.lim.MAX_USERNAME_SIZE),unique=False)

    rlist = r.OrderedDict([
        ("Username","username"),
        ("Password","plain_password"),
        ("API Type","usertype")
        ])
    rlist_priKey = "id"
    rlist_dis = "Msgapi Users" #display for r routes

    @staticmethod
    def update_auth(apitype):
        if(apitype == "MQTTv0"):
            # TODO : use mosquitto_passwd tool
            authfile = os.path.join(r.const.CFG_FILEDIR,'mosquitto.auth')
            if( os.path.isfile( authfile )):
                    os.remove( authfile )
            users = Msgapi_User.query.filter( Msgapi_User.usertype == apitype).all()
            with open( authfile, 'w') as afile:
                for u in users:
                    afile.write(u.username)
                    afile.write(':')
                    afile.write(u.plain_password)
                    afile.write('\n') #this line bugged the config file.
            rewrite_pwdfile = Popen(['mosquitto_passwd','-U',authfile])
            rewrite_pwdfile.wait()
            BrokerThread.restart() # restart the broker
        else:
            pass


    def __init__(self,insert_list):
        self.username = insert_list["username"]
        self.plain_password = insert_list["plain_password"]
        self.usertype = insert_list["usertype"]

    def default_add_action(self):
        # updates the config file
        Msgapi_User.update_auth(self.usertype)

    def default_mod_action(self):
        # updates the config file
        Msgapi_User.update_auth(self.usertype)

    def default_del_action(self):
        # updates the config file
        Msgapi_User.update_auth(self.usertype)

class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_username = r.StringField('MQTT UserName',validators=[ r.Length(max=r.lim.MAX_USERNAME_SIZE) ] )
    rgen_plain_password = r.StringField('MQTT UserPass(Plaintext)',validators=[ r.Length(max=r.lim.MAX_PASSWORD_SIZE) ] )
    rgen_usertype = r.SelectField('API Type',choices=apitypes)
