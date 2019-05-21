#--------------------------------------------------
# param3model.py
# Param3 is an example of a simple 3 field model
# this model should not contain any forms
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r

class StandardLog(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Standard_Logs"
    # TODO: DEFINE LIST OF COLUMNS
    timev0 = r.Column(r.DateTime, nullable=False) #insertion time
    timev1 = r.Column(r.DateTime, nullable=True) #time logging
    timev2 = r.Column(r.DateTime, nullable=True)

    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=False) #for data logging
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True)
    param2 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True)

    ref0 = r.Column(r.Integer, nullable=False) #for references
    ref1 = r.Column(r.Integer, nullable=True)
    ref2 = r.Column(r.Integer, nullable=True)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Entity ID":"id",
    "Param0":"param0",
    "Param1":"param1",
    "Param2":"param2",
    "Ref0":"ref0",
    "Ref1":"ref1",
    "Ref2":"ref2",
    "Time v0":"__time__/%b-%d-%Y %H:%M:%S/timev0",
    "Time v1":"timev1",
    "Time v2":"timev2"
    } #header:row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Standard Log Model" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):

        self.timev0 = r.datetime.datetime.now()
        self.timev1 = r.checkNull(insert_list,"timev1")
        self.timev1 = r.checkNull(insert_list,"timev2")

        self.param0 = insert_list["param0"]
        self.param1 = r.checkNull(insert_list,"param1")
        self.param2 = r.checkNull(insert_list,"param2")

        self.param0 = insert_list["ref0"]
        self.param1 = r.checkNull(insert_list,"ref1")
        self.param2 = r.checkNull(insert_list,"ref2")
    ######################################################################################################

# STANDARD LOG MODEL NOT MEANT TO BE ADDED MANUALLY BY HAND
