#--------------------------------------------------
# models.py
# this file contains the class definition
# (i.e) the columns are class attributes
# specifically for the database (sqlite3)
# created 8/12/2018
# u2 : PLEASE DO NOT APPEND TO THIS FILE !
# u2 : THIS FILE IS NOW ONLY MEANT FOR PERMANENT MODELS!
# ToraNova
#--------------------------------------------------

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from pkg.system.database import dbms
Base = dbms.Base0
from pkg import limits as lim     #lim dependency
from pkg import const as c
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime #u7

###############################################################################
#   System Permanent models
#   these models are used throughout all deployment of pyFlask server.
#   PLEASE DO NOT ADD RESOURCE MODELS HERE ! THEY ARE NOW MOVED TO THE RESOURCE
#   DIRECTORY UNDER pkg/resource. ADD A NEW FILE FOR ANY NON-PERMA MODELS THERE!
#   this model is imported directly onto fsqlite, likewise, resource models
#   added under resource must also be added there, but please split them up
#   so that we know which is permanent and deployment based.
###############################################################################

class System_User(Base, UserMixin):#This class is permanent in almost all pyFlask deployment
    #System_User is a mandatory class in any pyFlask system
    #This class stores information on the user which will access the system,
    #Examples of instances of this class are admin, user01, human_resource ...
    __tablename__ = "System_User"
    id = Column(Integer, primary_key=True)
    username = Column(String(lim.MAX_USERNAME_SIZE),unique=True,nullable=False)
    passhash = Column(String(lim.MAX_PASSWORD_SIZE),unique=False,nullable=False)
    usertype = Column(Integer(),unique=False,nullable=False) #refers to a userType
    creadate = Column(DateTime()) #date of user account creation

    def __init__(self,a_username = None,a_password = None,a_usertype = 10): #by default it is a guess account
        self.username = a_username
        self.set_password(a_password)
        self.usertype = a_usertype
        self.creadate = datetime.datetime.now()

    def set_password(self,password):
        self.passhash = generate_password_hash(password, method=c.HASH_ALGORITHM_0)

    def check_password(self,password):
        return check_password_hash(self.passhash,password)

    def getPriLevel(self):
        '''obtains the user privilege level'''
        t = System_UserType.query.filter(System_UserType.id == self.usertype).first()
        if(t == None):
            return 9
        else:
            return t.prilevel

    def getUserType(self):
        '''obtains the user type'''
        t = System_UserType.query.filter(System_UserType.id == self.usertype).first()
        if(t == None):
            return "N/A"
        else:
            return t.typename

    def __repr__(self):
        return '<%r %r %r>' % (self.__tablename__,self.username,self.adminpri)

class System_UserType(Base):
    __tablename__ = "System_UserType"
    id = Column(Integer, primary_key=True)
    prilevel = Column(Integer(),unique=False,nullable=False) #specify a privilege level
    #the privilege level is defined with 0 being the administrator (highest privilege)
    #and 9 being the lowest privilege level (non-login/guest account)
    typename = Column(String(lim.MAX_USERNAME_SIZE),unique=True,nullable=False)#the unique
    #typename of a user, e.g, admin, user, driver, teacher, student ...

    def __init__(self,a_typename = None,a_prilevel = None):
        self.typename = a_typename
        self.prilevel = a_prilevel

    #---------------------------------------------------------------------------
    #------PLEASE UPDATE THE FORMS UPON UPDATING THIS REFERENCE!! -u4
    # ('0','0:Administrator (Highest Privilege)'),
	# ('1','1:Can view/add all resources/operation without restrictions'),
	# ('2','2:Can view all resources/operation'),
	# ('3','3:Can view some resources/operation'),
	# ('4','4:Unimplemented'),
	# ('5','5:Unimplemented'),
	# ('6','6:Unimplemented'),
	# ('7','7:Unimplemented'),
	# ('8','8:Unimplemented'),
	# ('9','9:Guest Accounts/Visitors (Lowest Privilege)')
    #----------------------------------------------------------------------------

    def __repr__(self):
        return '<%r %r>' % (self.__tablename__,self.id)

class System_Configuration(Base):#This class is permanent in almost all pyFlask deployment
    #System_Configuration is a mandatory class in any pyFlask system
    #This class stores configurations of the system,
    #Examples of instances of this class are ipaddr, port, server_id ...
    __tablename__ = "System_Config"
    id = Column(Integer,primary_key=True)
    config_name = Column(String(lim.MAX_CONFIG_NAME_SIZE), unique=True,nullable=False)
    config_value = Column(String(lim.MAX_CONFIG_VALU_SIZE), unique=True,nullable=False)

    rlist_col = ["Configuration Name","Configuration Value"] #header
    rlist_dat = ['config_name','config_value'] #row data
    rlist_dis = "Local Configuration" #display

    def __init__(self,a_config_name,a_config_value):
        self.config_name = a_config_name
        self.config_value = a_config_value

    def __repr__(self):
        return '<%r %r>' % (self.__tablename__,self.id)
