#--------------------------------------------------
# r.py 
# r is a power tool that allows creation of database
# objects. r allows is the framework for object routes
# so users will only need to worry about model definitions
# introduced 8/12/2018
# updated on u8 (20/05/2019)
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask security import
from werkzeug.security import generate_password_hash
from flask_login import current_user,login_required

import pkg.const as const
from pkg.system.database import dbms
from pkg.system import assertw as a
from pkg.system.servlog import srvlog,logtofile

# resource imports
from pkg.resrc.res_import import checkNull
import pkg.resrc.rstruct as rstruct

#r.py (u3) uses the dist dictionary from rdef
#r.py (u8) uses the dicts from ddef, adef and recast as d/a_defines
from pkg.deploy.ddef import r_defines as d_defines
from pkg.msgapi.adef import r_defines as a_defines

# additional overheads
import os
import datetime

# primary blueprint
bp = Blueprint('resrc', __name__, url_prefix='/resrc')

##############################################################################################
# Resource-table # RESOURCES ARE ACTORS/ENTITIES IN THE SYSTEM. TRUCKS, STUDENTS ... etc
# ported from oldpyflask 29/12/2018
##############################################################################################

@bp.route('/radd/<tablename>', methods=['GET','POST'])
@a.admin_required
# The route for resource adding (check fform and fdist)
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def radd(tablename):

        lkup = d_defines # use the deployment lookup
        if lkup[tablename].addform == None:
                return render_template("errors/error.html",
                error_title="Adding Failure",
                error_message="This resource cannot be added manually!")
        resadd_form = lkup[tablename].addform() #creates an ADD FORM

        resadd_form = regenerateForm(resadd_form,lkup,None)
        #resadd_form.process()

        if resadd_form.validate_on_submit():
                d_point = getFormAttrList(resadd_form) #d_point has a dictionary for obj creation
                res_model = lkup[tablename].model
                try:
                        #try to add
                        target_add = res_model(d_point)
                        dbms.deploy.session.add(target_add)
                        dbms.deploy.session.commit()

                        if callable( getattr(target_add, "default_add_action", None) ):
                                try:
                                        target_add.default_add_action()
                                except Exception as e:
                                        dbms.deploy.session.rollback()
                                        dbms.msgapi.session.rollback()
                                        raise ValueError(tablename,"default_add_action",str(e))

                        return render_template("standard/message.html",
                display_title="Success",
                display_message="Added resource to system.")
                except Exception as e:
                        print("radd exception has occurred :",str(e))
                        dbms.deploy.session.rollback() #immediately rollback changes
                        return render_template("errors/error.html",
            error_title="Failure (Key Error?)",
            error_message=str(e))

        return render_template('res/radd0.html',
        form = resadd_form, tablename=tablename)

@bp.route('/rlist/<tablename>',methods=['GET','POST'])
@login_required
# The route for resource listing
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rlist(tablename):
        lkup = d_defines # use the deployment lookup
        mobj = getMatch(lkup,tablename)
        columnHead = mobj[0]
        match = mobj[1]
        prikey_match = mobj[2]
        display_tablename = lkup[tablename].model.rlist_dis
        return render_template('res/datalist0.html',
        colNum=len(columnHead),matches=match,columnHead=columnHead, tablename=tablename,
        prikeyMatch=prikey_match,
        data_table_name=display_tablename)

@bp.route('/rmod/<tablename>/<primaryKey>',methods=['GET','POST'])
@a.admin_required
# The route for resource modification.
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rmod(tablename,primaryKey):
        lkup = d_defines #use the deployment lookup
        if(lkup[tablename].editform == None):
                #edits disabled
                return render_template("errors/error.html",
                error_title="Modify Failure",
                error_message="This resource cannot be modified!")
        elif(lkup[tablename].editform == rstruct.del_only):
                #delete only
                pass
        else:
                rmod_form = lkup[tablename].editform() #generates the edit form

        if(request.method=="POST"):
                res_model = lkup[tablename].model
                if(request.form["button"]=="Delete"):
                        #DELETION PROCEDURE
                        target_del =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) == primaryKey ).first()

                        if callable( getattr(target_del, "default_del_action", None) ):
                                try:
                                        target_del.default_del_action()
                                except Exception as e:
                                        dbms.deploy.session.rollback()
                                        dbms.msgapi.session.rollback()
                                        raise ValueError(tablename,"default_del_action",primaryKey,str(e))

                        dbms.deploy.session.delete(target_del)
                        dbms.deploy.session.commit()
                        return redirect(url_for('resource.rlist',tablename=tablename))

                elif(request.form["button"]=="Modify"):

                        if(lkup[tablename].editform == rstruct.del_only):
                                return render_template("errors/error.html",
                                error_title="Modify Failure",
                                error_message="This resource can only be deleted!")

                        target_mod =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) == primaryKey).first()
                        #target_mod is the resource entity that we wish to edit
                        rmod_form = regenerateForm(rmod_form,target_mod)

                        rmod_form.process()
                        return render_template('res/rmod0.html',
                        primaryKey=primaryKey,tablename=tablename,form=rmod_form)

                elif(request.form["button"]=="Submit Changes"):
                        if rmod_form.validate_on_submit():
                                target_mod =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) == primaryKey).first()
                                d_point = getFormAttrList(rmod_form) #d_point has a dictionary for obj modification
                                for f,val in  d_point.items():
                                        target_mod.__setattr__(f,val)

                                if callable( getattr(target_mod, "default_mod_action", None) ):
                                        try:
                                                target_mod.default_mod_action()
                                        except Exception as e:
                                                dbms.deploy.session.rollback()
                                                dbms.msgapi.session.rollback()
                                                raise ValueError(tablename,"default_mod_action",primaryKey,str(e))

                                dbms.deploy.session.add(target_mod)
                                dbms.deploy.session.commit()
                                return redirect(url_for('resource.rlist',tablename=tablename))
                else:
                        abort(404)
        else:
                abort(400)

##############################################################################################
# Auxiliary methods, these methods aid the generelization of resource models/forms
##############################################################################################
def getMatch(rstype,tablename):
        '''obtains matching columns and data of a specific table
        updated on u3 compared to r9. now supports a cleaner model side requirement'''
        entityClass = rstype[tablename].model
        reslist = entityClass.rlist # the rlist element
        rawlist = entityClass.query.all() # all the records
        columnHead = []
        match = []
        pkey = []
        for key,val in reslist.items():
                columnHead.append(key) #adds keys in rlist dictionary to columnHeads

        for entry in rawlist:
                temp = []
                for key in reslist:
                        coltmp = {"meta":"text"}
                        if(reslist[key].startswith("__link__")):
                                try:
                                        rkey = reslist[key].split('/')[1]
                                        refTable = reslist[key].split('/')[2]
                                        refFKey = reslist[key].split('/')[3]
                                        refFKey = refFKey[:refFKey.find(':')]
                                        refLook = reslist[key].split(':')[1]
                                        refEntClass = rstype[refTable].model
                                        if(entry.__getattribute__(rkey) != None):
                                                coltmp["data"] = refEntClass.query.filter(
                                                        getattr(refEntClass,refFKey) ==
                                                        entry.__getattribute__(rkey)
                                                ).first().__getattribute__(refLook)
                                        else:
                                                coltmp["data"] = "Unlinked"
                                except Exception as e:
                                        #revert to simple display of id
                                        #error must have occured here
                                        # TODO: Logging
                                        print("Exception occurred while rlisting with __link__ :",str(e))
                                        try:
                                                coltmp["data"] = entry.__getattribute__(rkey)
                                        except Exception as e:
                                                coltmp["data"] = "err:__link__ "+str(e)

                        elif(reslist[key].startswith("__time__")):
                                # For formatting of time fields
                                try:
                                        tformat = reslist[key].split('/')[1]
                                        timedat = reslist[key].split('/')[2]
                                        if( entry.__getattribute__(timedat) != None ):
                                                coltmp["data"] = entry.__getattribute__(timedat).strftime(tformat)
                                        else:
                                                coltmp["data"] = "Null (No data)"
                                except Exception as e:
                                        print("Exception occurred while rlisting with __time__ :",str(e))
                                        try:
                                                coltmp["data"] = entry.__getattribute__(timedat)
                                        except Exception as e:
                                                coltmp["data"] = "err:__time__ "+str(e)

                        elif(reslist[key].startswith("__url__")):
                                try:
                                        urltarget = reslist[key].split('/')[1]
                                        urlparam = reslist[key].split('/')[2]
                                        if( entry.__getattribute__(urlparam) != None ):
                                                coltmp["meta"] = "url"
                                                coltmp["data"] = url_for(urltarget,urlparam=entry.__getattribute__(urlparam))
                                        else:
                                                coltmp["data"] = "Null (No data)"
                                except Exception as e:
                                        print("Exception occurred while rlisting with __url__ :",str(e))
                                        try:
                                                coltmp["data"] = entry.__getattribute__(urlparam)
                                        except Exception as e:
                                                coltmp["data"] = "err:__url__ "+str(e)

                        else:
                                coltmp["data"] = entry.__getattribute__(reslist[key])

                        #print(temp[-1]) #DEBUGGING USE ONLY
                        temp.append(coltmp)
                match.append(temp)
                pkey.append(entry.__getattribute__(entry.__getattribute__('rlist_priKey')))
        return [columnHead,match,pkey]

def getAttrList(in_obj):
        '''returns a list of attributes of an object, not including
        methods and intrinsic attribute another model of this is under
        auxtools in libraries/python/pymod'''
        out = []
        for a in dir(in_obj):
                if not a.startswith('__') and not callable(getattr(in_obj,a)):
                        out.append(a)
        return out

def getFormAttrList(form_obj):
        '''returns the data of a form. the keyword is rgen_
        it returns a dictionary with the attribute name striped of rgen_
        as the key and value of the actual data'''
        out = {}
        for a in dir(form_obj):
                if a.startswith(rstruct.rgen_keyword):
                        out[a[len(rstruct.rgen_keyword):]]=form_obj.__getattribute__(a).data
                elif a.startswith(rstruct.rgen_selkey):
                        out[a[len(rstruct.rgen_selkey):]]=form_obj.__getattribute__(a).data
                elif a.startswith(rstruct.rgen_timkey):
                        out[a[len(rstruct.rgen_selkey):]]=form_obj.__getattribute__(a).data
                elif a.startswith(rstruct.rgen_actkey):
                        form_action = form_obj.__getattribute__(a[len(rstruct.rgen_actkey):])
                        if callable( form_action ):
                                out.update( form_action( form_obj ) )

        return out

def regenerateForm(in_form,lkup,target=None):
        for a in dir(in_form): #for all form attributes
                if a.startswith(rstruct.rgen_keyword) and target != None: #only the ones defined under rgen
                        model_field = a[len(rstruct.rgen_keyword):] #FOR MODIFY ONLY
                        in_form.__getattribute__(a).default = target.__getattribute__(model_field)
                elif a.startswith(rstruct.rgen_selkey):
                        model_field = a[len(rstruct.rgen_selkey):] #GETS THE MODEL FIELD
                        fkeyres = lkup[in_form.fKeylist[model_field][0]].model.query.all()
                        in_form.__getattribute__(a).choices = dynamicSelectorHandler(fkeyres,in_form.fKeylist[model_field][1])
                        if(target != None):
                                in_form.__getattribute__(a).default = target.__getattribute__(model_field)
                elif a.startswith(rstruct.rgen_actkey):
                        pass
        return in_form


def dynamicSelectorHandler(sqlresult,ref_elem):
        '''takes in the sql result, parses the output to allow generation of
        a dynamic WTF select field this takes in a list of 3-tuples, merges
        the last two into a string and spits a list of 2-tuples used together with
        getattr(form,sfield).choices = dynamicSelectorHandler(query_all result,which element)'''
        outList = []
        for elements in sqlresult:
                outList.append((str(elements.__getattribute__(elements.rlist_priKey)),elements.__getattribute__(ref_elem)))

        outList.append((rstruct.rlin_nullk,'No Link'))

        return outList
