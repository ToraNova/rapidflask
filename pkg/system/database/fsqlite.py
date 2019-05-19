#--------------------------------------------------
# fsqlite.py
# this file is static and should not be tampered with
# it initializes the required models for the database engine
# introduced 8/12/2018
#--------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pkg.system.servlog import srvlog,logtofile
import pkg.const as const
import os

#configuration necessities
#fixed prefix on database filename : 'sqlite:///<filename>'
#3 slashes are necessary

#sy_session is the system engine
engine_sys = create_engine('sqlite:///'+const.DB00_NAME,convert_unicode=True)
sy_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine_sys)) 
#use Base0 to declare new models that are permanent with the system
Base0 = declarative_base()
Base0.query = sy_session.query_property()

#db_session is the deploy engine
engine_dep = create_engine('sqlite:///'+const.DB01_NAME,convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine_dep)) 
#use Base1 to declare new models that are permanent with the system
Base1 = declarative_base()
Base1.query = db_session.query_property()

def init_db():
    #call this during first init (full reset)
    delete_db(True,True,True)
    update_sys()
    update_meta()

    from pkg.system.database.defaults import default_add
    default_add()
    tokenfile = open(os.path.join(const.TOKN_DIR,"init.token"),"w+")
    tokenfile.close()
    return

def delete_db(sys=False,deploy=False,token=False):
    # deletes both dbs
    if(os.path.isfile( os.path.join(const.TOKN_DIR,"init.token")) and token):
        os.remove( os.path.join(const.TOKN_DIR,"init.token"))
    if(os.path.isfile(const.DB00_NAME) and sys):
        srvlog["sys"].warning("Deleting "+const.DB00_NAME)
        os.remove(const.DB00_NAME)
        sy_session.remove()
    if(os.path.isfile(const.DB01_NAME) and deploy):
        srvlog["oper"].warning("Deleting "+const.DB01_NAME)
        os.remove(const.DB01_NAME)
        db_session.remove()

def reset_db():
    delete_db( deploy=True ) 
    #reset the meta db (for deployment database only)
    update_meta()
    return

def update_sys():
    #-----------------------PERMA MODELS-------------------------------------
    from pkg.system.database.models import System_User #perma
    from pkg.system.database.models import System_Configuration #perma
    from pkg.system.database.models import System_UserType #perma
    #------------------------------------------------------------------------

    Base0.metadata.create_all(bind=engine_sys)

def update_meta():
    #this is called when we want to change our db
    #NOTE please add imports of new models here
    #as of u6 - r, just import rdef here
    #-----------------------Non PERMA----------------------------------------
    from pkg.resource import rdef
    #------------------------------------------------------------------------

    Base1.metadata.create_all(bind=engine_dep)
