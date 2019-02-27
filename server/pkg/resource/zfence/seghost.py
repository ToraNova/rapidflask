#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class SegmentHost(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "Segment_Host"
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

    g_nsen1 = r.Column(r.Integer, nullable = False, unique = False)
    g_nsen2 = r.Column(r.Integer, nullable = False, unique = False)

    r_nsen1 = r.Column(r.Integer, nullable = False, unique = False)
    r_nsen2 = r.Column(r.Integer, nullable = False, unique = False)

    g_fdrawseg1 = r.Column(r.Integer, nullable=True, unique=True)
    g_fdrawseg2 = r.Column(r.Integer, nullable=True, unique=True)

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
    "No. of Radars on branch 1":"g_nsen1",
    "No. of Radars on branch 2":"g_nsen2",
    "No. of GSensors on branch 1":"g_nsen1",
    "No. of GSensors on branch 2":"g_nsen2"
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

        self.g_nsen1 = insert_list["g_nsen1"]
        self.g_nsen2 = insert_list["g_nsen2"]

        self.r_nsen1 = insert_list["r_nsen1"]
        self.r_nsen2 = insert_list["r_nsen2"]

        self.description = r.checkNull(insert_list,"description")
        self.g_fdrawseg1 = r.checkNull(insert_list,"g_fdrawseg1")
        self.g_fdrawseg2 = r.checkNull(insert_list,"g_fdrawseg2")
        self.param0 = r.checkNull(insert_list,"param0")
        self.param1 = r.checkNull(insert_list,"param1")
        self.param2 = r.checkNull(insert_list,"param2")
        #FOR nullable=True, use a the checkNull method

    def default_add_action(self):
        #This will be run when the table is added via r-add
        try:
            from pkg.resource.zfence.gsensor import GSensor
            from pkg.resource.zfence.proxradar import ProxRadar
            from pkg.database.fsqlite import db_session
            for i in range(self.g_nsen1):
                #add sensors based on how many we have
                nsen = GSensor({"rpi_id":self.id,"segment_n":i+1,"branch_n":1,"threshold":1,"config_verify":False})
                db_session.add(nsen)
            for i in range(self.r_nsen1):
                nrad = ProxRadar({"rpi_id":self.id,"segment_n":i+1,"branch_n":1,
                "r_threshold":1,"r_steptarhi":15,"r_steptarlo":5,"config_verify":False})
                db_session.add(nrad)
            for i in range(self.g_nsen2):
                nsen = GSensor({"rpi_id":self.id,"segment_n":i+1,"branch_n":2,"threshold":1,"config_verify":False})
                db_session.add(nsen)
            for i in range(self.r_nsen2):
                nrad = ProxRadar({"rpi_id":self.id,"segment_n":i+1,"branch_n":2,
                "r_threshold":1,"r_steptarhi":15,"r_steptarlo":5,"config_verify":False})
                db_session.add(nrad)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise ValueError(self.__tablename__,"default_add_action",str(e))

    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])

    rgen_g_nsen1 = r.IntegerField('No. of Gsensors on Branch 1',validators=[r.InputRequired()])
    rgen_g_nsen2 = r.IntegerField('No. of Gsensors on Branch 2',validators=[r.InputRequired()])

    rgen_r_nsen1 = r.IntegerField('No. of Radars on Branch 1',validators=[r.InputRequired()])
    rgen_r_nsen2 = r.IntegerField('No. of Radars on Branch 2',validators=[r.InputRequired()])

    # rgensel_trig_scam = r.SelectField('Triggering RPi',choices=['0','No Camera'])
    # rgen_trig_branch = r.SelectField('Triggering Branch',choices=[('1','Branch 1'),('2','Branch 2')])
    # fKeylist = {"trig_scam":("Segment_Camera","ip_address")}

class EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_ip_address = r.StringField('IP Address',validators=[r.InputRequired(),r.Length(min=1,max=r.lim.MAX_IPADDR_SIZE)])
    rgen_description = r.TextAreaField('Description',validators=[r.Length(min=1,max=r.lim.MAX_DESCRIPTION_SIZE)])

    rgen_g_nsen1 = r.IntegerField('No. of Gsensors on Branch 1',validators=[r.InputRequired()])
    rgen_g_nsen2 = r.IntegerField('No. of Gsensors on Branch 2',validators=[r.InputRequired()])

    rgen_r_nsen1 = r.IntegerField('No. of Radars on Branch 1',validators=[r.InputRequired()])
    rgen_r_nsen2 = r.IntegerField('No. of Radars on Branch 2',validators=[r.InputRequired()])

    # rgensel_trig_scam = r.SelectField('Triggering RPi',choices=['0','No Camera'])
    # rgen_trig_branch = r.SelectField('Triggering Branch',choices=[('1','Branch 1'),('2','Branch 2')])
    # fKeylist = {"trig_scam":("Segment_Camera","ip_address")}
