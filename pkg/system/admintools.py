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
from pkg.system.database import dbcon
from pkg.system.user import models as md
from pkg.system.user import forms as fm
from pkg.system.servlog import srvlog,logtofile
from pkg.system.user.sysuser import tupleGenerator

# Flask mail
from flask_mail import Message

#additional overheads
import os, shutil

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
            dbms.system.session.add(target_add)#adds user object onto database.
            dbms.system.session.commit()
            srvlog["sys"].warning(useradd_form.username.data+ " registered under admintools/nologin ! type="+useradd_form.usertype.data) #logging
            return "admintools : ok" #TODO return a webpage
        except Exception as e:
            dbms.system.session.rollback() #rollback errors
            print("[ER]",__name__," Exception has occurred:",str(e))
            srvlog["sys"].warning("Sysuseradd/nologin with exception "+str(e)) #logging
            return "admintools : failed"
    return render_template('admintools/sysuseradd.html',form=useradd_form)

@bp.route('/resetdb/<octal>')
@a.route_disabled #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
@a.admin_required
def resetdb(octal='000'):
    #NOT RECOMMENDED FOR ACTUAL USE DUE TO SECURITY ISSUE
    '''resets the system/deploy/api database with some default adds defined
    DO NOT USE DURING DEPLOYMENT'''
    # parse the octal
    if( len(octal) < 3 ):
        return render_template("errors/error.html",
            error_title="Database Reset Failed",
            error_message="Invalid Octal Reset Code")
    else:
        sys = True if octal[0] == '1' else False
        dep = True if octal[1] == '1' else False
        api = True if octal[2] == '1' else False
    try:
        dbcon.reset_db(system=sys,deploy=dep,msgapi=api) # Call the reset functionality
        print("[IF]",__name__," Database reset called with octal "+octal)
        if(sys):
            srvlog["sys"].warning("System Database ({}) reset under admintools".format(\
                    dbms.system.dbfile))
        if(dep):
            # deletes all files in the upload directory as well
            try:
                wipe = os.path.join('pkg',const.STD_FILEDIR)
                print("[IF]",__name__," Wiping upload dir: "+wipe)
                shutil.rmtree(wipe)
            except Exception as e:
                # rethrow
                raise e
            finally:
                os.mkdir( wipe )
                gitkeep = open(os.path.join(wipe,".gitkeep"),"w+")
                gitkeep.close()

            srvlog["sys"].warning("Deployment Database ({}) reset under admintools".format(\
                    dbms.deploy.dbfile))
        if(api):
            srvlog["sys"].warning("MSG API Database ({}) reset under admintools".format(\
                    dbms.msgapi.dbfile))
        return render_template("standard/message.html",
            display_title="Admintools (DB Reset)",
            display_message="OK - "+octal)
    except Exception as e:
        print("[ER]",__name__," Exception has occurred:",str(e))
        srvlog["sys"].warning("Database reset "+octal+" with exception "+str(e)) #logging
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
    return render_template("flask_sockio/livelogs.html",logtype="logins",
            socket_io_proto=const.SOCKET_IO_PROTO)


##############################################################################################
# Use to send email to the admin
# Introduced update8
##############################################################################################
@bp.route('/hello')
@a.route_disabled
def hello_admin():
    '''sends a hello email to the the user "admin",
    this is for debugging purposes at the moment u8'''
    msg = Message(\
            subject="Hello!",\
            body="This is an automated email sent by my flask server ! Wormmz",
            sender="submarinechai@gmail.com",\
            recipients=[\
                "chia.jason.col@gmail.com",\
                "chaiyeeting96@gmail.com"
                ])
    from pkg.source import smail
    smail.send( msg )
    return render_template("standard/message.html",
        display_title="Admintools (Test mail)",
        display_message="OK")
