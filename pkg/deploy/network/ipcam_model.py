#--------------------------------------------------
# ipcam_model.py
# IPCamera Model is a model that allows
# one to classify a ip cam, this allows streaming/ image
# capture functionalities
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r

class IPCameraModel(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "IPCamera_Models"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    model_name = r.Column(r.String(r.lim.MAX_USERNAME_SIZE), nullable=False, unique=True)
    ffmpeg_url = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=False, unique=False)
    jpgcap_url = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=False, unique=False)
    webproto = r.Column(r.String(10),nullable=False,unique=False)
    def_uname = r.Column(r.String(r.lim.MAX_USERNAME_SIZE),nullable=True,unique=False)
    def_upass = r.Column(r.String(r.lim.MAX_PASSWORD_SIZE),nullable=True,unique=False)
    description = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=True, unique=False)

    # rlinking - do not have to change the variable name

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = r.OrderedDict([
    ("Model Name","model_name"),
    ("FFMPEG","ffmpeg_url"),
    ("JPEG","jpgcap_url"),
    ("Description","description"),# __link__ is a reserved keyword
    ("Access protocol","webproto"),
    ("Access username (default)","def_uname"),
    ("Access password (default)","def_upass")
    ]) #header,row data
    # use the __link__/ and __ route_id to 'link' route_id onto something
    # the linkage is defined under the rlink dictionary down there
    # see 'RLINK'

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "IP Camera Model List" #display for r routes

    #RLINK - indicate a link (foreign key reference lookup)
    #rlink - ref tablename, fkey, lookup
    #the key defines how a column is linked, route_id is linked
    #to the table Georoute, looking up for the ID in Georoute and retrieving
    #the name.

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.model_name = insert_list["model_name"]
        self.ffmpeg_url = insert_list["ffmpeg_url"]
        self.jpgcap_url = insert_list["jpgcap_url"]
        self.webproto = insert_list["webproto"]

        self.def_uname = r.checkNull(insert_list,"def_uname")
        self.def_upass = r.checkNull(insert_list,"def_upass")
        self.description = r.checkNull(insert_list,"description")

    def default_add_action(self):
        #This will be run when the table is added via r-add
        pass

    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_model_name = r.StringField('Model Name',
    validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_USERNAME_SIZE)])
    rgen_ffmpeg_url = r.StringField('FFMPEG URL',
    validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgen_jpgcap_url = r.StringField('JPEG CAPTURE URL',
    validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])

    rgen_webproto = r.StringField('Camera Access Protocol',validators=[r.InputRequired(),r.Length(min=1,max=10)],default="http")
    rgen_def_uname = r.StringField('Camera Access Username',
    validators=[r.Length(min=4,max=r.lim.MAX_USERNAME_SIZE)])
    rgen_def_upass = r.StringField('Camera Access Password',
    validators=[r.Length(min=8,max=r.lim.MAX_PASSWORD_SIZE)])

    rgen_description = r.TextAreaField('Description',
    validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ffmpeg_url = r.StringField('FFMPEG URL',
    validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgen_jpgcap_url = r.StringField('JPEG CAPTURE URL',
    validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])

    rgen_webproto = r.StringField('Camera Access Protocol',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_def_uname = r.StringField('Camera Access Username',
    validators=[r.Length(min=4,max=r.lim.MAX_USERNAME_SIZE)])
    rgen_def_upass = r.StringField('Camera Access Password',
    validators=[r.Length(min=8,max=r.lim.MAX_PASSWORD_SIZE)])

    rgen_description = r.TextAreaField('Description',
    validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
