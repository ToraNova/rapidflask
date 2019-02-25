#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class SegmentCamera(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "Segment_Camera"
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
    model_id = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=False, unique=False)

    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True, unique=False)
    # rlinking - do not have to change the variable name

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "CameraID":"id",
    "IP address":"ip_address",
    "Description":"description",
    "Model":"__link__/model_id/IPCamera_Model/id:model_name"
    #"Param0":"param0", # __link__ is a reserved keyword
    #"Param1":"param1"
    } #header:row data
    # use the __link__/ and __ route_id to 'link' route_id onto something
    # the linkage is defined under the rlink dictionary down there
    # see 'RLINK'

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Segment Camera List" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.ip_address = insert_list["ip_address"]
        self.description = insert_list["description"]
        self.model_id = insert_list["model_id"]

        self.param0 = r.checkNull(insert_list,"param0")
        self.param1 = r.checkNull(insert_list,"param1")
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgensel_model_id = r.SelectField('Camera Model',choices=['0','No Model'])
    fKeylist = {"model_id":("IPCamera_Model","model_name")}

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model

    rgensel_model_id = r.SelectField('Camera Model',choices=['0','No Model'])
    fKeylist = {"model_id":("IPCamera_Model","model_name")}
