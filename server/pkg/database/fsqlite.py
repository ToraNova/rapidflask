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
engine_sys = create_engine('sqlite:///'+const.DB00_NAME,convert_unicode=True)
sy_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine_sys)) #sy_session is the system engine
Base0 = declarative_base()
Base0.query = sy_session.query_property()

engine_dep = create_engine('sqlite:///'+const.DB01_NAME,convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine_dep)) #db_session is the deploy engine
Base1 = declarative_base()
Base1.query = db_session.query_property()

def init_db():
	#call this during first init (full reset)
	if(os.path.isfile(const.DB00_NAME)):
		srvlog["sys"].warning("Deleting "+const.DB00_NAME+" due to init_db call")
		os.remove(const.DB00_NAME)
		sy_session.remove()
	if(os.path.isfile(const.DB01_NAME)):
		srvlog["oper"].warning("Deleting "+const.DB01_NAME+" due to init_db call")
		os.remove(const.DB01_NAME)
		db_session.remove()

	update_sys()
	update_meta()

	from pkg.database.defaults import default_add
	default_add()
	tokenfile = open(os.path.join(const.TOKN_DIR,"init.token"),"w+")
	tokenfile.close()
	return

def reset_db():
	if(os.path.isfile(const.DB01_NAME)):
		srvlog["oper"].warning("Deleting "+const.DB01_NAME+" due to init_db call")
		os.remove(const.DB01_NAME)
		db_session.remove()
	#reset the meta db (for deployment database only)

	update_meta()
	return

def update_sys():
	#-----------------------PERMA MODELS-------------------------------------
	from pkg.database.models import System_User #perma
	from pkg.database.models import System_Configuration #perma
	from pkg.database.models import System_UserType #perma
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
