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
from flask_login import LoginManager
from flask import render_template
from flask_socketio import SocketIO

import pkg.const as const
from pkg.system.database import dbms

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

# System sourcing
import pkg.system as system
# Interface sourcing
import pkg.iface as iface
# MSGAPI sourcing
import pkg.msgapi as msgapi
# Resource sourcing
import pkg.resrc as resrc
# Deploy Sourcing
import pkg.deploy as deploy

# Exception (admintools kept separate)
from pkg.system import admintools

#######################################################################################################
# Login manager section
#######################################################################################################
from pkg.system import auth #auth required for login manager
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

bplist = [  system.bp, iface.bp, msgapi.bp, resrc.bp, deploy.bp, admintools.bp]

for bp in bplist:
        out.register_blueprint(bp)

#tear down context is done here.
@out.teardown_appcontext
def shutdown_session(exception=None):
    dbms.system.session.remove()
    dbms.deploy.session.remove()
    dbms.msgapi.session.remove()

# FLASK SOCKET USE 8/1/2019
out_nonsock = out
out = SocketIO(out_nonsock)

# out is rexported for use in emits

# import socketio files here
from pkg.iface import sysutilio
sysutil_ns = sysutilio.SystemUtilNamespace('/sysutil')
out.on_namespace(sysutil_ns)
