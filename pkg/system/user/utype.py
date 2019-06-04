#--------------------------------------------------
# type.py
# introduced u4 - 24/01/2019
# used for system user type adding (admin use only)
#--------------------------------------------------
#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask security import
from werkzeug.security import generate_password_hash
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
import pkg.limits as limits
from pkg.system import assertw as a
from pkg.system.database import dbms
from pkg.system.user import models as md
from pkg.system.user import forms as fm
from pkg.system.servlog import srvlog,logtofile

bp = Blueprint("sysutype",__name__,url_prefix='')

##############################################################################################
# system user type add/mod routes
# USERTYPE ADD
# u4 - introduced usertype, now dynamically generate choices
##############################################################################################
@bp.route('/utypeadd',methods=['GET','POST'])
@a.admin_required
def utypeadd():
    '''adds a system user type onto the system'''
    typeadd_form = fm.System_UserType_AddForm()
    if typeadd_form.validate_on_submit():
        target_add = md.System_UserType.query.filter(md.System_UserType.typename == typeadd_form.typename.data).first()
        if(target_add == None):
            target_add = md.System_UserType(typeadd_form.typename.data,typeadd_form.prilevel.data)#create usertype obj
            dbms.system.session.add(target_add)#adds usertype object onto database.
            dbms.system.session.commit()
            srvlog["sys"].info(typeadd_form.typename.data+" registered as new type, prilevel="+typeadd_form.prilevel.data) #logging
            return render_template("standard/message.html",
                display_title="Success",
                display_message="Added "+target_add.typename+" usertype into the system.")

        else:
            return render_template("errors/error.html",
            error_title="Failure",
            error_message="Usertype already exists!")

    return render_template('sysuser/typeadd.html',form=typeadd_form)

##############################################################################################
# USER TYPE LIST ROUTE
# introduced on u4
##############################################################################################
@bp.route('/utypelist',methods=['GET','POST'])
@a.admin_required
def utypelist():
    '''list out system user types'''
    columnHead = ["usertype","privelege level"]
    userlist = md.System_UserType.query.all()
    match = []
    for type in userlist:
        temp = [type.typename,type.prilevel]
        match.append(temp)
    return render_template('sysuser/typelist.html',
        colNum=len(columnHead),matches=match,columnHead=columnHead)

##############################################################################################
# USER TYPE MODIFY ROUTE
# introduced on u1
##############################################################################################
@bp.route('/utypemod/<primaryKey>',methods=['GET','POST'])
@a.admin_required
def utypemod(primaryKey):
    '''modify system user type'''
    if(request.method=="POST"):
        if(request.form["button"]=="Delete"):
            target_del = md.System_UserType.query.filter(md.System_UserType.typename == primaryKey).first()
            dbms.system.session.delete(target_del)
            dbms.system.session.commit()
            srvlog["sys"].info(primaryKey+" usertype deleted from the system") #logging
            return redirect(url_for('sysutype.utypelist'))

        elif(request.form["button"]=="Modify"):
            target_mod = md.System_UserType.query.filter(md.System_UserType.typename == primaryKey).first()
            typemod_form = fm.System_UserType_EditForm()
            typemod_form.prilevel.default = str(target_mod.prilevel)
            typemod_form.process()
            return render_template("sysuser/typemod.html",
            primaryKey=primaryKey,form = typemod_form)

        elif(request.form["button"]=="Submit Changes"):
            target_mod = md.System_UserType.query.filter(md.System_UserType.typename == primaryKey).first()
            target_mod.prilevel = request.form.get("prilevel")
            dbms.system.session.add(target_mod)
            dbms.system.session.commit()
            return redirect(url_for('sysutype.utypelist'))

        else:
            abort(404)
    else:
        abort(400)
