#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class PRadarAlert(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "Radar_Alert"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    branch_n = r.Column(r.Integer, nullable=False)
    segment_n = r.Column(r.Integer, nullable=False)
    radar_id = r.Column(r.Integer, nullable=False)
    time = r.Column(r.DateTime, nullable=False)

    stepval = r.Column(r.Integer, nullable=False)
    magnitude = r.Column(r.Integer,nullable=False)

    reason = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=True, unique=False)
    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    # rlinking - do not have to change the variable name

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Segment Host (RPi) ID":"rpi_id",
    "Radar Branch Number":"branch_n",
    "Radar Segment Number":"segment_n",
    "Alert Timestamp":"time",
    "Alert Reason":"reason"
    # "Param0":"param0",
    # "Param1":"param1"
    } #header:row data
    # use the __link__/ and __ route_id to 'link' route_id onto something
    # the linkage is defined under the rlink dictionary down there
    # see 'RLINK'

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Proximity Radar Alert Logs" #display for r routes

    #RLINK - indicate a link (foreign key reference lookup)
    #rlink - ref tablename, fkey, lookup
    #the key defines how a column is linked, route_id is linked
    #to the table Georoute, looking up for the ID in Georoute and retrieving
    #the name.


    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.rpi_id = insert_list["rpi_id"]
        self.segment_n = insert_list["segment_n"]
        self.branch_n = insert_list["branch_n"]
        self.time = insert_list["time"]
        self.stepval = insert_list["stepval"]
        self.magnitude = insert_list["magnitude"]

        self.reason = r.checkNull(insert_list,"reason")
        self.param0 = r.checkNull(insert_list,"param0")
        self.param1 = r.checkNull(insert_list,"param1")
        #FOR nullable=True, use a the checkNull method

    ######################################################################################################
