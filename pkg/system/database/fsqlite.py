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

    from pkg.system.user.defaults import default_add
    default_add() # adds the default system users (and configuration)
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
    '''this is called when we want to update our system database'''
    #-----------------------PERMA MODELS-------------------------------------
    from pkg.system import sdef #sdef is for perma imports (system)
    Base0.metadata.create_all(bind=engine_sys)
    #------------------------------------------------------------------------

def update_meta():
    '''this is called when we want to update our deployment database'''
    #-----------------------Non PERMA----------------------------------------
    from pkg.resource import rdef #rdef is for deployment dependent resources
    Base1.metadata.create_all(bind=engine_dep)
    #------------------------------------------------------------------------
