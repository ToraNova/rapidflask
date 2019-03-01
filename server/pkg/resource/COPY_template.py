#--------------------------------------------------
# COPY_template.py
# COPY_template is a resource template. Please
# use this as a base file when introducing new tables
# use ctrl-f on TODO to findout which parts to change
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class TODO_SAMPLE(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "PLS CHANGE THIS"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    long = r.Column(r.Float, nullable=False) #longitude
    lati = r.Column(r.Float, nullable=False) #latitude
    time = r.Column(r.DateTime, nullable=False)

    # rlinking - do not have to change the variable name
    route_id = r.Column(r.Integer, nullable=True)

    # TODO: DEFINE THE RLIST
    # CHANGED ON U6 : RLISTING NOW MERGED WITH RLINKING : see 'RLINKING _ HOW TO USE:'
    # The following is for r-listing (as of u6, rlinking as well) (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Geopoint ID":"id",
    "Longitude":"long",
    "Latitude":"lati",
    "Linked Entity":"__link__/route_id/Georoute/id:name", # __link__ is a reserved keyword
    "Timestamp":"time"
    } #header:row data

    # RLINKING _ HOW TO USE :
    # using the __link__ keyword, seperate the arguments with /
    # The first argument is the local reference, the field in which we use to refer
    # the second argument is the foreign table
    # the third argument is the foreign table Primary key
    # the fourth argument is the field we want to find from the foreign table
    # NOTICE that the fourth table uses ':' instead of /.
    # Example
    # "RPi id":"__link__/rpi_id/RPi/id:rpi_name"
    # for the display of RPi id, we link to a foreign table that is called RPi
    # we use the rpi_id foreign key on this table, to locate the id on the foreign table
    # then we query for the field rpi_name

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Geopoints" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.long = insert_list["long"]
        self.lati = insert_list["lati"]
        self.time = insert_list["time"]

        #FOR nullable=True, use a the checkNull method
        self.route_id = r.checkNull(insert_list,"route_id")

    def default_add_action(self):
        #This will be run when the table is added via r-add
        try:
            # may do some imports here
            #from pkg.database.fsqlite import db_session
            pass
        except Exception as e:
            #PLEASE DO NOT EDIT THIS, ENABLE the rollback if there are db changes
            #db_session.rollback()
            raise ValueError(self.__tablename__,"default_add_action",str(e))

    def default_mod_action(self):
        #This will be run when the table is added modified via r-mod
        try:
            # may do some imports here
            #from pkg.database.fsqlite import db_session
            pass
        except Exception as e:
            #PLEASE DO NOT EDIT THIS, ENABLE the rollback if there are db changes
            #db_session.rollback()
            raise ValueError(self.__tablename__,"default_mod_action",str(e))

    def default_del_action(self):
        #This will be run when the table is deleted
        try:
            # may do some imports here
            #from pkg.database.fsqlite import db_session
            pass
        except Exception as e:
            #PLEASE DO NOT EDIT THIS, ENABLE the rollback if there are db changes
            #db_session.rollback()
            raise ValueError(self.__tablename__,"default_del_action",str(e))
    ######################################################################################################

#TODO : DEFINE ADD RES FORM
#ADD FORM TEMPLATE
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_long = r.StringField('New Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('New Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #sample datepicker widget (allows date selection), use the rgentim_ prefix
    rgentim_time = r.DateField('T stamp', widget=r.DatePickerWidget(),default=r.datetime.datetime.now())

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgensel_route_id = r.SelectField('Assigned Route',choices=[('0','No route')])
    fKeylist = {"route_id":("Georoute","name")}

#TODO : DEFINE ADD RES FORM
#EDIT FORM TEMPLATE
class EditForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_long = r.StringField('New Longitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])
    rgen_lati = r.StringField('New Latitude',validators=[r.InputRequired(),r.Length(min=1,max=10)])

    #sample datepicker widget (allows date selection), use the rgentim_ prefix
    rgentim_time = r.DateField('T stamp', widget=r.DatePickerWidget(),default=r.datetime.datetime.now())

    #TODO: List select fields here, FIELDS MUST BE PREFIXED WITH rgensel_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgensel_route_id = r.SelectField('Reassigned Route',choices=[('0','No route')])
    fKeylist = {"route_id":("Georoute","name")}
