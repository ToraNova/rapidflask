#--------------------------------------------------
# pull.py
# pull is to query server using an URL API.
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort

#flask logins
from flask_login import login_required
from flask_login import current_user

#usual imports (copy pasta this)
import pkg.const as const
import pkg.limits as limits
from pkg.system import assertw as a
from pkg.system.database import dbms
from pkg.system.user import models as md
from pkg.system.user import forms as fm
from pkg.system.servlog import srvlog,logtofile
from pkg.resource.r import getMatch

from pkg.deploy.generic import param3model #SAMPLE ONLY, DO NOT USE FOR ACTUAL DEPLOYMENT
from pkg.deploy.ddef import r_defines as d_defines

#primary blueprint
from pkg.msgapi.http import bp #uses the __init__ blueprint

##############################################################################################
# API pull routings
##############################################################################################
@bp.route('/<tablename>/list')
#This route allows API callers to add an entry
def tableList(tablename):
    '''retrieves a list of objects of the table, no filter at the moment
    example : http://localhost:8000/api/param3/list
    ''' 

    upload_ip=request.remote_addr
    print("Pull request from host ",upload_ip,tablename,'list') #DEBUGGING ONLY

    try:
        match = getMatch(d_defines,tablename)[1]
        # #------------FORMATTING
        # out = ''
        # for row in match:
        #     for field in row:
        #         out += str(field)
        #         if( )
        #     out += ';'
        # #//----------FORMATTING
        out = str(match)
        return out
    except Exception as e:
        srvlog["oper"].error("pull/{}/list FAIL :".format(tablename))
        return "1/Fail: "+str(e)
