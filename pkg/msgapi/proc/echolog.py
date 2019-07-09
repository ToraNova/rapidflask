#--------------------------------------------------
# echolog.py
# echolog echos back a ping msg and
# logs it in the standard log
# ARG is none
#
# PROC dir for API
# exec takes in 2 arguments,
# the topic
# the message
# RETURN True ON SUCCESS
#--------------------------------------------------

from pkg.system.database import dbms

def exec(topic, msg):
    from __main__ import global_rqttclient
    from pkg.deploy.generic import StandardLog

    rc = 1
    try:
        s = StandardLog({"param0":"ping","ref0":0})
        dbms.deploy.session.add(s)
        rc = global_rqttclient.pubmsg('echolog/server',msg)
        print("RC VALUE:",rc)
        dbms.deploy.session.commit()
    except Exception as e:
        print("[ER]",__name__," Exception has occurred:",str(e))
        srvlog["oper"].error("echolog--exec exception:"+str(e)) #logging
        dbms.deploy.session.rollback()

    finally:
        if rc == 1 :
            return False
        else:
            return True




