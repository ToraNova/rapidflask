#--------------------------------------------------
# const.py
# this file serves to hold the important constants
# that are used in the project
# as the name implies, these are not meant to be
# changed
# introduced 8/12/2018
# updated u8 : config file is read here, sourced to
# rest of the project
#--------------------------------------------------

################################################################
# as of u8 - config is read here and sourced as constant values
# to all other files
################################################################
import configparser,os

################################################################
# Essential constant vars (consistent through deployments)
################################################################

#Database names
DB00_NAME = 'system.db'            # Perma db (system user/configs/generics)
DB01_NAME = 'deploy.db'         # Used for deployment data (Use-case dependent)
DB02_NAME = 'msgapi.db'            # Used for message storage (API and other usages)

# SHA algorithm used for password generation
HASH_ALGORITHM_0 = 'pbkdf2:sha512'
HASH_ALGORITHM_1 = 'sha256' # not used anymore

# Logging directories (Perma)
LOGS_DIR = 'logs'
TOKN_DIR = 'tokens'
TOKN_SYS = 'sysuser'

# File upload directories
STD_FILEDIR = 'uploads'
CFG_FILEDIR = 'configs'
USS_FILEDIR = 'screenshots' #screenshots

# THREAD params
# How long is the sleep time for killed threads
THREAD_DORMANT_WTIME = 10

#ADMIN_PLAINT_APIKEY = "abc123" #TODO: api keys

# Config file value obtainer
# Read the config file and store their values here
rcf = configparser.RawConfigParser()
conf_file =os.path.join( CFG_FILEDIR,"rapid.conf" )
rcf.read( conf_file )
BIND_ADDR = rcf.get('conn','hostaddr')
try:
    BIND_PORT = int(rcf.get('conn','port'))
except Exception as e:
    print("[ER]",__name__," : ","Exception occured while parsing port number.",str(e))
    BIND_PORT = 8000 # fallback default port

SSL_ENABLE = rcf.get('conn','ssl_enable') == '1'
SSL_CERT = rcf.get('conn','ssl_cert')
SSL_SKEY = rcf.get('conn','ssl_skey')
SSL_CA = rcf.get('conn','ssl_ca')

EDEBUG = rcf.get('flags','debug') == '1'
RELOAD = rcf.get('flags','reload') == '1'

BROKER_ENABLE = rcf.get('service','broker_enable') == '1'
BROKER_AUTOSTART = rcf.get('service','broker_autostart') == '1'

LOCAL_RQTT_ENABLE = rcf.get('local_rqtt','local_rqtt_enable') == '1'
LOCAL_RQTT_AUTOSTART = rcf.get('local_rqtt','local_rqtt_autostart') == '1'
LOCAL_RQTT_ADDR = rcf.get('local_rqtt','local_rqtt_addr')
try:
    LOCAL_RQTT_PORT = int(rcf.get('local_rqtt','local_rqtt_port'))
except Exception as e:
    print("[ER]",__name__," : ","Exception occured while parsing port number.",str(e))
    LOCAL_RQTT_PORT = 1883 # fallback default port
LOCAL_RQTT_ANON = rcf.get('local_rqtt','local_rqtt_anon') == '1'
LOCAL_RQTT_USERNAME = rcf.get('local_rqtt','local_rqtt_username')
LOCAL_RQTT_PASSWORD = rcf.get('local_rqtt','local_rqtt_password')
LOCAL_RQTT_EXTBROKE = rcf.get('local_rqtt','local_rqtt_extbroker') == '1'

DISABLE_CRIT_ROUTE = rcf.get('general','disable_crit_route') == '1'
SERVER_NAME = rcf.get('general','servername')

SOCKET_IO_PROTO = 'https' if SSL_ENABLE else 'http'

print("[IF]",__name__," : ",SERVER_NAME,"configured with",conf_file)
