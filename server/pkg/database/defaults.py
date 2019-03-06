#--------------------------------------------------
# defaults.py
# this file is meant to add default entities onto the database
# for easier development use.
# introduced 8/12/2018
#--------------------------------------------------

from pkg.database.fsqlite import sy_session

def default_add():

    #Perma models
    from pkg.database.models import System_User
    from pkg.database.models import System_UserType
    from pkg.database.models import System_Configuration

    #add default values of the configuration table
    #default_config_list = [["ScannerID","AR001"],["MainServerIP","127.0.0.1"],["MainServerPort","4000"]] #used for attemoni
    default_config_list = []
    for configs in default_config_list:
        sy_session.add(System_Configuration(configs[0],configs[1]))

    #adding default user - admin
    default_username = "admin"
    default_password = "1996-June-26" #placeholder
    default_user = System_User(default_username,default_password,1)
    default_user.passhash = 'pbkdf2:sha512:50000$Bpl7mvp6$d16d6dfff5047c77e14334c3562cc8cecf1e6d4a88cf13a990541317405231d204d6577ddc3a459cd5a5b4f3a6302adbc628ef26a1e0a47d9140a28ea47ee326'
    sy_session.add(default_user)

    #adding default userType - admin, seer
    default_utypelist = [["admin",0],["seer",1]]
    for utype in default_utypelist:
        sy_session.add(System_UserType(utype[0],utype[1]))

    sy_session.commit()
