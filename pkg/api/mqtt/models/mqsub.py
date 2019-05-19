#--------------------------------------------------
# mqsub.py
# MQTSUB is a database model to control subscriptions
# introduced in u8
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r
from pkg.system.database import dbms

class MQTTSubs(dbms.Base0):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "MQTT_Subs" #Try to use plurals here (i.e car's')
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    # the string topic of the topic to subscribe to
    topic = r.Column(r.String(r.lim.MAX_MQTT_TOPIC_SIZE, nullable=False) 
    description = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=True, unique=False)

    # TODO: DEFINE THE RLIST
    # CHANGED ON U6 : RLISTING NOW MERGED WITH RLINKING : see 'RLINKING _ HOW TO USE:'
    # The following is for r-listing (as of u6, rlinking as well) (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "Subscription ID":"id",
    "Topic Name":"topic",
    "Description":"description"
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
    rlist_dis = "MQTT Subscriptions" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.long = insert_list["topic"]

        #FOR nullable=True, use a the checkNull method
        self.description = r.checkNull(insert_list,"description")

    def default_add_action(self):
        # This will be run when the table is added via r-add
        # may do some imports here i.e (from pkg.database.fsqlite import db_session)
        # TODO add a MQTT restart function here
        pass

    def default_mod_action(self):
        # This will be run when the table is added modified via r-mod
        # may do some imports here i.e (from pkg.database.fsqlite import db_session)
        pass

    def default_del_action(self):
        # This will be run when the table is deleted
        # may do some imports here i.e (from pkg.database.fsqlite import db_session)
        pass
    ######################################################################################################

# The add and edit forms are the same
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_topic = r.StringField('MQTT Topic',validators=[ r.Lenght(max=r.lim.MAX_MQTT_TOPIC_SIZE) ] )
    rgen_description = r.TextAreaField('Description',validators=[r.Length(max=r.lim.MAX_DESCRIPTION_SIZE)])
