#--------------------------------------------------
# param3model.py
# Param3 is an example of a simple 3 field model
# this model should not contain any forms
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r

# non-standard usage
import os, datetime
from flask import send_file, Blueprint
from flask_login import login_required, current_user

bp = Blueprint('stdfile', __name__, url_prefix='/'+r.const.STD_FILEDIR)

@bp.route('/uploads/retrieve/<urlparam>')
@login_required
def retrieve_uploads(urlparam):
	targetfile = StandardFile.query.filter( StandardFile.filename == urlparam ).first()
	return send_file(os.path.join(r.const.STD_FILEDIR,targetfile.filename),mimetype=targetfile.mimetype)

class StandardFile(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Standard_Files"
    # TODO: DEFINE LIST OF COLUMNS
    filename = r.Column(r.String(r.lim.MAX_FILENAME_SIZE),nullable=False,unique=True)
    mimetype = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE),nullable=False,unique=False)
    uptime = r.Column(r.DateTime, nullable=False) #time logging (time of upload)
    fileown = r.Column(r.Integer, nullable=True)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = r.OrderedDict([
    ("Filename","filename"),
    ("URL","__url__/stdfile.retrieve_uploads/filename"),
    ("MIME type","mimetype"),
    ("Uploaded Time","__time__/%b %d %Y/uptime"),
    ("Uploader","fileown")
    ]) #header,row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Standard File Model" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.filename = insert_list["filename"]
        self.mimetype = insert_list["mimetype"]
        self.uptime = datetime.datetime.now()
        self.fileown = r.checkNull(insert_list,"fileown")

    def default_del_action(self):
        # This will be run when the table is deleted
        # may do some imports here i.e (from pkg.database.fsqlite import db_session)
        os.remove(os.path.join('pkg',r.const.STD_FILEDIR,self.filename))
    ######################################################################################################

class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgenact_file = r.FileField('Target File')
    rgen_mimetype = r.SelectField('MIME type',choices=[
    ('text/plain',"Plaintext"),
    ('image/jpeg',"Images (jpeg)"),
    ('application/pdf',"PDF"),
    ('text/html',"HTML"),
    ('application/x-troff-msvideo','.avi'),
    ('audio/mpeg3','.mp3'),
    ('video/mpeg','mpeg4')
    ])

    def file(self, return_form):
        out = {}
        print(return_form.rgenact_file.data,return_form.rgen_mimetype.data)
        out['filename'] = r.secure_filename(return_form.rgenact_file.data.filename)
        return_form.rgenact_file.data.save(os.path.join('pkg',r.const.STD_FILEDIR,out['filename']))
        out['fileown'] = current_user.username
        return out
