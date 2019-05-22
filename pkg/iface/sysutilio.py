#--------------------------------------------------
# socketio.py
# basic file that handles socket io use-cases
# introduced 8/1/2019
#--------------------------------------------------

from flask_socketio import Namespace
from flask_socketio import send, emit
from flask_socketio import join_room, leave_room
from flask import Blueprint

from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime

from pkg.system.servlog import srvlog
import pkg.const as const
import json

bp = Blueprint('sysutilio', __name__, url_prefix='')

#----------------------------------------------------------------------------------------
# External calls
# introduced u7
# The livelog functions allows other functions which are not registered with
# socketio to emit a message.
#----------------------------------------------------------------------------------------
def livelog(logstring,logtype='logins'):
    
    from pkg.source import out as socketio # use carefully to prevent circular imports

    try:
        #live logins - update7
        socketio.emit('livelog_cast',
        {'logtype':logtype,
        'logstring':logstring},
        namespace='/sysutil')
        # emit may also contain namespaces to emit to other classes
    except Exception as e:
        print("Exception has occurred".str(e))
        srvlog["oper"].info("Exception ocurred in live logging :"+str(e))

#----------------------------------------------------------------------------------------
# ROUTES
#----------------------------------------------------------------------------------------

@bp.route('/sysclock',methods=['GET','POST'])
def sysclock():
    return render_template('flask_sockio/sysclock.html')

@bp.route('/syschatter/<chatter_room>',methods=['GET','POST'])
def syschatter(chatter_room):
    return render_template('flask_sockio/chatter.html',chatter_room=chatter_room)

#SystemUtilNamespace is a socket.io class that handles system utility realtime
#data, currently implemented methods is the on_sync_time that allows a realtime
#clock on the server - 8/1/2019 ToraNova
#TODO: implement mapping system
class SystemUtilNamespace(Namespace):
    def on_connect(self):
        #print("sysutil on_connect")
        pass
        
    def on_disconnect(self):
        #print("sysutil on_disconnect")
        pass
        
    def on_handle_message(self,message):
        #print('received message: '+ message)
        pass    

    def on_handle_json(self,json):
        #print('received json: '+ str(json))
        pass

    def on_sync_time(self,json):
        #print("callback:",json['data'])
        dTString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emit('recv_sync', {"datetime":dTString})

    def on_joinedchatter(self,message):
        if(message.get("chatter_room") == None):
            return
        join_room(message.get("chatter_room")) # the sysutil chatter is a global chat
        # emit message only to users in the same room
        emit('status',{'msg':current_user.username+' has joined the chatter'},room=message.get('chatter_room')) 

    def on_msgchatter(self,message):
        if(message.get("chatter_room") == None):
            return
        dTString = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        join_room(message.get("chatter_room")) # the sysutil chatter is a global chat
        emit('text',{'msg': dTString+current_user.username+' : '+message.get('content')},room=message.get('chatter_room'))

    def on_leavechatter(self,message):
        if(message.get("chatter_room") == None):
            return
        leave_room(message.get('chatter_room'))
        emit('status',{'msg':current_user.username+' has left the chatter'},room=message.get('chatter_room')) 
