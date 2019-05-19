#--------------------------------------------------
# sysnologin.py
# introduced u4 - 24/01/2019
# nologin routes for users (registration, pwreset)
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask security import
from flask_login import current_user

import pkg.const as const
from pkg.system.database import dbms
from pkg.system.database import models as md
from pkg.system.database import forms as fm
from pkg.system import assertw as a
from pkg.system.auth import removeTokenFile
from pkg.system.servlog import srvlog,logtofile

bp = Blueprint('sysnologin', __name__, url_prefix='/sysnologin')

##############################################################################################
# system user add/mod routes
# USER REGISTRATION ROUTE (FOR NOLOGIN USE)
# last edit : update4
# THIS URL IS IDEALLY GENERATED BY THE ADMIN, and sent to relevant personnel for registration
##############################################################################################
@bp.route('/register',methods=['GET','POST'])
@a.token_check
def register():
    '''adds a system user onto the system on token auth'''
    typeid = request.args.get("token").split('%')[0]
    form = fm.System_User_URLRegisterForm()
    usertype = md.System_UserType.query.filter(md.System_UserType.id == typeid).first().typename
    if form.validate_on_submit():
        target_user = md.System_User.query.filter(md.System_User.username == form.username.data).first()
        if(target_user == None):
            target_add = md.System_User(form.username.data,form.password.data,typeid)#create user obj
            dbms.sy_session.add(target_add)#adds user object onto database.
            dbms.sy_session.commit()
            removeTokenFile(const.TOKN_SYS,request.args.get("token")) #remove token file
            srvlog["sys"].info(form.username.data+" registered as new user, type="+usertype) #logging
            return render_template("standard/redirect.html",
                display_header="Registration successful",button_string="Back to login",
                display_message="You may now log in to the system.",
                redirect_url=url_for("auth.login"))

        else:
            return render_template("sysuser/urlreg.html",
            typename=usertype,
            warning_string="username already exist !",form=form)

    return render_template("sysuser/urlreg.html",
    typename=usertype,
    warning_string="",form=form,token=request.args.get("token"))

##############################################################################################
# Password Reset
# introduced update4
# used together with tokens
# reset a user's password
##############################################################################################
@bp.route('/pwreset',methods=['GET','POST'])
@a.token_check
def pwreset():
    '''resets a user's password'''
    userid = request.args.get("token").split('%')[0]
    username = md.System_User.query.filter(md.System_User.id == userid ).first().username
    form = fm.System_User_URLPasswordResetForm()
    if form.validate_on_submit():
        target_user = md.System_User.query.filter(md.System_User.id == userid ).first()
        if(target_user == None):
            return render_template("errors/unauthorized.html",
        		display_message="Catastrophic Error, please contact administrator.")
        else:
            target_user.set_password(form.password.data)#edit user password
            dbms.sy_session.add(target_user)#adds user object onto database.
            dbms.sy_session.commit()
            removeTokenFile(const.TOKN_SYS,request.args.get("token")) #remove token file
            srvlog["sys"].info(username+" updated their password") #logging
            return render_template("standard/redirect.html",
                display_header="Password successfully updated",button_string="Back to login",
                display_message="You may now log in to the system.",
                redirect_url=url_for("auth.login"))

    return render_template("sysuser/urlpwr.html",
    username=username,
    warning_string="",form=form,token=request.args.get("token"))