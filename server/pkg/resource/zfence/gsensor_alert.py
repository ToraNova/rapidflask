#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class GSensorAlert(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "GSensor_Alert"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    time = r.Column(r.DateTime, nullable=False)
    sensor_id = r.Column(r.Integer, nullable=True)
    rpi_id = r.Column(r.Integer, nullable=True)
    reason = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=False, unique=False)
    wcut =  r.Column(r.Boolean(),unique=False,nullable=False)
    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    # rlinking - do not have to change the variable name

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "RPi ID":"__link__/rpi_id",
    "Sensor Branch Number":"__link__/sensor_id/GSensor/id:branch_n",
    "Sensor Segment Number":"__link__/sensor_id/Gsensor/id:segment_n",
    "Wirecut ?":"wcut",
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
    rlist_dis = "Acceleration Sensor Alert Logs" #display for r routes

    #RLINK - indicate a link (foreign key reference lookup)
    #rlink - ref tablename, fkey, lookup
    #the key defines how a column is linked, route_id is linked
    #to the table Georoute, looking up for the ID in Georoute and retrieving
    #the name.


    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.time = insert_list["time"]
        self.reason = insert_list["reason"]
        self.wcut = insert_list["wcut"]
        #FOR nullable=True, use a the checkNull method

        self.sensor_id = r.checkNull(insert_list,"sensor_id")
        self.rpi_id = r.checkNull(insert_list,"rpi_id")
        self.param0 = r.checkNull(insert_list,"param0")
        self.param1 = r.checkNull(insert_list,"param1")

    ######################################################################################################
