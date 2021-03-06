#--------------------------------------------------
# assert.py
# this file aims to provide wrapper functionality
# for some routes
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
import pkg.limits as limits
from pkg.system import assertw as a
from pkg.system.database import dbms
from pkg.msgapi.models import Msgapi_User
from pkg.system.servlog import srvlog,logtofile

from functools import wraps
import os

##############################################################################################
# Wrappers
##############################################################################################
def admin_required(fn):
    '''used for path that requires the highest
    privelege level only, equivalent to
    userpriv_required(0)'''
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if (not current_user.is_authenticated):
            return logandDisplay("Unauthenticated access",\
                    "Unauthenticated. Please login first !")
        elif ( current_user.getPriLevel() != 0 ):
            return render_template("errors/error.html",
                username=current_user.username,
                error_title="Unauthorized",
                error_message="You are not authorized to access this content.")
            #abort(401) #throw unauthorized_request 401'
        else:
            #here if user is admin and already logged in
            return fn(*args, **kwargs)
    return decorated_view

def userpriv_required(level):
    '''used to wrap for a path that
    requires a certain user privelege level
    e.g @userpriv_required(0) means admin or above required
    @userpriv_required(3) so only users with privlevel 3,2,1
    and 0 can access to that route'''
    def outer_dec(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if (not current_user.is_authenticated):
                return logandDisplay("Unauthenticated access",\
                        "Unauthenticated. Please login first !")
            elif ( current_user.getPriLevel() > level ):
                return render_template("errors/error.html",
                    username=current_user.username,
                    error_title="Unauthorized",
                    error_message="You are not authorized to access this content.")
                #abort(401) #throw unauthorized_request 401'
            else:
                #here if user is admin and already logged in
                return fn(*args, **kwargs)
        return decorated_view
    return outer_dec

def token_check(fn):
    '''this wrapper checks if the token exist, deletes it if it does and allow
    entry to the route, else, it denies entry and logs the incident'''
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if ( "token" not in request.args):
            return logandDisplay("Invalid token attempt",\
                    "Unauthorized, please contact administrator.")
        else:
            #check if token is valid
            if(os.path.isfile(os.path.join(const.TOKN_DIR,\
                const.TOKN_SYS,request.args.get("token")))):
                #token exists
                return fn(*args, **kwargs) #allow access
            else:
                return logandDisplay("Invalid token attempt",\
                        "Unauthorized, please contact administrator.")
    return decorated_view

def route_disabled(fn):
    #disable if DISABLE_CRIT_ROUTE from CONST is set to TRUE
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if (const.DISABLE_CRIT_ROUTE):
            abort(404)
        return fn(*args, **kwargs)
    return decorated_view

def AKEY_checker(fn):
    '''This wrapper checks if the access key entered is correct,
    this is for HTTPv0 APIs only !'''
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if ('akey' not in request.args):	 # get and check key
            return "Incorrect API call",404
        # obtain list of http api users
        htpu = Msgapi_User.query.filter( Msgapi_User.usertype == "HTTPv0" ).all()
        klist = [ mu.access_key for mu in htpu ]
        if( request.args.get('akey') not in klist ):
            return "Incorrect Key",400
        return fn(*args,**kwargs)
    return decorated_view

def ID_checker(fn):
    @wraps(fn)
    def decorated_view(*args,**kwargs):
        if('f0' not in request.args): 	  #f0 stores the ID for the client
            #this function may be disabled if client uses FIXED IP
            return "f0 unspecified",1 		
        return fn(*args,**kwargs)
    return decorated_view

def Localhost_only(fn):
    @wraps(fn)
    def decorated_view(*args,**kwargs):
        if(request.remote_addr != '127.0.0.1'): #only allows localhost access
            return "localhost access only",1
        return fn(*args,**kwargs)
    return decorated_view


##############################################################################################
# Helper func
##############################################################################################

def logandDisplay(logtitle,display_msg):
    '''using errors/unauthorized, logs and display the error msg'''
    srvlog["sys"].warning(logtitle+" from "+request.remote_addr) #logging
    return render_template("errors/unauthorized.html",
            display_message=display_msg)
