#--------------------------------------------------
# fsqlite.py
# this file is static and should not be tampered with
# it initializes the required models for the database engine
# introduced 8/12/2018
#--------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pkg.const as const

# Necessary imports on local package
from pkg.system.database.structure import DBstruct, DBMS, create_db, remove_db

#configuration necessities
#fixed prefix on database filename : 'sqlite:///<filename>'
#3 slashes are necessary

# TODO: must return a db struct type that consist of base,session and the dbfile
# Please implement this for all db systems
def constrEngine(dbfile):
    engine = create_engine('sqlite:///'+dbfile,convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
    base = declarative_base()
    base.query = session.query_property()
    return DBstruct(engine, base, session, dbfile )

# the dbms object is the most important element, please declare and fill it correctly
dbms = DBMS( 
        constrEngine( const.DB00_NAME ),
        constrEngine( const.DB01_NAME ),
        constrEngine( const.DB02_NAME )
        )

def init_db(system=False,deploy=False,msgapi=False):
    #call this during first init (full reset)
    create_db(dbms, system,deploy,msgapi )

def reset_db(system=False,deploy=False,msgapi=False):
    remove_db(dbms, system,deploy,msgapi )
    create_db(dbms, system,deploy,msgapi )

def delete_db(system=False,deploy=False,msgapi=False):
    remove_db(dbms, system,deploy,msgapi )
