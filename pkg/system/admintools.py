#--------------------------------------------------
# admintools.py
# this file contains functions and routes
# for admin usage
# introduced 8/12/2018
# removed the useradd route from this file, migrated to sysuser under user (u4)
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask security import
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
import pkg.limits as limits
from pkg.system import assertw as a
from pkg.system.database import dbms
from pkg.system.user import models as md
from pkg.system.user import forms as fm
from pkg.system.servlog import srvlog,logtofile

from pkg.system.user.sysuser import tupleGenerator

#additional overheads
import os

bp = Blueprint('admintools', __name__, url_prefix='/admintools')

##############################################################################################
# nologin routes (requires no login) PLEASE REFRAIN IN ACTUAL DEPLOYMENT SERVERS
##############################################################################################
@bp.route('/nologin',methods=['GET','POST'])
@a.route_disabled #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
def useradd_nologin():#This function is for initial server initialization only,
	#NOT RECOMMENDED FOR ACTUAL USE DUE TO SECURITY ISSUE
    '''Adds a user into system using admintools, no checking is done
    Use only in initial deployment phase, please switch off the routes
    regarding this one it is done. returns 0 on success and 1 on fail'''
    useradd_form = fm.System_User_RegisterForm()
    useradd_form.usertype.choices = tupleGenerator( md.System_UserType.query.all() )
    if useradd_form.validate_on_submit():
        try:
            target_add = md.System_User(
                useradd_form.username.data,useradd_form.password.data,useradd_form.usertype.data)#create user obj
            dbms.sy_session.add(target_add)#adds user object onto database.
            dbms.sy_session.commit()
            srvlog["sys"].warning(useradd_form.username.data+ " registered under admintools/nologin ! type="+useradd_form.usertype.data) #logging
            return "admintools : ok" #TODO return a webpage
        except Exception as e:
            dbms.sy_session.rollback() #rollback errors
            print("[ER]",__name__," Exception has occurred:",str(e))
            srvlog["sys"].warning("Sysuseradd/nologin with exception "+str(e)) #logging
            return "admintools : failed"
    return render_template('admintools/sysuseradd.html',form=useradd_form)

@bp.route('/totalreset')
@a.route_disabled #disable if DISABLE_CRIT_ROUTE from const is set to True
@a.admin_required
def totalreset():
    #NOT RECOMMENDED FOR ACTUAL USE DUE TO SECURITY ISSUE
    '''resets the the database system (both sys and deployment)
    and recreate with items only in default adds
    DO NOT USE DURING DEPLOYMENT'''
    try:
        dbms.init_db()
        print("[IF]",__name__," Total Database reset.")
        srvlog["sys"].warning("Database total reset under admintools/totalreset") #logging
        return render_template("standard/message.html",
            display_title="Admintools (TotalReset)",
            display_message="OK")
    except Exception as e:
        print("[ER]",__name__," Exception has occurred:",str(e))
        srvlog["sys"].warning("Database total reset with exception "+str(e)) #logging
        return render_template("errors/error.html",
            error_title="Admintools (TotalReset)",
            error_message="Failed:"+str(e))

@bp.route('/resetdb')
@a.route_disabled #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
@a.admin_required
def resetdb():
    #NOT RECOMMENDED FOR ACTUAL USE DUE TO SECURITY ISSUE
    '''resets the deploy database with some default adds defined
    DO NOT USE DURING DEPLOYMENT'''
    try:
        dbms.reset_db()
        print("[IF]",__name__," Database reset.")
        srvlog["sys"].warning("Deployment resource (deploy.db) reset under admintools/resetdb") #logging
        return render_template("standard/message.html",
            display_title="Admintools (DB Reset)",
            display_message="OK")
    except Exception as e:
        print("[ER]",__name__," Exception has occurred:",str(e))
        srvlog["sys"].warning("Deployment resource (deploy.db) reset with exception "+str(e)) #logging
        return render_template("errors/error.html",
            error_title="Admintools (DB Reset)",
            error_message="Failed:"+str(e))

##############################################################################################
# Logging routes (display server logs)
# ported from old pyflask project : update4
##############################################################################################
@bp.route('/logs/<logtype>')
@a.admin_required
def logview(logtype):
    #Display logs on the local server
    filebuff = []
    with open( os.path.join(const.LOGS_DIR,logtofile[logtype]) ,'r' ) as f:
        #opens the logfile of required logtype for reading
        for line in f:
            filebuff.append(line)
        if(len(filebuff) == 0):
            filebuff = ["Empty, No logs at the moment"]
        return render_template("admintools/logging.html",logfile = filebuff)

##############################################################################################
# Live Logs (in conjunction with flask_socketio)
# Introduced update7
##############################################################################################
@bp.route('/logs/live/<logtype>')
@a.admin_required
def livelogview(logtype):
    #Allow viewing of live logs
    return render_template("flask_sockio/livelogs.html",logtype="logins")
