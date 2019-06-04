
from flask_socketio import send, emit
from pkg.system.servlog import srvlog
#----------------------------------------------------------------------------------------
# External calls
# introduced u7
# The livelog functions allows other functions which are not registered with
# socketio to emit a message.
# Generalization (u8) 31/05/2019
# Now this can be called anywhere. just create listener sockets on the namespaces
# for it to work!
# 
# @author ToraNova
# @mailto chia_jason96@live.com
#----------------------------------------------------------------------------------------
def sockemit( enamespace, ename, emsg, eroom=None):
    
    from pkg.source import out as socketio # use carefully to prevent circular imports
    try:
        #live logins - update7
        if(eroom is None):
            socketio.emit( ename, emsg, namespace= enamespace)
        else:
            socketio.emit( ename, emsg, room = eroom, namespace= enamespace)
        # emit may also contain namespaces to emit to other classes
    except Exception as e:
        print("[EX]",__name__," : ","Exception has occurred",str(e))
        srvlog["oper"].info("Exception ocurred in sockemit :"+str(e))

