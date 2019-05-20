#--------------------------------------------------
# structure.py
# This file is to give a structure and reusable functions
# to other database systems in the app
# introduced 20/05/2019
#--------------------------------------------------

from collections import namedtuple
import pkg.const as const
import os
from pkg.system.servlog import srvlog
# Use to define individual database
DBstruct = namedtuple("DBstruct", ["engine","base","session","dbfile"])

# use to deifne a collective of databases
DBMS = namedtuple("DBMS",["system","deploy","msgapi"])

def delete_file_db( dbstruct ):
    if( os.path.isfile( dbstruct.dbfile )):
        os.remove( dbstruct.dbfile )
        dbstruct.session.remove()
        srvlog["sys"].warning("Deleting "+dbstruct.dbfile)

def remove_db(aDBMS,system=False,deploy=False,msgapi=False,token=True):
    # deletes both dbs
    if(os.path.isfile( os.path.join(const.TOKN_DIR,"init.token")) and token):
        os.remove( os.path.join(const.TOKN_DIR,"init.token"))
    if( system ):
        delete_file_db( aDBMS.system )
    if( deploy ):
        delete_file_db( aDBMS.deploy )
    if( msgapi ):
        delete_file_db( aDBMS.msgapi )

def create_db(aDBMS,system=False,deploy=False,msgapi=False,token=True):
    if(token):
        tokenfile = open(os.path.join(const.TOKN_DIR,"init.token"),"w+")
        tokenfile.close()
    if( system ):
        if( not os.path.isfile( aDBMS.system.dbfile)):
            from pkg.system import sdef
            aDBMS.system.base.metadata.create_all( bind = aDBMS.system.engine )
            srvlog["sys"].info("Creating metadata for SYS Database")
            sdef.default_add() # adds the default system users (and configuration)
    if( deploy ):
        if( not os.path.isfile( aDBMS.deploy.dbfile)):
            from pkg.deploy import ddef
            aDBMS.deploy.base.metadata.create_all( bind = aDBMS.deploy.engine )
            srvlog["sys"].info("Creating metadata for DEP Database")
            ddef.default_add() # adds the default system users (and configuration)
    if( msgapi ):
        if( not os.path.isfile( aDBMS.msgapi.dbfile)):
            from pkg.msgapi import adef
            aDBMS.msgapi.base.metadata.create_all( bind = aDBMS.msgapi.engine )
            srvlog["sys"].info("Creating metadata for API Database")
            adef.default_add() # adds the default system users (and configuration)


