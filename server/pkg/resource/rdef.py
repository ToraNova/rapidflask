#--------------------------------------------------
# rdef.py
# This file is used to define the resources used in
# the current deployment. It is meant to be dynamic
# refer to readme.txt before editing this file.
# introduced in u3
# as of u5, this file is imported and the database
# will be created from the imports here.
# ToraNova
#--------------------------------------------------

##########################################################
# PERSISTENT. DO NOT EDIT THIS !
##########################################################
#INDEX LIST enum
sqlClass = 0    #The SQL CLASS object INDEX
aForm = 1       #add form
eForm = 2       #edit form

rgen_keyword = "rgen_" #used to seek out form attributes
rgen_selkey = "rgensel_" #used to seek out SelectField form attr
rgen_timkey = "rgentim_"
rgen_actkey = "rgenact_"
rlin_nullk = "-1"

del_only = "DELONLY" #keyword for delete only objects (not modifiable but could be deleted)
##########################################################

#IMPORT RESOURCE CLASS HERE (MODEL AND FORMS)
# GEORES RESOURCES
from pkg.resource.geores import geopoint,georoute

# ZFENCING PROJECT
from pkg.resource.zfence import seghost, segcam
from pkg.resource.zfence import gsensor, proxradar
from pkg.resource.zfence import radar_alert, gsensor_alert

# Generic models
from pkg.resource.generic import param3model, ipcam_model
from pkg.resource.generic import canvas_circle, canvas_line
from pkg.resource.generic import standard_log, standard_file

##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
##########################################################

dist_resources = {
    "Param3":[
    param3model.Param3,
    param3model.AddForm,
    param3model.AddForm
    ],
    "IPCamera_Model":[
    ipcam_model.IPCameraModel,
    ipcam_model.AddForm,
    ipcam_model.EditForm
    ],
    "Standard_Log":[
    standard_log.StandardLog,
    None,
    del_only
    ],
    "Standard_File":[
    standard_file.StandardFile,
    standard_file.AddForm,
    del_only
    ]
}
