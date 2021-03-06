#--------------------------------------------------
# home.py
# this file serves home/dashboard routes
# introduced 8/12/2018
#--------------------------------------------------

#flask routing imports
from flask import render_template, redirect, url_for
from flask import request, abort
from flask import Blueprint

#flask logins
from flask_login import login_required
from flask_login import current_user

import pkg.const as const
from pkg.system import assertw as a

bp = Blueprint('home', __name__, url_prefix='')

##############################################################################################
# Index routings
##############################################################################################
@bp.route('/')
def index():
    return redirect(url_for("auth.login"))

@bp.route('/<username>/home',methods=['GET','POST'])
@login_required
def home(username):
    filebuff = []
    with open( "changelogs.txt" ,'r' ) as f:
        #opens the logfile of required logtype for reading
        #u8: using <pre> for fix-width display
        content = f.read()
    return render_template("standard/welcome.html",display_file=content)

####################################################################################
# favicon
####################################################################################
@bp.route('/favicon.ico')
def favicon():
    return redirect(url_for('static',filename='icons/redblack_right.ico'))
