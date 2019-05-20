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
from pkg.msgapi.mqtt.models import MQTT_Sub
from pkg.msgapi.mqtt.models import MQTT_Msg

from pkg.resource.rstruct import rsBlock, del_only
##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
# This is only for msg/api dependent resources.
##########################################################
r_defines = {
        }

def default_add():
    '''this is the function to add the object onto the system by 
    default (every re-initialization)'''
    pass
