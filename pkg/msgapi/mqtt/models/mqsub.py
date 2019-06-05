#--------------------------------------------------
# mqsub.py
# MQTSUB is a database model to control subscriptions
# introduced in u8
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r
from pkg.system.database import dbms
Base = dbms.msgapi.base

class MQTT_Sub(Base):
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
    topic = r.Column(r.String(r.lim.MAX_MQTT_TOPIC_SIZE), nullable=False, unique=True) 
    description = r.Column(r.String(r.lim.MAX_DESCRIPTION_SIZE), nullable=True, unique=False)
    stordur = r.Column(r.Integer, nullable=True) #how long to store messages
    delonproc = r.Column(r.Boolean, nullable=False) #delete the messages after processing?
    deloncas = r.Column(r.Boolean, nullable=False) #delete all msg if the topics get deleted

    # TODO: DEFINE THE RLIST
    # CHANGED ON U6 : RLISTING NOW MERGED WITH RLINKING : see 'RLINKING _ HOW TO USE:'
    # The following is for r-listing (as of u6, rlinking as well) (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = r.OrderedDict([
    ("Subscription ID","id"),
    ("Topic Name","topic"),
    ("Description","description"),
    ("Store N seconds (None/Null = Forever)","stordur"),
    ("Delete on processed?","delonproc"),
    ("Delete on cascade?","deloncas")
    ]) #header,row data

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
        self.topic = insert_list["topic"]
        self.delonproc = bool(insert_list["delonproc"])
        self.deloncas = bool(insert_list["deloncas"])

        #FOR nullable=True, use a the checkNull method
        self.description = r.checkNull(insert_list,"description")
        self.stordur = r.checkNull(insert_list,"stordur")

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
        # delete all linked on cascade
        if(self.deloncas):
            import pkg.system.database.dbms as dbms
            from pkg.msgapi.mqtt.models import MQTT_Msg
            links = MQTT_Msg.query.filter( MQTT_Msg.tlink == self.id ).all()
            for m in links:
                dbms.sy_session.delete( m )
            srvlog["oper"].warning("Removed MQTT SubTopic and messages with cascade")
            dbms.sy_session.commit()

    ######################################################################################################

# The add and edit forms are the same
class AddForm(r.FlaskForm):
    #TODO: List the fields here, FIELDS MUST BE PREFIXED WITH rgen_
    # The names here after the rgen_ prefix must correspond to a var name in the respective model
    rgen_topic = r.StringField('MQTT Topic',validators=[ r.Length(max=r.lim.MAX_MQTT_TOPIC_SIZE) ] )
    rgen_description = r.TextAreaField('Description',validators=[r.Length(max=r.lim.MAX_DESCRIPTION_SIZE)])
    rgen_stordur = r.IntegerField('Store at most N seconds (leave empty to store forever)')
    rgen_delonproc = r.SelectField('Delete messages after process?',choices=[('1','True'),('0','False')])
    rgen_deloncas = r.SelectField('Delete messages on cascade?',choices=[('1','True'),('0','False')])



