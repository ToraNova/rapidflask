#--------------------------------------------------
# ipcam.py
# IPCamera is a model that allows
# one to save the information about an ipcamera
# introduced in u8
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r

class IPCamera(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "IPCamera"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    ip_address = r.Column(r.String(r.lim.MAX_IPADDR_SIZE), nullable=False, unique=True)
    description = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=False, unique=False)
    model_id = r.Column(r.Integer, nullable=False, unique=False)

    # rlinking - do not have to change the variable name

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = r.OrderedDict([
        ("CameraID","id"),
        ("IP address","ip_address"),
        ("Description","description"),
        ("Model","__link__/model_id/IPCamera_Model/id:model_name")
    ]) #header,row data
    # use the __link__/ and __ route_id to 'link' route_id onto something
    # the linkage is defined under the rlink dictionary down there
    # see 'RLINK'

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "IP Camera List" #display for r routes

    #RLINK - indicate a link (foreign key reference lookup)
    #rlink - ref tablename, fkey, lookup
    #the key defines how a column is linked, route_id is linked
    #to the table Georoute, looking up for the ID in Georoute and retrieving
    #the name.

    def get_urls(self):
        from pkg.deploy.network.ipcam_model import IPCameraModel
        #returns a list that contains ffmpeg and jpegcap urls
        t = IPCameraModel.query.filter(IPCameraModel.id == self.model_id).first()
        if( t is not None ):
            out = {
                    "ffmpeg":t.ffmpeg_url,
                    "jpeg":t.jpeg_url
                    }
            return out
        else:
            return None

    def get_login(self):
        from pkg.deploy.network.ipcam_model import IPCameraModel
        #returns a tuple (uname,upass). returns None otherwise
        t = IPCameraModel.query.filter(IPCameraModel.id == self.model_id).first()
        if(t is not None):
            return (t.def_uname, t.def_upass)
        else:
            return (None,None)

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.ip_address = insert_list["ip_address"]
        self.description = insert_list["description"]
        self.model_id = insert_list["model_id"]

    def default_add_action(self):
        #This will be run when the table is added via r-add
        pass

    def default_mod_action(self):
        #This will be run when the table is added via r-mod
        pass

    def default_del_action(self):
        #This will be run when the table is added via r-del
        pass

    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgensel_model_id = r.NonValidatingSelectField('Camera Model',choices=['0','NA'])

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgensel_model_id = r.NonValidatingSelectField('Camera Model',choices=['0','NA'])
