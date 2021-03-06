#--------------------------------------------------
# auth.py
# this file is meant to store routes for authentication
# purposes such as login/logout or any other administr
# tasks
# introduced 8/12/2018
#--------------------------------------------------

#security and login imports
from flask_login import login_required, login_user, current_user, logout_user

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

# for live logins view
from pkg.iface import sockemit

import pkg.const as const
import pkg.limits as limits
from pkg.system import assertw as a
from pkg.system.database import dbms
from pkg.system.user import models as md
from pkg.system.user import forms as fm
from pkg.system.servlog import srvlog,logtofile

import random,string,os

# primary blueprint
bp = Blueprint('auth', __name__, url_prefix='')

#######################################################################################################
# Routing section
#######################################################################################################
@bp.route('/login', methods=['GET','POST'])
def login():
    userlogin_form = fm.LoginForm()
    if userlogin_form.validate_on_submit():
        target_user = md.System_User.query.filter(md.System_User.username == userlogin_form.username.data).first()
        if(target_user == None):
            #user does inexistent
            return render_template("errors/invalid_login.html",
            display_message="User does not exist!")
        else:
            if( target_user.check_password(userlogin_form.password.data)):
                #successful login
                srvlog["user"].info(userlogin_form.username.data+" logged onto the system") #logging
                login_user(target_user)#login_manager logins

                #logs it to the livelog monitor
                sockemit("/sysutil","livelog_cast",\
                        {
                            'logtype':'logins',
                            'logstring':'{} ({}) Logon to server.'.format(target_user.username,\
                                target_user.getUserType())
                        })

                return redirect(url_for("home.home",username=target_user.username))
            else:
                #incorrect password
                return render_template("errors/invalid_login.html",
                display_message="Invalid password")
    return render_template('standard/login.html',form=userlogin_form)

@bp.route('/logout')
@login_required
def logout():
    logout_username = current_user.username
    logout_usertype = current_user.getUserType()
    logout_user()
    #logs it to the livelog monitor
    sockemit("/sysutil","livelog_cast",\
            {
                'logtype':'logins',
                'logstring':'{} ({}) Logoff from server.'.format(logout_username,\
                        logout_usertype)
            })
    srvlog["user"].info(logout_username+" logged out the system") #logging
    return redirect(url_for("auth.login"))

@bp.route("/generate/token/<issue>/<param>",methods=['GET','POST'])
@a.admin_required
def tokengen(issue,param):

    issuemap = {
    "register":[request.form.get("usertype"),const.TOKN_SYS],
    "pwreset":[param,const.TOKN_SYS]
    }
    tokdir = issuemap[issue][1]
    uuid = issuemap[issue][0]

    while(True):
    #generate until unique
        rngstr = [ random.choice( string.ascii_uppercase + string.digits + string.ascii_lowercase ) \
                for i in range(limits.TOKEN_LENGTH) ]
        tokenstr = (uuid+'%'
            +''.join(rngstr))
        # The following works for python3.6x only
        #tokenstr = (uuid+'%'
        #    +''.join(random.choices(string.ascii_uppercase + string.digits, k=limits.TOKEN_LENGTH)))
        if(not os.path.isfile(os.path.join(const.TOKN_DIR,tokdir,tokenstr))):
            #non existent
            break

    tokenfile = open(os.path.join(const.TOKN_DIR,tokdir,tokenstr),"w") #creates the token file
    tokenfile.close()
    out = url_for('sysnologin.'+issue)+'?token='+tokenstr
    return render_template("standard/message.html",
    display_title="Token generation complete",
    display_message="Please use the following url (right click, copy link location)",
    display_url=out)

def removeTokenFile(tokendir,token):
    if(os.path.isfile(os.path.join(const.TOKN_DIR,tokendir,token))):
        os.remove(os.path.join(const.TOKN_DIR,tokendir,token))

def sysuser_getobj(id):
	return md.System_User.query.filter(md.System_User.id == id).first()
