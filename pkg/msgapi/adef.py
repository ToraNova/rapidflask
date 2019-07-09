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

from pkg.resrc.rstruct import rsBlock, del_only, all_only
##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
# This is only for msg/api dependent resources.
##########################################################
r_defines = {
        "MQTT_Broker_Configs": rsBlock(
            mqbrk.MQTT_Broker_Configuration,
            mqbrk.AddForm,
            all_only,
            mqbrk.AddForm),
        "Msgapi_Users": rsBlock(
            apiuser.Msgapi_User,
            apiuser.AddForm,
            all_only,
            apiuser.AddForm),
        "MQTT_Subs": rsBlock(
            mqsub.MQTT_Sub,
            mqsub.AddForm,
            all_only,
            mqsub.AddForm),
        "MQTT_Msgs": rsBlock(
            mqmsg.MQTT_Msg,
            None,
            all_only,
            del_only)
        }

def default_add():

    from pkg.system.database import dbms #it is important to import this ONLY in the function
    sub0 = mqsub.MQTT_Sub(\
            {'topic':'ping/server','description':'For Ping purposes on the server MQTT client','stordur':60,'delonproc':True,'deloncas':True,'instantp':True})
    dbms.msgapi.session.add(sub0)

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
        dbms.msgapi.session.add(mqbrk.MQTT_Broker_Configuration( insert_list ) )

    default_api_userlist = [
            ('localuser','mqtt_rocks','MQTTv0'),
            ('rqtt0','mqtt_rocks','MQTTv0'),
            ('http0','tcdmbedpeimdsswhileih5wamspd','HTTPv0')
            ]
    for au in default_api_userlist:
        insert_list = {"username": au[0], "access_key":au[1], "usertype":au[2]}
        dbms.msgapi.session.add( apiuser.Msgapi_User( insert_list ) )

    dbms.msgapi.session.commit()

