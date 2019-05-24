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
from pkg.deploy.generic import param3model, ipcam_model
from pkg.deploy.generic import canvas_circle, canvas_line
from pkg.deploy.generic import standard_log, standard_file

from pkg.resrc.rstruct import rsBlock, del_only
##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
# This is only for deployment dependent resources.
##########################################################
r_defines = {
        "param3": rsBlock( 
            param3model.Param3,
            param3model.AddForm,
            param3model.AddForm),
        "ipcamera_models": rsBlock( 
            ipcam_model.IPCameraModel,
            ipcam_model.AddForm,
            ipcam_model.EditForm),
        "standard_logs": rsBlock( 
            standard_log.StandardLog,
            None,
            del_only),
        "standard_files": rsBlock( 
            standard_file.StandardFile,
            standard_file.AddForm,
            del_only)
        }

def default_add():
    '''this is the function to add the object onto the system by 
    default (every re-initialization)'''
    from pkg.system.database import dbms #it is important to import this ONLY in the function
    pass
