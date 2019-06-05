#--------------------------------------------------
# param3model.py
# Param3 is an example of a simple 3 field model
# this model should not contain any forms
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r

class Param3(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Param3s"
    # TODO: DEFINE LIST OF COLUMNS
    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=False)
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True)
    param2 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = r.OrderedDict([
    ("Entity ID","id"),
    ("Param0","param0"),
    ("Param1","param1"),
    ("Param2","param2")
    ]) #header,row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Param 3 Model" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.param0 = insert_list["param0"]
        self.param1 = r.checkNull(insert_list,"param1")
        self.param2 = r.checkNull(insert_list,"param2")
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
#param3model share same edit / add form, only one needed
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_param0 = r.StringField('parameter0 Not Nullable',validators=[r.InputRequired(),r.Length(max=r.lim.MAX_UUPARAM_SIZE)])
    rgen_param1 = r.StringField('parameter1 Nullable',validators=[r.Length(max=r.lim.MAX_UUPARAM_SIZE)])
    rgen_param2 = r.StringField('parameter2 Nullable',validators=[r.Length(max=r.lim.MAX_UUPARAM_SIZE)])
