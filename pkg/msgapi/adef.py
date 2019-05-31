#--------------------------------------------------
# adef.py
# This file is used to define api models ( that is,
# database objects that are used together with the
# API system on rapidflask
# introduced in u8
# @author ToraNova
# @mailto chia_jason96@live.com
# @date 20/05/2019
#--------------------------------------------------


#IMPORT MSG/API CLASS HERE (MODEL AND FORMS)
#--------------------------------------------------
# API database schemas
# schemas/models imported here are created upon
# the update_sys call from the chosen dbms
# module (as of u8, sqlite3)
#--------------------------------------------------
# MQTT

from pkg.msgapi.mqtt.models import mqsub, mqmsg
from pkg.msgapi.mqtt.models import mqbrk
from pkg.msgapi.models import apiuser
#from pkg.msgapi.mqtt.models import MQTT_Sub
#from pkg.msgapi.mqtt.models import MQTT_Msg
#from pkg.msgapi.mqtt.models import MQTT_Broker_Configuration
#from pkg.msgapi.mqtt.models import MQTT_Broker_User

from pkg.resrc.rstruct import rsBlock, del_only
##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
# This is only for msg/api dependent resources.
##########################################################
r_defines = {
        "mqttbroker_configs": rsBlock(
            mqbrk.MQTT_Broker_Configuration,
            mqbrk.AddForm,
            mqbrk.AddForm),
        "msgapi_users": rsBlock(
            apiuser.Msgapi_User,
            apiuser.AddForm,
            apiuser.AddForm),
        "mqttclient_subs": rsBlock(
            mqsub.MQTT_Sub,
            mqsub.AddForm,
            mqsub.AddForm),
        "mqttclient_msgs": rsBlock(
            mqmsg.MQTT_Msg,
            None,
            del_only)
        }

def default_add():

    from pkg.system.database import dbms #it is important to import this ONLY in the function
    default_broker_config_list = [
            ("use_ssl","true"),
           ("allow_anonymous","false"),("allow_duplicate_messages","false"),
           ("allow_zero_length_clientid","true"),("auto_id_prefix","rapid"),
           ("connection_messages","true"),
           ("log_type","error"),("log_type","warning"),
           ("log_type","unsubscribe"),("log_type","subscribe"),
           ("log_type","notice"),("log_type","information"),
           ("port","1883")
            ]
    for configs in default_broker_config_list:
        insert_list = {"config_name":configs[0],"config_value":configs[1]}
        dbms.msgapi.session.add(mqbrk.MQTT_Broker_Configuration(insert_list))

    local_user = apiuser.Msgapi_User( {"username":"localuser","plain_password":"mqtt_rocks","usertype":"MQTTv0"} )
    dbms.msgapi.session.add( local_user )
    default_user = apiuser.Msgapi_User( {"username":"rqtt0","plain_password":"mqtt_rocks","usertype":"MQTTv0"} )
    dbms.msgapi.session.add( default_user )
    dbms.msgapi.session.commit()

