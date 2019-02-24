#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class RPi(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "RPi"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    ip_address = r.Column(r.String(r.lim.MAX_IPADDR_SIZE), nullable=False, unique=True)
    description = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=True, unique=False)
    r_threshold = r.Column(r.Integer, nullable=False, unique=False) #for radar MAG (FFT control)
    r_steptarhi = r.Column(r.Integer, nullable=False, unique=False)
    r_steptarlo = r.Column(r.Integer, nullable=False, unique=False) #for radar step (FFT control)
    g_nsen1 = r.Column(r.Integer, nullable = False, unique = False)
    g_nsen2 = r.Column(r.Integer, nullable = False, unique = False)

    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    param2 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    # rlinking - do not have to change the variable name

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "ID":"id",
    "IP address":"ip_address",
    "Radar Threshold":"r_threshold",
    "Radar Step Lower":"r_steptarlo",
    "Radar Step High":"r_steptarhi",
    "No. of sensors on branch 1":"g_nsen1",
    "No. of sensors on branch 2":"g_nsen2"
    # "Param0":"param0",
    # "Param1":"param1", # __link__ is a reserved keyword
    # "Param2":"param2"
    } #header:row data
    # use the __link__/ and __ route_id to 'link' route_id onto something
    # the linkage is defined under the rlink dictionary down there
    # see 'RLINK'

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "RPi Segment Host" #display for r routes

    #RLINK - indicate a link (foreign key reference lookup)
    #rlink - ref tablename, fkey, lookup
    #the key defines how a column is linked, route_id is linked
    #to the table Georoute, looking up for the ID in Georoute and retrieving
    #the name.

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.ip_address = insert_list["ip_address"]
        self.r_threshold = insert_list["r_threshold"]
        self.r_steptarlo = insert_list["r_steptarlo"]
        self.r_steptarhi = insert_list["r_steptarhi"]
        self.g_nsen1 = insert_list["g_nsen1"]
        self.g_nsen2 = insert_list["g_nsen2"]
        self.description = r.checkNull(insert_list,"description")
        self.param0 = r.checkNull(insert_list,"param0")
        self.param1 = r.checkNull(insert_list,"param1")
        self.param2 = r.checkNull(insert_list,"param2")
        #FOR nullable=True, use a the checkNull method

    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgen_r_threshold = r.IntegerField('Triggering Threshold',validators=[r.InputRequired()])
    rgen_r_steptarhi = r.IntegerField('Triggering Step Upper bound',validators=[r.InputRequired()])
    rgen_r_steptarlo = r.IntegerField('Triggering Step Lower bound',validators=[r.InputRequired()])

    rgen_g_nsen1 = r.IntegerField('No. of Gsensors on Branch 1',validators=[r.InputRequired()])
    rgen_g_nsen2 = r.IntegerField('No. of Gsensors on Branch 2',validators=[r.InputRequired()])

class EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgen_r_threshold = r.IntegerField('Triggering Threshold',validators=[r.InputRequired()])
    rgen_r_steptarhi = r.IntegerField('Triggering Step Upper bound',validators=[r.InputRequired()])
    rgen_r_steptarlo = r.IntegerField('Triggering Step Lower bound',validators=[r.InputRequired()])

    rgen_g_nsen1 = r.IntegerField('No. of Gsensors on Branch 1',validators=[r.InputRequired()])
    rgen_g_nsen2 = r.IntegerField('No. of Gsensors on Branch 2',validators=[r.InputRequired()])
