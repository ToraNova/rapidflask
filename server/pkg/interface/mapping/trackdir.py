#--------------------------------------------------
# trackdir.py
# an initial test for mapping on flask servers
# this now contains some example for geopoints u5
# u6: renamed to trackdir for as a directory list
# for all tracking functionalities on the server
# introduced 8/1/2019
# last update 3/2/2019
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask logins
from flask_login import login_required
from flask_login import current_user

import pkg.const as const
from pkg.database import models as md
from pkg.system import assertw as a
from pkg.resource import rdef as res

#primary blueprint
bp = Blueprint('maptrack', __name__, url_prefix='/track')
#-----------------------------------------------------------------
# Generic geopoint tracking
@bp.route('/basic')
def basic():
	#return render_template('flask_io/basic_map.html')
	return render_template('leaflet/geopoint/basic.html')

@bp.route('/geopoint')
@login_required
def point():
	#return render_template('flask_io/basic_map.html')
	return render_template('leaflet/geopoint/dashboard.html')
#-------------------------------------------------------------------

# U6 -- zfencing alert ui (Alert tracking)
@bp.route('/zfence')
def zfence():
	return render_template('standalone/zfence_alert_dashgum.html')

@bp.route('/zfence/edit')
def zfence_edit():
	#query for all segment host
	shostlist = res.seghost.SegmentHost.query.all() #obtain a hostlist
	#rawlist
	return render_template('standalone/zfence_edit_dashgum.html',list = shostlist)
