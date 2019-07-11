#--------------------------------------------------
# param3model.py
# Param3 is an example of a simple 3 field model
# this model should not contain any forms
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resrc import res_import as r
import datetime

class StandardLog(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: CHANGE TABLENAME
    __tablename__ = "Standard_Logs"
    # TODO: DEFINE LIST OF COLUMNS
    timev0 = r.Column(r.DateTime, nullable=False) #insertion time
    timev1 = r.Column(r.DateTime, nullable=True) #time logging
    timev2 = r.Column(r.DateTime, nullable=True)

    param0 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=False) #for data logging
    param1 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True)
    param2 = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=True)

    ref0 = r.Column(r.Integer, nullable=False) #for references
    ref1 = r.Column(r.Integer, nullable=True)
    ref2 = r.Column(r.Integer, nullable=True)

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = r.OrderedDict([
    ("Entity ID","id"),
    ("Param0","param0"),
    ("Param1","param1"),
    ("Param2","param2"),
    ("Ref0","ref0"),
    ("Ref1","ref1"),
    ("Ref2","ref2"),
    ("Time v0","__time__/%b-%d-%Y %H:%M:%S/timev0"),
    ("Time v1","__time__/%b-%d-%Y/timev1"),
    ("Time v2","__time__/%H:%M:%S/timev2")
    ]) #header,row data

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Standard Log Model" #display for r routes

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):

        self.timev0 = datetime.datetime.now()
        self.timev1 = r.checkNull(insert_list,"timev1")
        self.timev1 = r.checkNull(insert_list,"timev2")

        self.param0 = insert_list["param0"]
        self.param1 = r.checkNull(insert_list,"param1")
        self.param2 = r.checkNull(insert_list,"param2")

        self.ref0 = insert_list["ref0"]
        self.ref1 = r.checkNull(insert_list,"ref1")
        self.ref2 = r.checkNull(insert_list,"ref2")
    ######################################################################################################

# STANDARD LOG MODEL NOT MEANT TO BE ADDED MANUALLY BY HAND

# u81 -- LS forms (list forms)

class LsForm(r.FlaskForm):
    # Forms to allow filtering
    #tv0_start = r.LenientDateTimeField(\
    #        label='TimeV0 From', widget=r.DateTimePickerWidget(),\
    #        default=datetime.date.today())
    #tv0_end = r.LenientDateTimeField(\
    #        label='TimeV0 To', widget=r.DateTimePickerWidget(),\
    #        default=(datetime.date.today()+\
    #        datetime.timedelta(hours = 23,minutes=59,seconds=59)))
    tv0_ignore = r.SelectField("TimeV0 Ignore?",choices=[("1","Yes"),("0","No")])
    tv0_start = r.DateField(\
            'TimeV0 From  :', widget=r.DatePickerWidget(),\
            format='%m/%d/%Y',\
            default=datetime.date.today())
    tv0_end = r.DateField(\
            'TimeV0 Until :', widget=r.DatePickerWidget(),\
            format='%m/%d/%Y',\
            default=datetime.date.today()+\
            datetime.timedelta(hours=23,minutes=59,seconds=59))
    query_limit = r.IntegerField('Query Limit :',validators=\
            [r.InputRequired(),r.NumberRange(min=0)],default=0)

    def getrawquery(self):
        rawquery = StandardLog.query

        if(self.tv0_ignore.data == "0"):
            rawquery = rawquery.filter( StandardLog.timev0 >=\
                    self.tv0_start.data )
            rawquery = rawquery.filter( StandardLog.timev0 <=\
                    self.tv0_start.data + datetime.timedelta(days=1))

        if(self.query_limit.data > 0 ):
            rawquery = rawquery.limit(self.query_limit.data)

        return rawquery


# LS FORMS MAY ALSO ALLOW rgensel!
#import pkg.resrc.rstruct as rstruct
#class LsForm(r.FlaskForm):
#
#
#    branch = r.NonValidatingSelectField("Branch",choices=[(0,"All Branches"),\
#        (1,"Branch 1 (G-SENSOR)"),(2,"Branch 2 (G-SENSOR)"),\
#        (3,"Branch 3 (P-RADAR)"),(4,"Branch 4 (P-RADAR)")])
#    rgensel_rpi_id = r.NonValidatingSelectField("Box Name",choices=['0','NA'])
#    query_limit = r.IntegerField('Query Limit :',validators=\
#            [r.InputRequired(),r.NumberRange(min=0)],default=0)
#
#    fKeylist = {"rpi_id":("Segment_Hosts","sn_name")}
#
#    def getrawlist(self):
#
#        rawlist = GFElement.query
#
#        if( int(self.branch.data) > 0):
#            rawlist = rawlist.filter( GFElement.branch_n == self.branch.data )
#
#        if( self.rgensel_rpi_id.data != rstruct.rlin_nullk ):
#            rawlist = rawlist.filter( GFElement.rpi_id == self.rgensel_rpi_id.data )
#
#        if(self.query_limit.data > 0):
#            rawlist = rawlist.limit( self.query_limit.data)
#
#        rawlist = rawlist.all()
#
#        return rawlist

