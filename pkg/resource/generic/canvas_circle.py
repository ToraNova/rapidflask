#--------------------------------------------------
# canvas_circle.py
# This is a generic class for a canvas paint circle
# A circle consist of it's width, radius and a point
# also contains the color, and the FILL color
# FILL change color (for trig)
# triggering color change
# primarily used for html5 canvas context drawing
# introduced in u3
# ToraNova
#--------------------------------------------------

from pkg.resource import res_import as r

class CanvasCircle(r.Base):
    # PERMA : DO NOT CHANGE ANYTHING HERE UNLESS NECESSARY
    __tablename__ = "Canvas_Circles"
    id = r.Column(r.Integer, primary_key=True)
    def __repr__(self):
    	return '<%r %r>' % (self.__tablename__,self.id)
    #---------------------------------------------------------

    ######################################################################################################
    # EDITABLE ZONE
    ######################################################################################################
    # TODO: DEFINE LIST OF COLUMNS
    startx = r.Column(r.Integer, nullable=False,unique=False)
    starty = r.Column(r.Integer, nullable=False,unique=False)
    radius = r.Column(r.Integer, nullable=False,unique=False)
    width = r.Column(r.Integer, nullable=False,unique=False)
    color = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=False, unique=False)
    fcolor = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=False, unique=False) #FILL color
    tcolor = r.Column(r.String(r.lim.MAX_UUPARAM_SIZE), nullable=False, unique=False) #Trig color

    # rlinking - do not have to change the variable name

    # TODO: DEFINE THE RLIST
    #The following is for r-listing (resource listing)
    # the values in the rlist must be the same as the column var name
    rlist = {
    "startx":"startx",
    "starty":"starty",
    "radius":"radius",
    "width":"width",
    "defcolor":"color",
    "fillcolor":"fcolor",
    "trgcolor":"tcolor"# __link__ is a reserved keyword
    } #header:row data
    # use the __link__/ and __ route_id to 'link' route_id onto something
    # the linkage is defined under the rlink dictionary down there
    # see 'RLINK'

    # TODO: DEFINE THE priKey and display text
    #this primary key is used for rlisting/adding and mod.
    rlist_priKey = "id"
    rlist_dis = "Canvas Lines" #display for r routes

    #RLINK - indicate a link (foreign key reference lookup)
    #rlink - ref tablename, fkey, lookup
    #the key defines how a column is linked, route_id is linked
    #to the table Georoute, looking up for the ID in Georoute and retrieving
    #the name.

    # TODO: CONSTRUCTOR DEFINES, PLEASE ADD IN ACCORDING TO COLUMNS
    # the key in the insert_list must be the same as the column var name
    def __init__(self,insert_list):
        self.startx = insert_list["startx"]
        self.starty = insert_list["starty"]
        self.radius = insert_list["radius"]
        self.width = insert_list["width"]
        self.color = insert_list["color"]
        self.tcolor = insert_list["tcolor"]
        self.fcolor = insert_list["fcolor"]
    ######################################################################################################
