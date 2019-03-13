#--------------------------------------------------
# const.py
# this file serves to hold the important constants
# that are used in the project
# as the name implies, these are not meant to be
# changed
# introduced 8/12/2018
#--------------------------------------------------

################################################################
# Essential constant vars (consistent through deployments)
################################################################

#Database names
DB00_NAME = 'sys.db'            # Perma db (system user/configs/generics)
DB01_NAME = 'deploy.db'         # Used for deployment data (semi perma)

# SHA algorithm used for password generation
HASH_ALGORITHM_0 = 'pbkdf2:sha512'
HASH_ALGORITHM_1 = 'sha256' # not used anymore

# Logging directories (Perma)
LOGS_DIR = 'logs'
TOKN_DIR = 'tokens'
TOKN_SYS = 'sysuser'

# File upload directories
STD_FILEDIR = 'uploads'

SERVER_NAME = "minimal_server"
ADMIN_PLAINT_APIKEY = "abc123"
DISABLE_CRIT_ROUTE = False



#
