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

import pkg.const as const
from pkg.system.database import dbms

# This script works like a source file, sourcing files from pkg and leasing the important
# ones such as out (socketIO) and out_flask - the vanilla
config = None

#create and configures the server
out = Flask(__name__, instance_relative_config=True)
out.config.from_mapping(
        SECRET_KEY = 'torabuilds',
        DATABASE = const.DB01_NAME,
        UPLOAD_FOLDER = 'uploads',
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_USERNAME = 'submarinechai@gmail.com',
        MAIL_PASSWORD = 'thisisinplaintext99'
        #check out out.instance_path
)

if config is None:
        out.config.from_pyfile('config.py',silent=True)
else:
        out.config.from_mapping(config)

# System sourcing
from pkg.system import auth, admintools
from pkg.system.user import sysnologin, sysuser, utype

# Interface sourcing
from pkg.iface import home, sysutilio

# MSGAPI sourcing
from pkg.msgapi.http import push, pull
from pkg.msgapi.mqtt import rqtt

# Resource sourcing
from pkg.resrc import r

# Deployment additions
from pkg.deploy.generic import standard_file

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

bplist = [  
        auth.bp, admintools.bp, sysnologin.bp, sysuser.bp, utype.bp, rqtt.bp,
        home.bp, sysutilio.bp,  push.bp, pull.bp, r.bp, standard_file.bp]

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
#######################################
# Mails
from flask_mail import Mail
smail = Mail()
smail.init_app( out_nonsock )
#######################################
# Socket io
from flask_socketio import SocketIO
out = SocketIO(out_nonsock)
#######################################


# out is rexported for use in emits

# import socketio files here
sysutil_ns = sysutilio.SystemUtilNamespace('/sysutil')
mqttctl_ns = rqtt.MQTTCTLNamespace('/mqttctl')
out.on_namespace(sysutil_ns)
out.on_namespace(mqttctl_ns)
