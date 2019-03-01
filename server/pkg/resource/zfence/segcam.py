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

    trig_seghst = r.Column(r.Integer, nullable=True) #the seghost to trigger this camera
    trig_branch = r.Column(r.Integer, nullable=True) #the branch to trigger the ipcamera

    los_segment = r.Column(r.Integer, nullable=True, unique=True) #Line of sight

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
    "Model":"__link__/model_id/IPCamera_Model/id:model_name",
    "Triggered by seghost":"trig_seghst",
    "On branch/segment":"trig_branch"
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
        self.trig_seghst = r.checkNull(insert_list,"trig_seghst")
        self.trig_branch = r.checkNull(insert_list,"trig_branch")
        self.los_segment = r.checkNull(insert_list,"los_segment")

        self.param0 = r.checkNull(insert_list,"param0")
        self.param1 = r.checkNull(insert_list,"param1")

    def default_add_action(self):
        #This will be run when the table is added via r-add
        try:
            # may do some imports here
            #from pkg.database.fsqlite import db_session
            pass
        except Exception as e:
            #db_session.rollback()
            raise ValueError(self.__tablename__,"default_add_action",str(e))

    def default_del_action(self):
        #This will be run when the table is deleted
        try:
            # may do some imports here
            #from pkg.database.fsqlite import db_session
            from pkg.database.fsqlite import db_session
            from pkg.resource.generic.canvas_line import CanvasLine
            line1 = CanvasLine.query.filter(CanvasLine.id == self.los_segment).first()
            if(line1 != None):
                db_session.delete(line1)
            db_session.commit()
        except Exception as e:
            #PLEASE DO NOT EDIT THIS, ENABLE the rollback if there are db changes
            db_session.rollback()
            raise ValueError(self.__tablename__,"default_del_action",str(e))
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgensel_model_id = r.SelectField('Camera Model',choices=['0','NA'])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgensel_trig_seghst = r.SelectField('Triggering RPi',choices=['0','NA'])
    rgen_trig_branch = r.SelectField('Triggering Branch',choices=[('1','Segment (Branch) 1'),('2','Segment (Branch) 2')])

    fKeylist = {"model_id":("IPCamera_Model","model_name"),"trig_seghst":("Segment_Host","id")}

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgensel_model_id = r.SelectField('Camera Model',choices=['0','NA'])

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgensel_trig_seghst = r.SelectField('Triggering RPi',choices=['0','NA'])
    rgen_trig_branch = r.SelectField('Triggering Branch',choices=[('1','Segment (Branch) 1'),('2','Segment (Branch) 2')])

    fKeylist = {"model_id":("IPCamera_Model","model_name"),"trig_seghst":("Segment_Host","id")}
