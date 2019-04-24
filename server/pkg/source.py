#--------------------------------------------------
# Source.py
# this file sources the main flask object
# it also generates the the object
# based on configuration files
# created 8/12/2018
# author : ToraNova
#--------------------------------------------------

from flask import Flask
from flask import Blueprint
import pkg.const as const
from flask_login import LoginManager
from flask import render_template
import logging #to disable werkzeug logs

from pkg.database.fsqlite import db_session
from pkg.database.fsqlite import sy_session
from flask_socketio import SocketIO

# This script works like a source file, sourcing files from pkg and leasing the important
# ones such as out (socketIO) and out_flask - the vanilla
config = None

#create and configures the server
out = Flask(__name__, instance_relative_config=True)
out.config.from_mapping(
	SECRET_KEY='torabuilds',
	DATABASE=const.DB01_NAME,
	UPLOAD_FOLDER='uploads'
	#check out out.instance_path
)

if config is None:
	out.config.from_pyfile('config.py',silent=True)
else:
	out.config.from_mapping(config)

# Restrict werkzeug logs to only errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from pkg.interface import sysutilio #socket io import

from pkg.interface import home
from pkg.interface.API import push,pull
from pkg.system import auth,admintools
from pkg.system.user import sysuser,type,sysnologin
from pkg.resource import r

from pkg.resource.generic import standard_file

#######################################################################################################
# Login manager section
#######################################################################################################
login_manager = LoginManager()
login_manager.init_app(out)
@out.login_manager.user_loader
def load_user(id): #loads a sql object model as "login-ed"
	target_user = auth.sysuser_getobj(id)
	return target_user

@out.login_manager.unauthorized_handler
def unauthorized_warning():
	return render_template("errors/unauthorized.html",
		displat_message="Login required!")
login_manager.login_view = "login"
login_manager.login_message = "Please login first."
login_manager.login_message_category = "info"

bplist = [	r.bp,auth.bp,home.bp,admintools.bp,sysutilio.bp,
			push.bp,pull.bp,sysuser.bp,type.bp,sysnologin.bp,
			standard_file.bp]

for bp in bplist:
	out.register_blueprint(bp)

#tear down context is done here.
@out.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()
	sy_session.remove()

# FLASK SOCKET USE 8/1/2019
out_nonsock = out
out = SocketIO(out_nonsock)

# out is rexported for use in emits

sysutil_ns = sysutilio.SystemUtilNamespace('/sysutil')
out.on_namespace(sysutil_ns)
