#--------------------------------------------------
# sdef.py
# This file is used to deinfe the resources used in
# the system. It is meant to be permanent and
# consistent through many deployments. Please edit
# this file only for SYSTEM based changes.
# introduced in u8
# @author ToraNova
# @mailto chia_jason96@live.com
# @date 19/05/2019
#--------------------------------------------------


#--------------------------------------------------
# System database schemas
# schemas/models imported here are created upon
# the update_sys call from the chosen dbms
# module (as of u8, sqlite3)
#--------------------------------------------------
from pkg.system.user.models import System_User
from pkg.system.user.models import System_UserType
from pkg.system.user.models import System_Configuration

def default_add():
    '''default adds are now defined in sdef. this function is called when 
    the database systems re-creates the metadata (schema) for the database
    models'''

    from pkg.system.database import dbms # it is important to import this ONLY in the function

    #add default values of the configuration table
    #default_config_list = [["ScannerID","AR001"],["MainServerIP","127.0.0.1"],["MainServerPort","4000"]] #used for attemoni
    default_config_list = []
    for configs in default_config_list:
        dbms.system.session.add(System_Configuration(configs[0],configs[1]))

    #adding default user - admin
    default_username = "admin"
    default_password = "1996-June-26" #placeholder
    default_user = System_User(default_username,default_password,1)
    default_user.passhash = 'pbkdf2:sha512:50000$Bpl7mvp6$d16d6dfff5047c77e14334c3562cc8cecf1e6d4a88cf13a990541317405231d204d6577ddc3a459cd5a5b4f3a6302adbc628ef26a1e0a47d9140a28ea47ee326'

    dbms.system.session.add(default_user)

    default_username = "user0"
    default_password = "1996-June-26" #placeholder
    default_user = System_User(default_username,default_password,2)
    default_user.passhash = 'pbkdf2:sha512:50000$Bpl7mvp6$d16d6dfff5047c77e14334c3562cc8cecf1e6d4a88cf13a990541317405231d204d6577ddc3a459cd5a5b4f3a6302adbc628ef26a1e0a47d9140a28ea47ee326'

    dbms.system.session.add(default_user)

    #adding default userType - admin, seer
    default_utypelist = [["admin",0],["seer",1]]
    for utype in default_utypelist:
        dbms.system.session.add(System_UserType(utype[0],utype[1]))

    dbms.system.session.commit()
