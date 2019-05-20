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


#--------------------------------------------------
# API database schemas
# schemas/models imported here are created upon
# the update_sys call from the chosen dbms
# module (as of u8, sqlite3)
#--------------------------------------------------
from pkg.api.mqtt.models import MQTT_Sub
from pkg.api.mqtt.models import MQTT_Msg

def default_add():
    '''this is the function to add the object onto the system by 
    default (every re-initialization)'''
    pass
