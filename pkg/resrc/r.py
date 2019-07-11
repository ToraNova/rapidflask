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
from flask import request, abort, session
from flask import Blueprint

#flask security import
from werkzeug.security import generate_password_hash
from flask_login import current_user,login_required
from sqlalchemy import text
from sqlalchemy.dialects import sqlite

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
import json

# primary blueprint
bp = Blueprint('resrc', __name__, url_prefix='/resrc')

##############################################################################################
# Resource-table # RESOURCES ARE ACTORS/ENTITIES IN THE SYSTEM. TRUCKS, STUDENTS ... etc
# ported from oldpyflask 29/12/2018
##############################################################################################
def obtain_lkup( dbtype ):
    '''allows use of deploy and msgapi sessions and the r_defines on
    the r methods'''
    if(dbtype=='deploy'):
        return d_defines, dbms.deploy.session

    elif(dbtype=='msgapi'):
        return a_defines, dbms.msgapi.session

    else:
        return None

def rollback_alldb():
    '''rollback all database (for default add/mod/del usecases)'''
    dbms.msgapi.session.rollback()
    dbms.deploy.session.rollback()

def obtain_meta( dbtype ):
    '''allows obtaining of base metadata'''
    if(dbtype=='deploy'):
        return dbms.deploy.metadata
    elif(dbtype=='msgapi'):
        return dbms.msgapi.metadata
    else:
        return None

@bp.route('/radd/<dbtype>/<tablename>', methods=['GET','POST'])
@a.admin_required
# The route for resource adding (check fform and fdist)
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def radd(dbtype,tablename):

    lkup,dbsess = obtain_lkup(dbtype)
    if(lkup is None):
        return render_template("errors/error.html",
        error_title="Lookup Failure",
        error_message="Unknown Database")

    if lkup[tablename].addform is None:
        return render_template("errors/error.html",
        error_title="Adding Failure",
        error_message="This resource cannot be added manually!")

    # FORM GENERATION
    resadd_form = lkup[tablename].addform() #creates an ADD FORM
    resadd_form = regenerateForm(lkup,resadd_form,None)
    #resadd_form.process()

    if resadd_form.validate_on_submit():
        d_point = getFormAttrList(resadd_form) #d_point has a dictionary for obj creation
        res_model = lkup[tablename].model
        try:
            #try to add
            target_add = res_model(d_point)
            dbsess.add(target_add)
            dbsess.commit()

            if callable( getattr(target_add, "default_add_action", None) ):
                try:
                    target_add.default_add_action()
                except Exception as e:
                    rollback_alldb()
                    # rethrow the exception
                    raise ValueError(tablename,"default_add_action",str(e))

            return render_template("standard/message.html",
                display_title="Success",
                display_message="Added resource to system.")
        except Exception as e:
            dbsess.rollback() #immediately rollback changes
            print("[EX]",__name__," : ",dbtype,tablename,"radd exception has occurred :",str(e))
            srvlog["oper"].error( "{}/{} radd failed with exception : {}".format(dbtype,tablename,str(e)))
            return render_template("errors/error.html",
                error_title="Failure (Key Error?)",
                error_message=str(e))

    return render_template('res/radd0.html',
    form = resadd_form, dbtype = dbtype,tablename=tablename)

@bp.route('/rlist/<dbtype>/<tablename>',methods=['GET','POST'])
@login_required
# The route for resource listing
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rlist(dbtype,tablename):
    lkup,dbsess = obtain_lkup(dbtype)
    if(lkup is None):
        return render_template("errors/error.html",
        error_title="Lookup Failure",
        error_message="Unknown Database")

    display_tablename = lkup[tablename].model.rlist_dis
    if(lkup[tablename].lsform == rstruct.all_only):
        # Get all matches
        mobj = getMatch(lkup,tablename)
        columnHead = mobj[0]
        match = mobj[1]
        prikey_match = mobj[2]
        return render_template('res/datalist0.html', dbtype = dbtype,\
            colNum=len(columnHead),matches=match,\
            columnHead=columnHead, tablename=tablename,\
            prikeyMatch=prikey_match,\
            data_table_name=display_tablename)
    else:
        resls_form = lkup[tablename].lsform() #creates an LS FORM
        resls_form = regenerateForm(lkup,resls_form,None)

        if resls_form.validate_on_submit():
            q = resls_form.getrawquery()

        elif (session.get('query') is not None and session.get('param') is not None):
            # previous query is inplace
            q = session['query']
            qp = json.loads(session['param'])
            # THIS IS VERY DANGEROUS ! VULNERABLE TO SQLI -- ToraNova
            # But I have no choice to use this for the sake of convenience
            # Please look into
            # https://stackoverflow.com/questions/14845196/dynamically-constructing-filters-in-sqlalchemy
            q = dbsess.query( lkup[tablename].model ).from_statement( text(q) ).params( qp )

        else:
            # await user query
            crawq = "No Queries. Hit 'Query' to start"
            return render_template('res/datalist1.html', dbtype = dbtype,
                colNum=0,matches=[],columnHead=[], tablename=tablename,
                prikeyMatch=[],
                data_table_name=display_tablename,
                form = resls_form, dqstr = crawq)

        #session['query'] = str(q.with_labels().statement)
        # SPECIAL THANKS TO
        # https://stackoverflow.com/questions/4617291/how-do-i-get-a-raw-compiled-sql-query-from-a-sqlalchemy-expression
        # crawq = str(q.statement.compile(compile_kwargs={"literal_binds": True}))
        crawq = q.statement.compile(dialect=sqlite.dialect(paramstyle="named"))
        crawq_str = str(crawq)
        # Thanks again to
        # https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
        crawq_params = json.dumps(crawq.params,cls=ExtendedEncoder)
        session['query'] = crawq_str
        session['param'] = crawq_params
        # FOR LS FORM SESSION/QUERY READY
        rawlist = q.all()
        mobj = getMatch(lkup,tablename,rawlist)
        columnHead = mobj[0]
        match = mobj[1]
        prikey_match = mobj[2]
        return render_template('res/datalist1.html', dbtype = dbtype,\
            colNum=len(columnHead),matches=match,\
            columnHead=columnHead, tablename=tablename,\
            prikeyMatch=prikey_match,\
            data_table_name=display_tablename,
            form = resls_form, dqstr = crawq)


@bp.route('/rmod/<dbtype>/<tablename>/<primaryKey>',methods=['GET','POST'])
@a.admin_required
# The route for resource modification.
# This route deals alot with the dist pkg as it is different from the packages.
# Could be semi-permanent
def rmod(dbtype,tablename,primaryKey):
    lkup,dbsess = obtain_lkup(dbtype)
    if(lkup is None):
        return render_template("errors/error.html",
        error_title="Lookup Failure",
        error_message="Unknown Database")

    if(lkup[tablename].editform is None):
        #edits disabled
        return render_template("errors/error.html",
            error_title="Modify Failure",
            error_message="This resource cannot be modified!")
    elif(lkup[tablename].editform == rstruct.del_only):
        #delete only
        pass
    else:
        #generates the edit form
        rmod_form = lkup[tablename].editform()

    if(request.method=="POST"):
        res_model = lkup[tablename].model
        if(request.form["button"]=="Delete"):
            #DELETION PROCEDURE
            target_del =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) \
                    == primaryKey ).first()
            if callable( getattr(target_del, "default_del_action", None) ):
                try:
                    target_del.default_del_action()
                except Exception as e:
                    rollback_alldb()
                    # rethrow exception
                    raise ValueError(tablename,"default_del_action",primaryKey,str(e))

            dbsess.delete(target_del)
            dbsess.commit()
            return redirect(url_for('resrc.rlist',dbtype=dbtype,tablename=tablename))

        elif(request.form["button"]=="Modify"):
            #MODIFY PROCEDURE
            if(lkup[tablename].editform == rstruct.del_only):
                return render_template("errors/error.html",
                    error_title="Modify Failure",
                    error_message="This resource can only be deleted!")

            target_mod =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) \
                    == primaryKey).first()
            #target_mod is the resource entity that we wish to edit
            rmod_form = regenerateForm(lkup,rmod_form,target_mod)

            rmod_form.process()
            return render_template('res/rmod0.html',
                primaryKey=primaryKey,dbtype = dbtype,tablename=tablename,form=rmod_form)

        elif(request.form["button"]=="Submit Changes"):
            if rmod_form.validate_on_submit():
                target_mod =res_model.query.filter( getattr(res_model,res_model.rlist_priKey) \
                        == primaryKey).first()
                d_point = getFormAttrList(rmod_form) #d_point has a dictionary for obj modification
                for f,val in  d_point.items():
                    target_mod.__setattr__(f,val)

                if callable( getattr(target_mod, "default_mod_action", None) ):
                    try:
                        target_mod.default_mod_action()
                    except Exception as e:
                        rollback_alldb()
                        # rethrow exception
                        raise ValueError(tablename,"default_mod_action",primaryKey,str(e))
                dbsess.add(target_mod)
                dbsess.commit()
                return redirect(url_for('resrc.rlist',dbtype=dbtype,tablename=tablename))
        else:
            abort(404)
    else:
        abort(400)

##############################################################################################
# Auxiliary methods, these methods aid the generelization of resource models/forms
##############################################################################################
def getMatch(rstype,tablename,rawlist=None):
    '''obtains matching columns and data of a specific table
    updated on u3 compared to r9. now supports a cleaner model side requirement'''
    entityClass = rstype[tablename].model
    reslist = entityClass.rlist # the rlist element
    if(rawlist==None):
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
                    if(entry.__getattribute__(rkey) is not None and\
                            str(entry.__getattribute__(rkey)) != rstruct.rlin_nullk):
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
                    print("[EX]",__name__," : ",\
                        "Exception has occurred on getMatch __link__ :",str(e))
                    try:
                        coltmp["data"] = entry.__getattribute__(rkey)
                    except Exception as e:
                        coltmp["data"] = "err:__link__ "+str(e)

            elif(reslist[key].startswith("__time__")):
                # For formatting of time fields
                try:
                    tformat = reslist[key].split('/')[1]
                    timedat = reslist[key].split('/')[2]
                    tval = entry.__getattribute__(timedat)
                    if( tval is not None ):
                        if( isinstance(tval, str) ):
                            #REFORMAT TIME
                            coltmp["data"] = datetime.datetime.strptime(tval,"%Y-%m-%d %H:%M:%S.%f")\
                                            .strftime(tformat)
                        elif( isinstance(tval, datetime.datetime) ):
                            coltmp["data"] = tval.strftime(tformat)
                    else:
                        coltmp["data"] = "Null (No data)"
                except Exception as e:
                    print("[EX]",__name__," : ",\
                        "Exception has occurred on getMatch __time__ :",str(e))
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
                    print("[EX]",__name__," : ",\
                        "Exception has occurred on getMatch __url__ :",str(e))
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
            out[a[len(rstruct.rgen_timkey):]]=form_obj.__getattribute__(a).data
        elif a.startswith(rstruct.rgen_typebool):
            out[a[len(rstruct.rgen_typebool):]]=True if form_obj.__getattribute__(a).data == '1' else False
        elif a.startswith(rstruct.rgen_actkey):
            form_action = form_obj.__getattribute__(a[len(rstruct.rgen_actkey):])
            if callable( form_action ):
                out.update( form_action( form_obj ) )
    return out

def regenerateForm(lkup,in_form,target=None):
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
    outList.append((rstruct.rlin_nullk,'No Link'))
    for elements in sqlresult:
        outList.append((str(elements.__getattribute__(elements.rlist_priKey)),elements.__getattribute__(ref_elem)))

    return outList

class ExtendedEncoder(json.JSONEncoder):
    "Allows for datetime json encoding u82"
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, datetime.date):
            return o.isoformat()
        return super().default(o)
