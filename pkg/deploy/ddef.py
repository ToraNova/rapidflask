#--------------------------------------------------
# ddef.py
# This file is used to define the resources used in
# the current deployment. It is meant to be dynamic
# refer to readme.txt before editing this file.
# introduced in u3
# as of u5, this file is imported and the database
# will be created from the imports here.
# as of u8, this file is migrated to the deploy
# module and now consist of deployment definitions
# ToraNova
#--------------------------------------------------

#IMPORT DEPLOYMENT CLASS HERE (MODEL AND FORMS)
#--------------------------------------------------
# Deploy database schemas
# schemas/models imported here are created upon
# the update_sys call from the chosen dbms
# module (as of u8, sqlite3)
#--------------------------------------------------
# Generic
from pkg.deploy.generic import param3model
from pkg.deploy.generic import standard_log, standard_file
from pkg.deploy.network import ipcam_model, ipcam, netnode
from pkg.deploy.dcanvas import canvas_circle, canvas_line

from pkg.resrc.rstruct import rsBlock, del_only
##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
# This is only for deployment dependent resources.
##########################################################
r_defines = {
        "Param3s": rsBlock(
            param3model.Param3,
            param3model.AddForm,
            param3model.AddForm),
        "IPCamera_Models": rsBlock(
            ipcam_model.IPCameraModel,
            ipcam_model.AddForm,
            ipcam_model.EditForm),
        "Standard_Logs": rsBlock(
            standard_log.StandardLog,
            None,
            del_only),
        "Standard_Files": rsBlock(
            standard_file.StandardFile,
            standard_file.AddForm,
            del_only)
        }

def default_add():
    '''this is the function to add the object onto the system by
    default (every re-initialization)'''
    from pkg.system.database import dbms #it is important to import this ONLY in the function

    samples = [
            ("34624","abt3",None),
            ("22332","ttwz","0"),
            ("10002","msmw","1"),
            ("10033","mww0","0"),
            ("29933","wwaz","2"),
            ("22233","z01P",None),
            ("03030","ppq-",None),
            ("20152","tiff",None),
            ("03432","peim","9"),
            ("12345","tdmc","2"),
            ("12334","zzzz","0"),
            ("22310","zzm2",None),
            ("22891",None,None),
            ("03021",None,"-1")
            ]

    for s in samples:
        insert_list = {"param0":s[0],"param1":s[1],"param2":s[2]}
        dbms.deploy.session.add( param3model.Param3( insert_list ) )
    dbms.deploy.session.commit()
