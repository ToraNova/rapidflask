#--------------------------------------------------
# rstruct.py
# used to be named rdef, now rdef is rstruct on the
# logical structural definition of using r while
# the def side is split into system/deploy and api
# ToraNova
#--------------------------------------------------

##########################################################
# PERSISTENT. DO NOT EDIT THIS !
##########################################################
rgen_keyword = "rgen_" #used to seek out form attributes
rgen_selkey = "rgensel_" #used to seek out SelectField form attr
rgen_timkey = "rgentim_"
rgen_actkey = "rgenact_"
rgen_typebool = "rgenbool_" #used to forced parsing as a boolean
rlin_nullk = "-1"

del_only = "DELONLY" #keyword for delete only objects (not modifiable but could be deleted)
all_only = "ALLONLY" #keyword for objects that cannot be queried (list all upon a rlist)
nodel_at = "rmod_nodel" #keyword used as object attribute to indicate R may not delete it
##########################################################

from collections import namedtuple

# rsBlocks are resource standards. This is exported to def files (sdef, ddef and adef)
# the def files define which models and how are they used by the r module
rsBlock = namedtuple("rsBlock",["model","addform","lsform","editform"])



