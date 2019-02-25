#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class GSensor(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "GSensor"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    segment_n = r.Column(r.Integer, nullable=False)
    branch_n = r.Column(r.Integer,nullable=False)
    rpi_id= r.Column(r.Integer, nullable=True)
    threshold = r.Column(r.Integer, nullable=False)

    alert_state = r.Column(r.Boolean(),unique=False,nullable=False)

    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    # rlinking - do not have to change the variable name


    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Sensor Id":"id",
    "Segment Host(RPi) id":"__link__/rpi_id/Segment_Host/id:id",
    "Branch":"branch_n",
    "Segment Number":"segment_n",
    "G-Threshold":"threshold",
    "Alert Triggered":"alert_state"
    # "Param0":"param0",
    # "Param1":"param1"
    } #header:row data

    # RLINKING _ HOW TO USE :
    # using the __link__ keyword, seperate the arguments with /
    # The first argument is the local reference, the field in which we use to refer
    # the second argument is the foreign table
    # the third argument is the foreign table Primary key
    # the fourth argument is the field we want to find from the foreign table
    # NOTICE that the fourth table uses ':' instead of /.
    # Example
    # "RPi id":"__link__/rpi_id/RPi/id:rpi_name"
    # for the display of RPi id, we link to a foreign table that is called RPi
    # we use the rpi_id foreign key on this table, to locate the id on the foreign table
    # then we query for the field rpi_name

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "G-Sensor List" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.segment_n = insert_list["segment_n"]
        self.branch_n = insert_lits["branch_n"]
        self.threshold = insert_list["threshold"]
        self.alert_state = insert_list["alert_state"]
        #FOR nullable=True, use a the checkNull method
        #self.route_id = r.checkNull(insert_list,"route_id")
        self.rpi_id = r.checkNull(insert_list,"rpi_id")
        self.param0 = r.checkNull(insert_list,"param0")
        self.param1 = r.checkNull(insert_list,"param1")
