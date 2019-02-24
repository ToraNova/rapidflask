#--------------------------------------------------
# rdef.py
# This file is used to define the resources used in
# the current deployment. It is meant to be dynamic
# refer to readme.txt before editing this file.
# introduced in u3
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
rlin_nullk = "-1"
##########################################################

#IMPORT RESOURCE CLASS HERE (MODEL AND FORMS)
# GEORES RESOURCES
from pkg.resource.geores import geopoint,georoute

# ZFENCING PROJECT
from pkg.resource.zfence import rpi, segcam, gsensor
from pkg.resource.zfence import radar_alert, gsensor_alert

# Generic models
from pkg.resource.generic import param3model, ipcam_model

##########################################################
# PLEASE EDIT THE FOLLOWING FOR EACH DEPLOYMENT!
# The following dictionary will be exported to r.py
##########################################################

dist_resources = {
    "IPCamera_Model":[
    ipcam_model.IPCameraModel,
    ipcam_model.AddForm,
    ipcam_model.EditForm
    ],
    "Georoute":[
    georoute.Georoute,
    georoute.AddForm,
    georoute.EditForm
    ],
    "Geopoint":[
    geopoint.Geopoint,
    geopoint.AddForm,
    geopoint.EditForm
    ],
    "GSensor":[
    gsensor.GSensor,
    None,
    None
    ],
    "RPi":[
    rpi.RPi,
    rpi.AddForm,
    rpi.EditForm
    ],
    "Segment_Camera":[
    segcam.SegmentCamera,
    segcam.AddForm,
    segcam.EditForm
    ],
    "GSensor_Alert":[
    gsensor_alert.GSensorAlert,
    None,
    None
    ],
    "Radar_Alert":[
    radar_alert.PRadarAlert,
    None,
    None
    ]
}
